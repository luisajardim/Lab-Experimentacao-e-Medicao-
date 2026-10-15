#!/usr/bin/env python3
"""Concordância entre avaliadores e rótulo de consenso da amostra-ouro (PLAN T13).

Lê os três arquivos de rótulos independentes (``labels_A/B/C.csv``, gerados por
``label_tool.py``), calcula o κ de Fleiss por dimensão e grava o consenso.

Dimensões
---------
* ``tipo``: ``project_type`` (1 item por repositório);
* ``entrega``: ``delivers_to_user`` (1 item por repositório);
* ``corretiva``: ``corrective_1..5`` (5 itens por repositório, um por release).

O κ usa ``aggregate_raters`` + ``fleiss_kappa`` do ``statsmodels`` e é
interpretado pela escala de Landis & Koch (1977).

Consenso (``docs/consensus_protocol.md``)
-----------------------------------------
Maioria simples (≥ 2 de 3). Empates 1-1-1 (possíveis só em tipo e entrega) são
resolvidos em reunião e registrados na tabela de decisões do protocolo; o
script lê essa tabela. Empates sem decisão ficam vazios no CSV, são listados no
relatório e o script sai com código 1.

Saídas
------
* ``data/gold/labels_consensus.csv``: schema dos rótulos (sem ``notes``) +
  ``meeting_decisions`` (colunas decididas em reunião, separadas por ``;``);
* ``reports/agreement.md``: κ por dimensão, interpretação e resumo do consenso.

Uso
---
    python scripts/agreement.py
    python scripts/agreement.py --labels a.csv b.csv c.csv --output out.csv
"""

from __future__ import annotations

import argparse
import math
import sys
import warnings
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from label_tool import CORRECTIVE_COLUMNS, VALID_VALUES, read_csv, write_csv  # mesma pasta
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_LABELS = tuple(GOLD_DIR / f"labels_{member}.csv" for member in "ABC")
DEFAULT_PROTOCOL = PROJECT_ROOT / "docs" / "consensus_protocol.md"
DEFAULT_OUTPUT = GOLD_DIR / "labels_consensus.csv"
DEFAULT_REPORT = PROJECT_ROOT / "reports" / "agreement.md"

DIMENSIONS: dict[str, tuple[str, ...]] = {
    "tipo": ("project_type",),
    "entrega": ("delivers_to_user",),
    "corretiva": CORRECTIVE_COLUMNS,
}
URL_COLUMNS = tuple(f"release_url_{i}" for i in range(1, 6))
CONSENSUS_COLUMNS = (
    "full_name",
    "project_type",
    "delivers_to_user",
    *URL_COLUMNS,
    *CORRECTIVE_COLUMNS,
    "meeting_decisions",
)

# Landis & Koch (1977): limite superior (inclusivo) de cada faixa; κ < 0 é "pobre".
LANDIS_KOCH = (
    (0.20, "leve"),
    (0.40, "razoável"),
    (0.60, "moderada"),
    (0.80, "substancial"),
    (1.0, "quase perfeita"),
)

Labels = dict[str, dict[str, str]]  # full_name -> linha do CSV


@dataclass(frozen=True)
class DimensionAgreement:
    dimension: str
    items: int
    kappa: float
    unanimous: int

    @property
    def interpretation(self) -> str:
        return landis_koch(self.kappa)


@dataclass(frozen=True)
class Consensus:
    rows: list[dict[str, str]]
    # (dimensão, origem) -> contagem; origem ∈ unânime, maioria, reunião, pendente
    sources: Counter[tuple[str, str]]
    pending: list[tuple[str, str, tuple[str, ...]]]  # (full_name, coluna, votos)
    unused_decisions: list[tuple[str, str]]


def landis_koch(kappa: float) -> str:
    if math.isnan(kappa):
        return "indefinido (sem variação nos rótulos)"
    if kappa < 0:
        return "pobre"
    for upper, label in LANDIS_KOCH:
        if kappa <= upper:
            return label
    return LANDIS_KOCH[-1][1]


