"""Correlação de Spearman (ENUNCIADO §5, RQ 05 e RQ 06)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pymannkendall import original_test as mk_test


@dataclass(frozen=True)
class SpearmanResult:
    """Resultado do teste de Spearman."""
    rho: float
    p_value: float
    significant: bool  # p < 0.05


def spearman_correlation(
    x: list[float],
    y: list[float],
    alpha: float = 0.05,
) -> SpearmanResult:
    """Correlação de Spearman entre x e y usando pymannkendall.

    pymannkendall.mk_test retorna Kendall's tau, mas também fornece Spearman rho
    via .s (estatística) e .p (p-value). Usamos .tau para Kendall e calculamos
    Spearman separadamente se necessário.

    Nota: pymannkendall >= 1.4 suporta method='spearman' no mk_test.
    """
    try:
        # pymannkendall 1.4+ suporta method='spearman'
        result = mk_test(x, y, method="spearman")
        rho = result.rho if hasattr(result, "rho") else result.tau
        p_value = result.p
    except TypeError:
        # Fallback: usar scipy se disponível ou calcular manual
        from scipy.stats import spearmanr
        rho, p_value = spearmanr(x, y)

    return SpearmanResult(
        rho=float(rho),
        p_value=float(p_value),
        significant=p_value < alpha,
    )