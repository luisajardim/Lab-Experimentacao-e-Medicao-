#!/usr/bin/env python3
"""T20 — RQ05: correlação de Spearman entre deployment frequency e CFR.

Calcula ρ de Spearman (``scipy.stats.spearmanr``) entre deployment frequency
(releases por semana, RQ01) e cada variante do change failure rate (RQ03):

* **(a)** proxy de CI: ``cfr_a`` de ``data/datasets/metrics.csv``;
* **(b)** proxy de entrega: release seguida por release corretiva em até 7 dias
  (``metrics.cfr.cfr_b``). As corretivas são classificadas com a combinação da
  heurística escolhida na amostra-ouro (``data/gold/cfr_metrics.json``), aplicada
  pelo mesmo código do tuning (``scripts/tune_cfr.py``).

Para cada variante reporta ρ, p-valor, n e IC 95% por bootstrap BCa pareado
(reamostragem de repositórios, 2.000 réplicas, semente fixa).

Saídas em ``analysis/output/``:
* ``rq05_metrics.csv``: uma linha por variante;
* ``rq05_cfr_b.csv``: CFR(b) por repositório (releases avaliadas e que falharam);
* ``rq05_scatter.png``: dispersão com eixo x em escala logarítmica.

Uso:
    python -m analysis.rq05_spearman
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from collections.abc import Sequence
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from scipy.stats import DegenerateDataWarning, bootstrap, spearmanr  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_dossiers import (  # noqa: E402
    _commit_message,
    _commits_for,
    _previous_release,
    load_records,
)
from tune_cfr import Candidate, Item, predict  # noqa: E402

from metrics.cfr import FOLLOW_UP_DAYS, cfr_b  # noqa: E402

DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_CFR_METRICS = DEFAULT_GOLD_DIR / "cfr_metrics.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"

# Janela de observação (config.toml [window]; ENUNCIADO §3), datas inclusivas.
WINDOW_START = datetime.fromisoformat("2025-10-01T00:00:00+00:00")
WINDOW_END = datetime.fromisoformat("2026-09-30T23:59:59+00:00")

N_RESAMPLES = 2_000
RANDOM_STATE = 42
CONFIDENCE = 0.95

# Paleta de referência (skill dataviz): uma série por painel, um único tom.
SERIES = "#2a78d6"
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e4e3df"


def _parse(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def load_candidate(path: Path) -> Candidate:
    """Combinação da heurística escolhida no tuning (T14)."""
    best = json.loads(path.read_text(encoding="utf-8"))["best"]
    return Candidate(
        version=best["version"],
        keywords=best.get("keywords"),
        match=best.get("match"),
        cutoff=best.get("cutoff"),
        feature_weight=best.get("feature_weight"),
    )


def window_deploys(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Deploys da janela: releases publicadas, não-draft e não-pré-release (como em RQ01)."""
    deploys = [
        r
        for r in payload.get("releases", [])
        if not r.get("draft") and not r.get("prerelease") and r.get("published_at")
        and WINDOW_START <= _parse(r["published_at"]) <= WINDOW_END
    ]
    return sorted(deploys, key=lambda r: r["published_at"])


def repository_cfr_b(payload: dict[str, Any], candidate: Candidate) -> dict[str, Any]:
    deploys = window_deploys(payload)
    items = []
    for release in deploys:
        previous = _previous_release(payload, release)
        commits = _commits_for(payload, release)
        items.append(
            Item(
                full_name=payload["repository"]["full_name"],
                tag=release.get("tag_name"),
                previous_tag=previous.get("tag_name") if previous else None,
                messages=None if commits is None else tuple(map(_commit_message, commits)),
                expected=False,  # sem rótulo: só a predição é usada
            )
        )
    corrective = predict(candidate, items) if items else []
    timeline = [(_parse(r["published_at"]), c) for r, c in zip(deploys, corrective, strict=True)]
    follow_up = timedelta(days=FOLLOW_UP_DAYS)
    evaluated = [when for when, _ in timeline if when + follow_up <= WINDOW_END]
    value = cfr_b(timeline, WINDOW_END)
    return {
        "releases_window": len(deploys),
        "corrective_releases": sum(corrective),
        "releases_evaluated": len(evaluated),
        "releases_failed": None if value is None else round(value * len(evaluated)),
        "cfr_b": value,
    }


def compute_cfr_b(metrics: pd.DataFrame, gold_dir: Path, candidate: Candidate) -> pd.DataFrame:
    records = load_records([gold_dir])
    rows = []
    for name in metrics["full_name"]:
        payload = records.get(name)
        base = {"full_name": name}
        rows.append({**base, **repository_cfr_b(payload, candidate)} if payload else base)
    return pd.DataFrame(rows)


