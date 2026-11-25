"""Dashboard Streamlit do Lab05 — Experimento em Software Real (npm × pnpm × Yarn × Bun).

Quatro abas: Todos × npm · Yarn × Yarn · Adoção × desempenho · Impacto (+ seção de método e links).
Lê a coleta completa em `data/raw/<maquina>/runs.csv` via `schema.load_runs()`, que deixa de fora
o piloto e o sintético. Enquanto ela não existe, mostra o piloto (ou, sem piloto, o CSV sintético)
com aviso explícito.

Issues: #105 (T10), #111 (T14), #113 (T16), #115 (T18), #117 (T20).
"""

from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402

import adoption  # noqa: E402
import figures  # noqa: E402
import stats  # noqa: E402
from config import (  # noqa: E402
    ALPHA,
    CONTROL,
    MANAGERS,
    PROJECTS,
    PROJECTS_URL,
    REPO_URL,
    SCENARIOS,
    YARN_VARIANTS,
)
from schema import load_runs  # noqa: E402

TABS = (
    "Todos × npm",
    "Yarn × Yarn",
    "Adoção × desempenho",
    "Impacto",
    "Método & Links",
)


@st.cache_data
def get_runs() -> tuple[pd.DataFrame, str]:
    """Coleta completa; sem ela, o piloto; sem piloto, o CSV sintético."""
    df = load_runs()
    if not df.empty:
        machines = sorted(df["machine"].dropna().unique())
        if len(machines) < 3 or set(df["scenario"].unique()) < set(SCENARIOS):
            return df, "partial"
        return df, "full"
    pilot = load_runs(include_pilot=True)
    if not pilot.empty:
        return pilot, "pilot"
    return load_runs(include_synthetic=True), "synthetic"


def render_header(df: pd.DataFrame, source_kind: str) -> None:
    """Cabeçalho com pergunta de pesquisa, status dos dados e links do projeto."""
    st.title("Lab05 — Gerenciadores de Pacotes Node no Windows 11")
    st.markdown(
        "> **Pergunta:** *Quanto tempo e quanto disco cada gerenciador gasta para instalar projetos "
        "Node reais no Windows? As promessas dos fabricantes se confirmam? A adoção real acompanha "
        "o desempenho?*"
    )
    st.caption(
        f"[Repositório GitHub]({REPO_URL}) · [Board Kanban Lab]({PROJECTS_URL}) · "
        f"Controle: `{CONTROL}` · Nível de significância: `α = {ALPHA:.2f}`".replace(".", ",")
    )

    if source_kind == "synthetic":
        st.warning(
            "**Modo sintético:** Ainda não há coleta real versionada; exibindo `data/raw/synthetic/runs.csv` "
            "(números inventados apenas para desenvolvimento da interface e dos testes)."
        )
    elif source_kind in ("partial", "pilot"):
        machines = ", ".join(sorted(df["machine"].unique()))
        scenarios = ", ".join(sorted(df["scenario"].unique()))
        label = "Dados do piloto" if source_kind == "pilot" else "Coleta parcial"
        st.info(
            f"**{label}:** Exibindo {len(df)} instalações medidas "
            f"(máquina(s): `{machines}`; cenário(s): `{scenarios}`). "
            "A análise definitiva entra após a coleta completa nas 3 máquinas (T12a/b/c)."
        )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Instalações medidas", len(df))
    c2.metric("Tratamentos", df["manager"].nunique())
    c3.metric("Cenários", df["scenario"].nunique())
    valid_pct = ((df["exit_code"] == 0) & df["build_ok"].astype(bool)).mean()
    c4.metric("Taxa de builds válidos", f"{valid_pct:.1%}".replace(".", ","))


