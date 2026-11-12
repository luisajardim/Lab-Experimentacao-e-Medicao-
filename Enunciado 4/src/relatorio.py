"""Página "Relatório" do app do Lab04: o formato que o enunciado avalia (§4).

Sete seções, nesta ordem: 1 Cenário · 2 Os dados (G1) · 3 Como os testes
funcionam (G2) · 4 Erro tipo I (G3) · 5 Poder (G4) · 6 Dados reais (tabela) ·
7 Conclusão, mais o extra "Para discutir: tamanho da amostra" (#91). Links do
dashboard e do repositório/GitHub Projects no topo; cada gráfico acompanhado de
um texto curto (2 a 4 frases).

A página "Dashboard" (`app.py`) mostra os mesmos gráficos no formato de painel,
só com rótulos curtos, como o professor pediu; as duas usam as mesmas funções de
`figures.py`, então os números são idênticos. O α escolhido vale nas duas páginas.

Issues: #82 (T07), #87 (T12), #93 (deploy e links).
"""

import inspect
import json

import pandas as pd
import streamlit as st

import figures
import sample_size
import simulate
import stat_tests
from config import (
    ALPHAS,
    COLOR_PEARSON,
    COLOR_SPEARMAN,
    DASHBOARD_URL,
    DATA_REAL,
    DEFAULT_ALPHA,
    EFFECT_GRID,
    PROJECTS_URL,
    REPO_URL,
    REPS,
    SEED,
)
from data import FULL_CSV, SAMPLE_CSV
from figures import G1_TEXT, fig_g1
from fit import PARAMS_JSON

# Chave do α compartilhado entre as páginas (cada página tem o próprio widget).
SHARED_ALPHA = "alpha_compartilhado"

PILOT_JSON = DATA_REAL / "piloto.json"

SECTIONS = (
    "1. Cenário",
    "2. Os dados (G1)",
    "3. Como os testes funcionam (G2)",
    "4. Erro tipo I (G3)",
    "5. Poder (G4)",
    "6. Dados reais",
    "7. Conclusão",
)


@st.cache_data
def get_datasets() -> tuple[pd.DataFrame, pd.DataFrame, dict, dict | None]:
    """Carrega os CSVs reais, parâmetros ajustados e resultado do piloto."""
    sample_df = pd.read_csv(SAMPLE_CSV)
    full_df = pd.read_csv(FULL_CSV)
    params = json.loads(PARAMS_JSON.read_text(encoding="utf-8"))
    pilot = json.loads(PILOT_JSON.read_text(encoding="utf-8")) if PILOT_JSON.exists() else None
    return sample_df, full_df, params, pilot


def _call_optional_figure(func_name: str, alpha: float):
    """Chama `figures.<func_name>` se já estiver implementada (G2, G3, G4)."""
    fn = getattr(figures, func_name, None)
    if not callable(fn):
        return None
    sig = inspect.signature(fn)
    if "alpha" in sig.parameters:
        return fn(alpha=alpha)
    return fn()


