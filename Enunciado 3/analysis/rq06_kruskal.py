#!/usr/bin/env python3
"""T21 — RQ06: características dos repositórios associadas ao desempenho DORA.

Para cada fator × métrica DORA (RQ01-RQ04) testa se as distribuições diferem
entre os grupos do fator (ENUNCIADO §5, RQ 06):

* **Kruskal-Wallis** (≥ 3 grupos), com tamanho de efeito ε² = H / (n − 1);
* **Mann-Whitney** (2 grupos), com Cliff's delta δ = 2·U₁ / (n₁·n₂) − 1;
* **Holm** (``statsmodels.stats.multitest.multipletests``, ``method='holm'``)
  sobre todos os testes fator × métrica;
* **Dunn** post-hoc (com correção de empates e Holm dentro de cada teste) após
  Kruskal-Wallis significativo, com Cliff's delta para cada par.

Fatores (≥ 3 exigidos):
* ``linguagem``: linguagem principal; linguagens com menos de
  ``MIN_LANGUAGE_GROUP`` repositórios são agrupadas em "Outras";
* ``popularidade``: quartis de estrelas;
* ``idade``: quartis da idade do repositório (anos) no fim da janela;
* ``tipo``: tipo do projeto rotulado na amostra-ouro (consenso, T13), só para os
  repositórios rotulados e sem a categoria "outro".

Métricas: deployment frequency (RQ01), lead time (a) (RQ02), CFR (a) e (b)
(RQ03; a (b) vem de ``analysis/output/rq05_cfr_b.csv``) e tempo de recuperação
(RQ04). Valores ausentes são descartados por teste.

Interpretação do tamanho de efeito:
* Cliff's delta (Romano et al., 2006): |δ| < 0,147 desprezível; < 0,33 pequeno;
  < 0,474 médio; ≥ 0,474 grande;
* ε² (Rea & Parker, 1992): < 0,01 desprezível; < 0,04 fraco; < 0,16 moderado;
  < 0,36 relativamente forte; < 0,64 forte; ≥ 0,64 muito forte.

Saídas em ``analysis/output/``: ``rq06_tests.csv``, ``rq06_dunn.csv``,
``rq06_groups.csv`` e ``rq06_kruskal.md``.

Uso:
    python -m analysis.rq06_kruskal
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import kruskal, mannwhitneyu, norm, rankdata
from statsmodels.stats.multitest import multipletests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_dossiers import load_records  # noqa: E402

DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_CONSENSUS = DEFAULT_GOLD_DIR / "labels_consensus.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"
DEFAULT_CFR_B = DEFAULT_OUTPUT / "rq05_cfr_b.csv"

WINDOW_END = pd.Timestamp("2026-09-30T23:59:59Z")  # config.toml [window].end
ALPHA = 0.05
MIN_LANGUAGE_GROUP = 20
PROJECT_TYPES = ("biblioteca/framework", "aplicação/serviço", "ferramenta CLI")

METRICS = {
    "deployment_frequency_per_week": "Deployment frequency (releases/semana)",
    "lead_time_a_hours": "Lead time (a) (horas)",
    "cfr_a": "CFR (a)",
    "cfr_b": "CFR (b)",
    "recovery_hours": "Tempo de recuperação (horas)",
}
FACTORS = ("linguagem", "popularidade", "idade", "tipo")


# --- tamanhos de efeito ------------------------------------------------------

def cliffs_delta(x: Sequence[float], y: Sequence[float]) -> float:
    """δ = 2·U₁/(n₁·n₂) − 1 com U₁ de ``mannwhitneyu(x, y)`` (ENUNCIADO §5)."""
    u1 = mannwhitneyu(x, y, alternative="two-sided").statistic
    return float(2 * u1 / (len(x) * len(y)) - 1)


def delta_magnitude(delta: float) -> str:
    size = abs(delta)
    if size < 0.147:
        return "desprezível"
    if size < 0.33:
        return "pequeno"
    if size < 0.474:
        return "médio"
    return "grande"


def epsilon_squared(h: float, n: int) -> float:
    return float(h / (n - 1))


def epsilon_magnitude(epsilon: float) -> str:
    for upper, label in (
        (0.01, "desprezível"),
        (0.04, "fraco"),
        (0.16, "moderado"),
        (0.36, "relativamente forte"),
        (0.64, "forte"),
    ):
        if epsilon < upper:
            return label
    return "muito forte"


# --- testes ------------------------------------------------------------------

def dunn(groups: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    """Dunn (1964) com correção de empates; p-valores corrigidos por Holm."""
    labels = list(groups)
    pooled = np.concatenate([groups[g] for g in labels])
    ranks = rankdata(pooled)
    n_total = len(pooled)
    _, tie_counts = np.unique(pooled, return_counts=True)
    tie_term = float(np.sum(tie_counts**3 - tie_counts)) / (12 * (n_total - 1))
    sigma2 = n_total * (n_total + 1) / 12 - tie_term

    mean_rank, start = {}, 0
    for g in labels:
        size = len(groups[g])
        mean_rank[g] = ranks[start : start + size].mean()
        start += size

    rows = []
    for a, b in combinations(labels, 2):
        se = np.sqrt(sigma2 * (1 / len(groups[a]) + 1 / len(groups[b])))
        z = (mean_rank[a] - mean_rank[b]) / se
        delta = cliffs_delta(groups[a], groups[b])
        rows.append(
            {
                "group_a": a,
                "group_b": b,
                "n_a": len(groups[a]),
                "n_b": len(groups[b]),
                "z": float(z),
                "p_value": float(2 * norm.sf(abs(z))),
                "cliffs_delta": delta,
                "delta_magnitude": delta_magnitude(delta),
            }
        )
    if rows:
        adjusted = multipletests([r["p_value"] for r in rows], alpha=ALPHA, method="holm")[1]
        for row, p in zip(rows, adjusted, strict=True):
            row["p_holm"] = float(p)
            row["significant"] = bool(p < ALPHA)
    return rows


def compare(frame: pd.DataFrame, factor: str, metric: str) -> tuple[dict[str, Any], dict]:
    """Teste omnibus de ``metric`` entre os grupos de ``factor``."""
    data = frame[[factor, metric]].dropna()
    groups = {
        str(g): values[metric].to_numpy(dtype=float)
        for g, values in data.groupby(factor, observed=True)
        if len(values) >= 2
    }
    n = sum(len(v) for v in groups.values())
    row: dict[str, Any] = {"factor": factor, "metric": metric, "n": n, "k": len(groups)}
    if len(groups) < 2:
        return {**row, "test": "insuficiente"}, groups
    if len(groups) == 2:
        x, y = groups.values()
        result = mannwhitneyu(x, y, alternative="two-sided")
        delta = cliffs_delta(x, y)
        return {
            **row,
            "test": "Mann-Whitney",
            "statistic": float(result.statistic),
            "p_value": float(result.pvalue),
            "effect_name": "cliffs_delta",
            "effect": delta,
            "effect_magnitude": delta_magnitude(delta),
        }, groups
    result = kruskal(*groups.values())
    epsilon = epsilon_squared(result.statistic, n)
    return {
        **row,
        "test": "Kruskal-Wallis",
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "effect_name": "epsilon_squared",
        "effect": epsilon,
        "effect_magnitude": epsilon_magnitude(epsilon),
    }, groups


def run_tests(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    tests, all_groups = [], []
    for factor in FACTORS:
        for metric in METRICS:
            row, groups = compare(frame, factor, metric)
            tests.append(row)
            all_groups.append(groups)

    valid = [i for i, t in enumerate(tests) if "p_value" in t]
    adjusted = multipletests([tests[i]["p_value"] for i in valid], alpha=ALPHA, method="holm")[1]
    for i, p in zip(valid, adjusted, strict=True):
        tests[i]["p_holm"] = float(p)
        tests[i]["significant"] = bool(p < ALPHA)

    posthoc = []
    for test, groups in zip(tests, all_groups, strict=True):
        if test.get("test") == "Kruskal-Wallis" and test.get("significant"):
            for pair in dunn(groups):
                posthoc.append({"factor": test["factor"], "metric": test["metric"], **pair})
    return pd.DataFrame(tests), pd.DataFrame(posthoc)


# --- fatores -----------------------------------------------------------------

def _quartiles(values: pd.Series) -> pd.Series:
    labels = ["Q1 (menor)", "Q2", "Q3", "Q4 (maior)"]
    return pd.qcut(values.rank(method="first"), 4, labels=labels)


def build_factors(
    metrics: pd.DataFrame, records: dict[str, dict], consensus: pd.DataFrame | None
) -> pd.DataFrame:
    frame = metrics.copy()
    counts = frame["language"].value_counts()
    keep = counts[counts >= MIN_LANGUAGE_GROUP].index
    frame["linguagem"] = frame["language"].where(frame["language"].isin(keep), "Outras")
    frame["popularidade"] = _quartiles(frame["stars"])

    created = frame["full_name"].map(
        lambda n: (records.get(n) or {}).get("repository", {}).get("created_at")
    )
    frame["age_years"] = (WINDOW_END - pd.to_datetime(created, utc=True)).dt.days / 365.25
    frame["idade"] = _quartiles(frame["age_years"])

    frame["tipo"] = None
    if consensus is not None:
        types = consensus.set_index("full_name")["project_type"]
        frame["tipo"] = frame["full_name"].map(types).where(lambda s: s.isin(PROJECT_TYPES))
    return frame


def group_summary(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for factor in FACTORS:
        for group, data in frame.dropna(subset=[factor]).groupby(factor, observed=True):
            rows.append(
                {
                    "factor": factor,
                    "group": group,
                    "n": len(data),
                    **{f"median_{m}": data[m].median() for m in METRICS},
                }
            )
    return pd.DataFrame(rows)


# --- relatório ---------------------------------------------------------------

def _p(value: float) -> str:
    return "< 0,001" if value < 0.001 else f"{value:.3f}".replace(".", ",")


def _num(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def markdown(tests: pd.DataFrame, posthoc: pd.DataFrame, groups: pd.DataFrame) -> str:
    lines = [
        "# RQ06 — Características associadas ao desempenho DORA",
        "",
        "Gerado por `analysis/rq06_kruskal.py`. Kruskal-Wallis (≥ 3 grupos) ou "
        "Mann-Whitney (2 grupos); p-valores corrigidos por Holm sobre os "
        f"{tests['p_value'].notna().sum()} testes; α = 0,05.",
        "",
        "## Testes por fator × métrica",
        "",
        "| Fator | Métrica | Teste | n | Grupos | p | p (Holm) | Efeito | Interpretação |",
        "|---|---|---|---:|---:|---:|---:|---|---|",
    ]
    for _, t in tests.iterrows():
        if pd.isna(t.get("p_value")):
            lines.append(f"| {t['factor']} | {METRICS[t['metric']]} | {t['test']} | {t['n']} | {t['k']} | — | — | — | — |")
            continue
        symbol = "ε²" if t["effect_name"] == "epsilon_squared" else "δ"
        mark = " **\\***" if t["significant"] else ""
        lines.append(
            f"| {t['factor']} | {METRICS[t['metric']]} | {t['test']} | {t['n']} | {t['k']} "
            f"| {_p(t['p_value'])} | {_p(t['p_holm'])}{mark} | {symbol} = {_num(t['effect'])} "
            f"| {t['effect_magnitude']} |"
        )
    lines += [
        "",
        "\\* significativo após Holm (p < 0,05). ε²: Rea & Parker (1992); "
        "δ de Cliff: Romano et al. (2006).",
        "",
        "## Dunn post-hoc (Kruskal-Wallis significativos)",
        "",
    ]
    if posthoc.empty:
        lines.append("Nenhum Kruskal-Wallis significativo após Holm; post-hoc não aplicado.")
    else:
        lines += [
            "| Fator | Métrica | Grupo A | Grupo B | z | p (Holm) | δ de Cliff | Interpretação |",
            "|---|---|---|---|---:|---:|---:|---|",
        ]
        for _, d in posthoc.iterrows():
            mark = " **\\***" if d["significant"] else ""
            lines.append(
                f"| {d['factor']} | {METRICS[d['metric']]} | {d['group_a']} (n={d['n_a']}) "
                f"| {d['group_b']} (n={d['n_b']}) | {_num(d['z'], 2)} | {_p(d['p_holm'])}{mark} "
                f"| {_num(d['cliffs_delta'])} | {d['delta_magnitude']} |"
            )
        lines += ["", "δ > 0: o grupo A tende a ter valores maiores que o grupo B."]
    lines += ["", "## Grupos (n e mediana)", ""]
    header = " | ".join(METRICS.values())
    lines += [f"| Fator | Grupo | n | {header} |", "|---|---|---:|" + "---:|" * len(METRICS)]
    for _, g in groups.iterrows():
        medians = " | ".join(
            "—" if pd.isna(g[f"median_{m}"]) else _num(g[f"median_{m}"]) for m in METRICS
        )
        lines.append(f"| {g['factor']} | {g['group']} | {g['n']} | {medians} |")
    return "\n".join(lines) + "\n"


def load_cfr_b(path: Path, metrics: pd.DataFrame, gold_dir: Path) -> pd.DataFrame:
    """CFR(b) por repositório da RQ05; recalcula se o CSV ainda não existir."""
    if path.exists():
        return pd.read_csv(path)[["full_name", "cfr_b"]]
    from analysis.rq05_spearman import DEFAULT_CFR_METRICS, compute_cfr_b, load_candidate

    return compute_cfr_b(metrics, gold_dir, load_candidate(DEFAULT_CFR_METRICS))[
        ["full_name", "cfr_b"]
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    parser.add_argument("--consensus", type=Path, default=DEFAULT_CONSENSUS)
    parser.add_argument("--cfr-b", type=Path, default=DEFAULT_CFR_B)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    metrics = pd.read_csv(args.metrics)
    metrics = metrics.merge(load_cfr_b(args.cfr_b, metrics, args.gold_dir), on="full_name", how="left")
    consensus = (
        pd.read_csv(args.consensus, encoding="utf-8-sig") if args.consensus.exists() else None
    )
    frame = build_factors(metrics, load_records([args.gold_dir]), consensus)
    tests, posthoc = run_tests(frame)
    groups = group_summary(frame)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    tests.to_csv(args.output_dir / "rq06_tests.csv", index=False)
    posthoc.to_csv(args.output_dir / "rq06_dunn.csv", index=False)
    groups.to_csv(args.output_dir / "rq06_groups.csv", index=False)
    (args.output_dir / "rq06_kruskal.md").write_text(
        markdown(tests, posthoc, groups), encoding="utf-8"
    )

    significant = int((tests["significant"] == True).sum()) if "significant" in tests else 0  # noqa: E712
    print(f"{len(tests)} testes; {significant} significativos apos Holm; "
          f"{len(posthoc)} pares de Dunn. Saidas em {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
