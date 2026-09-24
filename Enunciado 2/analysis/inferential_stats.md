# Implementation Plan: `analysis/inferential_stats.py`

## Project Context
- **Repo**: Enunciado 2 (experiment infrastructure for crossover LLM productivity study)
- **Data Source**: `data/trials-log.json` (14 trials from 3 developers × 6 katas)
- **Output Dir**: `analysis/output/` (to be created)
- **Python Env**: `pyproject.toml` + `.venv` with scipy, numpy, pandas, matplotlib

---

## Key Design Decisions (Resolved)

| Decision | Choice |
|----------|--------|
| **Pairing for Wilcoxon** | **Pair by kata**: Match COM_IA vs SEM_IA for same kata across different developers (6 pairs, one per kata). Also run **Mann-Whitney U** on full unpaired samples as sensitivity analysis. |
| **Monte Carlo Method** | **Empirical bootstrap** — resample with replacement from observed `duration_seconds` and `test_attempts` per treatment group. |
| **Visualizations** | **Data output only** — produce `stats_summary.json` + `monte_carlo_simulations.csv`. Plots delegated to `charts_generator.py`. |
| **Dependencies** | `pyproject.toml` with `[project]` and `[build-system]`, managed via `.venv` |

---

## Data Structure (from `trials-log.json`)

```json
{
  "trial_id": "dev_kata_TREATMENT",
  "developer": "string",
  "kata": "string",
  "treatment": "COM_IA | SEM_IA",
  "start_time": "ISO8601",
  "end_time": "ISO8601",
  "duration_seconds": float,
  "test_attempts": int,
  "success": bool,
  "timeout": bool
}
```

**Current data**: 14 trials (6 katas × 2 treatments, but only 1 developer has both treatments; 2 developers have single treatment each).

---

## Algorithm Specification

### 1. Load & Validate Data
- Read `data/trials-log.json`
- Filter to `success == true` trials only (exclude timeouts/failures)
- Verify minimum sample size per group (≥3 per treatment for non-parametric tests)

### 2. Create Paired Samples (by Kata)
- For each of the 6 katas, find the COM_IA trial and SEM_IA trial
- Build paired arrays: `durations_com_ia[kata]`, `durations_sem_ia[kata]`, `attempts_com_ia[kata]`, `attempts_sem_ia[kata]`
- Result: 6 paired observations per metric

### 3. Descriptive Statistics (per treatment)
For each metric (`duration_seconds`, `test_attempts`) and treatment (`COM_IA`, `SEM_IA`):
- Median
- IQR (Q1, Q3)
- Mean ± SD (for reference)
- Sample size (n)
- Min, Max

### 4. Inferential Statistics

#### A. Wilcoxon Signed-Rank Test (Paired, by Kata)
- `scipy.stats.wilcoxon(x=durations_com_ia, y=durations_sem_ia, alternative='two-sided')`
- Report: W statistic, p-value, effect size `r = Z / sqrt(N)`
- Repeat for `test_attempts`