def render_header() -> float:
    """Renderiza o cabeçalho com links obrigatórios, paleta fixa e seletor de α."""
    st.title("Lab04 — Testes de Hipótese por Dentro (Pearson × Spearman)")
    st.markdown(
        "> **Pergunta de pesquisa:** *Em um sistema C++ da NASA, classes maiores tendem a ter "
        "mais defeitos de modo geral, ou a associação observada é puxada por poucas classes gigantes?*"
    )

    col_links, col_palette, col_alpha = st.columns([2.4, 1.6, 1.0])
    with col_links:
        st.markdown(
            f"🔗 **Links do Projeto:** "
            f"[Dashboard Online (Streamlit Cloud)]({DASHBOARD_URL}) · "
            f"[Repositório GitHub]({REPO_URL}) · "
            f"[Board Kanban Lab (GitHub Projects)]({PROJECTS_URL})"
        )
        st.caption(
            "**Grupo (Par P5):** Bernardo Souza Alvim (859148) · "
            "Luísa Oliveira Jardim (843759) · Pedro Augusto Santos Seabra (812784) "
            f"| Semente fixa: `SEED = {SEED}`"
        )
    with col_palette:
        st.markdown(
            "**Paleta fixa dos testes em todo o dashboard:**<br>"
            f"<span style='background-color:{COLOR_PEARSON};color:white;padding:3px 10px;"
            f"border-radius:4px;font-weight:600;margin-right:8px;'>Pearson ({COLOR_PEARSON})</span>"
            f"<span style='background-color:{COLOR_SPEARMAN};color:white;padding:3px 10px;"
            f"border-radius:4px;font-weight:600;'>Spearman ({COLOR_SPEARMAN})</span>",
            unsafe_allow_html=True,
        )
    with col_alpha:
        shared = st.session_state.get(SHARED_ALPHA, DEFAULT_ALPHA)
        alpha = st.selectbox(
            "Nível de significância (α)",
            options=list(ALPHAS),
            index=list(ALPHAS).index(shared),
            format_func=lambda a: f"α = {a:.2f}".replace(".", ","),
            help="Altera o limiar de rejeição nas análises de Erro Tipo I (G3) e Poder (G4).",
            key="alpha_relatorio",
        )
        st.session_state[SHARED_ALPHA] = float(alpha)

    st.divider()
    return float(alpha)


