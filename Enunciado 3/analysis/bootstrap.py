"""Intervalos de confiança BCa reutilizáveis nas análises.

O bootstrap é feito sobre repositórios, a unidade de análise do laboratório.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable, Iterable
from dataclasses import dataclass

import numpy as np
from scipy.stats import DegenerateDataWarning, bootstrap


@dataclass(frozen=True)
class BCAInterval:
    """Intervalo BCa para uma estatística, com limites inclusivos."""

    low: float
    high: float
    n: int
    n_resamples: int


def bca_interval(
    values: Iterable[float],
    statistic: Callable[[np.ndarray], float] = np.median,
    *,
    n_resamples: int = 2_000,
    random_state: int = 42,
    confidence_level: float = 0.95,
) -> BCAInterval | None:
    """Calcula IC BCa determinístico, ignorando valores ausentes/não finitos.

    Retorna ``None`` quando não há ao menos duas observações. A BCa requer
    reamostragem de uma distribuição empírica; inventar um intervalo nesses
    casos seria mais enganoso que reportar sua indisponibilidade.
    """
    sample = np.asarray(list(values), dtype=float)
    sample = sample[np.isfinite(sample)]
    if len(sample) < 2:
        return None

    # Para uma amostra constante (por exemplo, proporção de censura cuja
    # mediana é zero), o ajuste BCa é matematicamente indefinido. Isso não é
    # uma falha de execução: o relatório deve indicar IC indisponível.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DegenerateDataWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        result = bootstrap(
            (sample,),
            statistic,
            method="BCa",
            n_resamples=n_resamples,
            confidence_level=confidence_level,
            random_state=np.random.default_rng(random_state),
            vectorized=False,
        )
    if not np.isfinite(result.confidence_interval.low) or not np.isfinite(
        result.confidence_interval.high
    ):
        return None
    return BCAInterval(
        low=float(result.confidence_interval.low),
        high=float(result.confidence_interval.high),
        n=len(sample),
        n_resamples=n_resamples,
    )
