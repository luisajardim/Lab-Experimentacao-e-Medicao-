"""Gráficos do dashboard (Plotly).

G1: dados reais × simulados (histogramas de LOC e defeitos).
G2: distribuição da estatística sob H₀, região de rejeição e p-valor do exemplo.
G3: erro tipo I dos dois testes por situação, com linha em 5%.
G4: curvas de poder dos dois testes × tamanho do efeito.
Todos com título, eixos com unidade, legenda e a mesma cor para cada teste.

Issues: #80 (G1), #81 (G2), #84 (G3), #85 (G4).
"""

from functools import cache

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

import stat_tests
from config import DEFAULT_ALPHA, PALETTE, REPS, SEED
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


# Eixo t de -5 a 5; a densidade é relativa a todas as réplicas, mesmo as que ficam fora dele.
G2_T_LIMIT = 5.0
G2_BIN_WIDTH = 0.25
G2_REJECTION_COLOR = "rgba(127, 140, 141, 0.22)"
G2_INK = "#2C3E50"

G2_TEXT = (
    "**O que cada teste compara.** Os dois transformam um coeficiente na mesma estatística "
    "$t = r\\sqrt{(n-2)/(1-r^2)}$ e a comparam com o que seria esperado se não houvesse associação "
    "($H_0$), a distribuição $t$ com $n - 2$ graus de liberdade. O **Pearson** calcula o coeficiente "
    "sobre os valores de LOC e defeitos, então classes gigantes pesam muito; o **Spearman** calcula "
    "sobre os postos, então cada classe pesa igual. Por isso, sob $H_0$, o histograma do Spearman "
    "acompanha a curva, enquanto o do Pearson é mais pontudo e assimétrico, com a cauda direita "
    "longa: quando classes gigantes coincidem com muitos defeitos, o $t$ sobe bastante. Nesses dados, "
    "a curva $t$ é só uma aproximação para o Pearson, e quase todas as suas rejeições indevidas "
    "ficam na cauda direita.\n\n"
    "**Onde fica a região de rejeição.** Nas duas caudas (faixas cinza), onde $|t|$ passa do $t$ "
    "crítico: o teste é bicaudal, então rejeita $H_0$ tanto para associação positiva quanto negativa. "
    "O $t$ crítico é escolhido para que essas caudas somem $\\alpha$ na curva, e muda com o seletor "
    "de $\\alpha$.\n\n"
    "**O que o p-valor significa.** É a área colorida: a probabilidade de obter um $|t|$ tão ou mais "
    "extremo que o observado **se $H_0$ fosse verdadeira**. Rejeita-se $H_0$ quando ele é menor que "
    "$\\alpha$, ou seja, quando o $t$ observado cai na faixa cinza.\n\n"
    "**O que ele não significa.** Não é a probabilidade de $H_0$ ser verdadeira, nem a de o resultado "
    "ser obra do acaso, e não mede o tamanho da associação. Um p-valor grande também não prova que "
    "não há associação: pode faltar poder para detectá-la."
)