def render_sec1_cenario(params: dict, pilot: dict | None) -> None:
    """Seção 1 — Cenário (pergunta, hipóteses, situações, parâmetros e expectativa a priori)."""
    st.header("1. Cenário")

    col_h, col_resp = st.columns(2)
    with col_h:
        st.subheader("Variáveis e Hipóteses")
        st.markdown(
            "- **Variável $X$ (`loc`):** Tamanho da classe em linhas de código (`sumLOC_TOTAL`).\n"
            "- **Variável $Y$ (`defects`):** Número de defeitos registrados na classe (`NUMDEFECTS`).\n"
            "- **Fonte real:** NASA MDP **KC1** por classe (OpenML id 1070, 145 classes C++; "
            "amostra sorteada de $n = 30$ classes com `default_rng(42)`).\n\n"
            "| Hipótese | Em símbolos | Em palavras simples |\n"
            "|---|---|---|\n"
            "| **$H_0$ (nula)** | $\\rho = 0$ | O tamanho da classe não está associado ao número de defeitos. |\n"
            "| **$H_1$ (alternativa)** | $\\rho \\neq 0$ | O tamanho da classe está associado ao número de defeitos (para mais ou para menos). |\n\n"
            "**Direção:** Teste **bicaudal** ($\\alpha = 0,05$ padrão; seletor permite $\\alpha = 0,01$). "
            "Embora o grupo espere associação positiva ($\\rho > 0$), o teste bicaudal é mais conservador "
            "e não depende de aposta prévia na direção."
        )

    with col_resp:
        st.subheader("Como cada teste responde à pergunta")
        st.markdown(
            f"- **<span style='color:{COLOR_PEARSON}'>Correlação de Pearson ($r$)</span>:** "
            "Opera diretamente sobre os valores brutos. Uma única classe gigante com dezenas de defeitos "
            "domina a soma dos produtos padronizados — no KC1 inteiro, **uma única classe** (`2.883 LOC` e "
            "`101 defeitos`) eleva o $r$ de `0,57` para `0,69`.\n"
            f"- **<span style='color:{COLOR_SPEARMAN}'>Correlação de Spearman ($\\rho_s$)</span>:** "
            "Calcula a correlação de Pearson sobre os **postos (ranks)** (com posto médio nos empates). "
            "Cada classe tem peso limitado à sua posição relativa, medindo a tendência monotônica geral "
            "(`0,57` com todas as classes vs. `0,56` sem a classe extrema).\n"
            "- **Diagnóstico do cenário:** Comparar os dois testes nos dados reais e sob simulação mostra "
            "se a associação vem de uma tendência geral ou de poucos pontos extremos.",
            unsafe_allow_html=True,
        )

    st.subheader("Desenho da Simulação (4 Situações × 7 Tamanhos de Efeito)")
    effects = "; ".join(f"{v:.1f}".replace(".", ",") for v in EFFECT_GRID)
    reps = f"{REPS:,}".replace(",", ".")
    st.markdown(
        f"Em todas as situações, o efeito controlado é a correlação latente "
        f"$\\rho \\in \\{{{effects}\\}}$, com **{reps} réplicas** por combinação "
        f"(margem de Monte Carlo $\\approx \\pm 0,43$ pp em torno de $\\alpha = 5\\%$):"
    )
    situations_table = pd.DataFrame(
        [
            {
                "Situação": "S-base (bem-comportada)",
                "Como os dados são gerados": "Normal bivariada padronizada N₂(0, 1, ρ)",
                "n": 30,
                "Papel no estudo": "Cenário ideal onde todos os pressupostos do Pearson são atendidos.",
            },
            {
                "Situação": "S-real (realista)",
                "Como os dados são gerados": (
                    "Cópula gaussiana (ρ latente) → LOC ~ Gamma(0,607; 487,9) "
                    "e Defeitos ~ BinNeg(r=0,170; μ=4,61)"
                ),
                "n": 30,
                "Papel no estudo": "Reproduz assimetria forte, cauda longa e 57% de zeros (viola normalidade).",
            },
            {
                "Situação": "S-real-n10 (amostra pequena)",
                "Como os dados são gerados": "Mesmo gerador da S-real com tamanho amostral reduzido",
                "n": 10,
                "Papel no estudo": "Avalia degradação por amostra pequena somada a muitos empates em zero.",
            },
            {
                "Situação": "S-outlier (ponto dominante)",
                "Como os dados são gerados": (
                    "S-real em que cada classe tem chance 1/145 de ser trocada por classe extrema "
                    "(> percentil 99: LOC ≥ 1.770 e defeitos ≥ 57)"
                ),
                "n": 30,
                "Papel no estudo": "Reproduz o fenômeno do ponto dominante observado no KC1 (~19% das amostras).",
            },
        ]
    )
    st.dataframe(situations_table, width="stretch", hide_index=True)

    loc_p = params["loc"]
    def_p = params["defects"]
    obs_p = params["observed"]

    col_par, col_exp = st.columns(2)
    with col_par:
        st.subheader("Parâmetros Ajustados no KC1 (MLE)")
        st.markdown(
            f"- **LOC ~ Gamma(forma = `{loc_p['shape']:.3f}`, escala = `{loc_p['scale']:.1f}`):** "
            f"Média `{loc_p['mean_fit']:.0f}` LOC, mediana observada `{obs_p['loc_median']:.0f}` LOC e "
            f"assimetria `{obs_p['loc_skew']:.2f}`. Não rejeitada pelo teste KS (`p = {loc_p['ks_pvalue']:.2f}`), "
            "ao contrário da lognormal (`KS p = 0,001`).\n"
            f"- **Defeitos ~ Binomial Negativa(`r = {def_p['r']:.3f}`, `média = {def_p['mean']:.2f}`):** "
            f"Reproduz a fração de classes sem defeito (`{def_p['p_zero_fit']:.1%}` ajustado vs. "
            f"`{def_p['p_zero_obs']:.1%}` no KC1) e a cauda longa (`≥ 20 defeitos`: `{def_p['p_ge20_fit']:.1%}` vs. "
            f"`{def_p['p_ge20_obs']:.1%}`). A variância real (≈ 118) é 25× a média, descartando a Poisson."
        )

    with col_exp:
        st.subheader("Expectativa Registrada Antes de Simular")
        pilot_str = (
            f"No piloto com {pilot['n_subsamples']} subamostras reais de $n = 30$ do KC1, "
            f"Spearman rejeitou $H_0$ em **{pilot['reject_rate_spearman']:.1%}** das vezes contra "
            f"**{pilot['reject_rate_pearson']:.1%}** do Pearson."
            if pilot
            else ""
        )
        st.info(
            "**Hipótese a priori do grupo (registrada em 31/10/2026 na T03):**\n"
            "1. **Erro Tipo I (Q1):** Ambos próximos de 5% em `S-base`, `S-real` e `S-real-n10`, pois sob $\\rho = 0$ "
            "as variáveis $X$ e $Y$ são independentes.\n"
            "2. **Poder na `S-base` (Q2):** Pearson ligeiramente superior (teste ótimo sob normalidade; "
            "eficiência relativa assintótica do Spearman $\\approx 9/\\pi^2 \\approx 0,91$).\n"
            "3. **Poder na `S-real` e `S-real-n10` (Q3):** Spearman superior porque os postos limitam a "
            "variabilidade inflada por valores extremos da Gamma e da Binomial Negativa. " + pilot_str
        )