def render_tab_vs_npm(df: pd.DataFrame) -> None:
    """Aba 1: Todos × npm (descritiva, speedup, Wilcoxon pareado + Holm, Cliff's δ e disco)."""
    st.subheader("Desempenho vs. Controle (npm)")
    metric = st.selectbox(
        "Métrica de comparação",
        options=["wall_s", "footprint_mb", "disk_mb", "peak_rss_mb", "n_files"],
        format_func=lambda m: figures.METRIC_LABELS.get(m, m),
        key="tab1_metric",
    )

    desc = stats.describe(df, metric=metric)
    st.plotly_chart(figures.fig_metric_by_scenario(desc, metric=metric), width="stretch")

    vs_ctrl = stats.compare_to_control(df, metric=metric)
    if metric == "wall_s" and not vs_ctrl.empty:
        st.plotly_chart(figures.fig_speedup_vs_control(vs_ctrl), width="stretch")

    st.markdown("#### Tabela de Testes (Wilcoxon pareado + correção de Holm) e Tamanho do Efeito")
    if not vs_ctrl.empty:
        view = vs_ctrl.copy()
        view["project"] = view["project"].map(lambda p: PROJECTS[p]["label"])
        view["scenario"] = view["scenario"].map(lambda s: SCENARIOS[s]["label"])
        view["manager"] = view["manager"].map(lambda m: MANAGERS[m]["label"])
        st.dataframe(view.round(4), width="stretch", hide_index=True)

    st.caption("Análise completa e comparação com promessas dos fabricantes (pnpm / Bun) na T18 (#115).")


def render_tab_yarn(df: pd.DataFrame) -> None:
    """Aba 2: Yarn × Yarn (Classic 1.22 × Berry 4 node-modules × Berry 4 PnP)."""
    st.subheader("Evolução e Trade-offs na Família Yarn")
    yarn_df = df[df["manager"].isin(YARN_VARIANTS)]

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures.fig_yarn_comparison(yarn_df, metric="wall_s"), width="stretch")
    with col2:
        st.plotly_chart(figures.fig_yarn_comparison(yarn_df, metric="footprint_mb"), width="stretch")

    omnibus, posthoc = stats.yarn_friedman(df, metric="wall_s")
    st.markdown("#### Teste de Friedman (Tempo de Instalação)")
    if not omnibus.empty:
        st.dataframe(omnibus.round(4), width="stretch", hide_index=True)
    if not posthoc.empty:
        with st.expander("Ver comparações post-hoc (Wilcoxon + Holm)"):
            st.dataframe(posthoc.round(4), width="stretch", hide_index=True)

    st.caption("Análise detalhada de compatibilidade (PnP vs node_modules) e nº de arquivos na T14 (#111).")


@st.cache_data
def get_downloads() -> tuple[pd.DataFrame, pd.DataFrame, str]:
    """Séries de downloads da T15: diária, semanal e a data da coleta."""
    return adoption.load_daily(), adoption.load_weekly(), adoption.fetched_at()


