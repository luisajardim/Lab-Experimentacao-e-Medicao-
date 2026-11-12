"""Gráficos do dashboard (Plotly).

G1: dados reais × simulados (histogramas de LOC e defeitos).
G2: distribuição da estatística sob H₀, região de rejeição e p-valor do exemplo.
G3: erro tipo I dos dois testes por situação, com linha em α e faixa de Monte Carlo.
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

import simulate
import stat_tests
from config import DEFAULT_ALPHA, OUTLIER_RATE, PALETTE, REPS, SEED, SITUATIONS
from data import FULL_CSV, SAMPLE_CSV
from fit import PARAMS_JSON
from generate import generate, load_params

G1_TEXT = (
    "Os dados reais têm forte assimetria à direita: a maioria das classes é pequena (mediana de "
    "162 LOC), poucas são gigantes (até cerca de 2,9 mil LOC) e 58,6% não têm nenhum defeito, "
    "enquanto uma única classe acumula 101. Por isso a S-real usa uma Gamma para o LOC, que "
    "reproduz a cauda longa sem ser rejeitada pelo teste KS (p = 0,22, contra 0,001 da lognormal), "
    "e uma binomial negativa para os defeitos, que reproduz o excesso de zeros (56,8%) que uma "
    "Poisson não teria. Os histogramas simulados acompanham os reais nas duas variáveis; a principal "
    "diferença é que a simulação raramente gera uma classe tão extrema quanto a de 101 defeitos, "
    "motivo da situação S-outlier."
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
            f"a 1ª barra junta 0 a 4 defeitos; exatamente zero:<br>"
            f"KC1: {p_zero_obs:.1f}% · BinNeg (S-real): {p_zero_fit:.1f}%".replace(".", ",")
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
    "O **Pearson** compara os valores de LOC e defeitos e o **Spearman** compara os postos; os dois "
    "viram a estatística $t = r\\sqrt{(n-2)/(1-r^2)}$, cuja distribuição sob $H_0$ é aproximada pela "
    "curva $t$ com $n - 2$ graus de liberdade. Nos dados assimétricos da S-real, o histograma do "
    "Spearman acompanha a curva, mas o do Pearson tem a cauda direita longa, porque classes gigantes "
    "com muitos defeitos inflam o $t$ (quase todas as suas rejeições indevidas ficam desse lado). "
    "Como o teste é bicaudal, a região de rejeição são as duas faixas cinza, onde $|t|$ passa do $t$ "
    "crítico, que muda com o seletor de $\\alpha$. O p-valor do exemplo é a área colorida: a "
    "probabilidade de obter um $|t|$ tão ou mais extremo que o observado **se $H_0$ fosse "
    "verdadeira**, e não é a probabilidade de $H_0$ ser verdadeira."
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


# --------------------------------------------------------------------------- G3 (T09, #84)

G3_INK = "#2C3E50"
G3_BAND_COLOR = "rgba(127, 140, 141, 0.22)"
G3_TESTS = (("pearson", "Pearson", "r", "circle"), ("spearman", "Spearman", "rho_s", "diamond"))
G3_VERDICTS = {"perto": "perto de α", "liberal": "liberal", "conservador": "conservador"}
G3_OFFSCALE_FACTOR = 3.5  # taxas acima de 3,5·α ficam na borda do eixo (com seta)


@cache
def _g3_null() -> pd.DataFrame:
    """p-valores e coeficientes das réplicas com ρ = 0 (todas as situações)."""
    pvalues = simulate.load_pvalues()
    null = pvalues[pvalues["rho"] == 0].copy()
    null["situation"] = null["situation"].astype(str)
    return null


def mc_band(alpha: float, reps: int) -> tuple[float, float]:
    """Faixa de 95% de Monte Carlo em torno de α: α ± 1,96·√(α(1−α)/R) (±0,43 pp com α = 5%)."""
    half = 1.96 * np.sqrt(alpha * (1 - alpha) / reps)
    return alpha - half, alpha + half


def type1_table(alpha: float = DEFAULT_ALPHA, null: pd.DataFrame | None = None) -> pd.DataFrame:
    """Erro tipo I (p < α com ρ = 0) por situação e teste, com a cauda das rejeições.

    p-valor NaN (amostra constante) conta como "não rejeita", como no `simulate.summarize`.
    `verdict` compara a taxa com a faixa de Monte Carlo: dentro é "perto", acima "liberal",
    abaixo "conservador".
    """
    null = _g3_null() if null is None else null
    rows = []
    for situation in [s for s in SITUATIONS if s in set(null["situation"])]:
        group = null[null["situation"] == situation]
        reps = len(group)
        low, high = mc_band(alpha, reps)
        for test, name, coef, _ in G3_TESTS:
            p = group[f"p_{test}"].to_numpy()
            reject = p < alpha
            rate = float(reject.mean())
            verdict = "liberal" if rate > high else "conservador" if rate < low else "perto"
            rows.append(
                {
                    "situation": situation,
                    "test": name,
                    "rate": rate,
                    "mc_se": float(np.sqrt(rate * (1 - rate) / reps)),
                    "right": float((reject & (group[coef].to_numpy() > 0)).mean()),
                    "left": float((reject & (group[coef].to_numpy() < 0)).mean()),
                    "band_low": low,
                    "band_high": high,
                    "n_reps": reps,
                    "n_nan": int(np.isnan(p).sum()),
                    "verdict": verdict,
                }
            )
    return pd.DataFrame(rows)


def _pct(value: float, digits: int = 2) -> str:
    return f"{100 * value:.{digits}f}%".replace(".", ",")


def fig_g3(alpha: float = DEFAULT_ALPHA, table: pd.DataFrame | None = None) -> go.Figure:
    """Constrói o G3: taxa de rejeição com ρ = 0 de cada teste, por situação.

    Uma linha por situação; cada teste é um ponto (cor e símbolo fixos) com barra de ±1,96 erro
    padrão. Linha pontilhada em α e faixa cinza de Monte Carlo em torno dela.
    """
    table = type1_table(alpha) if table is None else table
    situations = list(dict.fromkeys(table["situation"]))
    low, high = table["band_low"].iloc[0], table["band_high"].iloc[0]
    # Taxas muito acima de α (S-outlier) iriam espremer a região perto de α, onde estão as
    # diferenças que importam: esses pontos ficam na borda, com seta, e o rótulo mostra o valor.
    offscale = table["rate"] > G3_OFFSCALE_FACTOR * alpha
    on_scale = table.loc[~offscale, "rate"] + 1.96 * table.loc[~offscale, "mc_se"]
    x_max = max(2 * alpha, 1.25 * float(on_scale.max()))

    fig = go.Figure()
    fig.add_vrect(x0=low, x1=high, fillcolor=G3_BAND_COLOR, line_width=0, layer="below")
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(symbol="square", size=12, color=G3_BAND_COLOR),
            name=f"Faixa de Monte Carlo ({_pct(low)} a {_pct(high)})",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[alpha, alpha],
            y=[-0.5, len(situations) - 0.5],
            mode="lines",
            line=dict(color=G3_INK, width=1.5, dash="dot"),
            name=f"α = {_pct(alpha, 0)} (nível nominal)",
            hoverinfo="skip",
        )
    )
    for offset, (_, name, _, symbol) in zip((-0.17, 0.17), G3_TESTS, strict=True):
        rows = table[table["test"] == name].set_index("situation").loc[situations]
        beyond = (rows["rate"] > G3_OFFSCALE_FACTOR * alpha).to_numpy()
        ys = np.arange(len(situations)) + offset
        fig.add_trace(
            go.Scatter(
                x=np.where(beyond, 0.97 * x_max, rows["rate"]),
                y=ys,
                mode="markers",
                name=name,
                marker=dict(
                    symbol=[f"{symbol}" if not b else "triangle-right" for b in beyond],
                    size=[11 if not b else 14 for b in beyond],
                    color=PALETTE[name],
                    line=dict(color="white", width=2),
                ),
                error_x=dict(
                    type="data",
                    array=np.where(beyond, 0, 1.96 * rows["mc_se"]),
                    color=PALETTE[name],
                    thickness=1.5,
                    width=4,
                ),
                customdata=np.stack(
                    [
                        [_pct(v) for v in rows["rate"]],
                        [G3_VERDICTS[v] for v in rows["verdict"]],
                        [_pct(v) for v in rows["right"]],
                        [_pct(v) for v in rows["left"]],
                        rows["n_nan"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    f"<b>{name}</b> — %{{customdata[1]}}<br>Rejeições com ρ = 0: "
                    "%{customdata[0]}<br>Cauda direita: %{customdata[2]} · esquerda: "
                    "%{customdata[3]}<br>Amostras constantes (não rejeitam): %{customdata[4]}"
                    "<extra></extra>"
                ),
            )
        )
        # Rótulos numa coluna à direita do gráfico, alinhados com cada ponto.
        for y, rate, verdict, off in zip(ys, rows["rate"], rows["verdict"], beyond, strict=True):
            fig.add_annotation(
                x=1.01,
                xref="paper",
                y=y,
                xanchor="left",
                showarrow=False,
                text=f"{name}: {_pct(rate)} · {G3_VERDICTS[verdict]}"
                + (" (fora da escala)" if off else ""),
                font=dict(color=G3_INK, size=11),
            )

    reps_text = f"{int(table['n_reps'].iloc[0]):,}".replace(",", ".")
    fig.update_xaxes(
        title_text="Taxa de rejeição com ρ = 0 (% de amostras com p < α)",
        range=[0, x_max],
        tickformat=".0%",
    )
    fig.update_yaxes(
        tickvals=list(range(len(situations))),
        ticktext=[G4_SITUATION_LABELS.get(s, s) for s in situations],
        autorange="reversed",
        showgrid=False,
        zeroline=False,
    )
    fig.update_layout(
        title=dict(
            text=f"G3 — Erro tipo I do Pearson × Spearman (α = {_decimal(alpha)}, "
            f"{reps_text} réplicas por ponto)",
            x=0.0,
            xanchor="left",
        ),
        height=500,
        template="plotly_white",
        separators=",.",
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="left", x=0.0),
        margin=dict(t=60, b=120, l=260, r=290),
    )
    return fig


def g3_text(alpha: float = DEFAULT_ALPHA, table: pd.DataFrame | None = None,
            population: pd.DataFrame | None = None) -> str:
    """Texto do G3 (Markdown), montado a partir das taxas simuladas para o α escolhido."""
    table = type1_table(alpha) if table is None else table
    population = simulate.load_population() if population is None else population
    low, high = table["band_low"].iloc[0], table["band_high"].iloc[0]
    reps_text = f"{int(table['n_reps'].iloc[0]):,}".replace(",", ".")
    rate = table.set_index(["situation", "test"])
    situations = list(dict.fromkeys(table["situation"]))

    def deviating(test: str, exclude: str | None = None) -> pd.DataFrame:
        rows = table[(table["test"] == test) & (table["verdict"] != "perto")]
        return rows[rows["situation"] != exclude]

    def tails(rows: pd.DataFrame) -> str:
        return "; ".join(
            f"{row.situation}: {_pct(row.rate)}, {_pct(row.right)} à direita e "
            f"{_pct(row.left)} à esquerda"
            for row in rows.itertuples()
        )

    paragraphs = [
        f"Com ρ = 0 e α = {_pct(alpha, 0)}, um teste correto rejeita H₀ em cerca de "
        f"{_pct(alpha, 0)} das amostras. Com {reps_text} réplicas, taxas entre {_pct(low)} e "
        f"{_pct(high)} (faixa cinza) não se distinguem de α; acima dela o teste é **liberal** "
        "(rejeita H₀ verdadeira mais do que deveria) e abaixo, **conservador**.",
        "\n".join(
            f"- **{situation}:** "
            + " · ".join(
                f"{name} {_pct(rate.loc[(situation, name), 'rate'])} "
                f"({G3_VERDICTS[rate.loc[(situation, name), 'verdict']]})"
                for _, name, _, _ in G3_TESTS
            )
            for situation in situations
        ),
    ]

    pearson_off = deviating("Pearson", exclude="S-outlier")
    why = (
        "**Por quê.** O Pearson só tem a distribuição t exata com dados normais (S-base). Com a "
        "forma do KC1, uma classe com LOC e defeitos altos ao mesmo tempo empurra o r para cima, "
        "então a distribuição do t sob H₀ fica assimétrica (veja o G2) e as rejeições do Pearson "
        "caem quase todas na cauda direita."
    )
    if pearson_off.empty:
        why += " Com este α, isso ainda não o tira da faixa fora da S-outlier."
    else:
        why += (
            f" Por isso ele fica liberal ({tails(pearson_off)}): a cauda direita longa passa do "
            "t crítico mais vezes do que a curva prevê, e isso pesa mais com n pequeno e com α "
            "menor."
        )
    spearman_off = deviating("Spearman")
    if spearman_off.empty:
        why += (
            " O Spearman fica perto de α em todas as situações: sob H₀, os postos de Y são uma "
            "permutação ao acaso dos postos de X, qualquer que seja a forma dos dados, e a curva "
            "t aproxima bem a distribuição dos postos."
        )
    else:
        why += (
            " O Spearman não depende da forma dos dados, mas a curva t é só uma aproximação da "
            "distribuição dos postos, pior com poucas observações; "
            f"por isso ele sai da faixa em {', '.join(spearman_off['situation'])} "
            f"({tails(spearman_off)}), sem o desequilíbrio entre as caudas do Pearson."
        )
    paragraphs.append(why)

    outlier_pop = population[(population["situation"] == "S-outlier") & (population["rho"] == 0)]
    if "S-outlier" in situations and not outlier_pop.empty:
        contaminated = 1 - (1 - OUTLIER_RATE) ** SITUATIONS["S-outlier"][1]
        spearman = rate.loc[("S-outlier", "Spearman")]
        spearman_text = (
            "enquanto o Spearman continua perto de α"
            if spearman["verdict"] == "perto"
            else f"enquanto o Spearman fica em {_pct(spearman['rate'])}"
        )
        paragraphs.append(
            "**S-outlier.** Aqui ρ = 0 vale só para as classes comuns: cerca de "
            f"{_pct(contaminated, 0)} das amostras recebem uma classe extrema (LOC e defeitos "
            f"altos), o que dá r = {_decimal(float(outlier_pop['r_pop'].iloc[0]))} na população, "
            f"contra ρₛ = {_decimal(float(outlier_pop['rho_s_pop'].iloc[0]))}. Os "
            f"{_pct(rate.loc[('S-outlier', 'Pearson'), 'rate'])} de rejeições do Pearson vêm "
            "principalmente dessas amostras, em que ele rejeita na maior parte das vezes. Não "
            "é um erro tipo I no sentido estrito, mas é o fenômeno da pergunta: o Pearson aponta "
            f"uma associação que vem só de poucas classes gigantes, {spearman_text}."
        )

    with_nan = table[(table["test"] == "Pearson") & (table["n_nan"] > 0)]
    if not with_nan.empty:
        paragraphs.append(
            f"As {int(with_nan['n_nan'].sum())} amostras em que todas as classes têm o mesmo "
            f"número de defeitos ({', '.join(with_nan['situation'])}) não têm coeficiente "
            "definido e contam como \"não rejeita\"."
        )
    return "\n\n".join(paragraphs)


# --------------------------------------------------------------------------- G4 (T10, #85)

G4_TARGET_POWER = 0.80
G4_INK = "#2C3E50"
G4_SITUATION_LABELS = {
    "S-base": "S-base — normal bivariada (n = 30)",
    "S-real": "S-real — Gamma × BinNeg (n = 30)",
    "S-real-n10": "S-real-n10 — amostra pequena (n = 10)",
    "S-outlier": "S-outlier — ponto dominante (n = 30)",
}

G4_TEXT = (
    "Na **S-base** (dados normais), o Pearson tem um pouco mais de poder em todos os efeitos "
    "(com ρ = 0,4, 62% contra 55% com α = 0,05), como prevê a teoria. Nos dados com a forma do KC1 "
    "(**S-real**), a vantagem troca de lado a partir de ρ ≈ 0,3: com ρ = 0,6 o Spearman detecta a "
    "associação em 85% das amostras e o Pearson em 70%, porque poucas classes extremas deixam o r muito "
    "instável. Com **n = 10** os dois ficam abaixo de 40% mesmo no maior efeito; o Pearson parece ganhar, "
    "mas parte disso é ilusória, já que com ρ = 0 ele rejeita H₀ em 6,5% das vezes (acima de 5%). Na "
    "**S-outlier**, a curva do Pearson já começa em 20% com ρ = 0 (rejeições falsas puxadas pela classe "
    "gigante), e o Spearman o ultrapassa a partir de ρ ≈ 0,4."
)


@cache
def _g4_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Resumo das simulações (taxas de rejeição) e r/ρₛ populacionais, lidos de `data/sim/`."""
    return simulate.load_summary(), simulate.load_population()


