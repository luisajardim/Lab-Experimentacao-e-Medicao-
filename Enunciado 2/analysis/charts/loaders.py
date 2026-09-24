from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .config import DATA_PATH, OUTPUT_DIR, QUALITY_METRICS
from .normalization import normalize_trials


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_trials(path: Path = DATA_PATH) -> pd.DataFrame:
    records = _read_json(path)
    if not isinstance(records, list) or not records:
        raise ValueError(f"Nenhum trial válido encontrado em {path}")
    required = {"kata", "treatment", "duration_seconds", "test_attempts", "success", "timeout"}
    missing = required - set(records[0])
    if missing:
        raise ValueError(f"Campos ausentes em {path}: {sorted(missing)}")
    return normalize_trials(pd.DataFrame(records))


def load_quality(path: Path | None = None) -> pd.DataFrame:
    csv_path = path or (OUTPUT_DIR / "code_quality_comparison.csv")
    result = pd.read_csv(csv_path)
    missing = set(QUALITY_METRICS) - set(result.columns)
    if missing:
        raise ValueError(f"Métricas ausentes em {csv_path}: {sorted(missing)}")
    return result


def load_analysis_summary() -> dict[str, Any]:
    summaries = {}
    for name in ("stats_summary.json", "code_quality_summary.json"):
        path = OUTPUT_DIR / name
        if path.exists():
            summaries[name] = _read_json(path)
    return summaries


def load_monte_carlo() -> pd.DataFrame | None:
    path = OUTPUT_DIR / "monte_carlo_simulations.csv"
    return pd.read_csv(path) if path.exists() else None
