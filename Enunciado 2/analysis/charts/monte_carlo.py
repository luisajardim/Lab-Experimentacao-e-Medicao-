from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .config import OUTPUT_DIR
from .rendering import save_chart


def _summary_interval(summary: dict, section: str) -> tuple[float, float, float]:
    values = summary.get("monte_carlo", {}).get(section, {})
    interval = values.get("ci_95", [None, None])
    return float(values.get("median", 0)), float(interval[0]), float(interval[1])


def plot_monte_carlo(simulations: pd.DataFrame, summary: dict) -> None:
    required = {"time_saved_pct", "attempts_reduction"}
    missing = required - set(simulations.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no Monte Carlo: {sorted(missing)}")

    metrics = [
        ("time_saved_pct", "Tempo economizado (%)", "mc_tempo_economizado_pct"),
        ("attempts_reduction", "Redução média de tentativas", "mc_reducao_tentativas"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    for axis, (column, label, _) in zip(axes, metrics):
        values = simulations[column].dropna()
        axis.hist(values, bins=35, color="#365F91", alpha=0.78, edgecolor="white")
        median, low, high = _summary_interval(summary, column)
        axis.axvline(median, color="#D97941", linewidth=2, label=f"Mediana: {median:.2f}")
        axis.axvline(low, color="#B33A3A", linestyle="--", linewidth=1.5, label=f"IC 95%: [{low:.2f}, {high:.2f}]")
        axis.axvline(high, color="#B33A3A", linestyle="--", linewidth=1.5)
        axis.set_xlabel(label)
        axis.set_ylabel("Frequência das simulações")
        axis.set_title(label)
        axis.legend(fontsize=9)

    backlog = summary.get("monte_carlo", {}).get("backlog_size", "?")
    fig.suptitle(f"Monte Carlo — projeção para backlog de {backlog} tarefas", y=1.03)
    fig.text(0.5, -0.01, "Bootstrap sobre as observações disponíveis; projeção, não novas observações experimentais.", ha="center", fontsize=10)
    fig.tight_layout()
    save_chart(fig, "monte_carlo_distribuicoes.png")