def _rho_ticks(population: pd.DataFrame, situation: str) -> tuple[list[float], list[str]]:
    """Rótulos do eixo x: ρ latente + r e ρₛ populacionais correspondentes."""
    pop = population[population["situation"] == situation].sort_values("rho")
    vals = pop["rho"].tolist()
    text = [
        f"<b>{_decimal(rho, 1)}</b><br>r={_decimal(r)}<br>ρₛ={_decimal(rs)}"
        for rho, r, rs in zip(pop["rho"], pop["r_pop"], pop["rho_s_pop"], strict=True)
    ]
    return vals, text


def fig_g4(
    alpha: float = DEFAULT_ALPHA,
    summary: pd.DataFrame | None = None,
    population: pd.DataFrame | None = None,
    cols: int = 2,
) -> go.Figure:
    """Constrói o G4: curvas de poder dos dois testes × ρ latente, um painel por situação.

    Em cada painel, Pearson e Spearman (mesmas cores do dashboard) com barras de ±1,96 erro
    padrão de Monte Carlo; linha pontilhada em α (o ponto em ρ = 0 é o erro tipo I) e linha
    tracejada em 80% de poder. O eixo x mostra, abaixo de cada ρ latente, o r e o ρₛ
    populacionais correspondentes (estimados numa amostra grande). `cols` painéis por linha
    (o dashboard usa uma linha só; as situações ausentes do `summary` não ganham painel).
    """
    if summary is None or population is None:
        default_summary, default_population = _g4_data()
        summary = default_summary if summary is None else summary
        population = default_population if population is None else population

    data = summary[np.isclose(summary["alpha"], alpha)]
    if data.empty:
        raise ValueError(f"Não há resultados simulados para α = {alpha}")

    situations = [s for s in SITUATIONS if s in set(data["situation"])]
    cols = max(1, min(cols, len(situations)))
    fig = make_subplots(
        rows=-(-len(situations) // cols),
        cols=cols,
        shared_yaxes=True,
        horizontal_spacing=0.06 if cols <= 2 else 0.03,
        vertical_spacing=0.22,
        subplot_titles=[G4_SITUATION_LABELS.get(s, s) for s in situations],
    )

    for i, situation in enumerate(situations):
        row, col = divmod(i, cols)
        row, col = row + 1, col + 1
        first = i == 0
        cell = data[data["situation"] == situation]
        pop = population[population["situation"] == situation].set_index("rho")
        for test, name in (("pearson", "Pearson"), ("spearman", "Spearman")):
            curve = cell[cell["test"] == test].sort_values("rho")
            pop_at = pop.reindex(curve["rho"])
            fig.add_trace(
                go.Scatter(
                    x=curve["rho"],
                    y=curve["reject_rate"],
                    mode="lines+markers",
                    name=name,
                    legendgroup=name,
                    showlegend=first,
                    line=dict(color=PALETTE[name], width=2.5),
                    marker=dict(size=7, color=PALETTE[name]),
                    error_y=dict(
                        type="data",
                        array=1.96 * curve["mc_se"],
                        thickness=1.2,
                        width=3,
                        color=PALETTE[name],
                    ),
                    customdata=np.stack([pop_at["r_pop"], pop_at["rho_s_pop"]], axis=-1),
                    hovertemplate=(
                        f"<b>{name}</b> — {situation}<br>ρ latente = %{{x:.1f}} "
                        "(r = %{customdata[0]:.2f}, ρₛ = %{customdata[1]:.2f})<br>"
                        "Rejeições: %{y:.1%}<extra></extra>"
                    ),
                ),
                row=row,
                col=col,
            )

        for level, dash, label in (
            (alpha, "dot", f"α = {_decimal(alpha)} (nível nominal)"),
            (G4_TARGET_POWER, "dash", "Poder de 80%"),
        ):
            fig.add_trace(
                go.Scatter(
                    x=[-0.03, 0.63],
                    y=[level, level],
                    mode="lines",
                    line=dict(color=G4_INK, width=1, dash=dash),
                    name=label,
                    legendgroup=label,
                    showlegend=first,
                    hoverinfo="skip",
                ),
                row=row,
                col=col,
            )

        tickvals, ticktext = _rho_ticks(population, situation)
        fig.update_xaxes(
            tickvals=tickvals,
            ticktext=ticktext,
            range=[-0.03, 0.63],
            tickfont=dict(size=10),
            title_text="ρ latente da cópula (r e ρₛ populacionais abaixo)",
            title_font=dict(size=11),
            row=row,
            col=col,
        )
        fig.update_yaxes(range=[0, 1.02], tickformat=".0%", row=row, col=col)
        if col == 1:
            fig.update_yaxes(title_text="Poder (% de amostras com p < α)", row=row, col=col)

    reps_text = f"{int(data['n_reps'].iloc[0]):,}".replace(",", ".")
    fig.update_layout(
        title=dict(
            text=(
                "G4 — Poder do Pearson × Spearman por tamanho do efeito "
                f"(α = {_decimal(alpha)}, {reps_text} réplicas por ponto)"
            ),
            x=0.0,
            xanchor="left",
        ),
        height=820,
        template="plotly_white",
        separators=",.",
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="left", x=0.0),
        margin=dict(t=110, b=60, l=70, r=30),
    )
    return fig


