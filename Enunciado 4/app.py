"""Dashboard Streamlit do Lab04.

Sete seções, nesta ordem: 1 Cenário · 2 Os dados (G1) · 3 Como os testes
funcionam (G2) · 4 Erro tipo I (G3) · 5 Poder (G4) · 6 Dados reais (tabela) ·
7 Conclusão. Links do dashboard e do repositório/GitHub Projects no topo; cada
gráfico acompanhado de um texto curto (2 a 4 frases).

Issues: #82 (T07), #87 (T12).
"""

import inspect
import json
import sys
from pathlib import Path

# Garante que `src/` esteja no sys.path tanto via `uv run lab04` quanto no Streamlit Cloud.
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import figures  # noqa: E402
import stat_tests  # noqa: E402
from config import (  # noqa: E402
    ALPHAS,
    COLOR_PEARSON,
    COLOR_SPEARMAN,
    DASHBOARD_URL,
    DATA_REAL,
    DEFAULT_ALPHA,
    EFFECT_GRID,
    REPO_URL,
    REPS,
    SEED,
)
from data import FULL_CSV, SAMPLE_CSV  # noqa: E402
from figures import G1_TEXT, fig_g1  # noqa: E402
from fit import PARAMS_JSON  # noqa: E402

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
            f"[Board Kanban Lab (GitHub Projects)]({REPO_URL}/projects)"
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
        alpha = st.selectbox(
            "Nível de significância (α)",
            options=list(ALPHAS),
            index=list(ALPHAS).index(DEFAULT_ALPHA),
            format_func=lambda a: f"α = {a:.2f}".replace(".", ","),
            help="Altera o limiar de rejeição nas análises de Erro Tipo I (G3) e Poder (G4).",
        )

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
    st.markdown(
        f"Em todas as situações, o efeito controlado é a correlação latente "
        f"$\\rho \\in \\{{{', '.join(str(v).replace('.', ',') for v in EFFECT_GRID)}\\}}$ "
        f"com **{REPS:,} réplicas** por combinação (margem de Monte Carlo $\\approx \\pm 0,43\\text{{ pp}}$ em $\\alpha = 5\\%$):".replace(
            ",", "."
        )
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
    st.dataframe(situations_table, use_container_width=True, hide_index=True)

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
    st.plotly_chart(fig1, use_container_width=True)

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

    fig2 = _call_optional_figure("fig_g2", alpha=alpha)
    if fig2 is not None:
        st.plotly_chart(fig2, use_container_width=True)
        g2_text = getattr(figures, "G2_TEXT", None)
        if g2_text:
            st.markdown(g2_text)
    else:
        st.markdown(
            "Ambos os testes avaliam a estatística $t = r \\sqrt{(n - 2) / (1 - r^2)}$ comparada à "
            "distribuição $t$ de Student com $n - 2$ graus de liberdade sob $H_0: \\rho = 0$. "
            "No **Pearson**, $r$ é calculado diretamente sobre os valores padronizados de LOC e defeitos; "
            "no **Spearman**, a mesma fórmula é aplicada sobre os postos médios das observações. "
            f"Para um teste bicaudal com $\\alpha = {alpha:.2f}$, a região de rejeição compreende as duas "
            "caudas onde $|t| > t_{{1 - \\alpha/2,\\, n-2}}$, e o **p-valor** representa a probabilidade, "
            "assumindo que $H_0$ é verdadeira, de observar uma estatística $|t|$ tão ou mais extrema que a "
            "da amostra (não sendo a probabilidade de $H_0$ ser verdadeira)."
        )
        st.caption("Gráfico G2 detalhado em integração pela tarefa T06b (Issue #81).")


def render_sec4_erro_tipo1(alpha: float) -> None:
    """Seção 4 — Erro tipo I (G3)."""
    st.header("4. Erro tipo I (G3)")

    fig3 = _call_optional_figure("fig_g3", alpha=alpha)
    if fig3 is not None:
        st.plotly_chart(fig3, use_container_width=True)
        g3_text = getattr(figures, "G3_TEXT", None)
        if g3_text:
            st.markdown(g3_text)
    else:
        st.info(
            f"**Seção preparada para a Sprint 2 (T08 `#83` e T09 `#84`):** "
            f"Exibirá a taxa empírica de rejeição sob $H_0$ ($\\rho = 0$) em 10.000 réplicas para as "
            f"4 situações (`S-base`, `S-real`, `S-real-n10`, `S-outlier`) com linha de referência em "
            f"$\\alpha = {alpha:.0%}$ e banda de erro de Monte Carlo."
        )


def render_sec5_poder(alpha: float) -> None:
    """Seção 5 — Poder (G4)."""
    st.header("5. Poder (G4)")

    fig4 = _call_optional_figure("fig_g4", alpha=alpha)
    if fig4 is not None:
        st.plotly_chart(fig4, use_container_width=True)
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


def render_sec6_dados_reais(sample_df: pd.DataFrame, full_df: pd.DataFrame) -> None:
    """Seção 6 — Aplicação dos testes aos dados reais (amostra n = 30 do KC1)."""
    st.header("6. Dados reais")

    real_table_fn = getattr(stat_tests, "real_data_table", None) or getattr(
        stat_tests, "evaluate_real_sample", None
    )
    if callable(real_table_fn):
        result_df = real_table_fn(sample_df)
        st.dataframe(result_df, use_container_width=True, hide_index=True)
    else:
        st.markdown(
            "Amostra sorteada de **$n = 30$ classes** do NASA KC1 (`data/real/kc1_sample30.csv`, `SEED = 42`). "
            "A tabela comparativa com estatística $t$, p-valor e IC 95% (Fisher $z$ para Pearson e bootstrap "
            "para Spearman) será consolidada na tarefa **T11 (Issue `#86`, Sprint 2)**."
        )
        col_a, col_b = st.columns([1.4, 1.0])
        with col_a:
            st.dataframe(sample_df, use_container_width=True, hide_index=True, height=260)
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
            st.dataframe(summary_df, use_container_width=True, hide_index=True)


def render_sec7_conclusao() -> None:
    """Seção 7 — Conclusão (síntese esperado × encontrado, recomendação e limitações)."""
    st.header("7. Conclusão")
    st.markdown(
        "- **Síntese preliminar (Sprint 1):** Os dados reais do NASA KC1 violam severamente a normalidade "
        "bivariada exigida pelo teste de Pearson, combinando forte assimetria positiva em LOC (`skew = 3,40`), "
        "inflação de zeros em defeitos (`58,6%` das classes com zero defeitos) e um ponto extremo dominante "
        "(`2.883 LOC`, `101 defeitos`) que sozinho desloca o $r$ de Pearson de `0,57` para `0,69`.\n"
        "- **Próximo passo (Sprint 2 — T12, Issue `#87`):** Confrontar a expectativa registrada na Seção 1 "
        "com as curvas empíricas de Erro Tipo I (G3) e Poder (G4) das 10.000 réplicas de Monte Carlo e "
        "formular a recomendação prática de quando usar Spearman ou Pearson.\n"
        "- **Principais limitações:** Dados históricos da NASA (2004/2005) sujeitos a críticas conhecidas de "
        "qualidade e duplicatas de classes triviais (Shepperd et al., 2013); LOC da classe obtido pela soma "
        "dos métodos; e simetria de cauda da cópula gaussiana (compensada pela criação da situação `S-outlier`)."
    )


def main() -> None:
    """Renderiza as 7 seções do dashboard na ordem do enunciado."""
    st.set_page_config(
        page_title="Lab04 — Pearson × Spearman (NASA KC1)",
        page_icon="📊",
        layout="wide",
    )

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
    render_sec6_dados_reais(sample_df, full_df)
    st.divider()
    render_sec7_conclusao()


if __name__ == "__main__":
    main()
