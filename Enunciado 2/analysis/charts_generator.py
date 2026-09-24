#!/usr/bin/env python3
"""Generate report-ready charts for RQ1-RQ3 from trials-log.json and metrics.json."""

import io
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "trials-log.json"
TRIALS_DIR = BASE_DIR / "trials"
CHARTS_DIR = BASE_DIR / "analysis" / "charts"

TREATMENTS = ("SEM_IA", "COM_IA")
TREATMENT_LABELS = {"SEM_IA": "Sem IA", "COM_IA": "Com IA"}
TREATMENT_PALETTE = {"SEM_IA": "#4C72B0", "COM_IA": "#DD8452"}

# Mesmos aliases usados em code_quality.py, para manter os katas agrupados
# corretamente mesmo quando o kataId mudou de nome entre trials antigos e novos.
ALIASES = {
    "kata-05-isbn-10-calculator": "kata-05-isbn-10-validator",
    "kata-06-pagination": "kata-06-array-chunking-pagination",
}

DPI = 300

sns.set_theme(style="whitegrid", context="talk")


def canonical_kata(kata: str) -> str:
    return ALIASES.get(kata, kata)


def load_trials_log() -> pd.DataFrame:
    """Consolida data/trials-log.json em um DataFrame, com kata_key normalizado."""
    with DATA_PATH.open(encoding="utf-8") as handle:
        records = json.load(handle)

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(f"{DATA_PATH} não contém registros de trials")

    df["kata_key"] = df["kata"].map(canonical_kata)
    df["treatment"] = df["treatment"].str.upper()
    df["duration_minutes"] = df["duration_seconds"] / 60
    return df


def parse_trial_directory(path: Path) -> Tuple[str, str, str]:
    """Extrai developer, kata e treatment a partir do nome da pasta do trial."""
    name = path.name
    match = re.match(r"^(?P<kata>.+)-(?P<treatment>com-ia|sem-ia)$", name, re.IGNORECASE)
    if not match:
        raise ValueError(f"Sufixo de tratamento desconhecido na pasta do trial: {path}")

    treatment = match.group("treatment").upper().replace("-", "_")
    return path.parent.name, match.group("kata"), treatment


def load_metrics() -> pd.DataFrame:
    """Consolida todos os trials/<dev>/<kata>-<tratamento>/metrics.json em um DataFrame."""
    rows: List[Dict[str, Any]] = []
    for metrics_path in sorted(TRIALS_DIR.glob("*/*/metrics.json")):
        developer, kata, treatment = parse_trial_directory(metrics_path.parent)
        with metrics_path.open(encoding="utf-8") as handle:
            payload = json.load(handle)

        metrics = payload.get("metrics", {})
        halstead = metrics.get("halstead", {})
        rows.append(
            {
                "trial_id": payload.get("trial_id"),
                "developer": developer,
                "kata": kata,
                "kata_key": canonical_kata(kata),
                "treatment": treatment,
                "cyclomatic_complexity": metrics.get("cyclomatic_complexity"),
                "halstead_volume": halstead.get("volume"),
                "halstead_difficulty": halstead.get("difficulty"),
            }
        )

    return pd.DataFrame(rows)


def savefig(fig: plt.Figure, filename: str) -> None:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    png_path = CHARTS_DIR / filename
    svg_path = png_path.with_suffix(".svg")
    fig.savefig(png_path, dpi=DPI, bbox_inches="tight")
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  - {png_path}")


def plot_rq1_boxplot(trials_df: pd.DataFrame) -> None:
    """RQ1: Boxplot do tempo de resolução (minutos) com pontos individuais."""
    successful = trials_df[trials_df["success"] == True].copy()  # noqa: E712
    order = list(TREATMENTS)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(
        data=successful,
        x="treatment",
        y="duration_minutes",
        order=order,
        hue="treatment",
        palette=TREATMENT_PALETTE,
        legend=False,
        showfliers=False,
        width=0.5,
        ax=ax,
    )
    sns.stripplot(
        data=successful,
        x="treatment",
        y="duration_minutes",
        order=order,
        color="black",
        alpha=0.6,
        size=7,
        jitter=0.15,
        ax=ax,
    )
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([TREATMENT_LABELS[t] for t in order])
    ax.set_xlabel("Tratamento")
    ax.set_ylabel("Tempo de resolução (minutos)")
    ax.set_title("RQ1 — Distribuição do tempo de resolução por tratamento")
    savefig(fig, "rq1_tempo_resolucao.png")


