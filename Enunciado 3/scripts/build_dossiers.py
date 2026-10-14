#!/usr/bin/env python3
"""Gera um dossiê Markdown por repositório da planilha-ouro.

O dossiê junta, em um único arquivo, o que o rotulador precisa ler: metadados
do repositório, README (se estiver nos JSONs), e para cada uma das 5 releases
sorteadas: notas da release, assets e mensagens dos commits entre a release
anterior e ela.

REGRA DE OURO (ENUNCIADO §6 / PLAN T12): o dossiê NÃO pode conter nenhuma saída
da heurística de release corretiva nem sinais derivados dela (nada de "só mudou
patch", palavras-chave destacadas, scores). Este script apenas EXIBE dados
brutos, na ordem cronológica, sem classificar nada.

Entrada
-------
* ``--template``: CSV gerado por ``generate_gold.py`` (define repositórios e
  quais 5 releases entram, via ``release_url_1..5``);
* ``--input-dir`` (repetível): pastas com os JSONs por repositório do pipeline
  (mesmo contrato do ``generate_gold.py``: ``repository.full_name`` + ``releases``).
  Campos opcionais usados se existirem: ``repository.description/language/topics/
  homepage``, ``readme`` (texto) e ``commits_between`` (ver ``_commits_for``).

Saída
-----
``--output-dir``/<owner>__<repo>.md, um por linha do template.

Exemplo
-------
    python scripts/build_dossiers.py --template data/gold/labels_template.csv \\
        --input-dir data/raw --output-dir data/gold/dossiers
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = PROJECT_ROOT / "data" / "gold" / "labels_template.csv"
DEFAULT_INPUT_DIRS = (PROJECT_ROOT / "data" / "raw",)
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "gold" / "dossiers"

MAX_README_CHARS = 2500
MAX_RELEASE_BODY_CHARS = 2000
MAX_COMMITS_SHOWN = 40


def dossier_filename(full_name: str) -> str:
    return full_name.replace("/", "__") + ".md"


def load_records(input_dirs: Sequence[Path]) -> dict[str, dict[str, Any]]:
    """Map full_name -> JSON payload, for every repository JSON found."""
    records: dict[str, dict[str, Any]] = {}
    for input_dir in input_dirs:
        if not input_dir.is_dir():
            raise ValueError(f"pasta de entrada inexistente: {input_dir}")
        for path in sorted(input_dir.rglob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue  # JSONs auxiliares (ex.: meta/) não são registros de repositório
            if not isinstance(payload, dict) or not isinstance(payload.get("repository"), dict):
                continue
            name = payload["repository"].get("full_name")
            if isinstance(name, str) and name.strip():
                records[name.strip()] = payload
    return records


def read_template(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _commit_message(commit: Any) -> str:
    if not isinstance(commit, dict):
        return ""
    inner = commit.get("commit")
    if isinstance(inner, dict) and isinstance(inner.get("message"), str):
        return inner["message"]
    message = commit.get("message")
    return message if isinstance(message, str) else ""


def _commit_date(commit: Any) -> str:
    if not isinstance(commit, dict):
        return ""
    inner = commit.get("commit")
    if isinstance(inner, dict) and isinstance(inner.get("author"), dict):
        return str(inner["author"].get("date", ""))[:10]
    return str(commit.get("date", ""))[:10]


def _commits_for(payload: dict[str, Any], release: dict[str, Any]) -> list[Any] | None:
    """Return commits between the previous release and ``release``, or None if unknown.

    Aceita dois formatos para ``commits_between`` (ajuste aqui se o pipeline
    gravar diferente):
      * dict  {tag_name: [commits] | {"commits": [...]}}
      * list  [{"head"|"tag_name"|"release"|"head_tag": tag, "commits": [...]}, ...]
    """
    data = payload.get("commits_between")
    tag = release.get("tag_name")
    entry: Any = None
    if isinstance(data, dict):
        entry = data.get(tag)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and tag in (
                item.get("head"),
                item.get("tag_name"),
                item.get("release"),
                item.get("head_tag"),
            ):
                entry = item
                break
    if isinstance(entry, dict):
        entry = entry.get("commits")
    return entry if isinstance(entry, list) else None


def _truncate(text: str, limit: int) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "\n[... truncado ...]"


def _previous_release(payload: dict[str, Any], release: dict[str, Any]) -> dict[str, Any] | None:
    published = [
        r
        for r in payload.get("releases", [])
        if isinstance(r, dict) and not r.get("draft", False) and r.get("published_at")
    ]
    published.sort(key=lambda r: str(r["published_at"]))
    previous = None
    for candidate in published:
        if candidate.get("html_url") == release.get("html_url"):
            return previous
        previous = candidate
    return None


def _release_section(index: int, url: str, payload: dict[str, Any]) -> str:
    release = next(
        (r for r in payload.get("releases", []) if isinstance(r, dict) and r.get("html_url") == url),
        None,
    )
    lines = [f"### Release {index}", "", f"Link: {url}"]
    if release is None:
        lines += ["", "_Release não encontrada nos JSONs — abra o link acima._", ""]
        return "\n".join(lines)

    previous = _previous_release(payload, release)
    lines += [
        f"- Tag: `{release.get('tag_name', '?')}`",
        f"- Nome: {release.get('name') or '(sem nome)'}",
        f"- Publicada em: {str(release.get('published_at', '?'))[:10]}",
        f"- Release anterior (cronológica): "
        f"{('`' + str(previous.get('tag_name')) + '`') if previous else '(nenhuma)'}",
    ]
    assets = [a.get("name") for a in release.get("assets", []) if isinstance(a, dict)]
    if assets:
        lines.append(f"- Assets: {', '.join(str(a) for a in assets[:15])}")

    body = release.get("body")
    lines += ["", "**Release notes**", ""]
    lines.append(_truncate(body, MAX_RELEASE_BODY_CHARS) if isinstance(body, str) and body.strip() else "_(vazio)_")

    commits = _commits_for(payload, release)
    lines += ["", "**Commits desde a release anterior**", ""]
    if commits is None:
        lines.append("_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_")
    elif not commits:
        lines.append("_(nenhum commit novo)_")
    else:
        lines.append(f"Total: {len(commits)}")
        lines.append("")
        for commit in commits[:MAX_COMMITS_SHOWN]:
            first_line = _commit_message(commit).strip().splitlines()[0:1]
            lines.append(f"- {_commit_date(commit)} {first_line[0] if first_line else '(sem mensagem)'}")
        if len(commits) > MAX_COMMITS_SHOWN:
            lines.append(f"- ... e mais {len(commits) - MAX_COMMITS_SHOWN} commits")
    lines.append("")
    return "\n".join(lines)


def build_dossier(row: dict[str, str], payload: dict[str, Any] | None) -> str:
    full_name = row["full_name"]
    lines = [f"# {full_name}", "", f"Repositório: https://github.com/{full_name}", ""]
    repo = (payload or {}).get("repository", {})
    meta = []
    for label, key in (("Descrição", "description"), ("Linguagem", "language"), ("Homepage", "homepage")):
        if repo.get(key):
            meta.append(f"- {label}: {repo[key]}")
    if isinstance(repo.get("topics"), list) and repo["topics"]:
        meta.append(f"- Topics: {', '.join(map(str, repo['topics']))}")
    if meta:
        lines += ["## Metadados", "", *meta, ""]

    readme = (payload or {}).get("readme")
    if isinstance(readme, str) and readme.strip():
        lines += ["## README (trecho)", "", _truncate(readme, MAX_README_CHARS), ""]

    lines += ["## Releases sorteadas", ""]
    for index in range(1, 6):
        url = (row.get(f"release_url_{index}") or "").strip()
        if url:
            lines.append(_release_section(index, url, payload or {}))
    return "\n".join(lines)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--input-dir", action="append", type=Path, metavar="DIR")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    input_dirs = tuple(args.input_dir) if args.input_dir else DEFAULT_INPUT_DIRS
    try:
        rows = read_template(args.template)
        records = load_records(input_dirs)
    except (OSError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    missing = 0
    for row in rows:
        payload = records.get(row["full_name"])
        if payload is None:
            missing += 1
        (args.output_dir / dossier_filename(row["full_name"])).write_text(
            build_dossier(row, payload), encoding="utf-8"
        )
    print(f"{len(rows)} dossiês em {args.output_dir} ({missing} sem JSON correspondente)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())