"""Ajuste dos parâmetros da simulação a partir dos dados reais.

Ajusta, no KC1 inteiro, uma Gamma para o LOC (forma e escala, máxima
verossimilhança) e uma binomial negativa para o nº de defeitos (média e
dispersão, máxima verossimilhança), e salva os parâmetros em
`data/real/params.json`, usados pelo gerador de dados simulados. A situação base
é uma normal bivariada padronizada (média 0, desvio 1).

Uso: `uv run python -m fit`

Issue: #77 (T03).
"""

import json

import numpy as np
import pandas as pd
from scipy import optimize, stats

from config import DATA_REAL
from data import FULL_CSV

PARAMS_JSON = DATA_REAL / "params.json"
QUANTILES = [0.10, 0.25, 0.50, 0.75, 0.90, 0.99]


def fit_gamma(x: np.ndarray) -> dict:
    """Gamma com locação 0, por máxima verossimilhança."""
    shape, _, scale = stats.gamma.fit(x, floc=0)
    dist = stats.gamma(shape, scale=scale)
    return {
        "dist": "gamma",
        "method": "MLE",
        "shape": float(shape),
        "scale": float(scale),
        "ks_pvalue": float(stats.kstest(x, dist.cdf).pvalue),
        "quantiles_fit": dist.ppf(QUANTILES).round(1).tolist(),
        "quantiles_obs": np.quantile(x, QUANTILES).round(1).tolist(),
        "mean_fit": float(dist.mean()),
    }


def fit_nbinom(y: np.ndarray) -> dict:
    """Binomial negativa (dispersão r, média μ) por máxima verossimilhança.

    No SciPy: `nbinom(n=r, p=r / (r + μ))`; variância = μ + μ²/r.
    """

    def nll(log_par):
        r, mean = np.exp(log_par)
        return -stats.nbinom.logpmf(y, r, r / (r + mean)).sum()

    start = np.log([0.5, y.mean()])
    res = optimize.minimize(nll, start, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-8})
    if not res.success:
        raise RuntimeError(f"Ajuste da binomial negativa não convergiu: {res.message}")
    r, mean = (float(v) for v in np.exp(res.x))
    p = r / (r + mean)
    return {
        "dist": "nbinom",
        "method": "MLE",
        "r": r,
        "mean": mean,
        "p": p,
        "p_zero_fit": float(stats.nbinom.pmf(0, r, p)),
        "p_zero_obs": float(np.mean(y == 0)),
        "p_ge20_fit": float(stats.nbinom.sf(19, r, p)),
        "p_ge20_obs": float(np.mean(y >= 20)),
    }


def observed_summary(x: np.ndarray, y: np.ndarray) -> dict:
    """Estatísticas descritivas e correlações observadas no KC1 inteiro."""
    normal_scores = [stats.norm.ppf(stats.rankdata(v) / (len(v) + 1)) for v in (x, y)]
    return {
        "n": int(len(x)),
        "loc_median": float(np.median(x)),
        "loc_skew": float(stats.skew(x)),
        "defects_median": float(np.median(y)),
        "defects_skew": float(stats.skew(y)),
        "defects_zero_share": float(np.mean(y == 0)),
        "pearson_r": float(stats.pearsonr(x, y)[0]),
        "spearman_rho": float(stats.spearmanr(x, y)[0]),
        "normal_scores_rho": float(np.corrcoef(*normal_scores)[0, 1]),
    }


def fit_params(df: pd.DataFrame) -> dict:
    x = df["loc"].to_numpy(dtype=float)
    y = df["defects"].to_numpy()
    return {
        "source": "NASA KC1 por classe (OpenML 1070), 145 classes — ver docs/fonte_dados.md",
        "base": {"dist": "normal bivariada padronizada", "mean": [0.0, 0.0], "sd": [1.0, 1.0]},
        "loc": fit_gamma(x),
        "defects": fit_nbinom(y),
        "observed": observed_summary(x, y),
    }


def main() -> None:
    params = fit_params(pd.read_csv(FULL_CSV))
    PARAMS_JSON.write_text(json.dumps(params, indent=2, ensure_ascii=False) + "\n")
    loc, dfc = params["loc"], params["defects"]
    print(f"LOC ~ Gamma(forma={loc['shape']:.3f}, escala={loc['scale']:.1f}) | KS p={loc['ks_pvalue']:.3f}")
    print(f"Defeitos ~ BinNeg(r={dfc['r']:.3f}, média={dfc['mean']:.2f}) | "
          f"P(0) ajustado={dfc['p_zero_fit']:.1%} vs observado={dfc['p_zero_obs']:.1%}")
    print(f"Salvo em {PARAMS_JSON.relative_to(DATA_REAL.parents[1])}")


if __name__ == "__main__":
    main()