# --------------------------------------------------------------------------- Dashboard (BI)
# Gráficos que só existem no painel: os dados reais vistos ponto a ponto, o tamanho do efeito
# com IC 95% e o resumo de onde cada teste tem mais poder.

BI_INK = "#2C3E50"
BI_NEUTRAL = "#E5E7EB"


def fig_real_scatter(
    sample_df: pd.DataFrame | None = None,
    full_df: pd.DataFrame | None = None,
    analysis: stat_tests.RealAnalysis | None = None,
) -> go.Figure:
    """LOC × defeitos: KC1 completo ao fundo, amostra de 30 por cima e a classe mais influente."""
    sample_df = pd.read_csv(SAMPLE_CSV) if sample_df is None else sample_df
    full_df = pd.read_csv(FULL_CSV) if full_df is None else full_df
    analysis = stat_tests.real_sample_analysis() if analysis is None else analysis

    fig = go.Figure()
    for name, df, color, size, opacity in (
        (f"KC1 (n = {len(full_df)})", full_df, PALETTE["real_full"], 7, 0.35),
        (f"Amostra (n = {len(sample_df)})", sample_df, PALETTE["real_sample"], 10, 0.9),
    ):
        fig.add_trace(
            go.Scatter(
                x=df["loc"],
                y=df["defects"],
                mode="markers",
                name=name,
                marker=dict(color=color, size=size, opacity=opacity, line=dict(color="white", width=1)),
                customdata=df["class_id"],
                hovertemplate=(
                    f"<b>{name}</b><br>Classe %{{customdata}}<br>LOC: %{{x:,.0f}}<br>"
                    "Defeitos: %{y}<extra></extra>"
                ),
            )
        )
    fig.add_annotation(
        x=float(np.log10(analysis.influential_loc)),
        y=analysis.influential_defects,
        text=f"{analysis.influential_loc:,.0f} LOC · {analysis.influential_defects:.0f} defeitos"
        .replace(",", "."),
        showarrow=True,
        arrowhead=0,
        ax=-70,
        ay=8,
        font=dict(size=11, color=BI_INK),
    )
    ticks = [1, 10, 100, 1000]
    fig.update_xaxes(type="log", title_text="LOC (escala log)", tickvals=ticks,
                     ticktext=[f"{v:,}".replace(",", ".") for v in ticks])
    fig.update_yaxes(title_text="Defeitos", rangemode="tozero")
    fig.update_layout(separators=",.", template="plotly_white")
    return fig


