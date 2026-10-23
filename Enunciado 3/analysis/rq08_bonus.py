#!/usr/bin/env python3
"""T23 — RQ08 (bônus): taxa de retrabalho (rework rate) e evolução temporal (Mann-Kendall).

Implementa ambos os bônus descritos no ENUNCIADO §5 e kanban #68:
1. Rework rate (DORA 2024): proporção de releases corretivas (identificadas pela
   heurística CFR(b) validada na amostra-ouro) sobre o total de releases.
2. Evolução temporal (Mann-Kendall): calcula métricas por trimestre (e mensal)
   e aplica o teste não-paramétrico de Mann-Kendall (pymannkendall) para verificar
   tendências de melhoria ou piora (increasing, decreasing, negligible para p < 0.05).

Uso:
    python -m analysis.rq08_bonus
    python -m analysis.rq08_bonus --metrics data/datasets/metrics.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pymannkendall as mk

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_METRICS = PROJECT_ROOT / "data" / "datasets" / "metrics.csv"
DEFAULT_GOLD_DIR = PROJECT_ROOT / "data" / "gold"
DEFAULT_CFR_METRICS = PROJECT_ROOT / "data" / "gold" / "cfr_metrics.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "analysis" / "output"

sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_dossiers import _commit_message, _commits_for, _previous_release  # noqa: E402
from tune_cfr import Candidate, Item, predict  # noqa: E402

from metrics.cfr import cfr_a  # noqa: E402

QUARTERS = (
    ("Q1", "2025-10-01", "2025-12-31", ("2025-10", "2025-11", "2025-12")),
    ("Q2", "2026-01-01", "2026-03-31", ("2026-01", "2026-02", "2026-03")),
    ("Q3", "2026-04-01", "2026-06-30", ("2026-04", "2026-05", "2026-06")),
    ("Q4", "2026-07-01", "2026-09-30", ("2026-07", "2026-08", "2026-09")),
)

MONTHS = (
    "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03",
    "2026-04", "2026-05", "2026-06",
    "2026-07", "2026-08", "2026-09",
)

WINDOW_START = "2025-10-01"
WINDOW_END = "2026-09-30"


@dataclass(frozen=True)
class MKResult:
    trend: str  # 'increasing', 'decreasing', 'negligible'
    p_value: float
    tau: float
    slope: float


def run_mann_kendall(series: Sequence[float | int], alpha: float = 0.05) -> MKResult:
    """Executa o teste de Mann-Kendall original mapeando para increasing/decreasing/negligible."""
    if len(series) < 3 or len(set(series)) <= 1:
        return MKResult(trend="negligible", p_value=1.0, tau=0.0, slope=0.0)
    try:
        res = mk.original_test(list(series), alpha=alpha)
        trend = res.trend if res.p < alpha and res.trend in ("increasing", "decreasing") else "negligible"
        return MKResult(
            trend=trend,
            p_value=float(res.p),
            tau=float(res.Tau),
            slope=float(res.slope),
        )
    except Exception:
        return MKResult(trend="negligible", p_value=1.0, tau=0.0, slope=0.0)


DEFAULT_CANDIDATE = Candidate(version="v2", keywords="base", match="palavra")


def load_candidate(cfr_metrics_path: Path) -> tuple[Candidate, str]:
    """Heurística escolhida no tuning (T14), a mesma usada na CFR (b) da RQ03/RQ05."""
    if not cfr_metrics_path.exists():
        return DEFAULT_CANDIDATE, DEFAULT_CANDIDATE.name
    meta = json.loads(cfr_metrics_path.read_text(encoding="utf-8"))
    best = meta["best"]
    candidate = Candidate(
        version=best["version"],
        keywords=best.get("keywords"),
        match=best.get("match"),
        cutoff=best.get("cutoff"),
        feature_weight=best.get("feature_weight"),
    )
    name = candidate.name
    if "f1" in best:
        name += f"; F1 = {best['f1']:.3f} no consenso da amostra-ouro"
    return candidate, name


def is_release_corrective(
    payload: dict[str, Any],
    release: dict[str, Any],
    candidate: Candidate,
) -> bool:
    """Classifica a release com a mesma heurística da CFR (b)."""
    prev = _previous_release(payload, release)
    commits = _commits_for(payload, release)
    item = Item(
        full_name=str(payload.get("repository", {}).get("full_name", "")),
        tag=release.get("tag_name"),
        previous_tag=prev.get("tag_name") if prev else None,
        messages=None if commits is None else tuple(map(_commit_message, commits)),
        expected=False,
    )
    return predict(candidate, [item])[0]


def _cfr_a_or_none(runs: list[dict[str, Any]]) -> float | None:
    """CFR (a) do período com a tabela de ``conclusion`` do ENUNCIADO §3."""
    return cfr_a([run.get("conclusion") for run in runs])


def _present(series: list[float | None]) -> list[float]:
    """Remove períodos sem nenhum run válido (sem sucesso nem falha)."""
    return [value for value in series if value is not None]


def process_repository(
    name: str,
    payload: dict[str, Any],
    candidate: Candidate,
) -> dict[str, Any]:
    """Processa um repositório calculando taxa de retrabalho e séries trimestrais/mensais."""
    # Deploy = release publicada, não-draft e não-pré-release (definição principal, como na RQ03 b).
    releases = [
        r
        for r in payload.get("releases", [])
        if not r.get("draft", False) and not r.get("prerelease", False) and r.get("published_at")
    ]
    releases.sort(key=lambda r: str(r["published_at"]))
    corrective = {id(r): is_release_corrective(payload, r, candidate) for r in releases}

    # Rework rate na janela
    window_releases = [r for r in releases if WINDOW_START <= str(r["published_at"])[:10] <= WINDOW_END]
    window_corrective = [r for r in window_releases if corrective[id(r)]]
    all_corrective = [r for r in releases if corrective[id(r)]]

    total_w = len(window_releases)
    corr_w = len(window_corrective)
    rework_rate_w = corr_w / total_w if total_w > 0 else None

    total_all = len(releases)
    corr_all = len(all_corrective)
    rework_rate_all = corr_all / total_all if total_all > 0 else None

    # Séries trimestrais
    q_releases: list[int] = []
    q_rework: list[float] = []
    q_cfr: list[float | None] = []

    rbm = payload.get("runs_by_month", {})

    for _, q_start, q_end, q_months in QUARTERS:
        q_rels = [r for r in window_releases if q_start <= str(r["published_at"])[:10] <= q_end]
        n_rel = len(q_rels)
        q_releases.append(n_rel)
        n_corr = sum(1 for r in q_rels if corrective[id(r)])
        q_rework.append(n_corr / n_rel if n_rel > 0 else 0.0)

        q_runs: list[dict[str, Any]] = []
        for m in q_months:
            q_runs.extend(rbm.get(m, []))
        q_cfr.append(_cfr_a_or_none(q_runs))

    # Séries mensais
    m_releases: list[int] = []
    m_cfr: list[float | None] = []
    for m in MONTHS:
        m_rels = [r for r in window_releases if str(r["published_at"])[:7] == m]
        m_releases.append(len(m_rels))
        m_cfr.append(_cfr_a_or_none(rbm.get(m, [])))

    # Mann-Kendall Trimestral
    mk_d_q = run_mann_kendall(q_releases)
    mk_r_q = run_mann_kendall(q_rework)
    mk_c_q = run_mann_kendall(_present(q_cfr))

    # Mann-Kendall Mensal
    mk_d_m = run_mann_kendall(m_releases)
    mk_c_m = run_mann_kendall(_present(m_cfr))

    return {
        "full_name": name,
        "total_releases_window": total_w,
        "corrective_releases_window": corr_w,
        "rework_rate_window": rework_rate_w,
        "total_releases_all": total_all,
        "corrective_releases_all": corr_all,
        "rework_rate_all": rework_rate_all,
        # Trimestral
        "q1_releases": q_releases[0],
        "q2_releases": q_releases[1],
        "q3_releases": q_releases[2],
        "q4_releases": q_releases[3],
        "deploy_trend_quarterly": mk_d_q.trend,
        "deploy_p_quarterly": mk_d_q.p_value,
        "deploy_tau_quarterly": mk_d_q.tau,
        "q1_rework": q_rework[0],
        "q2_rework": q_rework[1],
        "q3_rework": q_rework[2],
        "q4_rework": q_rework[3],
        "rework_trend_quarterly": mk_r_q.trend,
        "rework_p_quarterly": mk_r_q.p_value,
        "rework_tau_quarterly": mk_r_q.tau,
        "q1_cfr": q_cfr[0],
        "q2_cfr": q_cfr[1],
        "q3_cfr": q_cfr[2],
        "q4_cfr": q_cfr[3],
        "cfr_trend_quarterly": mk_c_q.trend,
        "cfr_p_quarterly": mk_c_q.p_value,
        "cfr_tau_quarterly": mk_c_q.tau,
        # Mensal
        "deploy_trend_monthly": mk_d_m.trend,
        "deploy_p_monthly": mk_d_m.p_value,
        "cfr_trend_monthly": mk_c_m.trend,
        "cfr_p_monthly": mk_c_m.p_value,
    }


def compute_bonus_metrics(
    metrics_csv: Path,
    gold_dir: Path,
    cfr_metrics_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, str]:
    """Calcula todas as métricas da RQ08 para a amostra final."""
    candidate, heur_name = load_candidate(cfr_metrics_path)
    metrics_df = pd.read_csv(metrics_csv)

    rows: list[dict[str, Any]] = []
    for name in metrics_df["full_name"]:
        json_path = gold_dir / f"{name}.json"
        if not json_path.exists():
            continue
        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows.append(process_repository(name, payload, candidate))

    df = pd.DataFrame(rows)
    merged = pd.merge(metrics_df[["full_name", "cfr_a", "stars", "language"]], df, on="full_name", how="inner")

    # CSV 1: Rework rate
    rework_cols = [
        "full_name",
        "stars",
        "language",
        "total_releases_window",
        "corrective_releases_window",
        "rework_rate_window",
        "cfr_a",
        "total_releases_all",
        "corrective_releases_all",
        "rework_rate_all",
    ]
    rework_df = merged[rework_cols].copy()
    rework_df["diff_rework_cfr_a"] = rework_df["rework_rate_window"] - rework_df["cfr_a"]

    # CSV 2: Temporal trends
    trend_cols = [
        "full_name",
        "q1_releases", "q2_releases", "q3_releases", "q4_releases",
        "deploy_trend_quarterly", "deploy_p_quarterly", "deploy_tau_quarterly",
        "q1_rework", "q2_rework", "q3_rework", "q4_rework",
        "rework_trend_quarterly", "rework_p_quarterly", "rework_tau_quarterly",
        "q1_cfr", "q2_cfr", "q3_cfr", "q4_cfr",
        "cfr_trend_quarterly", "cfr_p_quarterly", "cfr_tau_quarterly",
        "deploy_trend_monthly", "deploy_p_monthly",
        "cfr_trend_monthly", "cfr_p_monthly",
    ]
    trend_df = merged[trend_cols].copy()

    # Resumo agregado de tendências
    summary_records = []
    trend_targets = [
        ("Deploy Frequency (Trimestral)", "deploy_trend_quarterly"),
        ("Rework Rate (Trimestral)", "rework_trend_quarterly"),
        ("CFR CI (Trimestral)", "cfr_trend_quarterly"),
        ("Deploy Frequency (Mensal)", "deploy_trend_monthly"),
        ("CFR CI (Mensal)", "cfr_trend_monthly"),
    ]
    n_total = len(merged)
    for label, col in trend_targets:
        counts = merged[col].value_counts()
        inc = int(counts.get("increasing", 0))
        dec = int(counts.get("decreasing", 0))
        neg = int(counts.get("negligible", 0))
        summary_records.append({
            "metric_scale": label,
            "total_repositories": n_total,
            "increasing": inc,
            "pct_increasing": inc / n_total if n_total else 0.0,
            "decreasing": dec,
            "pct_decreasing": dec / n_total if n_total else 0.0,
            "negligible": neg,
            "pct_negligible": neg / n_total if n_total else 0.0,
        })
    summary_df = pd.DataFrame(summary_records)

    return rework_df, trend_df, summary_df, heur_name


def _pct(value: float) -> str:
    return f"{value:.1%}".replace(".", ",")


def _trend_sentence(summary_df: pd.DataFrame) -> str:
    rows = {r["metric_scale"]: r for r in summary_df.to_dict("records")}
    deploy = rows["Deploy Frequency (Mensal)"]
    cfr = rows["CFR CI (Mensal)"]
    return (
        f"a frequência de deploy aumenta em {_pct(deploy['pct_increasing'])} dos repositórios e cai em "
        f"{_pct(deploy['pct_decreasing'])}; o CFR (a) aumenta em {_pct(cfr['pct_increasing'])} e cai em "
        f"{_pct(cfr['pct_decreasing'])}. Os demais não têm tendência significativa a 5%."
    )


def markdown(
    rework_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    heur_name: str,
    n_repos: int,
) -> str:
    """Gera o relatório descritivo e metodológico da RQ08 em Markdown."""
    rw = rework_df["rework_rate_window"].dropna()
    cfr = rework_df["cfr_a"].dropna()
    diff = rework_df["diff_rework_cfr_a"].dropna()

    lines = [
        "# T23 — RQ08 (Bônus): Taxa de Retrabalho e Evolução Temporal",
        "",
        f"Amostra analisada: **{n_repos} repositórios** no período de observação "
        f"({WINDOW_START} a {WINDOW_END}).",
        f"Heurística de release corretiva: a mesma da CFR (b), escolhida no tuning contra o consenso "
        f"(**{heur_name}**). Deploy = release publicada, não-draft e não-pré-release.",
        "",
        "---",
        "",
        "## 1. Taxa de Retrabalho (Rework Rate — DORA 2024)",
        "",
        "A *Rework Rate* mede a proporção de releases corretivas frente ao total de releases entregues. "
        "Diferente da Change Failure Rate clássica de CI (que mede builds com falha no pipeline), a taxa "
        "de retrabalho reflete o percentual de esforço despendido em corrigir defeitos que já chegaram aos usuários.",
        "",
        "### Estatísticas Descritivas na Janela de Observação",
        "",
        "| Métrica | n | Média | Mediana | Desv. Padrão | Q1 (25%) | Q3 (75%) | IQR | Min | Max |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| Rework Rate (janela) | {len(rw)} | {rw.mean():.4f} | {rw.median():.4f} | {rw.std():.4f} | "
        f"{rw.quantile(0.25):.4f} | {rw.quantile(0.75):.4f} | {rw.quantile(0.75)-rw.quantile(0.25):.4f} | "
        f"{rw.min():.4f} | {rw.max():.4f} |",
        f"| Change Failure Rate (CFR a) | {len(cfr)} | {cfr.mean():.4f} | {cfr.median():.4f} | {cfr.std():.4f} | "
        f"{cfr.quantile(0.25):.4f} | {cfr.quantile(0.75):.4f} | {cfr.quantile(0.75)-cfr.quantile(0.25):.4f} | "
        f"{cfr.min():.4f} | {cfr.max():.4f} |",
        f"| Diferença (Rework − CFR) | {len(diff)} | {diff.mean():.4f} | {diff.median():.4f} | {diff.std():.4f} | "
        f"{diff.quantile(0.25):.4f} | {diff.quantile(0.75):.4f} | {diff.quantile(0.75)-diff.quantile(0.25):.4f} | "
        f"{diff.min():.4f} | {diff.max():.4f} |",
        "",
        "### Discussão Conceitual: Rework Rate vs. Change Failure Rate",
        "",
        "1. **Unidade de análise:** O CFR(a) baseia-se em *execuções de workflow de CI*, capturando falhas "
        "imediatas de integração antes ou durante a entrega. Já a Rework Rate baseia-se em *releases completas*, "
        "capturando defeitos pós-entrega que demandaram uma nova versão com foco corretivo.",
        f"2. **Ordem de magnitude observada:** a mediana da Rework Rate ({_pct(rw.median())}) é "
        f"muito superior à do CFR (a) ({_pct(cfr.median())}). A diferença vem da unidade: o CI corrige "
        "falhas de integração antes da release, enquanto boa parte das releases de projetos open-source "
        "é de patch, que a heurística tende a marcar como corretiva (precisão baixa na amostra-ouro).",
        "",
        "---",
        "",
        "## 2. Evolução Temporal (Teste de Mann-Kendall)",
        "",
        "Para cada repositório, foi aplicado o teste não-paramétrico de Mann-Kendall (`pymannkendall`) "
        "para identificar tendências monotônicas significativas ($p < 0{,}05$) em cada direção.",
        "",
        "### Proporções de Repositórios por Tendência",
        "",
        "| Dimensão / Escala | Total | Aumento (pior/mais) | % Aumento | Queda (melhor/menos) | % Queda | Estável / Desprezível | % Estável |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary_df.to_dict("records"):
        lines.append(
            f"| {row['metric_scale']} | {row['total_repositories']} | "
            f"{row['increasing']} | {row['pct_increasing']:.1%} | "
            f"{row['decreasing']} | {row['pct_decreasing']:.1%} | "
            f"{row['negligible']} | {row['pct_negligible']:.1%} |"
        )
    lines += [
        "",
        "### Achado Metodológico: Escala Trimestral vs. Mensal",
        "",
        "- **Limitação assintótica na escala trimestral ($n = 4$):** O teste de Mann-Kendall com apenas "
        "4 observações possui poder estatístico limitado para atingir $p < 0{,}05$ assintótico "
        "(a sequência monótona perfeita atinge $p \\approx 0{,}089$). Portanto, 100% dos repositórios "
        "são classificados como `negligible` (sem tendência estatisticamente comprovável a 5%).",
        f"- **Resolução na escala mensal ($n = 12$):** {_trend_sentence(summary_df)}",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metrics", type=Path, default=DEFAULT_METRICS)
    parser.add_argument("--gold-dir", type=Path, default=DEFAULT_GOLD_DIR)
    parser.add_argument("--cfr-metrics", type=Path, default=DEFAULT_CFR_METRICS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rework_df, trend_df, summary_df, heur_name = compute_bonus_metrics(
        args.metrics,
        args.gold_dir,
        args.cfr_metrics,
    )

    rework_df.to_csv(args.output_dir / "rq08_rework_rate.csv", index=False)
    trend_df.to_csv(args.output_dir / "rq08_temporal_trend.csv", index=False)
    summary_df.to_csv(args.output_dir / "rq08_summary.csv", index=False)

    report = markdown(rework_df, summary_df, heur_name, len(rework_df))
    (args.output_dir / "rq08_bonus.md").write_text(report, encoding="utf-8")

    print(f"T23 RQ08 concluído: {args.output_dir / 'rq08_bonus.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
