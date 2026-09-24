from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from .config import CHARTS_DIR

sns.set_theme(style="whitegrid", context="notebook", font_scale=1.05)


def save_chart(fig: plt.Figure, filename: str) -> Path:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    path = CHARTS_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches="tight")
    fig.savefig(path.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)
    return path


def treatment_labels(values):
    return ["Sem IA" if value == "SEM_IA" else "Com IA" for value in values]
