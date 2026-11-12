"""App Streamlit do Lab04: página "Dashboard" (painel de BI) e navegação para o "Relatório".

O app tem duas páginas, no menu do topo:
- **Dashboard** (padrão, este arquivo): o formato de painel descrito abaixo.
- **Relatório** (`src/relatorio.py`): as 7 seções com textos e tabelas que o enunciado avalia (§4).

Dashboard Streamlit do Lab04, no formato de painel (BI).

Só gráficos interativos e indicadores, com rótulos curtos; as explicações ficam na
apresentação (`APRESENTACAO.md`). Filtros numa linha no topo (α e situações), seis
indicadores e os gráficos na ordem do estudo: dados (G1 e dispersão real), como os
testes funcionam (G2) e efeito na amostra real, erro tipo I (G3) e vantagem de poder,
poder (G4) e, se a simulação extra existir, poder e erro tipo I × tamanho da amostra.

Issues: #82 (T07), #87 (T12), #93 (navegação entre Dashboard e Relatório).
"""

import sys
from pathlib import Path

# Garante que `src/` esteja no sys.path tanto via `uv run lab04` quanto no Streamlit Cloud.
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd  # noqa: E402
import plotly.graph_objects as go  # noqa: E402
import streamlit as st  # noqa: E402

import figures  # noqa: E402
import relatorio  # noqa: E402
import sample_size  # noqa: E402
import simulate  # noqa: E402
import stat_tests  # noqa: E402
from config import ALPHAS, DASHBOARD_URL, DEFAULT_ALPHA, PROJECTS_URL, REPO_URL, SITUATIONS  # noqa: E402
from data import FULL_CSV, SAMPLE_CSV  # noqa: E402

TITLE = "Pearson × Spearman · NASA KC1"

# Rótulos dos gráficos, na ordem em que aparecem.
CHARTS = {
    "g1": "Distribuição · real × simulado (S-real)",
    "scatter": "LOC × defeitos · dados reais",
    "g2": "Estatística t sob H₀ · S-real, n = 30",
    "effect": "Correlação na amostra real · IC 95%",
    "g3": "Erro tipo I · ρ = 0",
    "gap": "Spearman − Pearson · taxa de rejeição (pp)",
    "g4": "Poder × tamanho do efeito",
    "n": "Poder e erro tipo I × tamanho da amostra",
}

SHORT_SITUATIONS = {
    "S-base": "S-base (normal)",
    "S-real": "S-real",
    "S-real-n10": "S-real-n10",
    "S-outlier": "S-outlier",
}

KPI_EFFECT = 0.6  # ρ latente dos indicadores de poder


