#!/usr/bin/env python3
"""T19 — estatística descritiva das RQ01--RQ04 e classificação DORA C1.

Uso:
    python analysis/rq01_rq04.py
    python analysis/rq01_rq04.py --metrics data/datasets/metrics.csv

Lê exclusivamente o CSV final do pipeline. Cada linha é um repositório: a
mediana, IQR e IC BCa são, portanto, agregados entre repositórios, nunca entre
workflow runs individuais.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from analysis.bootstrap import bca_interval

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"

METRICS = (
    ("RQ01", "deployment_frequency_per_week", "releases por semana"),
    ("RQ02a", "lead_time_a_hours", "horas"),
    ("RQ02b", "lead_time_b_hours", "horas"),
    ("RQ03a", "cfr_a", "proporção"),
    ("RQ04", "recovery_hours", "horas"),
    ("RQ04 censura", "censored_proportion", "proporção"),
)
CATEGORIES = ("Elite", "High", "Medium", "Low")


def describe_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    """Resume cada métrica por repositório com mediana, IQR e IC BCa."""
    records: list[dict[str, float | int | str | None]] = []
    for rq, column, unit in METRICS:
        values = pd.to_numeric(frame[column], errors="coerce").dropna()
        interval = bca_interval(values)
        q1, q3 = values.quantile([0.25, 0.75]) if len(values) else (float("nan"), float("nan"))
        records.append(
            {
                "rq": rq,
                "metric": column,
                "unit": unit,
                "n_repositories": len(values),
                "median": values.median() if len(values) else None,
                "q1": q1 if len(values) else None,
                "q3": q3 if len(values) else None,
                "iqr": q3 - q1 if len(values) else None,
                "bca_95_low": interval.low if interval else None,
                "bca_95_high": interval.high if interval else None,
                "bootstrap_resamples": interval.n_resamples if interval else 0,
            }
        )
    return pd.DataFrame(records)


def describe_c1(frame: pd.DataFrame) -> pd.DataFrame:
    """Conta a classificação C1, mantendo explicitamente os não classificáveis."""
    categories = frame["dora_c1_category"].fillna("Não classificável").replace("", "Não classificável")
    order = [*CATEGORIES, "Não classificável"]
    counts = categories.value_counts()
    total = len(frame)
    return pd.DataFrame(
        {
            "dora_c1_category": order,
            "n_repositories": [int(counts.get(category, 0)) for category in order],
            "proportion": [float(counts.get(category, 0) / total) if total else 0.0 for category in order],
        }
    )


def markdown(summary: pd.DataFrame, c1: pd.DataFrame, source: Path) -> str:
    lines = [
        "# T19 — RQ01--RQ04 e classificação DORA C1",
        "",
        f"Fonte: `{source}`. ICs de 95% por bootstrap BCa com 2.000 reamostragens (semente 42).",
        "",
        "## Estatística descritiva por repositório",
        "",
        "| RQ | métrica | n | mediana | IQR (Q1--Q3) | IC BCa 95% | unidade |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in summary.to_dict("records"):
        interval = (
            f"{row['bca_95_low']:.4g}--{row['bca_95_high']:.4g}"
            if pd.notna(row["bca_95_low"])
            else "indisponível"
        )
        lines.append(
            f"| {row['rq']} | {row['metric']} | {row['n_repositories']} | "
            f"{row['median']:.4g} | {row['iqr']:.4g} ({row['q1']:.4g}--{row['q3']:.4g}) | "
            f"{interval} | {row['unit']} |"
        )
    lines += ["", "## Classificação DORA C1", "", "| categoria | n | proporção |", "|---|---:|---:|"]
    for row in c1.to_dict("records"):
        lines.append(f"| {row['dora_c1_category']} | {row['n_repositories']} | {row['proportion']:.1%} |")
    lines += [
        "",
        "C1 usa release como deploy, lead time por release (a), CFR de CI (a) e recovery. "
        "Repositórios sem alguma métrica necessária ficam explicitamente como não classificáveis.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    frame = pd.read_csv(args.metrics)
    required = {column for _, column, _ in METRICS} | {"dora_c1_category"}
    missing = required - set(frame.columns)
    if missing:
        parser.error(f"CSV sem colunas obrigatórias: {', '.join(sorted(missing))}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = describe_metrics(frame)
    c1 = describe_c1(frame)
    summary.to_csv(args.output_dir / "rq01_rq04_summary.csv", index=False)
    c1.to_csv(args.output_dir / "dora_c1_distribution.csv", index=False)
    (args.output_dir / "rq01_rq04.md").write_text(markdown(summary, c1, args.metrics), encoding="utf-8")
    print(f"T19 descritiva: {args.output_dir / 'rq01_rq04.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
