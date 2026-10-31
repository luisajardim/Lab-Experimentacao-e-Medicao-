"""Piloto nos dados reais: Pearson × Spearman em subamostras de 30 classes do KC1.

Sorteia 2.000 subamostras de 30 classes (sem reposição) das 145 do KC1, aplica
os dois testes (bicaudais) e conta em quantas cada um rejeita H₀ com α = 0,05.
Serviu de base para a expectativa registrada em `docs/cenario.md`, antes das
simulações. Não é simulação: usa só os dados reais, então não diz se o teste
acertou ou errou, apenas com que frequência cada um "vê" a associação com n = 30.

Uso: `uv run python scripts/piloto.py` → grava `data/real/piloto.json`.

Issue: #77 (T03).
"""

import json

import numpy as np
import pandas as pd
from scipy import stats

from config import DATA_REAL, SEED
from data import FULL_CSV, SAMPLE_SIZE

PILOT_JSON = DATA_REAL / "piloto.json"
N_SUBSAMPLES = 2_000
ALPHA = 0.05


def run_pilot(df: pd.DataFrame, k: int = N_SUBSAMPLES, n: int = SAMPLE_SIZE, seed: int = SEED) -> dict:
    x = df["loc"].to_numpy(dtype=float)
    y = df["defects"].to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    r_values, rho_values = [], []
    reject_pearson = reject_spearman = skipped = 0
    for _ in range(k):
        idx = rng.choice(len(x), size=n, replace=False)
        xs, ys = x[idx], y[idx]
        if np.ptp(ys) == 0:  # subamostra só com zeros: correlação indefinida
            skipped += 1
            continue
        r, p_r = stats.pearsonr(xs, ys)
        rho, p_rho = stats.spearmanr(xs, ys)
        r_values.append(r)
        rho_values.append(rho)
        reject_pearson += p_r < ALPHA
        reject_spearman += p_rho < ALPHA
    return {
        "n_subsamples": k,
        "subsample_size": n,
        "seed": seed,
        "alpha": ALPHA,
        "skipped_all_zero": skipped,
        "reject_rate_pearson": reject_pearson / k,
        "reject_rate_spearman": reject_spearman / k,
        "median_r": float(np.median(r_values)),
        "median_rho": float(np.median(rho_values)),
    }


def main() -> None:
    result = run_pilot(pd.read_csv(FULL_CSV))
    PILOT_JSON.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"{result['n_subsamples']} subamostras de {result['subsample_size']} classes: "
        f"Pearson rejeita {result['reject_rate_pearson']:.1%}, "
        f"Spearman rejeita {result['reject_rate_spearman']:.1%} "
        f"(r mediano={result['median_r']:.2f}, ρ mediano={result['median_rho']:.2f})"
    )


if __name__ == "__main__":
    main()
