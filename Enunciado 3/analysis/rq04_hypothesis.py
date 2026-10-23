#!/usr/bin/env python3
"""Teste da hipótese informal da RQ04: mais workflow runs ⇒ recuperação mais rápida.

Uso:
    python analysis/rq04_hypothesis.py

Conta, por repositório, os runs válidos da janela (``event=push`` no default
branch e ``conclusion`` de sucesso ou falha, como no CFR (a)) e calcula a
correlação de Spearman com ``recovery_hours`` do ``metrics.csv``. Gera
``rq04_hypothesis.csv`` (um repositório por linha) e ``rq04_hypothesis.md``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from analysis.rq05_spearman import spearman_with_ci  # noqa: E402
from metrics.cfr import FAILURE_CONCLUSIONS, SUCCESS_CONCLUSIONS  # noqa: E402

DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"
VALID = FAILURE_CONCLUSIONS | SUCCESS_CONCLUSIONS


def valid_runs(payload: dict[str, Any]) -> int:
    """Runs push no default branch com sucesso ou falha (denominador do CFR (a))."""
    branch = payload.get("repository", {}).get("default_branch")
    return sum(
        1
        for month in payload.get("runs_by_month", {}).values()
        for run in month
        if run.get("branch") == branch
        and run.get("event") == "push"
        and run.get("conclusion") in VALID
    )


def runs_table(metrics: pd.DataFrame, gold_dir: Path) -> pd.DataFrame:
    rows = []
    for name in metrics["full_name"]:
        path = gold_dir / f"{name}.json"
        runs = valid_runs(json.loads(path.read_text(encoding="utf-8"))) if path.exists() else None
        rows.append({"full_name": name, "valid_runs": runs})
    return metrics[["full_name", "recovery_hours"]].merge(pd.DataFrame(rows), on="full_name")


def markdown(table: pd.DataFrame, stats: dict[str, Any]) -> str:
    runs = table["valid_runs"].dropna()
    return "\n".join(
        [
            "# RQ04 — hipótese: mais workflow runs ⇒ recuperação mais rápida",
            "",
            "Gerado por `analysis/rq04_hypothesis.py`. Runs válidos = `push` no default branch, "
            "com `conclusion` de sucesso ou falha, dentro da janela.",
            "",
            f"- Runs válidos por repositório: mediana {runs.median():.0f} "
            f"(IQR {runs.quantile(0.25):.0f}–{runs.quantile(0.75):.0f}).",
            f"- Spearman(runs válidos, tempo de recuperação): ρ = {stats['rho']:.3f}, "
            f"p = {stats['p_value']:.4f}, n = {stats['n']}, "
            f"IC 95% BCa = [{stats['ci_low']:.3f}, {stats['ci_high']:.3f}].",
            "",
        ]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    table = runs_table(pd.read_csv(args.metrics), args.gold_dir)
    stats = spearman_with_ci(table["valid_runs"], table["recovery_hours"])
    args.output_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.output_dir / "rq04_hypothesis.csv", index=False)
    (args.output_dir / "rq04_hypothesis.md").write_text(markdown(table, stats), encoding="utf-8")
    print(markdown(table, stats))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
