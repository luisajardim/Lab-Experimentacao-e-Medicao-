#!/usr/bin/env python3
"""Consolidate static code-quality metrics for RQ3."""

import csv
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy import stats


BASE_DIR = Path(__file__).resolve().parents[1]
TRIALS_DIR = BASE_DIR / "trials"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"
CSV_PATH = OUTPUT_DIR / "code_quality_comparison.csv"
SUMMARY_JSON_PATH = OUTPUT_DIR / "code_quality_summary.json"
SUMMARY_MD_PATH = OUTPUT_DIR / "code_quality_summary.md"
ALPHA = 0.05

METRICS = (
    "loc",
    "cyclomatic_complexity",
    "halstead_volume",
    "halstead_difficulty",
    "halstead_effort",
    "duplication_percentage",
)
TREATMENTS = ("COM_IA", "SEM_IA")
ALIASES = {
    "kata-05-isbn-10-calculator": "kata-05-isbn-10-validator",
    "kata-06-pagination": "kata-06-array-chunking-pagination",
}


class DataError(ValueError):
    """Raised when a metrics artifact cannot be analyzed."""


def canonical_kata(kata: str) -> str:
    """Return the grouping key while preserving original names in the CSV."""
    return ALIASES.get(kata, kata)


def parse_trial_directory(path: Path) -> Tuple[str, str, str]:
    """Extract developer, kata and treatment from a trial directory name."""
    name = path.name
    match = re.match(r"^(?P<kata>.+)-(?P<treatment>com-ia|sem-ia)$", name, re.IGNORECASE)
    if not match:
        raise DataError(f"Unknown treatment suffix in trial directory: {path}")

    treatment = match.group("treatment").upper().replace("-", "_")
    return path.parent.name, match.group("kata"), treatment


def _number(value: Any, field: str, source: Path) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise DataError(f"{source}: metric '{field}' must be numeric")
    if not math.isfinite(float(value)):
        raise DataError(f"{source}: metric '{field}' must be finite")
    return float(value)


def read_artifact(path: Path) -> Dict[str, Any]:
    developer, kata, treatment = parse_trial_directory(path.parent)
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    try:
        metrics = payload["metrics"]
        halstead = metrics["halstead"]
        duplication = metrics["duplication"]
        record = {
            "trial_id": str(payload["trial_id"]),
            "developer": developer,
            "kata": kata,
            "kata_key": canonical_kata(kata),
            "treatment": treatment,
            "source": str(path.relative_to(BASE_DIR)),
            "loc": _number(metrics["loc"], "loc", path),
            "cyclomatic_complexity": _number(
                metrics["cyclomatic_complexity"], "cyclomatic_complexity", path
            ),
            "halstead_volume": _number(halstead["volume"], "halstead.volume", path),
            "halstead_difficulty": _number(
                halstead["difficulty"], "halstead.difficulty", path
            ),
            "halstead_effort": _number(halstead["effort"], "halstead.effort", path),
            "duplication_percentage": _number(
                duplication["percentage"], "duplication.percentage", path
            ),
        }
    except (KeyError, TypeError) as error:
        raise DataError(f"{path}: incomplete metrics schema ({error})") from error

    return record


def discover_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    accepted: List[Dict[str, Any]] = []
    excluded: List[Dict[str, str]] = []
    for path in sorted(TRIALS_DIR.glob("*/*/metrics.json")):
        try:
            record = read_artifact(path)
        except (DataError, json.JSONDecodeError) as error:
            excluded.append({"source": str(path.relative_to(BASE_DIR)), "reason": str(error)})
            continue
        accepted.append(record)
    if not accepted:
        raise DataError("No valid metrics artifacts remain after filtering")
    return accepted, excluded


def descriptive(values: Sequence[float]) -> Dict[str, Any]:
    if not values:
        return {"n": 0, "mean": None, "median": None, "sd": None, "q1": None, "q3": None,
                "iqr": None, "min": None, "max": None}
    array = np.asarray(values, dtype=float)
    q1, median, q3 = np.percentile(array, [25, 50, 75])
    return {
        "n": int(array.size),
        "mean": float(np.mean(array)),
        "median": float(median),
        "sd": float(np.std(array, ddof=1)) if array.size > 1 else 0.0,
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
    }


def cliffs_delta(com: Sequence[float], sem: Sequence[float]) -> Optional[float]:
    if not com or not sem:
        return None
    comparisons = [np.sign(x - y) for x in com for y in sem]
    return float(np.mean(comparisons))