def render_sec2_dados(sample_df: pd.DataFrame, full_df: pd.DataFrame, params: dict) -> None:
    """Seção 2 — Os dados (Gráfico G1 + texto curto de 2 a 4 frases)."""
    st.header("2. Os dados (G1)")

    fig1 = fig_g1(sample_df=sample_df, full_df=full_df)
    st.plotly_chart(fig1, width="stretch")

    st.markdown(G1_TEXT)

    with st.expander("Ver comparação de quantis e estatísticas (Real vs. Ajuste S-real)"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("LOC Mediana (KC1 / Amostra)", f"{full_df['loc'].median():.0f} / {sample_df['loc'].median():.0f}")
        c2.metric("LOC Máximo (KC1 / Amostra)", f"{full_df['loc'].max()} / {sample_df['loc'].max()}")
        c3.metric(
            "% Classes com 0 Defeitos",
            f"{(full_df['defects'] == 0).mean():.1%} (KC1) | {(sample_df['defects'] == 0).mean():.1%} (n=30)",
        )
        c4.metric(
            "Correlação no KC1 (n = 145)",
            f"r = {params['observed']['pearson_r']:.2f} | ρ = {params['observed']['spearman_rho']:.2f}",
        )


def render_sec3_como_funcionam(alpha: float) -> None:
    """Seção 3 — Como os testes funcionam (G2)."""
    st.header("3. Como os testes funcionam (G2)")

    st.plotly_chart(figures.fig_g2(alpha=alpha), width="stretch")
    st.markdown(figures.G2_TEXT)

    example = stat_tests.run_example()
    rho_text = f"{example.rho:.1f}".replace(".", ",")
    st.subheader(f"Exemplo: um conjunto simulado ({example.situation}, ρ latente = {rho_text})")
    st.markdown(stat_tests.interpret_example(example, alpha=alpha))


def _list_pt(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " e " + items[-1]


def g3_summary(alpha: float, table: pd.DataFrame | None = None) -> str:
    """Resumo do G3 em até 4 frases (o enunciado pede 2 a 4), a partir das mesmas taxas do gráfico.

    O texto completo (`figures.g3_text`) fica num expansor logo abaixo.
    """
    table = figures.type1_table(alpha) if table is None else table
    low, high = table["band_low"].iloc[0], table["band_high"].iloc[0]

    def off(test: str) -> list[str]:
        rows = table[(table["test"] == test) & (table["verdict"] != "perto")]
        return [f"{row.situation} ({_pct(row.rate)}, {figures.G3_VERDICTS[row.verdict]})"
                for row in rows.itertuples()]

    pearson_off, spearman_off = off("Pearson"), off("Spearman")
    sentences = [
        f"Com ρ = 0, um teste correto rejeita H₀ em cerca de {_pct(alpha)} das amostras; a faixa "
        f"cinza ({_pct(low)} a {_pct(high)}) é a variação esperada só pelo acaso nas réplicas.",
        "O Spearman fica perto de α em todas as situações." if not spearman_off
        else f"O Spearman fica perto de α, exceto em {_list_pt(spearman_off)}.",
    ]
    if pearson_off:
        sentences.append(
            f"O Pearson se afasta em {_list_pt(pearson_off)}: uma classe com LOC e defeitos altos ao "
            "mesmo tempo empurra o r para cima, e quase todas as rejeições indevidas caem na cauda direita."
        )
    sentences.append(
        "Concluímos que, nesses dados, o Spearman controla o erro tipo I e o Pearson não, "
        "principalmente quando há uma classe extrema (S-outlier)."
    )
    return " ".join(sentences)


def render_sec4_erro_tipo1(alpha: float) -> None:
    """Seção 4 — Erro tipo I (G3)."""
    st.header("4. Erro tipo I (G3)")

    st.plotly_chart(figures.fig_g3(alpha=alpha), width="stretch")
    st.markdown(g3_summary(alpha))
    with st.expander("Ver análise detalhada do G3"):
        st.markdown(figures.g3_text(alpha=alpha))


def render_sec5_poder(alpha: float) -> None:
    """Seção 5 — Poder (G4)."""
    st.header("5. Poder (G4)")

    fig4 = _call_optional_figure("fig_g4", alpha=alpha)
    if fig4 is not None:
        st.plotly_chart(fig4, width="stretch")
        g4_text = getattr(figures, "G4_TEXT", None)
        if g4_text:
            st.markdown(g4_text)
    else:
        st.info(
            f"**Seção preparada para a Sprint 2 (T08 `#83` e T10 `#85`):** "
            f"Exibirá as curvas de poder estatístico (proporção de rejeições com $p < {alpha:.2f}$) "
            f"em função do tamanho do efeito $\\rho \\in \\{{0,0; 0,1; \\dots; 0,6\\}}$ nas 4 situações, "
            "anotadas com os respectivos $r$ e $\\rho_s$ populacionais."
        )


def render_sec6_dados_reais(sample_df: pd.DataFrame, full_df: pd.DataFrame, alpha: float) -> None:
    """Seção 6 — Aplicação dos testes aos dados reais (amostra n = 30 do KC1)."""
    st.header("6. Dados reais")

    st.markdown(
        "Os dois testes aplicados à amostra sorteada de **30 classes** do NASA KC1 "
        "(`data/real/kc1_sample30.csv`, `SEED = 42`), com H₀: ρ = 0 bicaudal."
    )
    st.dataframe(stat_tests.real_data_table(alpha=alpha), width="stretch", hide_index=True)
    st.markdown(stat_tests.real_data_text(alpha=alpha))

    st.subheader("A amostra")
    col_a, col_b = st.columns([1.4, 1.0])
    with col_a:
        st.dataframe(sample_df, width="stretch", hide_index=True, height=260)
    with col_b:
        summary_df = pd.DataFrame(
            [
                {
                    "Conjunto": "KC1 Completo (n = 145)",
                    "LOC Mediana (IQR)": (
                        f"{full_df['loc'].median():.0f} "
                        f"({full_df['loc'].quantile(0.25):.0f}–{full_df['loc'].quantile(0.75):.0f})"
                    ),
                    "LOC Máx": int(full_df["loc"].max()),
                    "Defeitos Máx": int(full_df["defects"].max()),
                    "% Sem Defeitos": f"{(full_df['defects'] == 0).mean():.1%}",
                },
                {
                    "Conjunto": "Amostra Real (n = 30)",
                    "LOC Mediana (IQR)": (
                        f"{sample_df['loc'].median():.0f} "
                        f"({sample_df['loc'].quantile(0.25):.0f}–{sample_df['loc'].quantile(0.75):.0f})"
                    ),
                    "LOC Máx": int(sample_df["loc"].max()),
                    "Defeitos Máx": int(sample_df["defects"].max()),
                    "% Sem Defeitos": f"{(sample_df['defects'] == 0).mean():.1%}",
                },
            ]
        )
        st.dataframe(summary_df, width="stretch", hide_index=True)


def _rate(summary: pd.DataFrame, situation: str, rho: float, test: str, alpha: float) -> float:
    """Taxa de rejeição simulada de uma célula (situação × ρ × teste × α)."""
    row = summary[
        (summary["situation"] == situation)
        & ((summary["rho"] - rho).abs() < 1e-9)
        & (summary["test"] == test)
        & ((summary["alpha"] - alpha).abs() < 1e-9)
    ]
    return float(row["reject_rate"].iloc[0])


def _pct(value: float) -> str:
    return f"{value:.1%}".replace(".", ",")


def _num(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def expectation_table(summary: pd.DataFrame, alpha: float) -> pd.DataFrame:
    """Expectativa registrada na T03 × o que a simulação encontrou (números no α escolhido)."""

    def pair(situation: str, rho: float) -> str:
        p = _rate(summary, situation, rho, "pearson", alpha)
        s = _rate(summary, situation, rho, "spearman", alpha)
        return f"{_pct(p)} / {_pct(s)}"

    return pd.DataFrame(
        [
            {
                "Pergunta": "Q1 — Erro tipo I (ρ = 0)",
                "O grupo esperava (31/10)": "Os dois perto de α em S-base, S-real e S-real-n10.",
                "Simulação (Pearson / Spearman)": (
                    f"S-base {pair('S-base', 0.0)} · S-real {pair('S-real', 0.0)} · "
                    f"S-real-n10 {pair('S-real-n10', 0.0)}"
                ),
                "Confirmou?": (
                    "Em parte: o Spearman ficou em α em todas; o Pearson ficou liberal com n = 10 "
                    "(e, com α = 0,01, também na S-real)."
                ),
            },
            {
                "Pergunta": "Q2 — Poder na S-base (ρ = 0,4)",
                "O grupo esperava (31/10)": "Pearson com um pouco mais de poder (teste ótimo na normal).",
                "Simulação (Pearson / Spearman)": pair("S-base", 0.4),
                "Confirmou?": "Sim.",
            },
            {
                "Pergunta": "Q3 — Poder na S-real (ρ = 0,6)",
                "O grupo esperava (31/10)": "Spearman com mais poder (postos limitam as classes extremas).",
                "Simulação (Pearson / Spearman)": pair("S-real", 0.6),
                "Confirmou?": "Sim, a partir de ρ ≈ 0,3; com efeitos pequenos os dois ficam parecidos.",
            },
            {
                "Pergunta": "Q3 — Poder na S-real-n10 (ρ = 0,6)",
                "O grupo esperava (31/10)": "Os dois perdem poder; vantagem menor do Spearman.",
                "Simulação (Pearson / Spearman)": pair("S-real-n10", 0.6),
                "Confirmou?": (
                    "Não: o Pearson rejeita mais, mas parte disso é erro tipo I inflado; com ~57% de "
                    "zeros, 10 classes deixam o Spearman com poucos postos distintos."
                ),
            },
            {
                "Pergunta": "S-outlier (sem expectativa a priori)",
                "O grupo esperava (31/10)": "— (criada depois da análise exploratória).",
                "Simulação (Pearson / Spearman)": (
                    f"ρ = 0: {pair('S-outlier', 0.0)} · ρ = 0,6: {pair('S-outlier', 0.6)}"
                ),
                "Confirmou?": (
                    "Mostra o fenômeno da pergunta: uma classe gigante gera falsos positivos no Pearson."
                ),
            },
        ]
    )


def render_sec7_conclusao(alpha: float, sample_df: pd.DataFrame) -> None:
    """Seção 7 — Conclusão: esperado × encontrado, resposta, recomendação e principal limitação."""
    st.header("7. Conclusão")

    summary = simulate.load_summary()
    st.subheader("O que esperávamos × o que encontramos")
    st.caption(
        f"Taxas de rejeição com α = {_num(alpha)} (mude o seletor no topo). A expectativa foi "
        "registrada em `docs/cenario.md` antes de rodar a simulação."
    )
    st.dataframe(expectation_table(summary, alpha), width="stretch", hide_index=True)

    x = sample_df["loc"].to_numpy(dtype=float)
    y = sample_df["defects"].to_numpy(dtype=float)
    r_real, s_real = stat_tests.pearson(x, y), stat_tests.spearman(x, y)
    p_out0 = _rate(summary, "S-outlier", 0.0, "pearson", alpha)
    s_out0 = _rate(summary, "S-outlier", 0.0, "spearman", alpha)
    p_real6 = _rate(summary, "S-real", 0.6, "pearson", alpha)
    s_real6 = _rate(summary, "S-real", 0.6, "spearman", alpha)

    st.subheader("Resposta à pergunta")
    st.markdown(
        "Classes maiores **tendem, de modo geral, a ter mais defeitos**, mas a força da associação que o "
        "Pearson mostra é inflada por poucas classes gigantes. Na amostra de 30 classes do KC1, o "
        f"Spearman (ρₛ = {_num(s_real.coef)}) indica uma tendência moderada, que vale para a maioria "
        f"das classes; o Pearson dá um valor bem mais alto (r = {_num(r_real.coef)}), puxado pela "
        "classe de 2.883 LOC e 101 defeitos. No KC1 inteiro, tirar só essa classe derruba o r de "
        "0,69 para 0,57, enquanto o ρₛ quase não muda (0,57 → 0,56). A simulação confirma o "
        f"mecanismo: na S-outlier, sem efeito nenhum, o Pearson rejeita H₀ em {_pct(p_out0)} das "
        f"amostras e o Spearman em {_pct(s_out0)}."
    )

    st.subheader("Recomendação")
    st.markdown(
        "- **Usar o Spearman** para LOC × defeitos e métricas de software parecidas (assimétricas, com "
        "muitos zeros e classes gigantes): ele mantém o erro tipo I perto de α em todas as situações e "
        f"tem mais poder nos dados realistas (S-real, ρ = 0,6: {_pct(s_real6)} contra "
        f"{_pct(p_real6)}).\n"
        "- **A escolha mudaria para o Pearson** se os dados fossem aproximadamente normais e sem pontos "
        "extremos (S-base), onde ele tem um pouco mais de poder, ou se a pergunta fosse sobre "
        "**relação linear nos valores** (por exemplo, quantos defeitos a mais cada 100 LOC trazem).\n"
        "- **Com amostras muito pequenas (n ≈ 10)**, nenhum dos dois é confiável: o poder fica abaixo de "
        "40% mesmo no maior efeito, e o Pearson ainda rejeita H₀ demais. O melhor é coletar mais "
        "classes (o bloco \"Para discutir\" mostra quantas seriam necessárias)."
    )

    st.subheader("Principal limitação")
    st.markdown(
        "Os resultados de erro tipo I e de poder dependem de **como a simulação gera os dados**: a cópula "
        "gaussiana não produz classes tão extremas quanto a do KC1, e a S-outlier, criada para cobrir "
        "isso, se apoia em **uma única classe real** para definir a taxa de contaminação (1 em 145). "
        "Além disso, os dados da NASA são antigos (2004/2005) e têm problemas de qualidade conhecidos "
        "(Shepperd et al., 2013), então os números valem para sistemas parecidos com o KC1, não para "
        "qualquer software."
    )


def render_sample_size(alpha: float) -> None:
    """Extra (#91): poder e erro tipo I × tamanho da amostra, com texto e tabela."""
    results = sample_size.load()
    if results is None:
        return
    st.header("Para discutir: tamanho da amostra")
    st.plotly_chart(sample_size.fig_sample_size(results, alpha), width="stretch")
    st.markdown(sample_size.summary_text(results, alpha))
    with st.expander("Poder com n = 30 e n necessário para 80% de poder"):
        table = sample_size.n80_table(results, alpha)
        table["test"] = table["test"].map(lambda t: sample_size.TESTS[t][0])
        table["effect"] = table["effect"].map(sample_size.EFFECT_LABELS)
        table = table.rename(columns={
            "situation": "Situação", "effect": "Efeito", "rho": "ρ latente", "test": "Teste",
            "power_n30": "Poder com n = 30", "n80": "n para 80% de poder",
        })
        st.dataframe(table.round({"ρ latente": 2, "Poder com n = 30": 3, "n para 80% de poder": 0}),
                     width="stretch", hide_index=True)


def main() -> None:
    """Renderiza as 7 seções na ordem do enunciado (a configuração da página fica no `app.py`)."""
    sample_df, full_df, params, pilot = get_datasets()
    alpha = render_header()

    render_sec1_cenario(params, pilot)
    st.divider()
    render_sec2_dados(sample_df, full_df, params)
    st.divider()
    render_sec3_como_funcionam(alpha)
    st.divider()
    render_sec4_erro_tipo1(alpha)
    st.divider()
    render_sec5_poder(alpha)
    st.divider()
    render_sec6_dados_reais(sample_df, full_df, alpha)
    st.divider()
    render_sec7_conclusao(alpha, sample_df)
    # Extra opcional (#91): aparece só se data/sim/sample_size.csv existir.
    if sample_size.load() is not None:
        st.divider()
        render_sample_size(alpha)
