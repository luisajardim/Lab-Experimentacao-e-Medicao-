"""Gráficos Plotly do dashboard do Lab05.

Todas as figuras usam a paleta fixa (`config.PALETTE`), nomes legíveis (`config.MANAGERS`,
`config.SCENARIOS`, `config.PROJECTS`) e unidades nos eixos.

Issues: #105 (T10), #111 (T14), #113 (T16), #115 (T18).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import adoption
import stats
from config import CONTROL, MANAGERS, PALETTE, PROJECTS, SCENARIOS, YARN_VARIANTS

TEMPLATE = "plotly_white"
METRIC_LABELS = {
    "wall_s": "Tempo de instalação (s)",
    "footprint_mb": "Pegada total em disco: projeto + cache (MB)",
    "disk_mb": "Disco no projeto (MB)",
    "cpu_s": "Tempo de CPU (s)",
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


def fig_speedup_vs_control(vs_ctrl: pd.DataFrame, control: str = CONTROL,
                           log_y: bool = False) -> go.Figure:
    """Speedup (mediana do controle / mediana do gerenciador) com IC 95% por bootstrap.

    `log_y` deixa 2× e 0,5× à mesma distância do 1 (útil quando há ganhos e perdas).
    """
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
    if log_y:
        fig.update_yaxes(type="log", tickvals=[0.25, 0.5, 1, 2, 4, 8, 16, 32],
                         ticktext=["0,25×", "0,5×", "1×", "2×", "4×", "8×", "16×", "32×"])
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


FOOTPRINT_PARTS = (("disk_mb", "No projeto", ""), ("cache_mb", "No cache", "/"))


def fig_footprint(
    df: pd.DataFrame,
    scenario: str = "ci",
    managers: list[str] | None = None,
    title: str | None = None,
) -> go.Figure:
    """Pegada em disco: projeto (sólido) + cache (hachurado), por projeto.

    Usa um cenário só (`ci` por padrão: cache vazio antes, cheio depois), porque a pegada quase não
    muda entre cenários. Cada projeto tem o próprio eixo y: as escalas vão de MB a GB.
    """
    selected = list(MANAGERS) if managers is None else list(managers)
    sub = stats.valid_runs(df[(df["scenario"] == scenario) & df["manager"].isin(selected)])
    med = sub.groupby(["project", "manager"])[["disk_mb", "cache_mb"]].median()
    projects = [p for p in PROJECTS if p in set(sub["project"])]
    order = _manager_order(sub["manager"])
    fig = make_subplots(rows=1, cols=max(len(projects), 1),
                        subplot_titles=[PROJECTS[p]["label"] for p in projects],
                        horizontal_spacing=0.08)
    for col, project in enumerate(projects, start=1):
        for metric, part, pattern in FOOTPRINT_PARTS:
            values = [med.loc[(project, m), metric] if (project, m) in med.index else np.nan
                      for m in order]
            fig.add_trace(
                go.Bar(
                    x=[MANAGERS[m]["label"] for m in order],
                    y=values,
                    name=part,
                    legendgroup=part,
                    showlegend=col == 1,
                    marker=dict(color=[PALETTE[m] for m in order], pattern_shape=pattern,
                                pattern_fgcolor="white", line=dict(color="white", width=0.5)),
                    hovertemplate=f"<b>%{{x}}</b><br>{part}: %{{y:,.1f}} MB<extra></extra>",
                ),
                row=1, col=col,
            )
    fig.update_yaxes(title_text="Mediana (MB)", row=1, col=1)
    fig.update_xaxes(tickangle=-25)
    fig.update_layout(
        title=dict(text=title or f"Pegada em disco: projeto + cache (mediana, cenário {scenario})",
                   x=0.0, xanchor="left"),
        barmode="stack",
        template=TEMPLATE,
        height=430,
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0,
                    title_text="Sólido = no projeto · hachurado = no cache  "),
        margin=dict(t=95, b=80, l=65, r=25),
    )
    return fig


def fig_yarn_footprint(df: pd.DataFrame, scenario: str = "ci") -> go.Figure:
    """Pegada em disco das variantes do Yarn: projeto (sólido) + cache (hachurado), por projeto."""
    return fig_footprint(df, scenario=scenario, managers=list(YARN_VARIANTS))


# --------------------------------------------------------------------------- Adoção (T16, #113)


def _fonte(sufixo: str = "") -> str:
    """Crédito da fonte para o rodapé das figuras de adoção."""
    quando = adoption.fetched_at()
    data = f", coletada em {quando[:10]}" if quando else ""
    return f"Fonte: API pública de downloads do npm{data}.{sufixo}"


def fig_adoption_series(weekly: pd.DataFrame, log_y: bool = True) -> go.Figure:
    """Downloads semanais por pacote, ao longo de toda a janela coletada.

    Eixo Y em log por padrão: os volumes vão de milhares a centenas de milhões na mesma figura, e
    em escala linear as três séries menores viram uma linha rente ao zero. Só semanas completas
    entram (ver `adoption.load_weekly`), senão a última aparece como uma queda que não existe.

    Semanas com zero download saem quando o eixo é log: zero não tem lugar nessa escala, e
    mantê-las desenhava um mergulho vertical até 1 na borda esquerda do gráfico.
    """
    dados = weekly[weekly["downloads"] > 0] if log_y else weekly
    fig = go.Figure()
    for package in [p for p in adoption.PACKAGES if p in set(dados["package"])]:
        sub_p = dados[dados["package"] == package].sort_values("week_start")
        fig.add_trace(
            go.Scatter(
                x=sub_p["week_start"],
                y=sub_p["downloads"],
                mode="lines",
                name=adoption.PACKAGE_LABELS[package],
                line=dict(color=adoption.PACKAGE_PALETTE[package], width=2),
                hovertemplate=(
                    f"<b>{adoption.PACKAGE_LABELS[package]}</b><br>"
                    "Semana de %{x|%d/%m/%Y}<br>"
                    "%{y:,.0f} downloads<extra></extra>"
                ),
            )
        )
    fig.update_yaxes(title_text="Downloads por semana" + (" (escala log)" if log_y else ""),
                     type="log" if log_y else "linear")
    fig.update_xaxes(title_text="Semana")
    fig.update_layout(
        title=dict(text="Downloads semanais no registry npm, por pacote", x=0.0, xanchor="left"),
        template=TEMPLATE,
        height=430,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0),
        margin=dict(t=95, b=70, l=65, r=25),
    )
    fig.add_annotation(
        text=_fonte(" Só a era de cada ferramenta e só semanas completas."),
        xref="paper", yref="paper", x=0.0, y=-0.22, showarrow=False,
        font=dict(size=10, color="#7F8C8D"), xanchor="left",
    )
    return fig


def fig_adoption_share(weekly: pd.DataFrame) -> go.Figure:
    """Participação de cada pacote no total da semana, em área empilhada de 100 %.

    Composição ao longo do tempo: a pergunta aqui é "quem ganhou e quem perdeu espaço", e a área
    empilhada normalizada responde isso sem sofrer com as ordens de grandeza do gráfico absoluto.
    **Não é participação de mercado** — o npm vem com o Node.js e por isso quase não é baixado.
    """
    com_share = adoption.add_share(weekly)
    fig = go.Figure()
    for package in [p for p in adoption.PACKAGES if p in set(com_share["package"])]:
        sub_p = com_share[com_share["package"] == package].sort_values("week_start")
        fig.add_trace(
            go.Scatter(
                x=sub_p["week_start"],
                y=sub_p["share"] * 100,
                mode="lines",
                name=adoption.PACKAGE_LABELS[package],
                stackgroup="one",
                groupnorm="percent",
                line=dict(width=0.5, color=adoption.PACKAGE_PALETTE[package]),
                fillcolor=adoption.PACKAGE_PALETTE[package],
                hovertemplate=(
                    f"<b>{adoption.PACKAGE_LABELS[package]}</b><br>"
                    "Semana de %{x|%d/%m/%Y}<br>"
                    "%{y:.1f}% dos downloads<extra></extra>"
                ),
            )
        )
    fig.update_yaxes(title_text="Participação nos 5 pacotes (%)", range=[0, 100], ticksuffix="%")
    fig.update_xaxes(title_text="Semana")
    fig.update_layout(
        title=dict(text="Participação de cada pacote nos downloads da semana", x=0.0,
                   xanchor="left"),
        template=TEMPLATE,
        height=430,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0),
        margin=dict(t=95, b=70, l=65, r=25),
    )
    fig.add_annotation(
        text=_fonte(" Participação entre estes 5 pacotes — não é participação de mercado."),
        xref="paper", yref="paper", x=0.0, y=-0.22, showarrow=False,
        font=dict(size=10, color="#7F8C8D"), xanchor="left",
    )
    return fig


def fig_adoption_growth(table: pd.DataFrame) -> go.Figure:
    """Crescimento dos downloads no último ano, em barras horizontais ordenadas.

    Barras porque a pergunta é comparar categorias, horizontais porque os nomes dos pacotes são
    longos, e ordenadas pelo próprio valor. A linha em 0 % separa crescimento de queda.
    """
    dados = table.dropna(subset=["growth_pct"]).sort_values("growth_pct")
    fig = go.Figure(
        go.Bar(
            x=dados["growth_pct"],
            y=dados["label"],
            orientation="h",
            marker_color=[adoption.PACKAGE_PALETTE[p] for p in dados["package"]],
            text=[f"{v:+.0f}%".replace(".", ",") for v in dados["growth_pct"]],
            textposition="outside",
            cliponaxis=False,
            customdata=dados[["downloads_year", "downloads_prev_year"]].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Último ano: %{customdata[0]:,.0f}<br>"
                "Ano anterior: %{customdata[1]:,.0f}<br>"
                "Crescimento: %{x:+.1f}%<extra></extra>"
            ),
        )
    )
    fig.add_vline(x=0.0, line_color="#7F8C8D")
    fig.update_xaxes(title_text="Crescimento dos downloads no último ano (%)", ticksuffix="%")
    fig.update_layout(
        title=dict(text="Crescimento no último ano (365 dias contra os 365 anteriores)", x=0.0,
                   xanchor="left"),
        template=TEMPLATE,
        height=360,
        showlegend=False,
        margin=dict(t=85, b=110, l=140, r=70),
    )
    fig.add_annotation(
        text=_fonte(" Crescimento de tráfego no registry, não de número de pessoas."),
        xref="paper", yref="paper", x=0.0, y=-0.40, showarrow=False,
        font=dict(size=10, color="#7F8C8D"), xanchor="left",
    )
    return fig


def _log_range(values, pad_left: float = 0.55, pad_right: float = 0.45) -> list | None:
    """Faixa do eixo log com folga, para o rótulo do ponto da ponta não sair da figura."""
    if values is None or len(values) == 0:
        return None
    positivos = [float(v) for v in values if v and v > 0]
    if not positivos:
        return None
    return [np.log10(min(positivos)) - pad_left, np.log10(max(positivos)) + pad_right]


def _label_positions(points: pd.DataFrame) -> list[str]:
    """Rótulo acima do ponto; abaixo no mais baixo de cada par que divide o mesmo x.

    Os dois linkers do Berry caem exatamente no mesmo x (mesmo pacote), então sem isso os dois
    rótulos se escrevem um por cima do outro.
    """
    posicoes = []
    for _, row in points.iterrows():
        mesmos_x = points[points["downloads_year"] == row["downloads_year"]]
        embaixo = len(mesmos_x) > 1 and row["speedup_geo"] <= mesmos_x["speedup_geo"].min()
        posicoes.append("bottom center" if embaixo else "top center")
    return posicoes


def fig_adoption_vs_speedup(points: pd.DataFrame, control: str = CONTROL) -> go.Figure:
    """Adoção (downloads no último ano) × speedup medido contra o npm, um ponto por tratamento.

    Dispersão com rótulo em cada ponto, sem legenda e **sem linha de tendência**: são 5 pontos de
    dados observacionais, e qualquer reta aí sugeriria uma relação que 5 pontos não sustentam.
    O eixo X é log porque a adoção varia por ordens de grandeza.

    O npm não é um ponto: ele é a linha horizontal em 1×. O speedup dele é 1 por definição e o
    volume de downloads dele não é comparável (vem com o Node.js), então colocá-lo no eixo X
    produziria exatamente a leitura errada que a §4 de `docs/fonte_downloads.md` proíbe.

    As barras verticais são a **amplitude** do speedup entre as células (projeto × cenário), não
    um intervalo de confiança.
    """
    fig = go.Figure()
    if not points.empty:
        err_hi = (points["speedup_max"] - points["speedup_geo"]).clip(lower=0)
        err_lo = (points["speedup_geo"] - points["speedup_min"]).clip(lower=0)
        fig.add_trace(
            go.Scatter(
                x=points["downloads_year"],
                y=points["speedup_geo"],
                mode="markers+text",
                text=points["label"],
                textposition=_label_positions(points),
                textfont=dict(size=11),
                marker=dict(
                    size=15,
                    color=[PALETTE[m] for m in points["manager"]],
                    line=dict(width=1, color="white"),
                    symbol=["diamond" if s else "circle" for s in points["shared_package"]],
                ),
                error_y=dict(type="data", symmetric=False, array=err_hi, arrayminus=err_lo,
                             thickness=1.4, color="#7F8C8D"),
                customdata=points[["package_label", "n_cells", "speedup_min",
                                   "speedup_max"]].to_numpy(),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Pacote: %{customdata[0]}<br>"
                    "Downloads no último ano: %{x:,.0f}<br>"
                    "Speedup (média geométrica de %{customdata[1]} células): %{y:.2f}×<br>"
                    "Amplitude entre células: %{customdata[2]:.2f}× a %{customdata[3]:.2f}×"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )
    fig.add_hline(y=1.0, line_dash="dash", line_color=PALETTE[control])
    # Rótulo ancorado logo abaixo da própria linha, à esquerda: deixado a cargo do `add_hline`,
    # o texto flutuava para o canto superior e parecia legenda do ponto mais à direita.
    fig.add_annotation(
        text=f"{MANAGERS[control]['label']} (controle): 1× por definição",
        xref="paper", x=0.99, xanchor="right",
        # eixo log: a coordenada da anotação vai em log10, então 1× é 0, não 1
        yref="y", y=0.0, yanchor="top",
        showarrow=False, font=dict(size=11, color=PALETTE[control]),
    )
    fig.update_xaxes(title_text="Downloads no registry no último ano (escala log)", type="log",
                     range=_log_range(points["downloads_year"] if not points.empty else None))
    # Y também em log: speedup é razão, e só em log 0,5× e 2,0× ficam à mesma distância de 1×.
    # Em escala linear a amplitude entre células (que chega a 12×) achatava todos os pontos.
    fig.update_yaxes(
        title_text=f"Speedup vs. {MANAGERS[control]['label']} (×, >1 = mais rápido)",
        type="log",
        tickvals=[0.25, 0.5, 1, 2, 4, 8, 16],
        ticktext=["0,25×", "0,5×", "1×", "2×", "4×", "8×", "16×"],
    )
    fig.update_layout(
        title=dict(text="Associação entre adoção e desempenho medido", x=0.0, xanchor="left"),
        template=TEMPLATE,
        height=470,
        margin=dict(t=85, b=95, l=75, r=45),
    )
    fig.add_annotation(
        text=_fonte(" Desempenho: coleta própria. Barras = amplitude entre células, não IC. "
                    "Losango = tratamentos que compartilham o mesmo pacote."),
        xref="paper", yref="paper", x=0.0, y=-0.26, showarrow=False,
        font=dict(size=10, color="#7F8C8D"), xanchor="left", align="left",
    )
    return fig


# --------------------------------------------------------------------------- Promessas (T18, #115)


def fig_claims_vs_measured(claims_df: pd.DataFrame) -> go.Figure:
    """Speedup medido (pontos com IC 95%) comparado às promessas de pnpm e Bun (eixo log)."""
    managers = [m for m in ("pnpm", "bun") if m in set(claims_df["manager"])]
    scenarios = [s for s in SCENARIOS if s in set(claims_df["scenario"])]
    projects = [p for p in PROJECTS if p in set(claims_df["project"])]
    symbols = {"express-api": "circle", "react-vite": "square", "next-app": "diamond"}

    fig = make_subplots(
        rows=1,
        cols=max(len(managers), 1),
        subplot_titles=[f"{MANAGERS[m]['label']} — prometido × medido" for m in managers],
        shared_yaxes=True,
        horizontal_spacing=0.08,
    )

    for col, manager in enumerate(managers, start=1):
        sub_m = claims_df[claims_df["manager"] == manager]
        # Faixa ou valor anunciado por cenário
        for s_idx, scenario in enumerate(scenarios):
            c_rows = sub_m[sub_m["scenario"] == scenario]
            if c_rows.empty:
                continue
            c_lo = float(c_rows["claimed_low"].iloc[0])
            c_hi = float(c_rows["claimed_high"].iloc[0])
            x_left, x_right = s_idx - 0.34, s_idx + 0.34
            if c_hi > c_lo:
                fig.add_trace(
                    go.Scatter(
                        x=[x_left, x_right, x_right, x_left, x_left],
                        y=[c_lo, c_lo, c_hi, c_hi, c_lo],
                        fill="toself",
                        fillcolor="rgba(44, 62, 80, 0.14)",
                        line=dict(color="#2C3E50", width=1, dash="dot"),
                        name="Faixa/valor anunciado" if (col == 1 and s_idx == 0) else None,
                        legendgroup="anunciado",
                        showlegend=(col == 1 and s_idx == 0),
                        hovertemplate=(
                            f"<b>Anunciado ({MANAGERS[manager]['label']})</b><br>"
                            f"{SCENARIOS[scenario]['label']}: {c_rows['claimed_label'].iloc[0]}"
                            "<extra></extra>"
                        ),
                    ),
                    row=1,
                    col=col,
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[x_left, x_right],
                        y=[c_lo, c_lo],
                        mode="lines",
                        line=dict(color="#2C3E50", width=2.5, dash="dash"),
                        name="Faixa/valor anunciado" if (col == 1 and s_idx == 0) else None,
                        legendgroup="anunciado",
                        showlegend=(col == 1 and s_idx == 0),
                        hovertemplate=(
                            f"<b>Anunciado ({MANAGERS[manager]['label']})</b><br>"
                            f"{SCENARIOS[scenario]['label']}: {c_rows['claimed_label'].iloc[0]}"
                            "<extra></extra>"
                        ),
                    ),
                    row=1,
                    col=col,
                )

        # Pontos medidos (um deslocamento horizontal pequeno por projeto)
        offsets = np.linspace(-0.18, 0.18, max(len(projects), 1))
        for p_idx, project in enumerate(projects):
            sub_p = sub_m[sub_m["project"] == project].set_index("scenario").reindex(scenarios)
            err_hi = (sub_p["speedup_high"] - sub_p["speedup"]).clip(lower=0).fillna(0)
            err_lo = (sub_p["speedup"] - sub_p["speedup_low"]).clip(lower=0).fillna(0)
            x_pos = np.arange(len(scenarios)) + (offsets[p_idx] if len(projects) > 1 else 0.0)
            fig.add_trace(
                go.Scatter(
                    x=x_pos,
                    y=sub_p["speedup"],
                    mode="markers",
                    name=PROJECTS[project]["label"],
                    legendgroup=project,
                    showlegend=col == 1,
                    marker=dict(
                        size=10,
                        symbol=symbols.get(project, "circle"),
                        color=PALETTE[manager],
                        line=dict(width=1, color="white"),
                    ),
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=err_hi,
                        arrayminus=err_lo,
                        thickness=1.5,
                        color=PALETTE[manager],
                    ),
                    customdata=sub_p[["claimed_label", "status"]].to_numpy(),
                    hovertemplate=(
                        f"<b>{MANAGERS[manager]['label']} · {PROJECTS[project]['label']}</b><br>"
                        "Speedup medido: %{y:.2f}×<br>"
                        "Anunciado: %{customdata[0]}<br>"
                        "Status: %{customdata[1]}<extra></extra>"
                    ),
                ),
                row=1,
                col=col,
            )

        fig.add_hline(y=1.0, line_dash="dot", line_color=PALETTE[CONTROL], row=1, col=col)
        if manager == "bun":
            fig.add_hline(
                y=25.0,
                line_dash="dot",
                line_color=PALETTE["bun"],
                annotation_text='Slogan Bun: "até 25×"',
                annotation_position="top left",
                row=1,
                col=col,
            )
        fig.update_xaxes(
            tickvals=list(range(len(scenarios))),
            ticktext=[SCENARIOS[s]["label"] for s in scenarios],
            row=1,
            col=col,
        )

    fig.update_yaxes(
        title_text="Speedup vs. npm (×, escala log)",
        type="log",
        tickvals=[0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128],
        ticktext=["0,25×", "0,5×", "1×", "2×", "4×", "8×", "16×", "32×", "64×", "128×"],
        row=1,
        col=1,
    )
    for col_i in range(2, len(managers) + 1):
        fig.update_yaxes(type="log", row=1, col=col_i)
    fig.update_layout(
        title=dict(
            text="Promessas dos fabricantes (Linux / npm 12) × speedup medido no Windows 11 (IC 95%)",
            x=0.0,
            xanchor="left",
        ),
        template=TEMPLATE,
        height=460,
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="left", x=0.0),
        margin=dict(t=100, b=55, l=70, r=25),
    )
    return fig
