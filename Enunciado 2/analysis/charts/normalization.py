from __future__ import annotations

import pandas as pd

from .config import ALIASES, TREATMENTS


def canonical_kata(value: str) -> str:
    return ALIASES.get(value, value)


def normalize_trials(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["kata_key"] = result["kata"].map(canonical_kata)
    result["treatment"] = result["treatment"].str.upper()
    result["duration_minutes"] = result["duration_seconds"] / 60
    result["duration_plot_minutes"] = result["duration_minutes"].clip(upper=25)
    result["status"] = result.apply(
        lambda row: "Timeout" if bool(row["timeout"]) else ("Green" if bool(row["success"]) else "Falhou"),
        axis=1,
    )
    return result


def pair_by_kata(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    usable = df[df["treatment"].isin(TREATMENTS)].copy()
    pivot = usable.pivot_table(index="kata_key", columns="treatment", values=value_column, aggfunc="first")
    pivot = pivot.reindex(columns=TREATMENTS).dropna(how="all")
    pivot["difference_com_minus_sem"] = pivot.get("COM_IA") - pivot.get("SEM_IA")
    return pivot.reset_index()


def join_quality_with_trials(quality: pd.DataFrame, trials: pd.DataFrame) -> pd.DataFrame:
    status = trials[["developer", "kata_key", "treatment", "success", "timeout"]].drop_duplicates()
    return quality.merge(status, on=["developer", "kata_key", "treatment"], how="left")