def plot_rq2_violin(trials_df: pd.DataFrame) -> None:
    """RQ2: Violin plot de test_attempts com strip plot sobreposto (sem barras)."""
    successful = trials_df[trials_df["success"] == True].copy()  # noqa: E712
    order = list(TREATMENTS)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.violinplot(
        data=successful,
        x="treatment",
        y="test_attempts",
        order=order,
        hue="treatment",
        palette=TREATMENT_PALETTE,
        legend=False,
        inner=None,
        cut=0,
        bw_adjust=0.8,
        ax=ax,
    )
    sns.stripplot(
        data=successful,
        x="treatment",
        y="test_attempts",
        order=order,
        color="black",
        alpha=0.7,
        size=7,
        jitter=0.2,
        ax=ax,
    )
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([TREATMENT_LABELS[t] for t in order])
    ax.set_xlabel("Tratamento")
    ax.set_ylabel("Tentativas até o Time-to-Green")
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.set_title("RQ2 — Distribuição de tentativas (test_attempts) por tratamento")
    savefig(fig, "rq2_test_attempts_violin.png")


def plot_rq2_success_rate(trials_df: pd.DataFrame) -> None:
    """RQ2: Dot plot da taxa de sucesso (%) dentro do timebox, por tratamento."""
    grouped = trials_df.groupby("treatment")["success"]
    rate = (grouped.mean() * 100).reindex(TREATMENTS)
    counts = grouped.agg(["sum", "count"]).reindex(TREATMENTS)

    fig, ax = plt.subplots(figsize=(8, 4))
    y_positions = np.arange(len(TREATMENTS))
    colors = [TREATMENT_PALETTE[t] for t in TREATMENTS]

    ax.hlines(y=y_positions, xmin=0, xmax=rate.values, color="#999999", linewidth=2, zorder=1)
    ax.scatter(rate.values, y_positions, s=280, color=colors, zorder=2, edgecolor="white", linewidth=1.5)

    for y, value, treatment in zip(y_positions, rate.values, TREATMENTS):
        n_success = int(counts.loc[treatment, "sum"])
        n_total = int(counts.loc[treatment, "count"])
        ax.text(value + 3, y, f"{value:.1f}% ({n_success}/{n_total})", va="center", fontsize=13)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([TREATMENT_LABELS[t] for t in TREATMENTS])
    ax.set_xlim(0, 115)
    ax.set_xlabel("Taxa de sucesso dentro do timebox (%)")
    ax.set_title("RQ2 — Taxa de sucesso por tratamento")
    ax.grid(axis="x", alpha=0.3)
    ax.grid(axis="y", visible=False)
    savefig(fig, "rq2_taxa_sucesso_dotplot.png")


def plot_rq3_heatmap(metrics_df: pd.DataFrame) -> None:
    """RQ3: Heatmap de métricas de qualidade (médias), normalizadas por métrica."""
    metric_cols = ["cyclomatic_complexity", "halstead_volume", "halstead_difficulty"]
    metric_labels = {
        "cyclomatic_complexity": "Complexidade\nCiclomática",
        "halstead_volume": "Halstead\nVolume",
        "halstead_difficulty": "Halstead\nDifficulty",
    }

    means = metrics_df.groupby("treatment")[metric_cols].mean().reindex(TREATMENTS)

    # Normalização min-max por coluna apenas para a escala de cor;
    # os valores originais (não normalizados) permanecem anotados nas células.
    normalized = means.copy()
    for col in metric_cols:
        col_min, col_max = means[col].min(), means[col].max()
        span = col_max - col_min
        normalized[col] = 0.5 if span == 0 else (means[col] - col_min) / span

    display_cols = [metric_labels[c] for c in metric_cols]
    normalized_display = normalized[metric_cols].copy()
    normalized_display.columns = display_cols
    means_display = means[metric_cols].copy()
    means_display.columns = display_cols

    fig, ax = plt.subplots(figsize=(11, 4.5))
    sns.heatmap(
        normalized_display,
        annot=means_display.round(2),
        fmt=".2f",
        cmap="rocket_r",
        vmin=0,
        vmax=1,
        cbar_kws={"label": "Valor normalizado (min-max por métrica)", "shrink": 0.85},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    ax.set_yticklabels([TREATMENT_LABELS[t] for t in normalized.index], rotation=0)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_title("RQ3 — Métricas de qualidade por tratamento (médias originais anotadas)", pad=16)
    fig.tight_layout()
    savefig(fig, "rq3_metricas_qualidade_heatmap.png")


def main() -> None:
    trials_df = load_trials_log()
    metrics_df = load_metrics()

    if metrics_df.empty:
        raise ValueError(f"Nenhum metrics.json encontrado em {TRIALS_DIR}")

    print(f"Gerando gráficos em {CHARTS_DIR}")
    plot_rq1_boxplot(trials_df)
    plot_rq2_violin(trials_df)
    plot_rq2_success_rate(trials_df)
    plot_rq3_heatmap(metrics_df)
    print("Concluído.")


if __name__ == "__main__":
    main()