def load_labels(paths: Sequence[Path]) -> list[Labels]:
    """Lê os CSVs dos avaliadores e exige mesmo conjunto de repositórios e rótulos válidos."""
    raters = [{row["full_name"]: row for row in read_csv(path)} for path in paths]
    problems: list[str] = []
    reference = set(raters[0])
    for path, rater in zip(paths, raters, strict=True):
        if set(rater) != reference:
            diff = sorted(set(rater) ^ reference)
            problems.append(f"{path.name}: repositórios diferentes de {paths[0].name}: {diff}")
        for name, row in rater.items():
            for column, allowed in VALID_VALUES.items():
                value = (row.get(column) or "").strip()
                if value not in allowed:
                    problems.append(f"{path.name} {name}: {column}={value!r} inválido")
    if problems:
        raise ValueError("rótulos incompletos ou inconsistentes:\n  " + "\n  ".join(problems))
    return raters


def ratings(raters: Sequence[Labels], columns: Sequence[str]) -> list[tuple[str, ...]]:
    """Uma tupla de votos (um por avaliador) por item = (repositório, coluna)."""
    names = sorted(raters[0])
    return [
        tuple(rater[name][column].strip() for rater in raters)
        for name in names
        for column in columns
    ]


def fleiss(votes: Sequence[tuple[str, ...]], categories: Sequence[str]) -> float:
    codes = {category: index for index, category in enumerate(sorted(categories))}
    data = np.array([[codes[vote] for vote in item] for item in votes])
    table, _ = aggregate_raters(data, n_cat=len(codes))
    with warnings.catch_warnings(), np.errstate(divide="ignore", invalid="ignore"):
        warnings.simplefilter("ignore", RuntimeWarning)
        return float(fleiss_kappa(table, method="fleiss"))


def agreement(raters: Sequence[Labels]) -> list[DimensionAgreement]:
    results = []
    for dimension, columns in DIMENSIONS.items():
        votes = ratings(raters, columns)
        results.append(
            DimensionAgreement(
                dimension=dimension,
                items=len(votes),
                kappa=fleiss(votes, VALID_VALUES[columns[0]]),
                unanimous=sum(len(set(item)) == 1 for item in votes),
            )
        )
    return results


def majority(votes: Sequence[str]) -> str | None:
    value, count = Counter(votes).most_common(1)[0]
    return value if count * 2 > len(votes) else None


def parse_decisions(path: Path) -> dict[tuple[str, str], str]:
    """Lê a tabela ``| full_name | coluna | decisão | justificativa |`` do protocolo."""
    if not path.exists():
        return {}
    decisions: dict[tuple[str, str], str] = {}
    in_table = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells[:2] == ["full_name", "coluna"]:
            in_table = True
            continue
        if not in_table or set("".join(cells)) <= set("-: "):
            continue
        name, column, value = cells[0], cells[1], cells[2] if len(cells) > 2 else ""
        if column not in VALID_VALUES or value not in VALID_VALUES[column]:
            raise ValueError(f"{path.name}:{number}: decisão inválida {column}={value!r}")
        decisions[(name, column)] = value
    return decisions


def build_consensus(
    raters: Sequence[Labels], decisions: dict[tuple[str, str], str]
) -> Consensus:
    column_dimension = {c: d for d, columns in DIMENSIONS.items() for c in columns}
    rows: list[dict[str, str]] = []
    sources: Counter[tuple[str, str]] = Counter()
    pending: list[tuple[str, str, tuple[str, ...]]] = []
    used: set[tuple[str, str]] = set()

    for name in sorted(raters[0]):
        base = raters[0][name]
        row = {"full_name": name, **{c: base.get(c, "") for c in URL_COLUMNS}}
        meeting: list[str] = []
        for column, dimension in column_dimension.items():
            votes = tuple(rater[name][column].strip() for rater in raters)
            value = majority(votes)
            if value is not None:
                source = "unânime" if len(set(votes)) == 1 else "maioria"
            elif (name, column) in decisions:
                value, source = decisions[(name, column)], "reunião"
                used.add((name, column))
                meeting.append(column)
            else:
                value, source = "", "pendente"
                pending.append((name, column, votes))
            row[column] = value
            sources[(dimension, source)] += 1
        row["meeting_decisions"] = ";".join(meeting)
        rows.append(row)

    unused = sorted(set(decisions) - used)
    return Consensus(rows=rows, sources=sources, pending=pending, unused_decisions=unused)