def fig_real_effect(analysis: stat_tests.RealAnalysis | None = None) -> go.Figure:
    """r e ρₛ da amostra real com IC 95%, e o valor de cada um sem a classe mais influente."""
    a = stat_tests.real_sample_analysis() if analysis is None else analysis
    rows = (
        ("Pearson", "r", a.pearson, a.pearson_ci, a.r_without_influential, "Fisher z"),
        ("Spearman", "ρₛ", a.spearman, a.spearman_ci, a.rho_s_without_influential, "bootstrap BCa"),
    )
    fig = go.Figure()
    fig.add_vline(x=0, line=dict(color=BI_INK, width=1, dash="dot"))
    for name, symbol, result, (low, high), _, method in rows:
        coef = float(result.coef)
        fig.add_trace(
            go.Scatter(
                x=[coef],
                y=[name],
                mode="markers",
                name=f"{name} (IC 95%)",
                marker=dict(color=PALETTE[name], size=13, line=dict(color="white", width=2)),
                error_x=dict(
                    type="data", symmetric=False, array=[high - coef], arrayminus=[coef - low],
                    color=PALETTE[name], thickness=2.5, width=6,
                ),
                hovertemplate=(
                    f"<b>{name}</b><br>{symbol} = {_decimal(coef)}<br>IC 95% ({method}): "
                    f"{_decimal(low)} a {_decimal(high)}<br>p = {_decimal(float(result.p), 4)}"
                    "<extra></extra>"
                ),
            )
        )
    fig.add_trace(
        go.Scatter(
            x=[without for *_, without, _ in rows],
            y=[name for name, *_ in rows],
            mode="markers",
            name="Sem a classe mais influente",
            marker=dict(symbol="circle-open", size=13, color=BI_INK, line=dict(width=2)),
            hovertemplate="<b>%{y}</b> sem a classe mais influente<br>%{x:.2f}<extra></extra>",
        )
    )
    fig.update_xaxes(title_text="Coeficiente de correlação", range=[-0.1, 1.0], zeroline=False)
    fig.update_yaxes(range=[1.6, -0.6], showgrid=False)
    fig.update_layout(separators=",.", template="plotly_white")
    return fig


