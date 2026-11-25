"""Dashboard Streamlit do Lab05 — Experimento em Software Real (npm × pnpm × Yarn × Bun).

Quatro abas: Todos × npm · Yarn × Yarn · Adoção × desempenho · Impacto (+ seção de método e links).
Lê o dataset congelado pela validação (`data/processed/runs_all.csv`, T13). Sem ele, junta a coleta
em `data/raw/<maquina>/runs.csv` via `schema.load_runs()`, que deixa de fora o piloto e o
sintético. Enquanto ela não existe, mostra o piloto (ou, sem piloto, o CSV sintético) com aviso
explícito.

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
    DASHBOARD_URL,
    MANAGERS,
    PROJECTS,
    PROJECTS_URL,
    REPO_URL,
    SCENARIOS,
    YARN_VARIANTS,
)
from schema import load_dataset, load_runs  # noqa: E402

TABS = (
    "Todos × npm",
    "Yarn × Yarn",
    "Adoção × desempenho",
    "Impacto",
    "Método & Links",
)


@st.cache_data
def get_runs() -> tuple[pd.DataFrame, str]:
    """Dataset validado; sem ele, a coleta crua; sem ela, o piloto; sem piloto, o sintético."""
    df = load_dataset()
    if df.empty:
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
        f"[Dashboard publicado]({DASHBOARD_URL}) · [Repositório GitHub]({REPO_URL}) · "
        f"[Board Kanban Lab]({PROJECTS_URL}) · "
        f"Controle: `{CONTROL}` · Nível de significância: `α = {ALPHA:.2f}`".replace("0.", "0,")
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


def _num(x: float, decimals: int = 1) -> str:
    """Número no formato brasileiro (1.234,5)."""
    return f"{x:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _pval(p: float) -> str:
    return "< 0,001" if p < 0.001 else _num(p, 3)


def _range(low: float, high: float, decimals: int = 2) -> str:
    """"de 0,46 a 0,96 s", ou "cerca de 0,23 s" quando os extremos coincidem no arredondamento."""
    a, b = _num(low, decimals), _num(high, decimals)
    return f"cerca de {a} s" if a == b else f"de {a} a {b} s"


def _label(manager: str) -> str:
    return MANAGERS[manager]["label"]


def _cell(project: str, scenario: str) -> str:
    return f"{PROJECTS[project]['label']} · {SCENARIOS[scenario]['label']}"


def _join(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " e " + items[-1]


def _yarn_time_reading(yarn_df: pd.DataFrame, best: pd.DataFrame) -> str:
    """Leitura do tempo calculada dos dados: quem vence onde e se as máquinas concordam."""
    lines = []
    for manager in YARN_VARIANTS:
        wins = best[best["manager"] == manager]
        if wins.empty:
            lines.append(f"- **{_label(manager)}** não é o mais rápido em nenhuma célula.")
            continue
        cells = _join([_cell(r.project, r.scenario) for r in wins.itertuples()])
        lines.append(f"- **{_label(manager)}** é o mais rápido em {len(wins)} de {len(best)} "
                     f"células: {cells}.")

    med = (stats.valid_runs(yarn_df).groupby(["project", "scenario", "manager"])["wall_s"]
           .median().unstack())
    reinstall = med.xs("reinstall", level="scenario") if "reinstall" in med.index.get_level_values(
        "scenario") else pd.DataFrame()
    if not reinstall.empty and stats.YARN_BASE in reinstall:
        berry = reinstall.drop(columns=stats.YARN_BASE)
        lines.append(
            f"- No **reinstalar**, com tudo já instalado, o Classic leva "
            f"{_range(reinstall[stats.YARN_BASE].min(), reinstall[stats.YARN_BASE].max())}"
            f" e o Berry, {_range(berry.min().min(), berry.max().max())}: o Classic "
            "confere o arquivo de integridade e sai, e o Berry passa de novo pelas etapas de "
            "resolução, busca e link, mesmo sem baixar nada. A diferença absoluta fica abaixo de "
            "1 s, então é significativa, mas pouco relevante (C7 em `ameacas.md`)."
        )

    if {"yarn-berry-nm", "yarn-berry-pnp"} <= set(med.columns):
        ratio = (med["yarn-berry-nm"] / med["yarn-berry-pnp"]).dropna()
        if not ratio.empty:
            project, scenario = ratio.idxmax()
            files = (stats.valid_runs(yarn_df).query(
                "project == @project and scenario == @scenario and manager == 'yarn-berry-nm'")
                ["n_files"].median())
            lines.append(
                f"- A maior diferença entre os dois modos do Berry está em **{_cell(project, scenario)}**:"
                f" {_num(med.loc[(project, scenario), 'yarn-berry-nm'])} s com `node_modules` contra "
                f"{_num(med.loc[(project, scenario), 'yarn-berry-pnp'])} s com PnP "
                f"({_num(ratio.max())}×). Com o cache cheio, o modo `node_modules` ainda precisa "
                f"extrair cerca de {_num(files, 0)} arquivos dos zips do cache para o projeto; o PnP "
                "só escreve o mapa e lê os pacotes direto dos zips."
            )

    if not best.empty and best["n_machines"].notna().all():
        n_machines = int(best["n_machines"].max())
        same = best[best["n_agree"] == best["n_machines"]]
        text = (f"- O mais rápido é o mesmo nas {n_machines} máquinas em **{len(same)} de "
                f"{len(best)} células**")
        diff = best[best["n_agree"] < best["n_machines"]]
        if not diff.empty:
            text += (". Nas outras, a ordem muda em pelo menos uma máquina: "
                     + _join([_cell(r.project, r.scenario) for r in diff.itertuples()]))
        lines.append(text + ".")
    return "\n".join(lines)


def _yarn_disk_reading(yarn_df: pd.DataFrame, scenario: str = "ci") -> str:
    """Leitura de disco, arquivos e memória (cenário `ci`, em que a pegada se estabiliza)."""
    sub = stats.add_derived(stats.valid_runs(yarn_df[yarn_df["scenario"] == scenario]))
    med = sub.groupby(["project", "manager"])[
        ["n_files", "disk_mb", "cache_mb", "footprint_mb", "peak_rss_mb"]].median()
    if med.empty:
        return ""
    lines = []
    files = med["n_files"].unstack()
    if {"yarn-berry-pnp", "yarn-berry-nm"} <= set(files.columns):
        lines.append(
            f"- **O PnP quase não cria arquivos no projeto:** de {_num(files['yarn-berry-pnp'].min(), 0)}"
            f" a {_num(files['yarn-berry-pnp'].max(), 0)}, contra "
            f"{_num(files.drop(columns='yarn-berry-pnp').min().min(), 0)} a "
            f"{_num(files.drop(columns='yarn-berry-pnp').max().max(), 0)} das variantes com "
            "`node_modules`. O que sobra no projeto são o `.pnp.cjs`, o carregador e os pacotes que "
            "precisam ficar descompactados (binários nativos, por exemplo)."
        )
    disk = med["disk_mb"].unstack()
    cache = med["cache_mb"].unstack()
    if {"yarn-berry-pnp", "yarn-berry-nm"} <= set(disk.columns):
        cut = (1 - disk["yarn-berry-pnp"] / disk["yarn-berry-nm"]).dropna()
        lines.append(
            f"- **No projeto, o PnP ocupa de {_num(100 * cut.min(), 0)} % a {_num(100 * cut.max(), 0)} % "
            "menos disco** que o Berry com `node_modules`. O cache dos dois modos do Berry é o mesmo "
            "(um zip por pacote), então a economia é toda no projeto."
        )
    if stats.YARN_BASE in cache and "yarn-berry-nm" in cache:
        project = (cache[stats.YARN_BASE] / cache["yarn-berry-nm"]).idxmax()
        lines.append(
            f"- **O cache do Classic é o maior:** {_num(cache.loc[project, stats.YARN_BASE], 0)} MB "
            f"no {PROJECTS[project]['label']}, contra {_num(cache.loc[project, 'yarn-berry-nm'], 0)} MB "
            "do Berry. O Classic baixa para o cache os pacotes opcionais de **todas** as plataformas "
            "(binários nativos para Linux, macOS, AIX etc.) e instala no projeto só o da plataforma "
            "atual; o Berry baixa só o que a plataforma usa. No React + Vite, os 20 binários nativos "
            "do TypeScript 7 somam cerca de 716 MB do cache do Classic (reproduzido fora da coleta). "
            "Por isso a pegada total do Classic é a maior quando há dependências com binários nativos."
        )
    ram = med["peak_rss_mb"].unstack()
    if stats.YARN_BASE in ram and len(ram.columns) == len(YARN_VARIANTS):
        project = ram.max(axis=1).idxmax()
        lines.append(
            f"- Memória (métrica secundária, Co1): no {PROJECTS[project]['label']}, o Berry chega a "
            f"{_num(ram.loc[project].drop(stats.YARN_BASE).max(), 0)} MB de pico, contra "
            f"{_num(ram.loc[project, stats.YARN_BASE], 0)} MB do Classic. A amostragem subestima o "
            "pico, então o valor do Berry é um piso."
        )
    return "\n".join(lines)


def _yarn_compat_reading(yarn_df: pd.DataFrame) -> str:
    ok = (yarn_df["exit_code"] == 0) & yarn_df["build_ok"].astype(bool)
    rate = ok.groupby(yarn_df["manager"]).agg(["sum", "size"])
    parts = [f"{_label(m)}: {int(rate.loc[m, 'sum'])} de {int(rate.loc[m, 'size'])}"
             for m in YARN_VARIANTS if m in rate.index]
    head = ("Todas as instalações das três variantes terminaram sem erro e o build passou"
            if bool(ok.all()) else "Instalações que terminaram sem erro e com build válido")
    return (f"{head} ({'; '.join(parts)}). O PnP só compila os três projetos com o build ajustado "
            "(`vite build` sem `tsc -b` e `next build --webpack`), aplicado aos 6 tratamentos para "
            "manter a comparação justa. O sucesso do PnP vale **nessa configuração** (Co7 em "
            "`ameacas.md`); um projeto com ferramentas que leem o `node_modules` direto pode "
            "exigir mais ajustes.")


def render_tab_yarn(df: pd.DataFrame) -> None:
    """Aba 2: Yarn × Yarn (Classic 1.22 × Berry 4 node-modules × Berry 4 PnP), T14 (#111)."""
    st.subheader("Yarn × Yarn: a evolução do mesmo software e o trade-off do PnP")
    st.markdown(
        "Três modos do mesmo gerenciador: o **Yarn Classic 1.22**, a linha antiga, o **Yarn Berry 4 "
        "com `node_modules`** e o **Yarn Berry 4 com Plug'n'Play (PnP)**, que troca o "
        "`node_modules` por um mapa (`.pnp.cjs`) e lê os pacotes direto dos zips do cache. O "
        "Classic é a referência: a pergunta é o que mudou da versão antiga para a nova (RQ2)."
    )
    yarn_df = df[df["manager"].isin(YARN_VARIANTS)]
    if yarn_df.empty:
        st.info("Não há instalações do Yarn nos dados carregados.")
        return

    st.markdown("#### Tempo de instalação: depende do projeto e do cenário")
    vs_classic = stats.yarn_vs_classic(yarn_df)
    st.plotly_chart(figures.fig_speedup_vs_control(vs_classic, control=stats.YARN_BASE, log_y=True),
                    width="stretch")
    st.caption(
        "Speedup = mediana do Classic / mediana da variante, nos pares de mesma máquina e "
        "repetição. Acima de 1×, o Berry é mais rápido que o Classic. Barras: IC 95% por bootstrap "
        "pareado. Eixo em escala log, para 2× e 0,5× ficarem à mesma distância do 1×."
    )
    st.markdown(_yarn_time_reading(yarn_df, stats.machine_agreement(yarn_df, YARN_VARIANTS)))
    metric = st.selectbox(
        "Valores absolutos por métrica",
        options=["wall_s", "cpu_s", "peak_rss_mb"],
        format_func=lambda m: figures.METRIC_LABELS.get(m, m),
        key="tab2_metric",
    )
    st.plotly_chart(figures.fig_yarn_comparison(yarn_df, metric=metric), width="stretch")

    st.markdown("#### Disco e arquivos: o que o PnP economiza")
    st.plotly_chart(figures.fig_yarn_footprint(yarn_df), width="stretch")
    st.markdown(_yarn_disk_reading(yarn_df))
    ci = stats.add_derived(stats.valid_runs(yarn_df[yarn_df["scenario"] == "ci"]))
    if not ci.empty:
        table = (ci.groupby(["project", "manager"])[["n_files", "disk_mb", "cache_mb", "footprint_mb"]]
                 .median().reset_index())
        table["project"] = table["project"].map(lambda p: PROJECTS[p]["label"])
        table["manager"] = table["manager"].map(_label)
        st.dataframe(
            table.rename(columns={"project": "Projeto", "manager": "Variante",
                                  "n_files": "Arquivos no projeto", "disk_mb": "Projeto (MB)",
                                  "cache_mb": "Cache (MB)", "footprint_mb": "Total (MB)"}).round(1),
            width="stretch", hide_index=True,
        )
        st.caption("Medianas depois do cenário CI (lockfile presente, cache vazio antes da instalação).")

    st.markdown("#### Compatibilidade")
    st.markdown(_yarn_compat_reading(yarn_df))

    st.markdown("#### Testes: Friedman + post-hoc de Wilcoxon com Holm (tempo)")
    omnibus, posthoc = stats.yarn_friedman(yarn_df, metric="wall_s")
    if not omnibus.empty:
        rejected = int(omnibus["reject"].sum())
        st.markdown(
            f"O Friedman rejeita a igualdade das três variantes em **{rejected} de {len(omnibus)}** "
            f"combinações de projeto e cenário (α = {_num(ALPHA, 2)})."
        )
        view = pd.DataFrame({
            "Projeto": omnibus["project"].map(lambda p: PROJECTS[p]["label"]),
            "Cenário": omnibus["scenario"].map(lambda s: SCENARIOS[s]["label"]),
            "Blocos": omnibus["n_blocks"],
            **{f"Mediana {_label(v)} (s)": omnibus[f"median_{v}"].round(2) for v in YARN_VARIANTS},
            "χ²": omnibus["statistic"].round(1),
            "p": omnibus["p"].map(_pval),
            "Rejeita H₀": omnibus["reject"].map({True: "sim", False: "não"}),
        })
        st.dataframe(view, width="stretch", hide_index=True)
    if not posthoc.empty:
        not_sig = posthoc[~posthoc["reject"]]
        if not not_sig.empty:
            st.markdown(
                "No post-hoc, os pares **sem diferença significativa** depois do Holm são: "
                + _join([f"{_label(r.a)} × {_label(r.b)} em {_cell(r.project, r.scenario)}"
                         for r in not_sig.itertuples()]) + "."
            )
        faster_a = posthoc["median_a"] <= posthoc["median_b"]
        pairs = pd.DataFrame({
            "Projeto": posthoc["project"].map(lambda p: PROJECTS[p]["label"]),
            "Cenário": posthoc["scenario"].map(lambda s: SCENARIOS[s]["label"]),
            "Par": [f"{_label(a)} × {_label(b)}" for a, b in zip(posthoc["a"], posthoc["b"], strict=True)],
            "Mais rápido": [_label(a if f else b)
                            for a, b, f in zip(posthoc["a"], posthoc["b"], faster_a, strict=True)],
            "Razão das medianas": (posthoc[["median_a", "median_b"]].max(axis=1)
                                   / posthoc[["median_a", "median_b"]].min(axis=1)).round(2),
            "Cliff's δ": posthoc["cliffs_delta"].abs().round(2),
            "Magnitude": posthoc["magnitude"],
            "p (Holm)": posthoc["p_holm"].map(_pval),
            "Significativo": posthoc["reject"].map({True: "sim", False: "não"}),
        })
        with st.expander("Ver as comparações post-hoc"):
            st.dataframe(pairs, width="stretch", hide_index=True)
    st.caption(
        "Os blocos (máquina × repetição) são tratados como independentes: leia os p-valores como "
        "comparação **nestas 3 máquinas** (C1 em `ameacas.md`). O apoio mais forte para "
        "generalizar é a concordância entre as máquinas, mostrada acima."
    )


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