def render_report(
    results: Sequence[DimensionAgreement], consensus: Consensus, label_paths: Sequence[Path]
) -> str:
    lines = [
        "# Concordância entre avaliadores e consenso (T13)",
        "",
        "Gerado por `scripts/agreement.py`; não edite à mão.",
        f"Avaliadores: {', '.join(f'`{p.name}`' for p in label_paths)}.",
        "",
        "## κ de Fleiss por dimensão",
        "",
        "| Dimensão | Itens | Unânimes | κ de Fleiss | Interpretação (Landis & Koch) |",
        "|---|---:|---:|---:|---|",
    ]
    for r in results:
        kappa = "—" if math.isnan(r.kappa) else f"{r.kappa:.3f}"
        unanimous = f"{r.unanimous} ({r.unanimous / r.items:.0%})"
        lines.append(
            f"| {r.dimension} | {r.items} | {unanimous} | {kappa} | {r.interpretation} |"
        )
    lines += [
        "",
        "Escala de Landis & Koch (1977): < 0 pobre; 0,00–0,20 leve; 0,21–0,40 razoável; "
        "0,41–0,60 moderada; 0,61–0,80 substancial; 0,81–1,00 quase perfeita.",
        "",
        "## Origem do rótulo de consenso",
        "",
        "| Dimensão | Unânime | Maioria | Reunião | Pendente |",
        "|---|---:|---:|---:|---:|",
    ]
    for dimension in DIMENSIONS:
        counts = [consensus.sources[(dimension, s)] for s in ("unânime", "maioria", "reunião")]
        pending = consensus.sources[(dimension, "pendente")]
        lines.append(f"| {dimension} | {' | '.join(map(str, counts))} | {pending} |")

    lines += ["", "## Empates 1-1-1 pendentes", ""]
    if consensus.pending:
        lines += [
            "Decidir em reunião e registrar em `docs/consensus_protocol.md`:",
            "",
            "| full_name | coluna | votos (A, B, C) |",
            "|---|---|---|",
        ]
        lines += [f"| {n} | {c} | {', '.join(v)} |" for n, c, v in consensus.pending]
    else:
        lines.append("Nenhum.")
    if consensus.unused_decisions:
        lines += ["", "Decisões registradas que não correspondem a empate (ignoradas):", ""]
        lines += [f"- {n} / {c}" for n, c in consensus.unused_decisions]
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> int:
    raters = load_labels(args.labels)
    results = agreement(raters)
    consensus = build_consensus(raters, parse_decisions(args.protocol))

    write_csv(args.output, CONSENSUS_COLUMNS, consensus.rows)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render_report(results, consensus, args.labels), encoding="utf-8")

    for r in results:
        kappa = "—" if math.isnan(r.kappa) else f"{r.kappa:.3f}"
        print(f"{r.dimension:<10} kappa={kappa:>6}  ({r.interpretation}, n={r.items})")
    print(f"consenso: {args.output}  relatório: {args.report}")
    if consensus.pending:
        print(f"{len(consensus.pending)} empate(s) 1-1-1 sem decisão; veja o relatório.")
        return 1
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--labels", type=Path, nargs=3, default=list(DEFAULT_LABELS),
                        metavar=("A", "B", "C"))
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        return run(args)
    except (OSError, KeyError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