def render_tab_adoption(df: pd.DataFrame) -> None:
    """Aba 3: Adoção (API de downloads do npm) × Desempenho (T16, #113).

    A ordem é proposital: primeiro as séries, depois o cruzamento, e o texto das limitações
    **antes** do gráfico que mais convida à leitura causal.
    """
    st.subheader("Adoção × Desempenho")
    st.markdown(
        "*O mercado escolhe o mais rápido?* Este é o **2º caminho** do estudo: dados de operação "
        "do registry público, lidos ao lado do desempenho que medimos nas 3 máquinas."
    )

    if not adoption.available():
        st.info(
            "**Sem séries coletadas.** Rode `uv run lab05 downloads` para gerar "
            "`data/npm_downloads/*.csv` (T15, `#112`)."
        )
        return

    daily, weekly, quando = get_downloads()
    if daily.empty or weekly.empty:
        st.warning("Os CSVs de downloads existem, mas estão vazios. Refaça a coleta da T15.")
        return

    table = adoption.adoption_table(daily)
    inicio, fim = daily["day"].min(), daily["day"].max()
    st.caption(
        f"Série de {inicio:%d/%m/%Y} a {fim:%d/%m/%Y} · {len(daily):,} dias-pacote · "
        f"coletada em {quando[:10] if quando else '—'} · "
        "só a era de cada ferramenta ([por quê](https://github.com/luisajardim/"
        "Lab-Experimentacao-e-Medicao-/blob/main/Enunciado%205/docs/fonte_downloads.md))"
        .replace(",", ".")
    )

    st.error(
        "**Leia antes dos gráficos: download não é uso.** O npm **já vem instalado com o "
        "Node.js**, então quase ninguém o baixa do registry — ele aparece aqui com "
        f"{table.loc[table['package'] == 'npm', 'share_window'].iloc[0]:.1%} dos downloads da "
        "semana, o inverso do uso declarado no Stack Overflow Survey. "
        "**Não compare o nível do npm com o dos outros.** O que estes gráficos sustentam é a "
        "**tendência de cada série** e a comparação **entre os não-npm**, que dependem do "
        "registry para se instalar."
    )

    # ---------------------------------------------------------------- 1. séries temporais
    st.markdown("#### 1. Séries históricas de downloads")
    serie_abs, serie_share = st.tabs(["Valores absolutos", "Participação (%)"])
    with serie_abs:
        st.plotly_chart(figures.fig_adoption_series(weekly), width="stretch")
    with serie_share:
        st.plotly_chart(figures.fig_adoption_share(weekly), width="stretch")

    # ---------------------------------------------------------------- 2. último ano
    st.markdown("#### 2. Crescimento no último ano")
    col_graf, col_tab = st.columns([3, 2])
    with col_graf:
        st.plotly_chart(figures.fig_adoption_growth(table), width="stretch")
    with col_tab:
        view = table.rename(columns={
            "label": "Pacote",
            "downloads_window": "7 dias",
            "share_window": "Fatia",
            "downloads_year": "365 dias",
            "downloads_prev_year": "365 anteriores",
            "growth_pct": "Crescimento",
        })[["Pacote", "7 dias", "Fatia", "365 dias", "365 anteriores", "Crescimento"]]
        st.dataframe(
            view.style.format({
                "7 dias": "{:,.0f}",
                "Fatia": "{:.1%}",
                "365 dias": "{:,.0f}",
                "365 anteriores": "{:,.0f}",
                "Crescimento": "{:+.0f}%",
            }),
            width="stretch",
            hide_index=True,
        )

    # ---------------------------------------------------------------- 3. limitações
    st.markdown("#### 3. O que esta comparação pode e não pode dizer")
    st.markdown(
        "São **5 gerenciadores**, ou seja 5 pontos: a análise é **descritiva**, sem teste de "
        "correlação. Com n = 5 e dados observacionais, qualquer coeficiente seria ruído com "
        "aparência de resultado, e não há tratamento atribuído que permita falar de causa.\n\n"
        "**Limites de cada eixo:**\n"
        "- **Adoção (eixo X).** Cada ferramenta tem canais que não passam pelo registry: o npm vem "
        "com o Node, o pnpm tem Corepack e script próprio, o Bun recomenda o próprio instalador e "
        "o Berry é versionado dentro do projeto — é o que os nossos lockfiles fazem. O viés "
        "**não é igual entre os tratamentos**, então a ordem dos downloads não é a ordem da "
        "adoção. Um download também não é uma pessoa: CI, espelhos, bots e rebuilds de imagem "
        "Docker contam igual.\n"
        "- **O pacote `yarn` mistura as duas linhas.** O `yarn` 1.22 é o Classic e também o atalho "
        "que inicia um projeto Berry, então `yarn` → Yarn Classic é aproximado. O "
        "`@yarnpkg/cli` serve aos **dois** linkers do Berry: esses pontos compartilham o mesmo x "
        "(marcados com losango).\n"
        "- **Desempenho (eixo Y).** É a média geométrica dos speedups das células (projeto × "
        "cenário) — média geométrica porque speedup é razão. As barras são a **amplitude entre as "
        "células**, não intervalo de confiança: o IC por bootstrap está na aba *Todos × npm*, "
        "onde ele é calculado por célula.\n\n"
        "Ameaças registradas como **Co5** e **Co12** em `docs/ameacas.md`."
    )

    # ---------------------------------------------------------------- 4. cruzamento
    st.markdown("#### 4. Adoção × speedup medido")
    points = adoption.adoption_vs_performance(df, daily)
    if points.empty:
        st.info("Sem desempenho pareado suficiente para cruzar com a adoção.")
        return
    st.plotly_chart(figures.fig_adoption_vs_speedup(points), width="stretch")

    mais_rapido = points.loc[points["speedup_geo"].idxmax()]
    mais_baixado = points.loc[points["downloads_year"].idxmax()]
    if mais_rapido["manager"] == mais_baixado["manager"]:
        leitura = (
            f"Entre os não-npm, **{mais_rapido['label']}** é ao mesmo tempo o mais rápido "
            f"({mais_rapido['speedup_geo']:.2f}×) e o mais baixado. Os dois sinais apontam para o "
            "mesmo lado — o que é consistente com a adoção acompanhar o desempenho, mas com 5 "
            "pontos observacionais **não demonstra** que um causa o outro."
        )
    else:
        leitura = (
            f"Entre os não-npm, o mais rápido é **{mais_rapido['label']}** "
            f"({mais_rapido['speedup_geo']:.2f}×), mas o mais baixado é "
            f"**{mais_baixado['label']}**. Os dois sinais **não coincidem**: pelo menos nesta "
            "amostra, a adoção medida por downloads não segue o desempenho."
        )
    st.markdown(leitura)
    st.caption(
        "Análise completa contra as promessas dos fabricantes na T18 (`#115`); tradução em horas "
        "e custo de CI na T20 (`#117`)."
    )


