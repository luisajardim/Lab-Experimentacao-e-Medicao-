from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from .config import TIMEBOX_MINUTES, TREATMENT_LABELS, TREATMENT_PALETTE, TREATMENTS
from .differences import improvement_by_kata
from .rendering import save_chart


def _kata_label(value: str) -> str:
    return value.replace("kata-", "K").replace("-", " ").title()


def plot_time_by_kata(trials: pd.DataFrame) -> None:
    pairs = trials.pivot_table(index="kata_key", columns="treatment", values="duration_plot_minutes", aggfunc="first").reindex(columns=TREATMENTS).dropna()
    timeout_pairs = trials.pivot_table(index="kata_key", columns="treatment", values="timeout", aggfunc="first").reindex(columns=TREATMENTS)
    fig, ax = plt.subplots(figsize=(8, 7))
    for kata, row in pairs.iterrows():
        sem_timeout = bool(timeout_pairs.loc[kata, "SEM_IA"])
        com_timeout = bool(timeout_pairs.loc[kata, "COM_IA"])
        marker = "D" if sem_timeout and com_timeout else "x" if sem_timeout else "^" if com_timeout else "o"
        ax.scatter(row["SEM_IA"], row["COM_IA"], color="#4A5568", marker=marker, s=120, edgecolor="white", linewidth=1.2)
    for kata, row in pairs.iterrows():
        ax.annotate(_kata_label(kata), (row["SEM_IA"], row["COM_IA"]), xytext=(6, 5), textcoords="offset points", fontsize=9)
    ax.plot([0, TIMEBOX_MINUTES], [0, TIMEBOX_MINUTES], color="#555555", linestyle="--", label="Mesmo tempo")
    ax.set_xlim(0, TIMEBOX_MINUTES + 1)
    ax.set_ylim(0, TIMEBOX_MINUTES + 1)
    ax.set_xlabel("Tempo sem IA (minutos)")
    ax.set_ylabel("Tempo com IA (minutos)")
    ax.set_title("RQ1 — Relação entre tempos por kata")
    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor="#4A5568", label="Sem timeout", markersize=9),
        plt.Line2D([0], [0], marker="x", color="#4A5568", label="Timeout Sem IA", markersize=9),
        plt.Line2D([0], [0], marker="^", color="#4A5568", label="Timeout Com IA", markersize=9),
        plt.Line2D([0], [0], marker="D", color="#4A5568", label="Timeout nos dois", markersize=8),
        plt.Line2D([0], [0], color="#555555", linestyle="--", label="Mesmo tempo"),
    ]
    ax.legend(handles=handles, loc="upper left")
    ax.text(0, -0.16, "Pontos abaixo da diagonal indicam Com IA mais rápido. O marcador identifica qual tratamento atingiu o timeout de 25 min.", transform=ax.transAxes, fontsize=9)
    fig.tight_layout()
    save_chart(fig, "rq1_tempo_por_kata.png")


def plot_time_difference(trials: pd.DataFrame) -> None:
    pairs = improvement_by_kata(trials, "duration_plot_minutes")
    pairs = pairs.sort_values("improvement")
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh([_kata_label(value) for value in pairs["kata_key"]], pairs["improvement"], color="#2F855A")
    ax.set_xlabel("Redução de tempo observada (minutos)")
    ax.set_ylabel("Kata")
    ax.set_title("RQ1 — Redução de tempo por kata")
    ax.text(0, -0.2, "Apenas reduções são exibidas; casos sem redução aparecem como zero.", transform=ax.transAxes, fontsize=9)
    fig.tight_layout()
    save_chart(fig, "rq1_diferenca_tempo.png")