#### B. Mann-Whitney U Test (Unpaired, All Data)
- `scipy.stats.mannwhitneyu(x=all_com_ia, y=all_sem_ia, alternative='two-sided')`
- Report: U statistic, p-value, effect size (Cliff's Delta)

#### C. Effect Size Calculations
- **Rank-biserial correlation (r)** for Wilcoxon: `r = Z / sqrt(N)`
- **Cliff's Delta** for Mann-Whitney: proportion of pairs where COM_IA < SEM_IA minus proportion where COM_IA > SEM_IA

### 5. Monte Carlo Simulation (Empirical Bootstrap)

**Parameters**:
- Iterations: 10,000
- Backlog size: 40 tasks (configurable)
- Resample with replacement from each treatment's empirical distribution

**Procedure per iteration**:
1. Sample 40 `duration_seconds` values with replacement from COM_IA pool → sum = `total_time_com_ia`
2. Sample 40 `duration_seconds` values with replacement from SEM_IA pool → sum = `total_time_sem_ia`
3. Sample 40 `test_attempts` values with replacement from each pool → mean attempts per task
4. Compute:
   - `time_saved_seconds = total_time_sem_ia - total_time_com_ia`
   - `time_saved_pct = time_saved_seconds / total_time_sem_ia * 100`
   - `attempts_reduction = mean_attempts_sem_ia - mean_attempts_com_ia`

**Output per iteration (CSV row)**:
```
iteration,total_time_com_ia,total_time_sem_ia,time_saved_seconds,time_saved_pct,mean_attempts_com_ia,mean_attempts_sem_ia,attempts_reduction
```

**Summary Statistics (from 10k iterations)**:
- Median, Q1, Q3 of `time_saved_pct` and `attempts_reduction`
- 95% CI (2.5th, 97.5th percentiles)
- Probability `time_saved_pct > 0` (proportion of iterations where COM_IA is faster)

### 6. Output Files

#### `analysis/output/stats_summary.json`
```json
{
  "descriptive": {
    "duration_seconds": {
      "COM_IA": { "median": ..., "iqr": [...], "mean": ..., "sd": ..., "n": ..., "min": ..., "max": ... },
      "SEM_IA": { ... }
    },
    "test_attempts": { ... }
  },
  "wilcoxon_paired_by_kata": {
    "duration_seconds": { "W": ..., "p_value": ..., "effect_size_r": ..., "n_pairs": 6 },
    "test_attempts": { "W": ..., "p_value": ..., "effect_size_r": ..., "n_pairs": 6 }
  },
  "mannwhitney_unpaired": {
    "duration_seconds": { "U": ..., "p_value": ..., "cliffs_delta": ..., "n_com_ia": ..., "n_sem_ia": ... },
    "test_attempts": { ... }
  },
  "monte_carlo": {
    "n_iterations": 10000,
    "backlog_size": 40,
    "time_saved_pct": { "median": ..., "q1": ..., "q3": ..., "ci_95": [...], "prob_positive": ... },
    "attempts_reduction": { "median": ..., "q1": ..., "q3": ..., "ci_95": [...], "prob_positive": ... },
    "total_time_com_ia_median": ...,
    "total_time_sem_ia_median": ...
  },
  "metadata": {
    "data_file": "data/trials-log.json",
    "analysis_date": "ISO8601",
    "successful_trials_only": true,
    "n_total_trials": 14,
    "n_com_ia": 7,
    "n_sem_ia": 7
  }
}
```

#### `analysis/output/monte_carlo_simulations.csv`
- 10,001 rows (header + 10k iterations)
- Columns as defined above

---

## File Structure to Create

```
Enunciado 2/
├── pyproject.toml              # Python project config
├── analysis/
│   ├── inferential_stats.py    # Main script (this plan)
│   ├── __init__.py             # Optional, for module imports
│   └── output/                 # Created at runtime
│       ├── stats_summary.json
│       └── monte_carlo_simulations.csv
```

---

## Implementation Steps

### Step 1: Create `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "experiment-analysis"
version = "0.1.0"
description = "Statistical analysis for LLM productivity experiment"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "scipy>=1.10",
    "pandas>=2.0",
    "matplotlib>=3.7"
]

[tool.ruff]
target-version = "py310"
line-length = 100
```

### Step 2: Implement `inferential_stats.py`

**Module Structure**:
```python
#!/usr/bin/env python3
"""Inferential statistics for RQ1 (time) and RQ2 (attempts) with Monte Carlo projection."""

import json
import numpy as np
import pandas as pd
from scipy import stats
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# --- Constants ---
DATA_PATH = Path("data/trials-log.json")
OUTPUT_DIR = Path("analysis/output")
N_ITERATIONS = 10_000
BACKLOG_SIZE = 40
ALPHA = 0.05

# --- Functions ---
def load_and_filter_data(path: Path) -> pd.DataFrame
def create_paired_samples(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
def descriptive_stats(arr: np.ndarray) -> Dict[str, Any]
def wilcoxon_with_effect(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]
def mannwhitney_with_effect(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]
def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float
def run_monte_carlo(com_durations: np.ndarray, sem_durations: np.ndarray,
                    com_attempts: np.ndarray, sem_attempts: np.ndarray,
                    n_iter: int, backlog: int) -> Tuple[pd.DataFrame, Dict[str, Any]]
def main() -> None

if __name__ == "__main__":
    main()
```

### Step 3: Run & Validate
```bash
cd Enunciado\ 2
python -m venv .venv
source .venv/bin/activate
pip install -e .
python analysis/inferential_stats.py
# Verify outputs exist and are valid JSON/CSV
```

---

## Edge Cases & Validation

| Scenario | Handling |
|----------|----------|
| Missing paired kata (one treatment absent) | Skip that kata in Wilcoxon; log warning |
| All trials timeout/fail in one group | Raise informative error |
| `duration_seconds` = 0 (instant) | Keep as-is; bootstrap handles it |
| `test_attempts` = 0 | Should not occur (min 1 attempt on success) |
| Small sample size (< 6 pairs) | Note limitation in output metadata |

---

## Acceptance Criteria

1. ✅ Script runs without errors from `Enunciado 2/` directory
2. ✅ Creates `analysis/output/stats_summary.json` with all required fields
3. ✅ Creates `analysis/output/monte_carlo_simulations.csv` with 10,001 rows
4. ✅ Wilcoxon uses 6 kata-paired samples; Mann-Whitney uses all 7+7 samples
5. ✅ Effect sizes (r and Cliff's Delta) computed correctly
6. ✅ Monte Carlo uses empirical bootstrap (resample with replacement)
7. ✅ Output JSON is valid and contains all specified keys
8. ✅ No visualizations generated (data-only mode)

---

## Out of Scope

- Generating plots (delegated to `charts_generator.py`)
- RQ3 code quality analysis (`code_quality.py`)
- Power analysis / sample size calculation
- Bayesian alternatives

---

## Next Steps After Implementation

1. Run script and verify outputs
2. Review `stats_summary.json` for reasonableness
3. Pass CSV to `charts_generator.py` for visualization
4. Document any data limitations in final report