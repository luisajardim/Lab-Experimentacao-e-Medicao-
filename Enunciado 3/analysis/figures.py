"""Figuras do relatório (RQ01–RQ08, funil e amostra-ouro).

Lê somente os CSVs/JSONs já gerados pelas análises e grava PNGs em
``analysis/output/figures/``. Rode depois dos scripts de ``analysis/``:

    uv run python analysis/figures.py

Escolhas de forma seguem a síntese "Escolhendo o gráfico certo": distribuições
assimétricas em histograma/boxplot com escala log e mediana marcada; categorias
em barras; relação entre variáveis em dispersão (RQ05, gerada por
``rq05_spearman.py``); matrizes em heatmap; proporções em barra 100%.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from lifelines import KaplanMeierFitter  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from analysis.rq06_kruskal import WINDOW_END, _quartiles  # noqa: E402

DATASETS = PROJECT_ROOT / "data" / "datasets"
GOLD = PROJECT_ROOT / "data" / "gold"
OUTPUT = PROJECT_ROOT / "analysis" / "output"

# Paleta de referência (validada; os 3 primeiros slots passam em todos os pares).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e4e3df"
NEUTRAL = "#b8b6af"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]
BLUE_RAMP = ["#e8f1fc", "#c3dbf6", "#8fbbed", "#5a98e0", "#2a78d6", "#1b5aa8", "#123d73"]
DORA_ORDER = ["Elite", "High", "Medium", "Low"]


# --- estilo ----------------------------------------------------------------------


def setup() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "axes.edgecolor": GRID,
            "axes.labelcolor": INK,
            "axes.titlecolor": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
            "xtick.color": INK_SECONDARY,
            "ytick.color": INK_SECONDARY,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "xtick.minor.size": 0,
            "ytick.minor.size": 0,
            "legend.frameon": False,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
        }
    )


def title(fig, text: str, subtitle: str | None = None) -> None:
    """Título à esquerda (+ subtítulo) e layout com margem fixa em polegadas."""
    height = fig.get_figheight()
    fig.suptitle(text, x=0.01, y=1 - 0.08 / height, ha="left", va="top", fontsize=12, color=INK)
    top = 0.32
    if subtitle:
        fig.text(0.01, 1 - 0.36 / height, subtitle, ha="left", va="top", fontsize=9, color=INK_SECONDARY)
        top = 0.52
    fig.tight_layout(rect=(0, 0, 1, 1 - top / height))


def fmt_num(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def plain_log(ax, axis: str = "x") -> None:
    formatter = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(formatter)


def log_bins(values: pd.Series, n: int = 30) -> np.ndarray:
    positive = values[values > 0]
    return np.logspace(np.log10(positive.min()), np.log10(positive.max()), n)


def median_line(ax, value: float, label: str, orientation: str = "v") -> None:
    if orientation == "v":
        ax.axvline(value, color=INK, linewidth=1.5, linestyle="--", zorder=4)
        ax.text(value, 1.0, f" {label}", transform=ax.get_xaxis_transform(),
                ha="left", va="bottom", fontsize=9, color=INK)
    else:
        ax.axhline(value, color=INK, linewidth=1.5, linestyle="--", zorder=4)


def threshold_lines(ax, cuts: list[tuple[float, str]], orientation: str = "v") -> None:
    for value, label in cuts:
        if orientation == "v":
            ax.axvline(value, color=NEUTRAL, linewidth=1, zorder=1)
            ax.text(value, 0.97, f"{label} ", transform=ax.get_xaxis_transform(), rotation=90,
                    ha="right", va="top", fontsize=8, color=INK_SECONDARY, zorder=5)
        else:
            ax.axhline(value, color=NEUTRAL, linewidth=1, zorder=1)
            ax.text(1.0, value, f" {label}", transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=8, color=INK_SECONDARY)


def box_strip(ax, groups: list[pd.Series], labels: list[str], log: bool = False,
              colors: list[str] | None = None, annotate: bool = True) -> None:
    """Boxplot com os pontos (jitter) por baixo e a mediana anotada."""
    colors = colors or [SERIES[0]] * len(groups)
    rng = np.random.default_rng(42)
    for i, (data, color) in enumerate(zip(groups, colors, strict=True), start=1):
        x = i + rng.uniform(-0.18, 0.18, len(data))
        ax.scatter(x, data, s=10, color=color, alpha=0.35, linewidths=0, zorder=2)
    ax.boxplot(
        groups, widths=0.5, showfliers=False, patch_artist=True, zorder=3,
        boxprops={"facecolor": "none", "edgecolor": INK, "linewidth": 1.2},
        medianprops={"color": INK, "linewidth": 2},
        whiskerprops={"color": INK, "linewidth": 1},
        capprops={"color": INK, "linewidth": 1},
    )
    for i, data in enumerate(groups, start=1):
        med = data.median()
        if not annotate:
            continue
        ax.text(i + 0.3, med, f"mediana {fmt_num(med, 3 if med < 1 else 1)}",
                va="center", fontsize=8.5, color=INK)
    ticks = [f"{lbl}\n(n={len(g)})" for lbl, g in zip(labels, groups, strict=True)]
    if not annotate:
        ticks = [f"{t}\nmed. {fmt_num(g.median(), 3 if g.median() < 1 else 1)}" for t, g in zip(ticks, groups, strict=True)]
    ax.set_xticks(range(1, len(groups) + 1), ticks)
    ax.grid(axis="x", visible=False)
    if log:
        ax.set_yscale("log")
        plain_log(ax, "y")


def save(fig, name: str, out: Path) -> Path:
    for ax in fig.axes:
        if ax.get_ylabel() == "Repositórios":
            ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    path = out / name
    fig.savefig(path)
    plt.close(fig)
    return path


# --- dados -----------------------------------------------------------------------


def load_metrics() -> pd.DataFrame:
    metrics = pd.read_csv(DATASETS / "metrics.csv")
    cfr_b = pd.read_csv(OUTPUT / "rq05_cfr_b.csv")[["full_name", "cfr_b"]]
    manifest = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "candidate_manifest.csv")
    frame = metrics.merge(cfr_b, on="full_name", how="left").merge(
        manifest[["full_name", "created_at"]], on="full_name", how="left"
    )
    frame["age_years"] = (WINDOW_END - pd.to_datetime(frame["created_at"], utc=True)).dt.days / 365.25
    frame["idade"] = _quartiles(frame["age_years"])
    return frame


# --- figuras ---------------------------------------------------------------------


def fig_funnel(out: Path) -> Path:
    candidates = len(pd.read_csv(PROJECT_ROOT / "data/raw/candidates.csv"))
    collected = sum(1 for p in GOLD.rglob("*.json") if p.parent != GOLD and p.parent.name != "dossiers")
    manifest = len(pd.read_csv(PROJECT_ROOT / "data/raw/candidate_manifest.csv"))
    final = len(pd.read_csv(DATASETS / "metrics.csv"))
    eligible = _count_eligible()
    stages = [
        ("Resultados da busca\n(12 faixas de estrelas)", candidates),
        ("Coletados localmente", collected),
        ("≥ 5 releases e ≥ 50 runs\nna janela", eligible),
        ("Manifesto congelado\n(seed 42)", manifest),
        ("Amostra final\n(seed 42)", final),
    ]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    labels, values = zip(*stages, strict=True)
    y = np.arange(len(stages))[::-1]
    ax.barh(y, values, color=SERIES[0], height=0.6)
    for yi, v in zip(y, values, strict=True):
        ax.text(v, yi, f"  {v:,}".replace(",", "."), va="center", fontsize=9, color=INK)
    ax.set_yticks(y, labels)
    ax.set_xscale("log")
    plain_log(ax)
    ax.set_xlim(100, candidates * 3)
    ax.set_xlabel("Repositórios (escala log)")
    ax.grid(axis="y", visible=False)
    title(fig, "Funil de seleção da amostra")
    return save(fig, "fig00_funil.png", out)


def _count_eligible() -> int:
    import tomllib

    cfg = tomllib.loads((PROJECT_ROOT / "config.toml").read_text(encoding="utf-8"))
    start, end = cfg["window"]["start"], cfg["window"]["end"]
    min_rel, min_runs = cfg["filters"]["min_releases"], cfg["filters"]["min_workflow_runs"]
    count = 0
    for path in GOLD.rglob("*.json"):
        if path.parent == GOLD or path.parent.name == "dossiers":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        repo = payload.get("repository", {})
        branch = repo.get("default_branch")
        releases = [
            r for r in payload.get("releases", [])
            if start <= str(r.get("published_at", ""))[:10] <= end
            and not r.get("draft") and not r.get("prerelease")
        ]
        runs = [
            r for month in payload.get("runs_by_month", {}).values() for r in month
            if r.get("branch") == branch and r.get("event") == "push"
        ]
        count += len(releases) >= min_rel and len(runs) >= min_runs
    return count


def fig_gold(out: Path) -> Path:
    agreement = {"tipo": None, "entrega": None, "corretiva": None}
    for line in (PROJECT_ROOT / "reports" / "agreement.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 5 and agreement.get(cells[0], 0) is None and "%" in cells[2]:
            agreement[cells[0]] = float(cells[3])
    best = json.loads((GOLD / "cfr_metrics.json").read_text(encoding="utf-8"))["best"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.3, 1]})
    bands = [(0.0, 0.2, "leve"), (0.2, 0.4, "razoável"), (0.4, 0.6, "moderada"),
             (0.6, 0.8, "substancial"), (0.8, 1.0, "quase perfeita")]
    for i, (lo, hi, name) in enumerate(bands):
        ax1.axvspan(lo, hi, color=BLUE_RAMP[0] if i % 2 else SURFACE, zorder=0)
        ax1.text((lo + hi) / 2, 1.02, name, transform=ax1.get_xaxis_transform(),
                 ha="center", va="bottom", fontsize=7.5, color=INK_SECONDARY)
    names = list(agreement)
    y = np.arange(len(names))[::-1]
    ax1.barh(y, [agreement[n] for n in names], color=SERIES[0], height=0.5, zorder=2)
    for yi, n in zip(y, names, strict=True):
        ax1.text(agreement[n] + 0.01, yi, fmt_num(agreement[n], 3), va="center", fontsize=9)
    ax1.set_yticks(y, ["Tipo de projeto\n(60 itens)", "Entrega ao usuário\n(60 itens)", "Release corretiva\n(300 itens)"])
    ax1.set_xlim(0, 1.0)
    ax1.set_xlabel("κ de Fleiss (faixas de Landis & Koch)")
    ax1.grid(axis="y", visible=False)

    matrix = np.array([[best["tp"], best["fn"]], [best["fp"], best["tn"]]])
    ax2.imshow(matrix, cmap=matplotlib.colors.ListedColormap(BLUE_RAMP[1:6]), vmin=0, vmax=matrix.max())
    for (i, j), v in np.ndenumerate(matrix):
        ax2.text(j, i, str(v), ha="center", va="center", fontsize=12,
                 color="white" if v > matrix.max() * 0.6 else INK)
    ax2.set_xticks([0, 1], ["corretiva", "não corretiva"])
    ax2.set_yticks([0, 1], ["corretiva", "não corretiva"])
    ax2.set_xlabel("Heurística")
    ax2.set_ylabel("Consenso")
    ax2.grid(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.set_title(f"Heurística {best['version']} × consenso\nP = {fmt_num(best['precision'])}  "
                  f"R = {fmt_num(best['recall'])}  F1 = {fmt_num(best['f1'])}",
                  fontsize=9.5, color=INK_SECONDARY, loc="left")
    title(fig, "Amostra-ouro: concordância entre avaliadores e validação da CFR (b)")
    return save(fig, "fig01_amostra_ouro.png", out)


def fig_rq01(frame: pd.DataFrame, out: Path) -> list[Path]:
    df = frame["deployment_frequency_per_week"].dropna()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df, bins=log_bins(df), color=SERIES[0], edgecolor=SURFACE, linewidth=1)
    ax.set_xscale("log")
    plain_log(ax)
    threshold_lines(ax, [(1 / 4.345, "mensal"), (1, "semanal"), (7, "diária")])
    median_line(ax, df.median(), f"mediana = {fmt_num(df.median())}/semana")
    ax.set_xlabel("Deployment frequency (releases por semana, escala log)")
    ax.set_ylabel("Repositórios")
    ax.grid(axis="x", visible=False)
    title(fig, "RQ01 — Distribuição da frequência de deploys",
          f"n = {len(df)}; linhas cinza = cortes DORA usados na classificação")
    p1 = save(fig, "fig02_rq01_deploy_freq.png", out)

    counts = frame["dora_c1_category"].fillna("Não classificável").value_counts()
    order = DORA_ORDER + ["Não classificável"]
    values = [int(counts.get(c, 0)) for c in order]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(order, values, color=[SERIES[0]] * 4 + [NEUTRAL], width=0.6)
    total = sum(values)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v}\n({fmt_num(100 * v / total, 1)}%)", ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Repositórios")
    ax.set_ylim(0, max(values) * 1.25)
    ax.grid(axis="x", visible=False)
    title(fig, "Classificação DORA geral (variante C1)", f"n = {total}")
    return [p1, save(fig, "fig03_rq01_dora_c1.png", out)]


def fig_rq02(frame: pd.DataFrame, out: Path) -> Path:
    paired = frame[["lead_time_a_hours", "lead_time_b_hours"]].dropna()
    paired = paired[(paired > 0).all(axis=1)]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    box_strip(ax, [paired["lead_time_a_hours"], paired["lead_time_b_hours"]],
              ["(a) por release", "(b) por commit"], log=True, colors=SERIES[:2])
    threshold_lines(ax, [(24, "1 dia"), (24 * 7, "1 semana"), (24 * 30, "1 mês")], orientation="h")
    ax.set_ylabel("Lead time (horas, escala log)")
    ax.set_xlim(0.5, 2.9)
    title(fig, "RQ02 — Lead time for changes: variante (a) × (b)",
          "mesmos repositórios nas duas caixas; linhas cinza = cortes DORA")
    return save(fig, "fig04_rq02_lead_time.png", out)


def fig_rq03(frame: pd.DataFrame, out: Path) -> Path:
    a, b = frame["cfr_a"].dropna(), frame["cfr_b"].dropna()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    box_strip(ax, [a, b], ["(a) proxy de CI", "(b) proxy de entrega"], colors=SERIES[:2])
    threshold_lines(ax, [(0.15, "15%"), (0.30, "30%"), (0.45, "45%")], orientation="h")
    ax.set_ylabel("Change failure rate (proporção)")
    ax.set_ylim(-0.03, 1.03)
    ax.set_xlim(0.5, 2.9)
    title(fig, "RQ03 — Change failure rate: variante (a) × (b)",
          "linhas cinza = cortes DORA usados na classificação (CFR a)")
    return save(fig, "fig05_rq03_cfr.png", out)


def fig_rq04(frame: pd.DataFrame, out: Path) -> Path:
    rec = frame["recovery_hours"].dropna()
    episodes = pd.read_csv(OUTPUT / "recovery_episodes.csv")
    episodes = episodes[episodes["duration_hours"] > 0]
    km = KaplanMeierFitter().fit(episodes["duration_hours"], event_observed=~episodes["censored"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    ax1.hist(rec, bins=log_bins(rec), color=SERIES[0], edgecolor=SURFACE, linewidth=1)
    ax1.set_xscale("log")
    plain_log(ax1)
    threshold_lines(ax1, [(1, "1 h"), (24, "1 dia"), (24 * 7, "1 semana")])
    median_line(ax1, rec.median(), f"mediana = {fmt_num(rec.median())} h")
    ax1.set_xlabel("Mediana de recuperação por repositório (horas, log)")
    ax1.set_ylabel("Repositórios")
    ax1.grid(axis="x", visible=False)
    ax1.set_title(f"Por repositório (n = {len(rec)})", loc="left", fontsize=10)

    sf = km.survival_function_
    ci = km.confidence_interval_survival_function_
    ax2.fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1], step="post", color=SERIES[0], alpha=0.2, linewidth=0)
    ax2.step(sf.index, sf.iloc[:, 0], where="post", color=SERIES[0], linewidth=2)
    med = km.median_survival_time_
    ax2.axhline(0.5, color=NEUTRAL, linewidth=1)
    ax2.axvline(med, color=INK, linestyle="--", linewidth=1.5)
    ax2.text(med, 0.95, f" mediana KM = {fmt_num(med)} h", fontsize=9)
    ax2.set_xscale("log")
    ax2.set_xlim(0.01, sf.index.max())
    plain_log(ax2)
    ax2.set_ylim(0, 1.02)
    ax2.set_xlabel("Horas desde o início do episódio de falha (log)")
    ax2.set_ylabel("Probabilidade de ainda não ter recuperado")
    n_cens = int(episodes["censored"].sum())
    ax2.set_title(f"Kaplan–Meier por episódio ({len(episodes):,} episódios; {n_cens} censurados)".replace(",", "."),
                  loc="left", fontsize=10)
    title(fig, "RQ04 — Tempo de recuperação após falha de CI/CD")
    return save(fig, "fig06_rq04_recovery.png", out)


def fig_rq06(frame: pd.DataFrame, out: Path) -> list[Path]:
    tests = pd.read_csv(OUTPUT / "rq06_tests.csv")
    metric_labels = {
        "deployment_frequency_per_week": "Deploy freq.",
        "lead_time_a_hours": "Lead time (a)",
        "cfr_a": "CFR (a)",
        "cfr_b": "CFR (b)",
        "recovery_hours": "Recuperação",
    }
    factor_labels = {"linguagem": "Linguagem", "popularidade": "Popularidade (estrelas)",
                     "idade": "Idade", "tipo": "Tipo de projeto (n≈55)"}
    eff = tests.pivot(index="factor", columns="metric", values="effect").loc[list(factor_labels), list(metric_labels)]
    sig = tests.pivot(index="factor", columns="metric", values="significant").loc[list(factor_labels), list(metric_labels)]

    fig, ax = plt.subplots(figsize=(8, 3.8))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("blue", BLUE_RAMP)
    im = ax.imshow(eff.values, cmap=cmap, vmin=0, vmax=0.3, aspect="auto")
    for (i, j), v in np.ndenumerate(eff.values):
        star = " *" if sig.values[i, j] else ""
        ax.text(j, i, f"{fmt_num(v, 3)}{star}", ha="center", va="center", fontsize=9.5,
                color="white" if v > 0.17 else INK, fontweight="bold" if star else "normal")
    ax.set_xticks(range(len(metric_labels)), metric_labels.values())
    ax.set_yticks(range(len(factor_labels)), factor_labels.values())
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    bar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    bar.set_label("ε² (tamanho de efeito)")
    bar.outline.set_visible(False)
    title(fig, "RQ06 — Tamanho de efeito (ε²) do Kruskal-Wallis por fator × métrica",
          "* = significativo após correção de Holm (20 testes, α = 0,05)")
    p1 = save(fig, "fig07_rq06_heatmap.png", out)

    panels = [
        ("deployment_frequency_per_week", "Deploy freq. (releases/semana)", True),
        ("lead_time_a_hours", "Lead time (a) (horas)", True),
        ("cfr_b", "CFR (b)", False),
    ]
    age_ranges = frame.groupby("idade", observed=True)["age_years"].agg(["min", "max"])
    groups_order = list(age_ranges.index)
    labels = [f"{g.split(' ')[0]}: {fmt_num(r['min'], 1)}–{fmt_num(r['max'], 1)} a"
              for g, r in age_ranges.iterrows()]
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
    for ax, (col, label, log) in zip(axes, panels, strict=True):
        data = [frame.loc[frame["idade"] == g, col].dropna() for g in groups_order]
        if log:
            data = [d[d > 0] for d in data]
        box_strip(ax, data, labels, log=log, annotate=False)
        ax.tick_params(axis="x", labelsize=8)
        ax.set_xlim(0.4, len(data) + 0.6)
        row = tests[(tests["factor"] == "idade") & (tests["metric"] == col)].iloc[0]
        p = "< 0,001" if row["p_holm"] < 0.001 else fmt_num(row["p_holm"], 3)
        ax.set_title(f"{label}\nε² = {fmt_num(row['effect'], 3)}; p (Holm) {p}", loc="left", fontsize=9.5)
    axes[0].set_ylabel("Valor por repositório")
    title(fig, "RQ06 — Métricas DORA por quartil de idade do repositório")
    return [p1, save(fig, "fig08_rq06_idade.png", out)]


def fig_rq07(out: Path) -> list[Path]:
    dist = pd.read_csv(OUTPUT / "rq07_distribution.csv").set_index("category").loc[DORA_ORDER]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    width = 0.26
    x = np.arange(len(DORA_ORDER))
    for i, variant in enumerate(["C1", "C2", "C3"]):
        bars = ax.bar(x + (i - 1) * (width + 0.01), dist[variant], width, color=SERIES[i], label=variant)
        for rect, v in zip(bars, dist[variant], strict=True):
            ax.text(rect.get_x() + rect.get_width() / 2, v, str(v), ha="center", va="bottom", fontsize=8)
    ax.set_xticks(x, DORA_ORDER)
    ax.set_ylabel("Repositórios")
    ax.grid(axis="x", visible=False)
    ax.legend(ncol=3, loc="upper right")
    title(fig, "RQ07 — Distribuição das categorias DORA por variante",
          "246 repositórios classificáveis nas três variantes (69 não classificáveis em todas)")
    p1 = save(fig, "fig09_rq07_distribuicao.png", out)

    summary = pd.read_csv(OUTPUT / "rq07_sensitivity.csv")
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("blue", BLUE_RAMP)
    for ax, pair in zip(axes, ["c1_c2", "c1_c3", "c2_c3"], strict=True):
        first, second = pair.upper().split("_")
        m = pd.read_csv(OUTPUT / f"rq07_transition_{pair}.csv", index_col=0).loc[DORA_ORDER, DORA_ORDER]
        ax.imshow(np.log1p(m.values), cmap=cmap, vmin=0, vmax=np.log1p(140))
        for (i, j), v in np.ndenumerate(m.values):
            ax.text(j, i, str(v), ha="center", va="center", fontsize=10,
                    color="white" if v > 40 else INK, fontweight="bold" if i == j else "normal")
        ax.set_xticks(range(4), DORA_ORDER)
        ax.set_yticks(range(4), DORA_ORDER)
        ax.set_xlabel(second)
        ax.set_ylabel(first)
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
        row = summary[summary["pair"].str.lower().str.replace("x", "_") == pair]
        if not row.empty:
            r = row.iloc[0]
            ax.set_title(f"{first} × {second}: {fmt_num(100 * r['pct_changed'], 1)}% mudaram; κ = {fmt_num(r['kappa_linear'], 3)}",
                         loc="left", fontsize=9.5)
    title(fig, "RQ07 — Matrizes de transição entre variantes (diagonal = manteve a categoria)")
    return [p1, save(fig, "fig10_rq07_transicoes.png", out)]


def fig_rq08(out: Path) -> Path:
    rework = pd.read_csv(OUTPUT / "rq08_rework_rate.csv")
    trend = pd.read_csv(OUTPUT / "rq08_temporal_trend.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.2), gridspec_kw={"width_ratios": [1, 1.3]})
    box_strip(ax1, [rework["rework_rate_window"].dropna(), rework["cfr_a"].dropna()],
              ["Rework rate", "CFR (a)"], colors=SERIES[:2])
    ax1.set_xlim(0.5, 2.9)
    ax1.set_ylim(-0.03, 1.03)
    ax1.set_ylabel("Proporção por repositório")
    ax1.set_title("Rework rate × CFR (a) na janela", loc="left", fontsize=10)

    rows = [("Deploy freq. (mensal)", "deploy_trend_monthly"), ("CFR (a) (mensal)", "cfr_trend_monthly"),
            ("Deploy freq. (trimestral)", "deploy_trend_quarterly"), ("Rework (trimestral)", "rework_trend_quarterly"),
            ("CFR (a) (trimestral)", "cfr_trend_quarterly")]
    cats = [("increasing", "alta", SERIES[1]), ("negligible", "sem tendência", NEUTRAL), ("decreasing", "baixa", SERIES[0])]
    y = np.arange(len(rows))[::-1]
    for yi, (_, col) in zip(y, rows, strict=True):
        counts = trend[col].fillna("negligible").replace({"no trend": "negligible"}).value_counts(normalize=True) * 100
        left = 0.0
        for key, _, color in cats:
            v = float(counts.get(key, 0))
            ax2.barh(yi, v, left=left, color=color, height=0.6, edgecolor=SURFACE, linewidth=2)
            if v >= 9:
                ax2.text(left + v / 2, yi, f"{fmt_num(v, 1)}%", ha="center", va="center", fontsize=8.5,
                         color="white" if key != "negligible" else INK)
            left += v
    ax2.set_yticks(y, [r[0] for r in rows])
    ax2.set_xlim(0, 100)
    ax2.set_xlabel("% dos repositórios (Mann-Kendall, p < 0,05)")
    ax2.grid(axis="y", visible=False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in cats]
    ax2.legend(handles, [lbl for _, lbl, _ in cats], ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    title(fig, f"RQ08 — Rework rate e tendência temporal (n = {len(rework)})")
    return save(fig, "fig11_rq08_rework_tendencia.png", out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT / "figures")
    args = parser.parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    setup()
    frame = load_metrics()
    paths = [fig_funnel(args.output_dir), fig_gold(args.output_dir)]
    paths += fig_rq01(frame, args.output_dir)
    paths += [fig_rq02(frame, args.output_dir), fig_rq03(frame, args.output_dir), fig_rq04(frame, args.output_dir)]
    paths += fig_rq06(frame, args.output_dir)
    paths += fig_rq07(args.output_dir)
    paths.append(fig_rq08(args.output_dir))
    for path in paths:
        print(path.relative_to(PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
