from __future__ import annotations

import pandas as pd


def positive_improvement(baseline: pd.Series, treatment: pd.Series) -> pd.Series:
    """Return only favorable reductions; non-improvements are represented as zero."""
    return (baseline - treatment).clip(lower=0)


def improvement_by_kata(
    data: pd.DataFrame,
    value_column: str,
    baseline: str = "SEM_IA",
    treatment: str = "COM_IA",
) -> pd.DataFrame:
    pairs = data.pivot_table(
        index="kata_key",
        columns="treatment",
        values=value_column,
        aggfunc="first",
    ).reindex(columns=[baseline, treatment]).dropna()
    pairs["improvement"] = positive_improvement(pairs[baseline], pairs[treatment])
    pairs["raw_difference"] = pairs[baseline] - pairs[treatment]
    return pairs.reset_index()