def _dec(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def _pct(value: float, digits: int = 1, sign: bool = False) -> str:
    return f"{100 * value:{'+' if sign else ''}.{digits}f}%".replace(".", ",")


def _subtitles(fig: go.Figure) -> None:
    """Títulos dos painéis no mesmo tamanho em todos os gráficos."""
    for annotation in fig.layout.annotations:
        if annotation.yref == "paper":
            annotation.font = dict(size=12)


@st.cache_data
def get_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Amostra real (n = 30), KC1 completo e resumo das simulações."""
    return pd.read_csv(SAMPLE_CSV), pd.read_csv(FULL_CSV), simulate.load_summary()


@st.cache_resource
def get_analysis() -> stat_tests.RealAnalysis:
    """Testes na amostra real com IC 95% (o bootstrap leva alguns segundos)."""
    return stat_tests.real_sample_analysis()


def rate(summary: pd.DataFrame, situation: str, rho: float, test: str, alpha: float) -> float:
    """Taxa de rejeição simulada de uma célula (situação × ρ × teste × α)."""
    row = summary[
        (summary["situation"] == situation)
        & ((summary["rho"] - rho).abs() < 1e-9)
        & (summary["test"] == test)
        & ((summary["alpha"] - alpha).abs() < 1e-9)
    ]
    return float(row["reject_rate"].iloc[0])


# --------------------------------------------------------------------------- aparência


def card(fig: go.Figure, key: str, height: int) -> go.Figure:
    """Padrão visual dos cartões: título curto, legenda horizontal embaixo, margens enxutas."""
    fig.update_layout(
        title=dict(text=CHARTS[key], x=0.0, xanchor="left", y=0.98, yanchor="top",
                   font=dict(size=15)),
        height=height,
        margin=dict(t=64, b=8, l=8, r=8),
        legend=dict(orientation="h", yanchor="top", y=-0.22, xanchor="left", x=0.0,
                    title_text=None, font=dict(size=11)),
        hoverlabel=dict(font_size=12),
    )
    return fig


def show(fig: go.Figure, key: str) -> None:
    with st.container(border=True):
        st.plotly_chart(fig, width="stretch", key=key,
                        config={"displaylogo": False, "modeBarButtonsToRemove": ["lasso2d", "select2d"]})


def _drop_annotations(fig: go.Figure, keep=lambda a: False) -> None:
    fig.layout.annotations = [a for a in fig.layout.annotations if keep(a)]


def chart_g1(sample_df: pd.DataFrame, full_df: pd.DataFrame) -> go.Figure:
    fig = figures.fig_g1(sample_df=sample_df, full_df=full_df)
    _drop_annotations(fig)
    fig.update_xaxes(title_text="LOC (escala log)", row=1, col=1)
    fig.update_xaxes(title_text="Defeitos por classe", row=1, col=2)
    fig.update_yaxes(title_text="% de classes", row=1, col=1)
    fig.update_yaxes(title_text=None, row=1, col=2)
    for trace in fig.data:
        trace.name = trace.name.replace(" (ref. 500 réplicas)", " (500 réplicas)")
    return card(fig, "g1", 400)


def chart_scatter(sample_df, full_df, analysis) -> go.Figure:
    fig = figures.fig_real_scatter(sample_df, full_df, analysis)
    return card(fig, "scatter", 400)


def chart_g2(alpha: float) -> go.Figure:
    fig = figures.fig_g2(alpha=alpha)
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="Densidade", row=1, col=1)
    _subtitles(fig)
    fig = card(fig, "g2", 430)
    fig.update_layout(legend=dict(y=-0.2))
    return fig


def chart_effect(analysis) -> go.Figure:
    fig = card(figures.fig_real_effect(analysis), "effect", 430)
    fig.update_layout(legend=dict(y=-0.25))
    return fig


def chart_g3(alpha: float, situations: list[str]) -> go.Figure:
    table = figures.type1_table(alpha)
    table = table[table["situation"].isin(situations)]
    fig = figures.fig_g3(alpha=alpha, table=table)
    # Sem a coluna de rótulos à direita: os valores ficam no hover; só o ponto fora da escala
    # (seta na borda) ganha o valor ao lado.
    _drop_annotations(fig)
    shown = [s for s in situations if s in set(table["situation"])]
    x_edge = 0.97 * fig.layout.xaxis.range[1]
    for offset, (_, name, _, _) in zip((-0.17, 0.17), figures.G3_TESTS, strict=True):
        rows = table[table["test"] == name].set_index("situation").loc[shown]
        for i, value in enumerate(rows["rate"]):
            if value > figures.G3_OFFSCALE_FACTOR * alpha:
                fig.add_annotation(x=x_edge, y=i + offset, text=_pct(value), showarrow=False,
                                   xanchor="right", xshift=-10, font=dict(size=11))
    fig.update_yaxes(ticktext=[SHORT_SITUATIONS[s] for s in shown])
    fig.update_xaxes(title_text="% de rejeições com ρ = 0")
    fig = card(fig, "g3", 400)
    fig.update_layout(margin=dict(l=8, r=16))
    return fig


def chart_gap(alpha: float, summary: pd.DataFrame, situations: list[str]) -> go.Figure:
    fig = figures.fig_power_gap(alpha, summary[summary["situation"].isin(situations)])
    fig.update_yaxes(ticktext=[SHORT_SITUATIONS[s] for s in situations],
                     tickvals=situations)
    return card(fig, "gap", 400)


def chart_g4(alpha: float, summary: pd.DataFrame, situations: list[str]) -> go.Figure:
    fig = figures.fig_g4(alpha=alpha, summary=summary[summary["situation"].isin(situations)],
                         cols=len(situations))
    for annotation in fig.layout.annotations:
        annotation.text = SHORT_SITUATIONS.get(annotation.text.split(" — ")[0], annotation.text)
        annotation.font = dict(size=12)
    fig.update_xaxes(tickvals=[0.0, 0.2, 0.4, 0.6], ticktext=["0", "0,2", "0,4", "0,6"],
                     title_text="ρ latente", title_font=dict(size=11), tickfont=dict(size=11))
    fig.update_yaxes(title_text=None)
    fig.update_yaxes(title_text="Poder", row=1, col=1)
    fig = card(fig, "g4", 380)
    fig.update_layout(legend=dict(y=-0.28))
    return fig


def chart_sample_size(results: pd.DataFrame, alpha: float) -> go.Figure:
    fig = sample_size.fig_sample_size(results, alpha)
    _subtitles(fig)
    fig.update_xaxes(title_text="n (classes, escala log)", row=2)
    fig.update_yaxes(title_text=None)
    fig.update_yaxes(title_text="Rejeições", row=1, col=1)
    fig.update_yaxes(title_text="Rejeições", row=2, col=1)
    fig = card(fig, "n", 560)
    fig.update_layout(legend=dict(y=-0.12))
    return fig


# --------------------------------------------------------------------------- página


def render_filters() -> tuple[float, list[str]]:
    """Título, link do repositório e os dois filtros (α e situações) numa linha."""
    col_title, col_alpha, col_sit = st.columns([2.2, 1.0, 2.4], vertical_alignment="bottom")
    with col_title:
        st.markdown(f"### {TITLE}")
        st.caption(
            f"[Dashboard online]({DASHBOARD_URL}) · [Repositório]({REPO_URL}) · "
            f"[GitHub Projects]({PROJECTS_URL}) · textos e tabelas na página **Relatório**"
        )
    with col_alpha:
        alpha = st.segmented_control(
            "α",
            options=list(ALPHAS),
            default=st.session_state.get(relatorio.SHARED_ALPHA, DEFAULT_ALPHA),
            format_func=lambda a: _dec(a),
            key="alpha",
        )
    with col_sit:
        situations = st.multiselect(
            "Situações",
            options=list(SITUATIONS),
            default=list(SITUATIONS),
            key="situations",
        )
    # Desmarcar tudo não deixa o painel vazio: volta ao padrão.
    alpha = DEFAULT_ALPHA if alpha is None else float(alpha)
    st.session_state[relatorio.SHARED_ALPHA] = alpha  # o Relatório abre com o mesmo α
    situations = [s for s in SITUATIONS if s in situations] or list(SITUATIONS)
    return alpha, situations


def render_kpis(alpha: float, summary: pd.DataFrame, analysis) -> None:
    """Seis indicadores: correlação real, erro tipo I na S-outlier e poder na S-real."""
    a = analysis
    t1_p = rate(summary, "S-outlier", 0.0, "pearson", alpha)
    t1_s = rate(summary, "S-outlier", 0.0, "spearman", alpha)
    pw_p = rate(summary, "S-real", KPI_EFFECT, "pearson", alpha)
    pw_s = rate(summary, "S-real", KPI_EFFECT, "spearman", alpha)
    rho = _dec(KPI_EFFECT, 1)
    tiles = (
        ("r · amostra real", _dec(float(a.pearson.coef)),
         f"{_dec(a.r_without_influential - float(a.pearson.coef))} sem a maior classe", "off"),
        ("ρₛ · amostra real", _dec(float(a.spearman.coef)),
         f"{_dec(a.rho_s_without_influential - float(a.spearman.coef))} sem a maior classe", "off"),
        ("Erro tipo I · Pearson · S-outlier", _pct(t1_p),
         f"{_pct(t1_p - alpha, sign=True)} vs α", "inverse"),
        ("Erro tipo I · Spearman · S-outlier", _pct(t1_s),
         f"{_pct(t1_s - alpha, sign=True)} vs α", "inverse"),
        (f"Poder · Pearson · S-real, ρ = {rho}", _pct(pw_p, 0), None, "normal"),
        (f"Poder · Spearman · S-real, ρ = {rho}", _pct(pw_s, 0), None, "normal"),
    )
    for col, (label, value, delta, color) in zip(st.columns(len(tiles)), tiles, strict=True):
        col.metric(label, value, delta=delta, delta_color=color, border=True)


def dashboard_page() -> None:
    """Página "Dashboard": filtros, indicadores e gráficos, sem textos explicativos."""
    st.markdown(
        "<style>.block-container{padding-top:1.6rem;padding-bottom:1rem}</style>",
        unsafe_allow_html=True,
    )

    sample_df, full_df, summary = get_data()
    analysis = get_analysis()
    alpha, situations = render_filters()
    render_kpis(alpha, summary, analysis)

    left, right = st.columns([3, 2])
    with left:
        show(chart_g1(sample_df, full_df), "g1")
    with right:
        show(chart_scatter(sample_df, full_df, analysis), "scatter")

    left, right = st.columns([3, 2])
    with left:
        show(chart_g2(alpha), "g2")
    with right:
        show(chart_effect(analysis), "effect")

    left, right = st.columns(2)
    with left:
        show(chart_g3(alpha, situations), "g3")
    with right:
        show(chart_gap(alpha, summary, situations), "gap")

    show(chart_g4(alpha, summary, situations), "g4")

    # Extra opcional (#91): aparece só se data/sim/sample_size.csv existir.
    results = sample_size.load()
    if results is not None:
        show(chart_sample_size(results, alpha), "n")


def main() -> None:
    """Configura a página e monta o menu com as duas páginas (Dashboard é a padrão)."""
    st.set_page_config(page_title="Lab04 · Pearson × Spearman", page_icon="📊", layout="wide")
    pages = [
        st.Page(dashboard_page, title="Dashboard", icon="📊", url_path="dashboard", default=True),
        st.Page(relatorio.main, title="Relatório", icon="📄", url_path="relatorio"),
    ]
    st.navigation(pages, position="top").run()


if __name__ == "__main__":
    main()