def render_tab_impact(df: pd.DataFrame) -> None:
    """Aba 4: Impacto prático (horas e custo em CI + espaço em disco)."""
    st.subheader("Impacto Prático (CI e Máquina do Desenvolvedor)")
    st.info(
        "**Aba preparada para a S03 (T20 `#117`):** "
        "Traduzirá os speedups validados na coleta completa para horas economizadas e custo mensal "
        "em GitHub Actions, além da pegada total em disco (`disk_mb + cache_mb`) para múltiplos projetos."
    )
    desc_disk = stats.describe(df, metric="footprint_mb")
    if not desc_disk.empty:
        st.markdown("#### Prévia da Pegada Total em Disco (`disk_mb + cache_mb`, em MB)")
        pivot = desc_disk.pivot_table(
            index="manager", columns=["project", "scenario"], values="median"
        )
        st.dataframe(pivot.round(1), width="stretch")


def render_tab_method() -> None:
    """Aba 5: Método, protocolo e links de referência."""
    st.subheader("Método e Desenho Experimental")
    st.markdown(
        "- **Tratamentos (6):** `npm` (controle), `pnpm`, `bun`, `yarn-classic` (1.22), "
        "`yarn-berry-nm` (4.18.1) e `yarn-berry-pnp` (4.18.1).\n"
        "- **Cargas (3):** `express-api` (API pequena), `react-vite` (SPA) e `next-app` (SSR/App Router).\n"
        "- **Cenários (4):** `cold` (sem cache/lockfile), `ci` (lockfile, sem cache), "
        "`warm-cache` (lockfile + cache) e `reinstall` (tudo presente).\n"
        "- **Isolamento de rede:** Registry local **Verdaccio** com cache pré-aquecido.\n"
        "- **Testes não paramétricos:** Wilcoxon pareado por `(máquina, projeto, cenário, repetição)` "
        "com correção de Holm (`α = 0,05`); Friedman + post-hoc para família Yarn; Cliff's δ e "
        "speedup com IC 95% por bootstrap pareado."
    )


def main() -> None:
    st.set_page_config(
        page_title="Lab05 — Gerenciadores de Pacotes Node",
        page_icon="📦",
        layout="wide",
    )
    df, source_kind = get_runs()
    render_header(df, source_kind)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(list(TABS))
    with tab1:
        render_tab_vs_npm(df)
    with tab2:
        render_tab_yarn(df)
    with tab3:
        render_tab_adoption(df)
    with tab4:
        render_tab_impact(df)
    with tab5:
        render_tab_method()


if __name__ == "__main__":
    main()