def power_gap_table(alpha: float = DEFAULT_ALPHA, summary: pd.DataFrame | None = None) -> pd.DataFrame:
    """Taxa de rejeição do Spearman menos a do Pearson (pontos percentuais), situação × ρ."""
    summary = _g4_data()[0] if summary is None else summary
    data = summary[np.isclose(summary["alpha"], alpha)]
    rates = data.pivot_table(index=["situation", "rho"], columns="test", values="reject_rate")
    gap = (100 * (rates["spearman"] - rates["pearson"])).unstack("rho")
    return gap.loc[[s for s in SITUATIONS if s in gap.index]]


def _signed(value: float) -> str:
    """Inteiro com sinal (+3, −7); o que arredonda para zero fica só "0"."""
    rounded = int(round(value))
    return "0" if rounded == 0 else f"{rounded:+d}".replace("-", "−")


def fig_power_gap(alpha: float = DEFAULT_ALPHA, summary: pd.DataFrame | None = None) -> go.Figure:
    """Mapa de calor da diferença Spearman − Pearson: verde onde o Spearman rejeita mais."""
    gap = power_gap_table(alpha, summary)
    limit = float(np.nanmax(np.abs(gap.to_numpy()))) or 1.0
    fig = go.Figure(
        go.Heatmap(
            z=gap.to_numpy(),
            x=[_decimal(rho, 1) for rho in gap.columns],
            y=list(gap.index),
            zmin=-limit,
            zmax=limit,
            colorscale=[
                [0.0, PALETTE["Pearson"]],
                [0.5, BI_NEUTRAL],
                [1.0, PALETTE["Spearman"]],
            ],
            xgap=2,
            ygap=2,
            text=[[_signed(v) for v in row] for row in gap.to_numpy()],
            texttemplate="%{text}",
            textfont=dict(size=12),
            colorbar=dict(title=dict(text="pp", side="top"), thickness=10, len=0.9),
            hovertemplate=(
                "<b>%{y}</b> · ρ latente = %{x}<br>Spearman − Pearson: %{z:+.1f} pp"
                "<extra></extra>"
            ),
        )
    )
    fig.update_xaxes(title_text="ρ latente", type="category", showgrid=False)
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_layout(separators=",.", template="plotly_white")
    return fig
