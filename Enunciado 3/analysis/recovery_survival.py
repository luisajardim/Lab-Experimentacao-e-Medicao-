#!/usr/bin/env python3
"""T19 — curva Kaplan--Meier agregada do tempo de recuperação.

Uso:
    python analysis/recovery_survival.py

O script lê ``metrics_full.json``, que contém somente os tempos e indicadores
de censura dos episódios já apurados pelo pipeline. Não faz chamadas à API.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics_full.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"


def episode_frame(records: list[dict]) -> pd.DataFrame:
    """Extrai episódios persistidos pelo estágio metrics e valida seus valores."""
    rows = []
    for record in records:
        name = record.get("repository", {}).get("full_name", "")
        for episode in record.get("recovery_episodes", []):
            duration = episode.get("duration_hours")
            if duration is None:
                continue
            try:
                duration = float(duration)
            except (TypeError, ValueError):
                continue
            if np.isfinite(duration) and duration >= 0:
                rows.append(
                    {
                        "full_name": name,
                        "duration_hours": duration,
                        "censored": bool(episode.get("censored", False)),
                    }
                )
    return pd.DataFrame(rows, columns=["full_name", "duration_hours", "censored"])


def fit_survival(episodes: pd.DataFrame) -> KaplanMeierFitter:
    if episodes.empty:
        raise ValueError("metrics_full.json não contém episódios de recovery; rode o estágio metrics atualizado")
    model = KaplanMeierFitter(label="Probabilidade de ainda não recuperar")
    model.fit(
        durations=episodes["duration_hours"],
        event_observed=~episodes["censored"],
    )
    return model


def save_plot(model: KaplanMeierFitter, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    model.plot_survival_function(ax=ax, ci_show=True, color="#2166ac")
    ax.set_xlabel("Horas desde o início do episódio de falha")
    ax.set_ylabel("Probabilidade de não recuperação")
    ax.set_title("Tempo até recuperação — Kaplan–Meier agregada")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics-full", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    records = json.loads(args.metrics_full.read_text(encoding="utf-8"))
    episodes = episode_frame(records)
    model = fit_survival(episodes)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    save_plot(model, args.output_dir / "recovery_survival.png")
    median = model.median_survival_time_
    summary = {
        "source": str(args.metrics_full),
        "n_episodes": int(len(episodes)),
        "n_repositories": int(episodes["full_name"].nunique()),
        "n_events": int((~episodes["censored"]).sum()),
        "n_censored": int(episodes["censored"].sum()),
        "censored_proportion": float(episodes["censored"].mean()),
        "km_median_hours": float(median) if np.isfinite(median) else None,
    }
    (args.output_dir / "recovery_survival_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    episodes.to_csv(args.output_dir / "recovery_episodes.csv", index=False)
    print(
        f"Kaplan–Meier: {summary['n_episodes']} episódios, "
        f"{summary['n_censored']} censurados ({summary['censored_proportion']:.1%})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
