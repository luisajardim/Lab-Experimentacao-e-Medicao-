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

import simulate
import stat_tests
from config import DEFAULT_ALPHA, PALETTE, REPS, SEED, SITUATIONS
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
) -> go.Figure:
    """Constrói o G4: curvas de poder dos dois testes × ρ latente, um painel por situação.

    Em cada painel, Pearson e Spearman (mesmas cores do dashboard) com barras de ±1,96 erro
    padrão de Monte Carlo; linha pontilhada em α (o ponto em ρ = 0 é o erro tipo I) e linha
    tracejada em 80% de poder. O eixo x mostra, abaixo de cada ρ latente, o r e o ρₛ
    populacionais correspondentes (estimados numa amostra grande).
    """
    if summary is None or population is None:
        default_summary, default_population = _g4_data()
        summary = default_summary if summary is None else summary
        population = default_population if population is None else population

    data = summary[np.isclose(summary["alpha"], alpha)]
    if data.empty:
        raise ValueError(f"Não há resultados simulados para α = {alpha}")

    situations = [s for s in SITUATIONS if s in set(data["situation"])]
    fig = make_subplots(
        rows=2,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.06,
        vertical_spacing=0.22,
        subplot_titles=[G4_SITUATION_LABELS.get(s, s) for s in situations],
    )

    for i, situation in enumerate(situations):
        row, col = divmod(i, 2)
        row, col = row + 1, col + 1
        first = i == 0
        cell = data[data["situation"] == situation]
        for test, name in (("pearson", "Pearson"), ("spearman", "Spearman")):
            curve = cell[cell["test"] == test].sort_values("rho")
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
                    hovertemplate=(
                        f"<b>{name}</b> — {situation}<br>ρ latente = %{{x:.1f}}<br>"
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
