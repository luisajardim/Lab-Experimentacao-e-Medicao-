"""Dashboard Streamlit do Lab05 — Experimento em Software Real (npm × pnpm × Yarn × Bun).

Quatro abas: Todos × npm · Yarn × Yarn · Adoção × desempenho · Impacto (+ seção de método e links).
Lê os dados reais em `data/raw/*/runs.csv` via `schema.load_runs()`; enquanto não há coleta
completa (ou real), utiliza os dados disponíveis (piloto ou CSV sintético) com aviso explícito.

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

import figures  # noqa: E402
import stats  # noqa: E402
from config import (  # noqa: E402
    ALPHA,
    CONTROL,
    DATA_DOWNLOADS,
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
    """Carrega os dados reais disponíveis; se vazio, cai para o CSV sintético."""
    df = load_runs()
    if not df.empty:
        machines = sorted(df["machine"].dropna().unique())
        if len(machines) < 3 or set(df["scenario"].unique()) < set(SCENARIOS):
            return df, "partial"
        return df, "full"
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
    elif source_kind == "partial":
        machines = ", ".join(sorted(df["machine"].unique()))
        scenarios = ", ".join(sorted(df["scenario"].unique()))
        st.info(
            f"**Dados parciais (piloto):** Exibindo {len(df)} instalações medidas "
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


def render_tab_adoption() -> None:
    """Aba 3: Adoção (API de downloads do npm) × Desempenho."""
    st.subheader("Adoção × Desempenho")
    csvs = list(DATA_DOWNLOADS.glob("*.csv")) if DATA_DOWNLOADS.exists() else []
    if not csvs:
        st.info(
            "**Aba preparada para a S02 (T15 `#112` e T16 `#113`):** "
            "Exibirá as séries históricas de downloads da API pública do npm (`npm`, `pnpm`, `yarn`, "
            "`@yarnpkg/cli`, `bun`) cruzadas com o speedup medido no experimento."
        )
    else:
        st.success(f"{len(csvs)} arquivo(s) de séries de downloads encontrados em `data/npm_downloads/`.")


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
        render_tab_adoption()
    with tab4:
        render_tab_impact(df)
    with tab5:
        render_tab_method()


if __name__ == "__main__":
    main()