def wilcoxon_result(com: Sequence[float], sem: Sequence[float]) -> Dict[str, Any]:
    result: Dict[str, Any] = {"n_pairs": len(com), "W": None, "p_value": None, "effect_size_r": None}
    if len(com) < 3:
        result["note"] = "Insufficient pairs for Wilcoxon test (need >= 3)"
        return result
    differences = np.asarray(com, dtype=float) - np.asarray(sem, dtype=float)
    if np.allclose(differences, 0):
        result.update({"W": 0.0, "p_value": 1.0, "effect_size_r": 0.0})
        result["note"] = "All paired differences are zero"
        return result
    try:
        test = stats.wilcoxon(com, sem, alternative="two-sided", zero_method="wilcox")
        p_value = float(test.pvalue)
        z = stats.norm.ppf(1 - p_value / 2) if p_value > 0 else 0.0
        if np.median(differences) < 0:
            z = -abs(z)
        result.update({"W": float(test.statistic), "p_value": p_value,
                       "effect_size_r": float(z / math.sqrt(len(com)))})
    except ValueError as error:
        result["note"] = str(error)
    return result


def mannwhitney_result(com: Sequence[float], sem: Sequence[float]) -> Dict[str, Any]:
    result: Dict[str, Any] = {
        "n_com_ia": len(com), "n_sem_ia": len(sem), "U": None,
        "p_value": None, "cliffs_delta": cliffs_delta(com, sem),
    }
    if not com or not sem:
        result["note"] = "Empty treatment group"
        return result
    test = stats.mannwhitneyu(com, sem, alternative="two-sided")
    result.update({"U": float(test.statistic), "p_value": float(test.pvalue)})
    return result


