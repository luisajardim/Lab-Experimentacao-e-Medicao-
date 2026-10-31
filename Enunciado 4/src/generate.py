"""Gerador de dados simulados.

Gera, de forma vetorizada, conjuntos de dados para as quatro situações:
S-base (normal bivariada padronizada com correlação ρ, n = 30), S-real (cópula gaussiana com
correlação latente ρ → LOC Gamma e defeitos binomial negativa, n = 30),
S-real-n10 (mesmo gerador da S-real com n = 10) e S-outlier (S-real em que cada
classe tem chance de 1 em 145, a proporção do KC1, de ser trocada por uma classe
extrema, acima do percentil 99 em LOC e em defeitos).

Na S-real, o LOC é arredondado para cima (inteiro ≥ 1, como nos dados reais) e
os defeitos já saem inteiros. Com ρ = 0, X e Y são independentes nos geradores
base e real; na S-outlier, as classes não contaminadas também são independentes,
e qualquer associação com ρ = 0 vem só das classes extremas.

Issue: #78 (T04).
"""

import json
from functools import cache

import numpy as np
from scipy import stats

from config import OUTLIER_RATE, OUTLIER_TAIL, SITUATIONS
from fit import PARAMS_JSON

GENERATORS = ("base", "real", "outlier")


@cache
def load_params() -> dict:
    return json.loads(PARAMS_JSON.read_text())


def latent_normal(rho: float, n: int, reps: int, rng: np.random.Generator):
    """Pares (Z₁, Z₂) normais padrão com correlação ρ, formato [reps, n] cada."""
    if not -1 < rho < 1:
        raise ValueError(f"ρ precisa estar em (-1, 1); recebido {rho}")
    e1, e2 = rng.standard_normal((2, reps, n))
    return e1, rho * e1 + np.sqrt(1 - rho**2) * e2


def to_kc1_marginals(z1: np.ndarray, z2: np.ndarray, params: dict | None = None):
    """Cópula gaussiana: leva (Z₁, Z₂) para LOC ~ Gamma e defeitos ~ BinNeg."""
    params = params or load_params()
    loc, dfc = params["loc"], params["defects"]
    x = stats.gamma.ppf(stats.norm.cdf(z1), loc["shape"], scale=loc["scale"])
    x = np.maximum(np.ceil(x), 1)
    y = stats.nbinom.ppf(stats.norm.cdf(z2), dfc["r"], dfc["p"])
    return x, y


def contaminate(x: np.ndarray, y: np.ndarray, rng: np.random.Generator,
                rate: float = OUTLIER_RATE, tail: float = OUTLIER_TAIL, params: dict | None = None):
    """Troca cada classe, com probabilidade `rate`, por uma classe extrema.

    A classe extrema tem LOC e defeitos sorteados acima do quantil `tail` das
    distribuições ajustadas (sorteios independentes nas duas caudas).
    Modifica e devolve `x` e `y`.
    """
    params = params or load_params()
    loc, dfc = params["loc"], params["defects"]
    mask = rng.uniform(size=x.shape) < rate
    k = int(mask.sum())
    x[mask] = np.ceil(stats.gamma.ppf(rng.uniform(tail, 1, k), loc["shape"], scale=loc["scale"]))
    y[mask] = stats.nbinom.ppf(rng.uniform(tail, 1, k), dfc["r"], dfc["p"])
    return x, y


def generate(situation: str, rho: float, n: int | None = None, reps: int = 1,
             rng: np.random.Generator | None = None):
    """Gera `reps` conjuntos de dados de tamanho `n` para uma situação.

    `situation` pode ser uma situação de `config.SITUATIONS` (ex.: "S-real-n10",
    que já define n) ou um gerador ("base", "real" ou "outlier", exigindo `n`).
    Devolve `(x, y)`, dois arrays float de formato [reps, n].
    """
    if situation in SITUATIONS:
        kind, default_n = SITUATIONS[situation]
        n = default_n if n is None else n
    elif situation in GENERATORS:
        kind = situation
        if n is None:
            raise ValueError(f"Informe n para o gerador '{situation}'")
    else:
        raise ValueError(f"Situação desconhecida: {situation}")
    if rng is None:
        raise ValueError("Passe um numpy.random.Generator criado a partir de config.SEED")

    z1, z2 = latent_normal(rho, n, reps, rng)
    if kind == "base":
        return z1, z2
    x, y = to_kc1_marginals(z1, z2)
    if kind == "outlier":
        x, y = contaminate(x, y, rng)
    return x, y
