from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import TREATMENT_LABELS, TREATMENT_PALETTE, TREATMENTS
from .rendering import save_chart


def _wilson_interval(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    z = 1.959963984540054
    proportion = successes / total
    denominator = 1 + z**2 / total
    center = (proportion + z**2 / (2 * total)) / denominator
    margin = z * np.sqrt(proportion * (1 - proportion) / total + z**2 / (4 * total**2)) / denominator
    return center - margin, center + margin


def plot_attempts(trials: pd.DataFrame) -> None:
    successful = trials[trials["success"] & ~trials["timeout"]].copy()
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.boxplot(data=successful, x="treatment", y="test_attempts", order=TREATMENTS, hue="treatment", palette=TREATMENT_PALETTE, legend=False, showfliers=False, width=0.45, ax=ax)
    sns.stripplot(data=successful, x="treatment", y="test_attempts", order=TREATMENTS, color="#222222", jitter=0.13, size=8, ax=ax)
    ax.set_xticks(range(len(TREATMENTS)))
    ax.set_xticklabels([TREATMENT_LABELS[t] for t in TREATMENTS])
    ax.set_xlabel("Tratamento")
    ax.set_ylabel("Tentativas até o Green")
    ax.set_title("RQ2 — Tentativas entre trials concluídos")
    ax.set_yticks(range(1, int(successful["test_attempts"].max()) + 1))
    ax.grid(axis="x", visible=False)
    ax.text(0, -0.2, "Boxplot = mediana e IQR; pontos = trials individuais. Falhas não entram nesta figura.", transform=ax.transAxes, fontsize=9)
    fig.tight_layout()
    save_chart(fig, "rq2_tentativas_stripplot.png")


def plot_success_rate(trials: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for index, treatment in enumerate(TREATMENTS):
        group = trials[trials["treatment"] == treatment]
        total = len(group)
        successes = int(group["success"].sum())
        rate = successes / total if total else 0
        low, high = _wilson_interval(successes, total)
        ax.bar(index, rate * 100, color=TREATMENT_PALETTE[treatment], width=0.55, label=TREATMENT_LABELS[treatment])
        ax.errorbar(index, rate * 100, yerr=[[rate * 100 - low * 100], [high * 100 - rate * 100]], fmt="none", ecolor="#222222", capsize=5, capthick=1.5)
        ax.text(index, min(108, rate * 100 + 5), f"{rate * 100:.1f}% ({successes}/{total})", ha="center", fontsize=10)
    ax.set_xticks(range(len(TREATMENTS)))
    ax.set_xticklabels([TREATMENT_LABELS[t] for t in TREATMENTS])
    ax.set_ylim(0, 115)
    ax.set_ylabel("Trials concluídos dentro do timebox (%)")
    ax.set_xlabel("Tratamento")
    ax.set_title("RQ2 — Taxa de sucesso por tratamento")
    ax.grid(axis="x", visible=False)
    ax.text(0, -0.2, "Barras de erro = intervalo de confiança de Wilson (95%).", transform=ax.transAxes, fontsize=9)
    fig.tight_layout()
    save_chart(fig, "rq2_taxa_sucesso.png")
