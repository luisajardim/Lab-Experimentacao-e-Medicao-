"""Gráficos Plotly do dashboard do Lab05.

Todas as figuras usam a paleta fixa (`config.PALETTE`), nomes legíveis (`config.MANAGERS`,
`config.SCENARIOS`, `config.PROJECTS`) e unidades nos eixos.

Issues: #105 (T10), #111 (T14), #113 (T16), #115 (T18).
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import stats
from config import CONTROL, MANAGERS, PALETTE, PROJECTS, SCENARIOS, YARN_VARIANTS

TEMPLATE = "plotly_white"
METRIC_LABELS = {
    "wall_s": "Tempo de instalação (s)",
    "footprint_mb": "Pegada total em disco: projeto + cache (MB)",
    "disk_mb": "Disco no projeto (MB)",
    "peak_rss_mb": "Pico de memória RAM (MB)",
    "n_files": "Nº de arquivos criados",
}


def _manager_order(present) -> list[str]:
    return [m for m in MANAGERS if m in set(present)]


def fig_metric_by_scenario(
    desc: pd.DataFrame,
    metric: str = "wall_s",
    title: str | None = None,
    managers: list[str] | None = None,
) -> go.Figure:
    """Barras horizontais ou verticais da mediana (com IQR em barra de erro) por cenário e projeto."""
    if managers is not None:
        desc = desc[desc["manager"].isin(managers)]
    projects = [p for p in PROJECTS if p in set(desc["project"])]
    scenarios = [s for s in SCENARIOS if s in set(desc["scenario"])]
    order = _manager_order(desc["manager"])

    fig = make_subplots(
        rows=1,
        cols=max(len(projects), 1),
        subplot_titles=[PROJECTS[p]["label"] for p in projects],
        shared_yaxes=True,
        horizontal_spacing=0.06,
    )

    for col, project in enumerate(projects, start=1):
        sub_p = desc[desc["project"] == project]
        first = col == 1
        for manager in order:
            sub_m = sub_p[sub_p["manager"] == manager].set_index("scenario").reindex(scenarios)
            err_plus = (sub_m["q3"] - sub_m["median"]).clip(lower=0).fillna(0)
            err_minus = (sub_m["median"] - sub_m["q1"]).clip(lower=0).fillna(0)
            fig.add_trace(
                go.Bar(
                    x=[SCENARIOS[s]["label"] for s in scenarios],
                    y=sub_m["median"],
                    name=MANAGERS[manager]["label"],
                    legendgroup=manager,
                    showlegend=first,
                    marker_color=PALETTE[manager],
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=err_plus,
                        arrayminus=err_minus,
                        thickness=1.2,
                    ),
                    hovertemplate=(
                        f"<b>{MANAGERS[manager]['label']}</b><br>"
                        "Cenário: %{x}<br>"
                        "Mediana: %{y:.2f}<extra></extra>"
                    ),
                ),
                row=1,
                col=col,
            )

    fig.update_yaxes(title_text=METRIC_LABELS.get(metric, metric), row=1, col=1)
    fig.update_layout(
        title=dict(
            text=title or f"Mediana e IQR — {METRIC_LABELS.get(metric, metric)}",
            x=0.0,
            xanchor="left",
        ),
        barmode="group",
        template=TEMPLATE,
        height=430,
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0),
        margin=dict(t=95, b=50, l=65, r=25),
    )
    return fig


def fig_speedup_vs_control(vs_ctrl: pd.DataFrame, control: str = CONTROL) -> go.Figure:
    """Speedup (mediana npm / mediana gerenciador) com IC 95% por bootstrap."""
    projects = [p for p in PROJECTS if p in set(vs_ctrl["project"])]
    scenarios = [s for s in SCENARIOS if s in set(vs_ctrl["scenario"])]
    order = [m for m in MANAGERS if m != control and m in set(vs_ctrl["manager"])]

    fig = make_subplots(
        rows=1,
        cols=max(len(projects), 1),
        subplot_titles=[PROJECTS[p]["label"] for p in projects],
        shared_yaxes=True,
        horizontal_spacing=0.06,
    )

    for col, project in enumerate(projects, start=1):
        sub_p = vs_ctrl[vs_ctrl["project"] == project]
        first = col == 1
        for manager in order:
            sub_m = sub_p[sub_p["manager"] == manager].set_index("scenario").reindex(scenarios)
            err_hi = (sub_m["speedup_high"] - sub_m["speedup"]).clip(lower=0).fillna(0)
            err_lo = (sub_m["speedup"] - sub_m["speedup_low"]).clip(lower=0).fillna(0)
            fig.add_trace(
                go.Scatter(
                    x=[SCENARIOS[s]["label"] for s in scenarios],
                    y=sub_m["speedup"],
                    mode="markers",
                    name=MANAGERS[manager]["label"],
                    legendgroup=manager,
                    showlegend=first,
                    marker=dict(size=10, color=PALETTE[manager]),
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=err_hi,
                        arrayminus=err_lo,
                        thickness=1.6,
                    ),
                    hovertemplate=(
                        f"<b>{MANAGERS[manager]['label']}</b><br>"
                        "Cenário: %{x}<br>"
                        "Speedup: %{y:.2f}×<extra></extra>"
                    ),
                ),
                row=1,
                col=col,
            )
        fig.add_hline(y=1.0, line_dash="dash", line_color="#7F8C8D", row=1, col=col)

    fig.update_yaxes(title_text=f"Speedup vs. {MANAGERS[control]['label']} (×, >1 = mais rápido)",
                     row=1, col=1)
    fig.update_layout(
        title=dict(
            text=f"Speedup em relação ao {MANAGERS[control]['label']} (IC 95% por bootstrap)",
            x=0.0,
            xanchor="left",
        ),
        template=TEMPLATE,
        height=420,
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0),
        margin=dict(t=95, b=50, l=65, r=25),
    )
    return fig


def fig_yarn_comparison(df: pd.DataFrame, metric: str = "wall_s") -> go.Figure:
    """Atalho para o gráfico de comparação entre as 3 variantes do Yarn."""
    desc = stats.describe(df[df["manager"].isin(YARN_VARIANTS)], metric=metric)
    return fig_metric_by_scenario(
        desc,
        metric=metric,
        title=f"Família Yarn — {METRIC_LABELS.get(metric, metric)}",
        managers=list(YARN_VARIANTS),
    )

