from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .config import QUALITY_LABELS, QUALITY_METRICS, TREATMENT_LABELS, TREATMENT_PALETTE, TREATMENTS
from .differences import improvement_by_kata
from .normalization import join_quality_with_trials
from .rendering import save_chart


def plot_quality_distributions(quality: pd.DataFrame, trials: pd.DataFrame) -> None:
    data = join_quality_with_trials(quality, trials)
    data = data[data["success"] & ~data["timeout"]].copy()
    long = data.melt(id_vars=["treatment"], value_vars=QUALITY_METRICS, var_name="metric", value_name="value")
    long["Métrica"] = long["metric"].map(QUALITY_LABELS)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    for axis, metric in zip(axes.flat, QUALITY_METRICS):
        subset = long[long["metric"] == metric]
        sns.boxplot(data=subset, x="treatment", y="value", order=TREATMENTS, hue="treatment", palette=TREATMENT_PALETTE, legend=False, showfliers=False, width=0.45, ax=axis)
        sns.stripplot(data=subset, x="treatment", y="value", order=TREATMENTS, color="#222222", jitter=0.12, size=6, ax=axis)
        axis.set_title(QUALITY_LABELS[metric])
        axis.set_xticklabels([TREATMENT_LABELS[t] for t in TREATMENTS])
        axis.set_xlabel("")
        axis.set_ylabel("Valor")
    fig.suptitle("RQ3 — Distribuição das métricas de qualidade", y=1.02)
    fig.text(0.5, -0.02, "Boxplot = mediana e IQR; pontos = observações individuais. Métricas estáticas não representam qualidade global.", ha="center", fontsize=10)
    save_chart(fig, "rq3_metricas_distribuicao.png")


def plot_quality_radar(quality: pd.DataFrame) -> None:
    medians = quality.groupby("treatment")[list(QUALITY_METRICS)].median().reindex(TREATMENTS)
    normalized = medians.copy()
    for metric in QUALITY_METRICS:
        observations = quality[metric].dropna()
        low, high = observations.min(), observations.max()
        normalized[metric] = 0.5 if high == low else (medians[metric] - low) / (high - low)

    labels = [QUALITY_LABELS[metric] for metric in QUALITY_METRICS]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})
    for treatment in TREATMENTS:
        values = normalized.loc[treatment].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=TREATMENT_LABELS[treatment], color=TREATMENT_PALETTE[treatment])
        ax.fill(angles, values, color=TREATMENT_PALETTE[treatment], alpha=0.12)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=8)
    ax.set_title("RQ3 — Perfil relativo das métricas por tratamento", pad=25)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
    fig.text(0.5, 0.02, "Medianas normalizadas pelo intervalo das observações válidas; use como perfil, não como magnitude absoluta.", ha="center", fontsize=9)
    fig.tight_layout()
    save_chart(fig, "rq3_perfil_radar.png")


def plot_quality_effects(quality: pd.DataFrame) -> None:
    data = quality.copy()
    pairs = []
    for metric in QUALITY_METRICS:
        improvements = improvement_by_kata(data, metric)
        for _, row in improvements.iterrows():
            pairs.append({"metric": metric, "kata_key": row["kata_key"], "improvement": row["improvement"]})
    differences = pd.DataFrame(pairs)
    fig, axes = plt.subplots(2, 3, figsize=(14, 8), constrained_layout=True)
    for axis, metric in zip(axes.flat, QUALITY_METRICS):
        subset = differences[differences["metric"] == metric].sort_values("improvement")
        axis.barh(subset["kata_key"].str.replace("kata-", "K", regex=False), subset["improvement"], color="#2F855A")
        axis.set_title(QUALITY_LABELS[metric])
        axis.set_xlabel("Redução")
        axis.set_ylabel("")
    fig.suptitle("RQ3 — Redução das métricas por kata", y=1.02)
    fig.text(0.5, -0.02, "Cada painel tem escala própria para preservar a leitura; apenas reduções são exibidas e casos sem redução aparecem como zero.", ha="center", fontsize=10)
    fig.tight_layout()
    save_chart(fig, "rq3_efeitos_metricas.png")
