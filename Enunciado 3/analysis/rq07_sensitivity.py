#!/usr/bin/env python3
"""T22 — RQ07: sensibilidade da classificação DORA à definição operacional.

Uso:
    python -m analysis.rq07_sensitivity
    python -m analysis.rq07_sensitivity --metrics data/datasets/metrics.csv

Compara as classificações C1 (referência), C2 e C3 de ``metrics.csv`` em cada
par (C1×C2, C1×C3, C2×C3):

* matriz de transição 4×4 (Elite/High/Medium/Low), linhas = primeira variante;
* % de repositórios que mudam de categoria;
* κ de Cohen ponderado linear (``cohen_kappa_score(..., weights="linear")``),
  interpretado pela escala de Landis & Koch (1977).

As métricas de concordância usam só os repositórios classificáveis nas duas
variantes do par; quantos ficaram de fora é reportado explicitamente.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import pandas as pd
from sklearn.metrics import cohen_kappa_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"

CATEGORIES = ("Elite", "High", "Medium", "Low")
VARIANTS = {
    "C1": "dora_c1_category",
    "C2": "dora_c2_category",
    "C3": "dora_c3_category",
}
VARIANT_DESCRIPTIONS = {
    "C1": "deploy = release; lead time (a) por release; CFR (a)",
    "C2": "deploy = release + tags com data; lead time (a) por release; CFR (a)",
    "C3": "deploy = release + tags com data; lead time (b) por commit; CFR (a)",
}


@dataclass(frozen=True)
class PairResult:
    first: str
    second: str
    n_total: int
    n_compared: int
    n_excluded: int
    n_changed: int
    pct_changed: float
    n_up: int
    n_down: int
    n_jump_2plus: int
    kappa_linear: float | None
    interpretation: str
    transitions: pd.DataFrame


def landis_koch(kappa: float | None) -> str:
    """Interpretação de Landis & Koch (1977) para um valor de κ."""
    if kappa is None or pd.isna(kappa):
        return "indisponível"
    if kappa < 0:
        return "pobre"
    if kappa <= 0.20:
        return "leve"
    if kappa <= 0.40:
        return "razoável"
    if kappa <= 0.60:
        return "moderada"
    if kappa <= 0.80:
        return "substancial"
    return "quase perfeita"


def normalize(series: pd.Series) -> pd.Series:
    """Mantém só as quatro categorias válidas; o resto vira NA (não classificável)."""
    cleaned = series.astype("string").str.strip()
    return cleaned.where(cleaned.isin(CATEGORIES))


def transition_matrix(first: pd.Series, second: pd.Series) -> pd.DataFrame:
    """Matriz 4×4 de contagens, com linhas/colunas sempre na ordem Elite→Low."""
    matrix = pd.crosstab(
        pd.Categorical(first, categories=CATEGORIES),
        pd.Categorical(second, categories=CATEGORIES),
        dropna=False,
    )
    matrix.index = list(CATEGORIES)
    matrix.columns = list(CATEGORIES)
    return matrix.astype(int)


def compare_pair(frame: pd.DataFrame, first: str, second: str) -> PairResult:
    a = normalize(frame[VARIANTS[first]])
    b = normalize(frame[VARIANTS[second]])
    both = a.notna() & b.notna()
    a_ok, b_ok = a[both].astype(str), b[both].astype(str)

    rank = {category: index for index, category in enumerate(CATEGORIES)}
    delta = a_ok.map(rank) - b_ok.map(rank)  # >0: segunda variante é melhor (mais perto de Elite)
    n_compared = int(both.sum())
    n_changed = int((delta != 0).sum())

    kappa: float | None = None
    if n_compared and (a_ok.nunique() > 1 or b_ok.nunique() > 1):
        kappa = float(cohen_kappa_score(a_ok, b_ok, labels=list(CATEGORIES), weights="linear"))
    elif n_compared:
        kappa = 1.0 if n_changed == 0 else None

    return PairResult(
        first=first,
        second=second,
        n_total=len(frame),
        n_compared=n_compared,
        n_excluded=len(frame) - n_compared,
        n_changed=n_changed,
        pct_changed=n_changed / n_compared if n_compared else float("nan"),
        n_up=int((delta > 0).sum()),
        n_down=int((delta < 0).sum()),
        n_jump_2plus=int((delta.abs() >= 2).sum()),
        kappa_linear=kappa,
        interpretation=landis_koch(kappa),
        transitions=transition_matrix(a_ok, b_ok),
    )


def compare_all(frame: pd.DataFrame) -> list[PairResult]:
    return [compare_pair(frame, first, second) for first, second in combinations(VARIANTS, 2)]


def distribution(frame: pd.DataFrame) -> pd.DataFrame:
    """Contagem por categoria em cada variante, incluindo não classificáveis."""
    order = [*CATEGORIES, "Não classificável"]
    data = {}
    for name, column in VARIANTS.items():
        counts = normalize(frame[column]).fillna("Não classificável").value_counts()
        data[name] = [int(counts.get(category, 0)) for category in order]
    return pd.DataFrame(data, index=order)


def summary_frame(results: list[PairResult]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "pair": f"{r.first}x{r.second}",
                "n_total": r.n_total,
                "n_compared": r.n_compared,
                "n_excluded": r.n_excluded,
                "n_changed": r.n_changed,
                "pct_changed": r.pct_changed,
                "n_improved_in_second": r.n_up,
                "n_worsened_in_second": r.n_down,
                "n_jump_2plus_levels": r.n_jump_2plus,
                "kappa_linear": r.kappa_linear,
                "interpretation": r.interpretation,
            }
            for r in results
        ]
    )


def _matrix_markdown(matrix: pd.DataFrame, first: str, second: str) -> list[str]:
    header = f"| {first} \\ {second} | " + " | ".join(CATEGORIES) + " | total |"
    lines = [header, "|---|" + "---:|" * (len(CATEGORIES) + 1)]
    for category in CATEGORIES:
        row = matrix.loc[category]
        cells = [f"**{v}**" if category == col else str(v) for col, v in row.items()]
        lines.append(f"| {category} | " + " | ".join(cells) + f" | {int(row.sum())} |")
    totals = matrix.sum(axis=0)
    lines.append("| total | " + " | ".join(str(int(v)) for v in totals) + f" | {int(totals.sum())} |")
    return lines


def markdown(results: list[PairResult], dist: pd.DataFrame, source: Path) -> str:
    lines = [
        "# T22 — RQ07: sensibilidade da classificação DORA",
        "",
        f"Fonte: `{source.name}` ({results[0].n_total if results else 0} repositórios). "
        "κ de Cohen ponderado linear (`sklearn.metrics.cohen_kappa_score`, `weights='linear'`), "
        "interpretado pela escala de Landis & Koch (1977).",
        "",
        "## Variantes comparadas",
        "",
        "| variante | definição |",
        "|---|---|",
        *(f"| {name} | {desc} |" for name, desc in VARIANT_DESCRIPTIONS.items()),
        "",
        "## Distribuição por variante",
        "",
        "| categoria | " + " | ".join(dist.columns) + " |",
        "|---|" + "---:|" * len(dist.columns),
        *(
            f"| {category} | " + " | ".join(str(v) for v in dist.loc[category]) + " |"
            for category in dist.index
        ),
        "",
        "## Concordância entre pares",
        "",
        "| par | n comparado | excluídos | mudaram | % mudou | melhoraram | pioraram "
        "| saltos ≥ 2 níveis | κ linear | interpretação |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for r in results:
        kappa = f"{r.kappa_linear:.3f}" if r.kappa_linear is not None else "—"
        lines.append(
            f"| {r.first}×{r.second} | {r.n_compared} | {r.n_excluded} | {r.n_changed} | "
            f"{r.pct_changed:.1%} | {r.n_up} | {r.n_down} | {r.n_jump_2plus} | {kappa} | "
            f"{r.interpretation} |"
        )
    lines += [
        "",
        "\"Melhoraram\"/\"pioraram\" referem-se à segunda variante do par em relação à primeira "
        "(melhorar = mais perto de Elite). Excluídos = não classificáveis em pelo menos uma das "
        "duas variantes (alguma métrica ausente).",
        "",
        "## Matrizes de transição",
        "",
        "Linhas = primeira variante, colunas = segunda. A diagonal (negrito) são os "
        "repositórios que mantiveram a categoria.",
    ]
    for r in results:
        lines += ["", f"### {r.first} × {r.second}", "", *_matrix_markdown(r.transitions, r.first, r.second)]
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    frame = pd.read_csv(args.metrics)
    missing = set(VARIANTS.values()) - set(frame.columns)
    if missing:
        parser.error(f"CSV sem colunas obrigatórias: {', '.join(sorted(missing))}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    results = compare_all(frame)
    dist = distribution(frame)

    summary_frame(results).to_csv(args.output_dir / "rq07_sensitivity.csv", index=False)
    dist.to_csv(args.output_dir / "rq07_distribution.csv", index_label="category")
    for r in results:
        r.transitions.to_csv(
            args.output_dir / f"rq07_transition_{r.first.lower()}_{r.second.lower()}.csv",
            index_label=f"{r.first}\\{r.second}",
        )
    report = args.output_dir / "rq07_sensitivity.md"
    report.write_text(markdown(results, dist, args.metrics), encoding="utf-8")
    print(f"T22 sensibilidade: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
