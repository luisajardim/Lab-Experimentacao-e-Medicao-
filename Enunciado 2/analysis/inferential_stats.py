#!/usr/bin/env python3
"""Inferential statistics for RQ1 (time) and RQ2 (attempts) with Monte Carlo projection."""

import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats

DATA_PATH = Path("data/trials-log.json")
OUTPUT_DIR = Path("analysis/output")
N_ITERATIONS = 10_000
BACKLOG_SIZE = 40
ALPHA = 0.05

KATAS = [
    "kata-01-fizzbuzz",
    "kata-02-roman-numerals",
    "kata-03-string-calculator",
    "kata-04-bowling-game",
    "kata-05-isbn-10-validator",
    "kata-06-pagination",
]


def load_and_filter_data(path: Path) -> pd.DataFrame:
    """Load trial log and filter to successful trials only."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df = df[df["success"] == True].copy()
    df = df[~df["timeout"]].copy()

    if df.empty:
        raise ValueError("No successful trials found in data")

    return df


def create_paired_samples(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Create paired samples by kata: COM_IA vs SEM_IA for each kata."""
    com_durations = []
    sem_durations = []
    com_attempts = []
    sem_attempts = []

    for kata in KATAS:
        com_row = df[(df["kata"] == kata) & (df["treatment"] == "COM_IA")]
        sem_row = df[(df["kata"] == kata) & (df["treatment"] == "SEM_IA")]

        if len(com_row) == 1 and len(sem_row) == 1:
            com_durations.append(com_row.iloc[0]["duration_seconds"])
            sem_durations.append(sem_row.iloc[0]["duration_seconds"])
            com_attempts.append(com_row.iloc[0]["test_attempts"])
            sem_attempts.append(sem_row.iloc[0]["test_attempts"])
        else:
            warnings.warn(
                f"Kata {kata}: COM_IA={len(com_row)}, SEM_IA={len(sem_row)}. Skipping from paired analysis."
            )

    return (
        np.array(com_durations, dtype=float),
        np.array(sem_durations, dtype=float),
        np.array(com_attempts, dtype=int),
        np.array(sem_attempts, dtype=int),
    )


