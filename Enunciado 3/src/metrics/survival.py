"""Análise de sobrevivência — Kaplan-Meier (ENUNCIADO §5, RQ 08).

Estima a curva de sobrevivência do tempo até recuperação (recovery time).
Episódios censurados (não recuperados dentro da janela) são incluídos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from lifelines import KaplanMeierFitter


@dataclass(frozen=True)
class SurvivalResult:
    """Resultado da estimação de Kaplan-Meier."""
    median_survival: float | None  # em horas
    confidence_interval: tuple[float, float] | None  # (lower, upper)
    n_events: int  # episódios não censurados (recuperados)
    n_censored: int  # episódios censurados
    n_total: int


def kaplan_meier_recovery(
    durations: list[float],
    censored: list[bool],
) -> SurvivalResult:
    """Estima curva de Kaplan-Meier para tempo de recuperação.

    Args:
        durations: tempos em horas (para censurados, tempo até fim da janela)
        censored: True = censurado (não recuperado), False = evento (recuperado)
    """
    if not durations:
        return SurvivalResult(
            median_survival=None,
            confidence_interval=None,
            n_events=0,
            n_censored=0,
            n_total=0,
        )

    kmf = KaplanMeierFitter()
    kmf.fit(durations=durations, event_observed=[not c for c in censored])

    median = kmf.median_survival_time_
    ci = kmf.confidence_interval_

    n_total = len(durations)
    n_censored = sum(censored)
    n_events = n_total - n_censored

    return SurvivalResult(
        median_survival=float(median) if median is not None else None,
        confidence_interval=(
            float(ci.iloc[0, 0]),
            float(ci.iloc[0, 1]),
        ) if ci is not None and not ci.empty else None,
        n_events=n_events,
        n_censored=n_censored,
        n_total=n_total,
    )