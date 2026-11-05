"""Gráficos do dashboard (Plotly).

G1: dados reais × simulados (histogramas de LOC e defeitos).
G2: distribuição da estatística sob H₀, região de rejeição e p-valor do exemplo.
G3: erro tipo I dos dois testes por situação, com linha em 5%.
G4: curvas de poder dos dois testes × tamanho do efeito.
Todos com título, eixos com unidade, legenda e a mesma cor para cada teste.

Issues: #80 (G1), #81 (G2), #84 (G3), #85 (G4).
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import PALETTE, SEED
from data import FULL_CSV, SAMPLE_CSV
from fit import PARAMS_JSON
from generate import generate, load_params

G1_TEXT = (
    "Os dados reais do NASA KC1 apresentam forte assimetria à direita tanto no tamanho da classe "
    "(LOC com mediana de 162 linhas, assimetria de 3,40 e máximo de 2.883 linhas) quanto no número "
    "de defeitos (assimetria de 5,53, máximo de 101 defeitos e 58,6% das classes empatadas com zero defeitos). "
    "Por isso, na situação realista (S-real), o LOC foi modelado com uma distribuição Gamma(forma = 0,607; "
    "escala = 487,9) — que captura a concentração de classes pequenas e a cauda longa sem ser rejeitada "
    "no teste KS (p = 0,22, ao contrário da lognormal com p = 0,001) — e os defeitos com uma Binomial "
    "Negativa(r = 0,170; média = 4,61), cuja sobredispersão reproduz o excesso de zeros (56,8%) e a cauda "
    "pesada que uma Poisson não conseguiria representar. A cópula gaussiana conecta essas duas marginais "
    "preservando a forma individual de cada variável ao lado da amostra real (n = 30) e do KC1 completo (n = 145)."
)


def fig_g1(
    sample_df: pd.DataFrame | None = None,
    full_df: pd.DataFrame | None = None,
    rho: float = 0.6,
    seed: int = SEED,
) -> go.Figure:
    """Constrói o gráfico G1: histogramas de LOC (escala log) e defeitos (real × simulado S-real).

    Compara a amostra real (n = 30), o dataset KC1 completo como referência (n = 145)
    e os dados simulados pela situação S-real (uma amostra n = 30 e a distribuição
    esperada em 500 réplicas), usando proporção percentual de classes para permitir
    comparação direta entre diferentes tamanhos amostrais.
    """
    if sample_df is None:
        sample_df = pd.read_csv(SAMPLE_CSV)
    if full_df is None:
        full_df = pd.read_csv(FULL_CSV)

    params = load_params() if PARAMS_JSON.exists() else None
    rng_sample = np.random.default_rng(seed)
    sim_loc_30, sim_def_30 = generate("S-real", rho=rho, reps=1, rng=rng_sample)
    sim_loc_30 = sim_loc_30[0]
    sim_def_30 = sim_def_30[0]

    rng_ref = np.random.default_rng(seed + 100)
    sim_loc_ref, sim_def_ref = generate("S-real", rho=rho, reps=500, rng=rng_ref)
    sim_loc_ref = sim_loc_ref.ravel()
    sim_def_ref = sim_def_ref.ravel()

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Tamanho da Classe — LOC (escala log₁₀)",
            "Número de Defeitos por Classe",
        ),
        horizontal_spacing=0.10,
    )

    #Séries comparadas: (nome na legenda, loc_array, defects_array, cor, opacidade)
    series = [
        (
            "Real — Amostra (n = 30)",
            sample_df["loc"].to_numpy(dtype=float),
            sample_df["defects"].to_numpy(dtype=float),
            PALETTE["real_sample"],
            0.88,
        ),
        (
            "Real — KC1 completo (n = 145, ref.)",
            full_df["loc"].to_numpy(dtype=float),
            full_df["defects"].to_numpy(dtype=float),
            PALETTE["real_full"],
            0.75,
        ),
        (
            "Simulado — S-real (amostra n = 30)",
            sim_loc_30,
            sim_def_30,
            PALETTE["sim_sample"],
            0.85,
        ),
        (
            "Simulado — S-real (ref. 500 réplicas)",
            sim_loc_ref,
            sim_def_ref,
            PALETTE["sim_expected"],
            0.70,
        ),
    ]

    loc_bins = dict(start=0.0, end=3.6, size=0.45)
    def_bins = dict(start=0.0, end=105.0, size=5.0)

    for label, loc_vals, def_vals, color, opacity in series:
        # Painel 1: log10(LOC) com rótulos em linhas de código reais
        fig.add_trace(
            go.Histogram(
                x=np.log10(np.maximum(loc_vals, 1.0)),
                name=label,
                legendgroup=label,
                showlegend=True,
                histnorm="percent",
                xbins=loc_bins,
                marker_color=color,
                opacity=opacity,
                hovertemplate=(
                    f"<b>{label}</b><br>"
                    "Faixa log₁₀(LOC): %{x}<br>"
                    "Proporção: %{y:.1f}%<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )

        # Painel 2: Defeitos por classe
        fig.add_trace(
            go.Histogram(
                x=def_vals,
                name=label,
                legendgroup=label,
                showlegend=False,
                histnorm="percent",
                xbins=def_bins,
                marker_color=color,
                opacity=opacity,
                hovertemplate=(
                    f"<b>{label}</b><br>"
                    "Defeitos (faixa): %{x}<br>"
                    "Proporção: %{y:.1f}%<extra></extra>"
                ),
            ),
            row=1,
            col=2,
        )

    # Eixo X do LOC em escala logarítmica legível (linhas de código)
    tick_locs = [1, 3, 10, 30, 100, 300, 1000, 3000]
    fig.update_xaxes(
        title_text="Tamanho da classe — LOC (linhas de código, escala log₁₀)",
        tickvals=[float(np.log10(v)) for v in tick_locs],
        ticktext=[f"{v:,}".replace(",", ".") for v in tick_locs],
        row=1,
        col=1,
    )
    fig.update_yaxes(
        title_text="Proporção de classes (%)",
        row=1,
        col=1,
    )

    fig.update_xaxes(
        title_text="Número de defeitos registrados (defeitos / classe)",
        range=[0, 105],
        row=1,
        col=2,
    )
    fig.update_yaxes(
        title_text="Proporção de classes (%)",
        row=1,
        col=2,
    )

    # Anotações de destaque das características-chave (zeros e outlier extremo)
    p_zero_obs = (full_df["defects"] == 0).mean() * 100
    p_zero_fit = (
        params["defects"]["p_zero_fit"] * 100
        if params is not None
        else (sim_def_ref == 0).mean() * 100
    )
    fig.add_annotation(
        x=18,
        y=68,
        text=(
            f"<b>Excesso de zeros (empates):</b><br>"
            f"KC1: {p_zero_obs:.1f}% sem defeitos<br>"
            f"BinNeg (S-real): {p_zero_fit:.1f}% sem defeitos"
        ),
        showarrow=True,
        arrowhead=2,
        ax=45,
        ay=-15,
        bgcolor="rgba(255,255,255,0.88)",
        bordercolor="#BDC3C7",
        font=dict(size=11),
        row=1,
        col=2,
    )

    fig.add_annotation(
        x=101,
        y=5,
        text="<b>Outlier KC1:</b><br>101 defeitos (2.883 LOC)",
        showarrow=True,
        arrowhead=2,
        ax=-45,
        ay=-35,
        bgcolor="rgba(255,255,255,0.88)",
        bordercolor="#BDC3C7",
        font=dict(size=11),
        row=1,
        col=2,
    )

    fig.update_layout(
        title=dict(
            text="G1 — Distribuição dos Dados Reais (NASA KC1) vs. Simulados (S-real)",
            x=0.0,
            xanchor="left",
        ),
        barmode="group",
        bargap=0.15,
        bargroupgap=0.06,
        height=480,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.08,
            xanchor="left",
            x=0.0,
            title_text="Conjunto de dados:",
        ),
        margin=dict(t=105, b=60, l=60, r=30),
    )

    return fig
