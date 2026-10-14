#!/usr/bin/env python3
"""Ferramenta de rotulagem manual da amostra-ouro (terminal).

Mostra o dossiê de cada repositório (gerado por ``build_dossiers.py``) e grava
as respostas em ``labels_<MEMBRO>.csv``, validando os valores na hora.

Colunas do arquivo de rótulos: as do template + ``corrective_1..5`` (corretiva
sim/não para cada uma das 5 releases, exigido pelo ENUNCIADO §6 item iii; o
template do generate_gold.py não tem essas colunas).

Retomada: ao rodar de novo, repositórios já completos são pulados.
Auditoria (PLAN T12): ``labels_<MEMBRO>.audit.json`` registra início e conclusão.

Uso
---
    python scripts/label_tool.py --member A
    python scripts/label_tool.py --member B --template data/gold/labels_template.csv
    python scripts/label_tool.py --validate data/gold/labels_A.csv

Teclas em qualquer pergunta: ``q`` salva e sai; ``u`` volta à pergunta anterior
do mesmo repositório.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path

from build_dossiers import dossier_filename  # mesma pasta (scripts/)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_DIR = PROJECT_ROOT / "data" / "gold"

PROJECT_TYPES = {
    "1": "biblioteca/framework",
    "2": "aplicação/serviço",
    "3": "ferramenta CLI",
    "4": "outro",
}
DELIVERS = {"s": "sim", "sim": "sim", "n": "não", "nao": "não", "não": "não", "i": "incerto", "incerto": "incerto"}
CORRECTIVE = {"s": "sim", "sim": "sim", "n": "não", "nao": "não", "não": "não"}

CORRECTIVE_COLUMNS = tuple(f"corrective_{i}" for i in range(1, 6))
LABEL_COLUMNS = ("project_type", "delivers_to_user", *CORRECTIVE_COLUMNS, "notes")
VALID_VALUES = {
    "project_type": set(PROJECT_TYPES.values()),
    "delivers_to_user": {"sim", "não", "incerto"},
    **{column: {"sim", "não"} for column in CORRECTIVE_COLUMNS},
}


class Quit(Exception):
    pass


class Undo(Exception):
    pass


def output_columns(template_columns: Sequence[str]) -> list[str]:
    base = [c for c in template_columns if c != "notes"]
    return [*base, *CORRECTIVE_COLUMNS, "notes"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path: Path, columns: Sequence[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def is_complete(row: dict[str, str]) -> bool:
    return all((row.get(column) or "").strip() in VALID_VALUES[column] for column in VALID_VALUES)


def validate(path: Path) -> int:
    rows = read_csv(path)
    problems = 0
    for number, row in enumerate(rows, start=2):
        for column, allowed in VALID_VALUES.items():
            value = (row.get(column) or "").strip()
            if value not in allowed:
                problems += 1
                print(f"{path.name}:{number} {row.get('full_name')}: {column}={value!r} inválido")
    print(f"{len(rows)} linhas, {problems} problemas")
    return 1 if problems else 0


def ask(prompt: str, options: dict[str, str], allow_undo: bool) -> str:
    while True:
        raw = input(prompt).strip().lower()
        if raw == "q":
            raise Quit
        if raw == "u" and allow_undo:
            raise Undo
        if raw in options:
            return options[raw]
        print("  valor inválido; tente de novo.")


def label_row(row: dict[str, str], dossier_dir: Path) -> None:
    dossier = dossier_dir / dossier_filename(row["full_name"])
    print("\n" + "=" * 78)
    print(dossier.read_text(encoding="utf-8") if dossier.exists() else f"(sem dossiê) {row['full_name']}")
    print("=" * 78)

    steps = [
        ("project_type", "Tipo [1]biblioteca/framework [2]aplicação/serviço [3]CLI [4]outro: ", PROJECT_TYPES),
        ("delivers_to_user", "Releases são entregas reais ao usuário? [s]im [n]ão [i]ncerto: ", DELIVERS),
        *(
            (f"corrective_{i}", f"Release {i} é corretiva? [s]im [n]ão: ", CORRECTIVE)
            for i in range(1, 6)
        ),
    ]
    index = 0
    while index < len(steps):
        column, prompt, options = steps[index]
        try:
            row[column] = ask(prompt, options, allow_undo=index > 0)
            index += 1
        except Undo:
            index -= 1
    note = input("Notas (opcional, Enter para pular): ").strip()
    if note.lower() == "q":
        raise Quit
    row["notes"] = note


def run(args: argparse.Namespace) -> int:
    output = args.output or GOLD_DIR / f"labels_{args.member.upper()}.csv"
    template_rows = read_csv(args.template)
    columns = output_columns(list(template_rows[0].keys()) if template_rows else [])

    rows = template_rows
    if output.exists():
        existing = {r["full_name"]: r for r in read_csv(output)}
        rows = [{**t, **existing.get(t["full_name"], {})} for t in template_rows]
    for row in rows:
        for column in LABEL_COLUMNS:
            row.setdefault(column, "")

    audit_path = output.with_suffix(".audit.json")
    audit = json.loads(audit_path.read_text()) if audit_path.exists() else {}
    audit.setdefault("started_at", datetime.now(timezone.utc).isoformat())

    pending = [r for r in rows if not is_complete(r)]
    print(f"Membro {args.member.upper()}: {len(rows) - len(pending)}/{len(rows)} completos. 'q' salva e sai.")
    try:
        for row in pending:
            print(f"\n[{rows.index(row) + 1}/{len(rows)}]")
            label_row(row, args.dossier_dir)
            write_csv(output, columns, rows)  # salva a cada repositório
    except (Quit, EOFError, KeyboardInterrupt):
        print("\nSaindo; progresso salvo.")
    write_csv(output, columns, rows)

    if all(is_complete(r) for r in rows):
        audit["completed_at"] = datetime.now(timezone.utc).isoformat()
        print("Todos os repositórios rotulados.")
    audit_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--member", choices=["A", "B", "C", "a", "b", "c"])
    parser.add_argument("--template", type=Path, default=GOLD_DIR / "labels_template.csv")
    parser.add_argument("--dossier-dir", type=Path, default=GOLD_DIR / "dossiers")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", type=Path, metavar="CSV")
    args = parser.parse_args(argv)
    if not args.validate and not args.member:
        parser.error("informe --member A|B|C ou --validate CSV")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return validate(args.validate) if args.validate else run(args)
    except (OSError, KeyError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())