def paired_records(records: Sequence[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    pairs: List[Dict[str, Any]] = []
    skipped: List[Dict[str, str]] = []
    for kata in sorted({record["kata_key"] for record in records}):
        by_treatment = {
            treatment: [r for r in records if r["kata_key"] == kata and r["treatment"] == treatment]
            for treatment in TREATMENTS
        }
        if all(len(by_treatment[treatment]) == 1 for treatment in TREATMENTS):
            pairs.append({
                "kata": kata,
                "COM_IA": by_treatment["COM_IA"][0]["source"],
                "SEM_IA": by_treatment["SEM_IA"][0]["source"],
                "metrics": {
                    metric: {
                        "COM_IA": by_treatment["COM_IA"][0][metric],
                        "SEM_IA": by_treatment["SEM_IA"][0][metric],
                        "difference_com_minus_sem": (
                            by_treatment["COM_IA"][0][metric] - by_treatment["SEM_IA"][0][metric]
                        ),
                    }
                    for metric in METRICS
                },
            })
        else:
            skipped.append({
                "kata": kata,
                "reason": f"COM_IA={len(by_treatment['COM_IA'])}, SEM_IA={len(by_treatment['SEM_IA'])}",
            })
    return pairs, skipped


def write_csv(records: Sequence[Dict[str, Any]]) -> None:
    fields = ["trial_id", "developer", "kata", "kata_key", "treatment", "source", *METRICS]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({field: record[field] for field in fields} for record in records)


def build_summary(records: Sequence[Dict[str, Any]], excluded: Sequence[Dict[str, str]]) -> Dict[str, Any]:
    pairs, skipped = paired_records(records)
    descriptive_by_treatment: Dict[str, Dict[str, Any]] = {}
    for treatment in TREATMENTS:
        group = [record for record in records if record["treatment"] == treatment]
        descriptive_by_treatment[treatment] = {
            metric: descriptive([record[metric] for record in group]) for metric in METRICS
        }

    by_kata: Dict[str, Any] = {}
    for kata in sorted({record["kata_key"] for record in records}):
        by_kata[kata] = {
            treatment: {
                metric: descriptive([
                    record[metric] for record in records
                    if record["kata_key"] == kata and record["treatment"] == treatment
                ]) for metric in METRICS
            }
            for treatment in TREATMENTS
        }

    inferential: Dict[str, Any] = {}
    for metric in METRICS:
        com = [record[metric] for record in records if record["treatment"] == "COM_IA"]
        sem = [record[metric] for record in records if record["treatment"] == "SEM_IA"]
        paired_com = [pair["metrics"][metric]["COM_IA"] for pair in pairs]
        paired_sem = [pair["metrics"][metric]["SEM_IA"] for pair in pairs]
        inferential[metric] = {
            "wilcoxon_paired_by_kata": wilcoxon_result(paired_com, paired_sem),
            "mannwhitney_unpaired": mannwhitney_result(com, sem),
        }

    return {
        "metadata": {
            "analysis_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "data_directory": str(TRIALS_DIR.relative_to(BASE_DIR)),
            "alpha": ALPHA,
            "filter_policy": "include every valid metrics.json; exclude only unreadable or invalid-schema artifacts",
            "n_discovered": len(records) + len(excluded),
            "n_included": len(records),
            "n_excluded": len(excluded),
            "n_com_ia": sum(record["treatment"] == "COM_IA" for record in records),
            "n_sem_ia": sum(record["treatment"] == "SEM_IA" for record in records),
            "n_paired_katas": len(pairs),
            "metrics": list(METRICS),
            "aliases": ALIASES,
            "limitations": [
                "Pairing is by kata, not by developer.",
                "The sample is small; p-values should be interpreted alongside effect sizes.",
                "Maintainability Index is not available in the metrics runner.",
            ],
        },
        "descriptive_by_treatment": descriptive_by_treatment,
        "descriptive_by_kata": by_kata,
        "paired_katas": pairs,
        "skipped_katas": skipped,
        "inferential": inferential,
        "excluded_artifacts": list(excluded),
    }


def display_name(metric: str) -> str:
    return {
        "loc": "LOC",
        "cyclomatic_complexity": "Complexidade ciclomática",
        "halstead_volume": "Halstead volume",
        "halstead_difficulty": "Halstead difficulty",
        "halstead_effort": "Halstead effort",
        "duplication_percentage": "Duplicação (%)",
    }[metric]


def write_markdown(summary: Dict[str, Any]) -> None:
    descriptive_data = summary["descriptive_by_treatment"]
    inferential_data = summary["inferential"]
    lines = [
        "# Consolidação de Qualidade de Código (RQ3)",
        "",
        "A análise inclui os artefatos `metrics.json` com status válido no log de trials. "
        f"Foram incluídos {summary['metadata']['n_included']} de "
        f"{summary['metadata']['n_discovered']} artefatos; "
        f"{summary['metadata']['n_excluded']} foram excluídos.",
        "",
        "## Estatísticas descritivas",
        "",
        "| Métrica | COM_IA (mediana; média +/- DP) | SEM_IA (mediana; média +/- DP) |",
        "|---|---:|---:|",
    ]
    for metric in METRICS:
        values = []
        for treatment in TREATMENTS:
            item = descriptive_data[treatment][metric]
            values.append(
                f"{item['median']:.2f}; {item['mean']:.2f} +/- {item['sd']:.2f} (n={item['n']})"
            )
        lines.append(f"| {display_name(metric)} | {values[0]} | {values[1]} |")

    lines.extend([
        "",
        "## Testes inferenciais",
        "",
        "| Métrica | Wilcoxon (p; r) | Mann-Whitney (p; Cliff's delta) |",
        "|---|---:|---:|",
    ])
    for metric in METRICS:
        wilcoxon = inferential_data[metric]["wilcoxon_paired_by_kata"]
        mannwhitney = inferential_data[metric]["mannwhitney_unpaired"]
        wilcoxon_text = (
            f"{wilcoxon['p_value']:.4f}; {wilcoxon['effect_size_r']:.2f}"
            if wilcoxon["p_value"] is not None else f"indisponível ({wilcoxon.get('note', '')})"
        )
        mw_text = (
            f"{mannwhitney['p_value']:.4f}; {mannwhitney['cliffs_delta']:.2f}"
            if mannwhitney["p_value"] is not None else "indisponível"
        )
        lines.append(f"| {display_name(metric)} | {wilcoxon_text} | {mw_text} |")

    lines.extend([
        "",
        "## Texto para resultados",
        "",
        f"Foram analisados {summary['metadata']['n_included']} artefatos de qualidade, "
        f"com {summary['metadata']['n_paired_katas']} katas pareados entre COM_IA e SEM_IA. "
        "As diferenças foram avaliadas pelo teste de Wilcoxon pareado por kata e, "
        "como análise complementar, pelo teste de Mann-Whitney U sobre as distribuições agregadas. "
        "Os resultados devem ser interpretados com cautela devido ao tamanho amostral reduzido; "
        "o sinal de Cliff's delta positivo indica valores maiores em COM_IA.",
        "",
        "## Exclusões",
        "",
    ])
    if summary["excluded_artifacts"]:
        lines.extend(f"- `{item['source']}`: {item['reason']}" for item in summary["excluded_artifacts"])
    else:
        lines.append("Nenhum artefato foi excluído.")
    SUMMARY_MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records, excluded = discover_records()
    records = sorted(records, key=lambda record: (record["kata_key"], record["treatment"], record["source"]))
    write_csv(records)
    summary = build_summary(records, excluded)
    SUMMARY_JSON_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(summary)
    print(f"Analysis complete: {len(records)} included, {len(excluded)} excluded")
    print(f"  - {CSV_PATH}")
    print(f"  - {SUMMARY_JSON_PATH}")
    print(f"  - {SUMMARY_MD_PATH}")


if __name__ == "__main__":
    main()