def descriptive_stats(arr: np.ndarray) -> Dict[str, Any]:
    """Compute descriptive statistics for an array."""
    if len(arr) == 0:
        return {
            "median": None,
            "q1": None,
            "q3": None,
            "iqr": None,
            "mean": None,
            "sd": None,
            "n": 0,
            "min": None,
            "max": None,
        }

    q1, median, q3 = np.percentile(arr, [25, 50, 75])
    return {
        "median": float(median),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(q3 - q1),
        "mean": float(np.mean(arr)),
        "sd": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
        "n": int(len(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def wilcoxon_with_effect(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """Wilcoxon signed-rank test with effect size r = Z / sqrt(N)."""
    if len(x) < 3 or len(y) < 3:
        return {
            "W": None,
            "p_value": None,
            "effect_size_r": None,
            "n_pairs": int(len(x)),
            "note": "Insufficient pairs for Wilcoxon test (need >= 3)",
        }

    try:
        result = stats.wilcoxon(x, y, alternative="two-sided", zero_method="wilcox", correction=True)
        W = float(result.statistic)
        p_value = float(result.pvalue)

        N = len(x)
        Z = stats.norm.ppf(1 - p_value / 2) if p_value > 0 else 0
        if result.statistic < N * (N + 1) / 4:
            Z = -abs(Z)
        else:
            Z = abs(Z)

        effect_size_r = float(Z / np.sqrt(N)) if N > 0 else 0.0

        return {
            "W": W,
            "p_value": p_value,
            "effect_size_r": effect_size_r,
            "n_pairs": int(N),
        }
    except Exception as e:
        return {
            "W": None,
            "p_value": None,
            "effect_size_r": None,
            "n_pairs": int(len(x)),
            "error": str(e),
        }


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    """Calculate Cliff's Delta effect size for Mann-Whitney U."""
    if len(x) == 0 or len(y) == 0:
        return 0.0

    n_x, n_y = len(x), len(y)
    greater = 0
    less = 0

    for xi in x:
        for yj in y:
            if xi > yj:
                greater += 1
            elif xi < yj:
                less += 1

    return (greater - less) / (n_x * n_y)


def mannwhitney_with_effect(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """Mann-Whitney U test with Cliff's Delta effect size."""
    if len(x) == 0 or len(y) == 0:
        return {
            "U": None,
            "p_value": None,
            "cliffs_delta": None,
            "n_com_ia": int(len(x)),
            "n_sem_ia": int(len(y)),
            "note": "Empty group(s)",
        }

    try:
        result = stats.mannwhitneyu(x, y, alternative="two-sided")
        U = float(result.statistic)
        p_value = float(result.pvalue)
        delta = cliffs_delta(x, y)

        return {
            "U": U,
            "p_value": p_value,
            "cliffs_delta": float(delta),
            "n_com_ia": int(len(x)),
            "n_sem_ia": int(len(y)),
        }
    except Exception as e:
        return {
            "U": None,
            "p_value": None,
            "cliffs_delta": None,
            "n_com_ia": int(len(x)),
            "n_sem_ia": int(len(y)),
            "error": str(e),
        }


def run_monte_carlo(
    com_durations: np.ndarray,
    sem_durations: np.ndarray,
    com_attempts: np.ndarray,
    sem_attempts: np.ndarray,
    n_iter: int,
    backlog: int,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Run empirical bootstrap Monte Carlo simulation."""
    if len(com_durations) == 0 or len(sem_durations) == 0:
        raise ValueError("Empty duration arrays for Monte Carlo")

    rng = np.random.default_rng()
    results = []

    for i in range(n_iter):
        com_dur_sample = rng.choice(com_durations, size=backlog, replace=True)
        sem_dur_sample = rng.choice(sem_durations, size=backlog, replace=True)

        com_att_sample = rng.choice(com_attempts, size=backlog, replace=True)
        sem_att_sample = rng.choice(sem_attempts, size=backlog, replace=True)

        total_com = float(np.sum(com_dur_sample))
        total_sem = float(np.sum(sem_dur_sample))
        time_saved = total_sem - total_com
        time_saved_pct = (time_saved / total_sem * 100) if total_sem > 0 else 0.0

        mean_att_com = float(np.mean(com_att_sample))
        mean_att_sem = float(np.mean(sem_att_sample))
        att_reduction = mean_att_sem - mean_att_com

        results.append({
            "iteration": i,
            "total_time_com_ia": total_com,
            "total_time_sem_ia": total_sem,
            "time_saved_seconds": time_saved,
            "time_saved_pct": time_saved_pct,
            "mean_attempts_com_ia": mean_att_com,
            "mean_attempts_sem_ia": mean_att_sem,
            "attempts_reduction": att_reduction,
        })

    df_results = pd.DataFrame(results)

    time_saved_pct_vals = df_results["time_saved_pct"].values
    att_reduction_vals = df_results["attempts_reduction"].values

    summary = {
        "n_iterations": n_iter,
        "backlog_size": backlog,
        "time_saved_pct": {
            "median": float(np.median(time_saved_pct_vals)),
            "q1": float(np.percentile(time_saved_pct_vals, 25)),
            "q3": float(np.percentile(time_saved_pct_vals, 75)),
            "ci_95": [
                float(np.percentile(time_saved_pct_vals, 2.5)),
                float(np.percentile(time_saved_pct_vals, 97.5)),
            ],
            "prob_positive": float(np.mean(time_saved_pct_vals > 0)),
        },
        "attempts_reduction": {
            "median": float(np.median(att_reduction_vals)),
            "q1": float(np.percentile(att_reduction_vals, 25)),
            "q3": float(np.percentile(att_reduction_vals, 75)),
            "ci_95": [
                float(np.percentile(att_reduction_vals, 2.5)),
                float(np.percentile(att_reduction_vals, 97.5)),
            ],
            "prob_positive": float(np.mean(att_reduction_vals > 0)),
        },
        "total_time_com_ia_median": float(np.median(df_results["total_time_com_ia"])),
        "total_time_sem_ia_median": float(np.median(df_results["total_time_sem_ia"])),
    }

    return df_results, summary


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_filter_data(DATA_PATH)

    com_df = df[df["treatment"] == "COM_IA"]
    sem_df = df[df["treatment"] == "SEM_IA"]

    com_durations_all = com_df["duration_seconds"].values
    sem_durations_all = sem_df["duration_seconds"].values
    com_attempts_all = com_df["test_attempts"].values
    sem_attempts_all = sem_df["test_attempts"].values

    com_durations_paired, sem_durations_paired, com_attempts_paired, sem_attempts_paired = create_paired_samples(df)

    desc_duration = {
        "COM_IA": descriptive_stats(com_durations_all),
        "SEM_IA": descriptive_stats(sem_durations_all),
    }
    desc_attempts = {
        "COM_IA": descriptive_stats(com_attempts_all),
        "SEM_IA": descriptive_stats(sem_attempts_all),
    }

    wilcoxon_duration = wilcoxon_with_effect(com_durations_paired, sem_durations_paired)
    wilcoxon_attempts = wilcoxon_with_effect(com_attempts_paired, sem_attempts_paired)

    mw_duration = mannwhitney_with_effect(com_durations_all, sem_durations_all)
    mw_attempts = mannwhitney_with_effect(com_attempts_all, sem_attempts_all)

    mc_df, mc_summary = run_monte_carlo(
        com_durations_all,
        sem_durations_all,
        com_attempts_all,
        sem_attempts_all,
        N_ITERATIONS,
        BACKLOG_SIZE,
    )

    summary = {
        "descriptive": {
            "duration_seconds": desc_duration,
            "test_attempts": desc_attempts,
        },
        "wilcoxon_paired_by_kata": {
            "duration_seconds": wilcoxon_duration,
            "test_attempts": wilcoxon_attempts,
        },
        "mannwhitney_unpaired": {
            "duration_seconds": mw_duration,
            "test_attempts": mw_attempts,
        },
        "monte_carlo": mc_summary,
        "metadata": {
            "data_file": str(DATA_PATH),
            "analysis_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "successful_trials_only": True,
            "n_total_trials": int(len(df)),
            "n_com_ia": int(len(com_df)),
            "n_sem_ia": int(len(sem_df)),
            "n_paired_katas": int(len(com_durations_paired)),
        },
    }

    summary_path = OUTPUT_DIR / "stats_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    mc_path = OUTPUT_DIR / "monte_carlo_simulations.csv"
    mc_df.to_csv(mc_path, index=False)

    print(f"Analysis complete. Outputs written to {OUTPUT_DIR}")
    print(f"  - {summary_path}")
    print(f"  - {mc_path} ({len(mc_df)} rows)")


if __name__ == "__main__":
    main()