def _rho(x: np.ndarray, y: np.ndarray) -> float:
    return float(spearmanr(x, y).statistic)


def spearman_with_ci(x: Sequence[float], y: Sequence[float]) -> dict[str, Any]:
    """ρ, p-valor e IC BCa pareado; ignora pares com valor ausente."""
    data = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(data)
    if n < 3:
        return {"n": n, "rho": None, "p_value": None, "ci_low": None, "ci_high": None}
    result = spearmanr(data["x"], data["y"])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DegenerateDataWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        ci = bootstrap(
            (data["x"].to_numpy(), data["y"].to_numpy()),
            _rho,
            paired=True,
            vectorized=False,
            method="BCa",
            n_resamples=N_RESAMPLES,
            confidence_level=CONFIDENCE,
            random_state=np.random.default_rng(RANDOM_STATE),
        ).confidence_interval
    finite = np.isfinite(ci.low) and np.isfinite(ci.high)
    return {
        "n": n,
        "rho": float(result.statistic),
        "p_value": float(result.pvalue),
        "ci_low": float(ci.low) if finite else None,
        "ci_high": float(ci.high) if finite else None,
    }


def summarize(merged: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for variant, column, label in (
        ("a", "cfr_a", "CFR (a) proxy de CI"),
        ("b", "cfr_b", "CFR (b) proxy de entrega"),
    ):
        stats = spearman_with_ci(merged["deployment_frequency_per_week"], merged[column])
        rows.append(
            {
                "variant": variant,
                "description": label,
                **stats,
                "ci_method": f"bootstrap BCa pareado, {N_RESAMPLES} réplicas, seed {RANDOM_STATE}",
                "significant_0.05": None if stats["p_value"] is None else stats["p_value"] < 0.05,
            }
        )
    return pd.DataFrame(rows)


def _fmt(value: float | None, digits: int = 3) -> str:
    return "—" if value is None or pd.isna(value) else f"{value:.{digits}f}"


def plot(merged: pd.DataFrame, summary: pd.DataFrame, path: Path) -> None:
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, facecolor=SURFACE)
    for ax, (_, row) in zip(axes, summary.iterrows(), strict=True):
        column = f"cfr_{row['variant']}"
        data = merged[["deployment_frequency_per_week", column]].dropna()
        ax.set_facecolor(SURFACE)
        ax.scatter(
            data["deployment_frequency_per_week"],
            data[column],
            s=36,
            color=SERIES,
            alpha=0.75,
            edgecolors=SURFACE,
            linewidths=1.2,
            zorder=3,
        )
        ax.set_xscale("log")
        ax.set_ylim(-0.03, 1.03)
        ax.grid(True, which="major", color=GRID, linewidth=0.8, zorder=0)
        ax.tick_params(colors=INK_SECONDARY, length=0)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        ax.set_title(row["description"], loc="left", color=INK, fontsize=11,
                     fontweight="bold", pad=24)
        ax.set_xlabel("Deployment frequency (releases/semana, escala log)")
        p_text = "p < 0.001" if row["p_value"] is not None and row["p_value"] < 0.001             else f"p = {_fmt(row['p_value'])}"
        ax.text(
            0,
            1.02,
            f"ρ = {_fmt(row['rho'])}   IC95% [{_fmt(row['ci_low'])}; {_fmt(row['ci_high'])}]"
            f"   {p_text}   n = {row['n']}",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            color=INK_SECONDARY,
            fontsize=9,
        )
    axes[0].set_ylabel("Change failure rate")
    fig.suptitle(
        "RQ05 — Deployment frequency × change failure rate (Spearman)",
        x=0.01,
        ha="left",
        color=INK,
        fontsize=12,
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    parser.add_argument("--cfr-metrics", type=Path, default=DEFAULT_CFR_METRICS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    metrics = pd.read_csv(args.metrics)
    candidate = load_candidate(args.cfr_metrics)
    cfr_b_df = compute_cfr_b(metrics, args.gold_dir, candidate)
    merged = metrics[["full_name", "deployment_frequency_per_week", "cfr_a"]].merge(
        cfr_b_df, on="full_name", how="left"
    )
    summary = summarize(merged)
    summary.insert(2, "heuristic_cfr_b", candidate.name)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output_dir / "rq05_metrics.csv", index=False)
    cfr_b_df.to_csv(args.output_dir / "rq05_cfr_b.csv", index=False)
    plot(merged, summary, args.output_dir / "rq05_scatter.png")

    for _, row in summary.iterrows():
        print(
            f"CFR({row['variant']}): rho={_fmt(row['rho'])} p={_fmt(row['p_value'], 4)} "
            f"n={row['n']} IC95%=[{_fmt(row['ci_low'])}, {_fmt(row['ci_high'])}]"
        )
    print(f"saidas em {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