@cache
def _null_t(reps: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    """t de Pearson e de Spearman sob H₀ (situação do exemplo, ρ = 0), sem réplicas constantes."""
    x, y = generate(stat_tests.EXAMPLE_SITUATION, 0.0, reps=reps, rng=np.random.default_rng(seed))
    pearson_t, spearman_t = stat_tests.pearson(x, y).t, stat_tests.spearman(x, y).t
    return pearson_t[~np.isnan(pearson_t)], spearman_t[~np.isnan(spearman_t)]


def _null_density(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Centros e densidade dos bins; valores fora do eixo continuam no denominador."""
    edges = np.arange(-G2_T_LIMIT, G2_T_LIMIT + G2_BIN_WIDTH, G2_BIN_WIDTH)
    counts, edges = np.histogram(t, bins=edges)
    return (edges[:-1] + edges[1:]) / 2, counts / (t.size * G2_BIN_WIDTH)


def _two_tails(start: float, height) -> tuple[list, list]:
    """Polígonos das caudas |t| ≥ start; `height(grade)` dá o contorno superior."""
    grid = np.linspace(start, G2_T_LIMIT, 200)
    right_x = [start, *grid, G2_T_LIMIT]
    right_y = [0.0, *height(grid), 0.0]
    return [*(-v for v in right_x), None, *right_x], [*right_y, None, *right_y]


def _decimal(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def fig_g2(
    alpha: float = DEFAULT_ALPHA,
    example: stat_tests.Example | None = None,
    reps: int = REPS,
    seed: int = SEED,
) -> go.Figure:
    """Constrói o G2: nula de cada teste, curva t(n − 2), região de rejeição e p-valor do exemplo.

    Um painel por teste, com a nula simulada na situação do exemplo (S-real, ρ = 0).
    """
    example = example or stat_tests.run_example()
    df = example.pearson.df
    t_critical = float(stats.t.ppf(1 - alpha / 2, df))
    null_pearson, null_spearman = _null_t(reps, seed + 1)
    panels = (
        ("Pearson", example.pearson, _null_density(null_pearson)),
        ("Spearman", example.spearman, _null_density(null_spearman)),
    )

    curve_x = np.linspace(-G2_T_LIMIT, G2_T_LIMIT, 501)
    curve_y = stats.t.pdf(curve_x, df)
    y_top = 1.3 * max(curve_y.max(), *(density.max() for _, _, (_, density) in panels))

    fig = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.05,
        subplot_titles=[
            f"{name}: t = {_decimal(result.t)}, p = {_decimal(result.p, 3)}"
            for name, result, _ in panels
        ],
    )
    for col, (name, result, (centers, density)) in enumerate(panels, start=1):
        first = col == 1
        color = PALETTE[name]
        reject_x, reject_y = _two_tails(t_critical, lambda grid: np.full_like(grid, y_top))
        fig.add_trace(
            go.Scatter(
                x=reject_x,
                y=reject_y,
                mode="lines",
                line=dict(width=0),
                fill="toself",
                fillcolor=G2_REJECTION_COLOR,
                name=f"Região de rejeição (|t| > {_decimal(t_critical)}, α = {_decimal(alpha)})",
                legendgroup="rejeicao",
                showlegend=first,
                hoverinfo="skip",
            ),
            row=1,
            col=col,
        )
        fig.add_trace(
            go.Bar(
                x=centers,
                y=density,
                width=G2_BIN_WIDTH * 0.92,
                marker=dict(color=color, opacity=0.4, line=dict(width=0)),
                name=f"Nula simulada — {name}",
                legendgroup=f"nula-{name}",
                hovertemplate=f"{name}, H₀ simulada<br>t ≈ %{{x}}<br>Densidade: %{{y:.3f}}<extra></extra>",
            ),
            row=1,
            col=col,
        )
        if abs(result.t) < G2_T_LIMIT:
            area_x, area_y = _two_tails(
                abs(float(result.t)), lambda grid: stats.t.pdf(grid, df)
            )
            fig.add_trace(
                go.Scatter(
                    x=area_x,
                    y=area_y,
                    mode="lines",
                    line=dict(width=0),
                    fill="toself",
                    fillcolor=color,
                    opacity=0.55,
                    name=f"p-valor do exemplo — {name}",
                    legendgroup=f"p-{name}",
                    hoverinfo="skip",
                ),
                row=1,
                col=col,
            )
            for sign in (-1, 1):
                fig.add_trace(
                    go.Scatter(
                        x=[sign * abs(result.t)] * 2,
                        y=[0, 0.8 * y_top],
                        mode="lines",
                        line=dict(color=G2_INK, width=2, dash="dot"),
                        showlegend=False,
                        hovertemplate="t observado (±): %{x:.2f}<extra></extra>",
                    ),
                    row=1,
                    col=col,
                )
            fig.add_annotation(
                x=float(result.t),
                y=0.8 * y_top,
                text=f"t observado = {_decimal(result.t)}",
                showarrow=False,
                yanchor="bottom",
                font=dict(color=G2_INK, size=11),
                row=1,
                col=col,
            )
        fig.add_trace(
            go.Scatter(
                x=curve_x,
                y=curve_y,
                mode="lines",
                line=dict(color=G2_INK, width=2),
                name=f"Curva teórica t({df})",
                legendgroup="curva",
                showlegend=first,
                hovertemplate=f"t({df})<br>t = %{{x:.2f}}<br>Densidade: %{{y:.3f}}<extra></extra>",
            ),
            row=1,
            col=col,
        )
        for sign in (-1, 1):
            fig.add_annotation(
                x=sign * (t_critical + G2_T_LIMIT) / 2,
                y=y_top,
                text="Rejeita H₀",
                showarrow=False,
                yanchor="top",
                font=dict(color=G2_INK, size=11),
                row=1,
                col=col,
            )
        fig.update_xaxes(
            title_text="Estatística t (adimensional)",
            range=[-G2_T_LIMIT, G2_T_LIMIT],
            dtick=1,
            row=1,
            col=col,
        )
    fig.update_yaxes(title_text="Densidade de probabilidade", range=[0, y_top], row=1, col=1)
    fig.update_layout(
        title=dict(
            text=f"G2 — Estatística t sob H₀ ({example.situation}, n = {example.n}), "
            "região de rejeição e p-valor do exemplo",
            x=0.0,
            xanchor="left",
        ),
        barmode="overlay",
        height=520,
        template="plotly_white",
        separators=",.",
        legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="left", x=0.0),
        margin=dict(t=70, b=130, l=60, r=30),
    )
    return fig
