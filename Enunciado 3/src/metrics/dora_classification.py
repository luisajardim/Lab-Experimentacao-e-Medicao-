"""Classificação DORA — variantes C1, C2, C3 (ENUNCIADO §5, RQ 07).

C1: lead_time_by_release + CFR(a) + median_recovery + deployment_frequency (releases)
C2: lead_time_by_release + CFR(a) + median_recovery + deployment_frequency (releases + tags com data)
C3: lead_time_by_commit  + CFR(a) + median_recovery + deployment_frequency (releases + tags com data)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .cfr import cfr_a
from .deployment_frequency import deployment_frequency
from .lead_time import lead_time_by_release, lead_time_by_commit
from .recovery import median_recovery_hours


class DORAVariant(Enum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"


@dataclass(frozen=True)
class DORAClassification:
    """Classificação DORA de um repositório."""
    variant: DORAVariant
    lead_time_hours: float | None
    cfr: float | None
    recovery_hours: float | None
    deployment_frequency_per_week: float | None

    def elite(self) -> bool | None:
        if any(v is None for v in (self.lead_time_hours, self.cfr, self.recovery_hours, self.deployment_frequency_per_week)):
            return None
        # ENUNCIADO §5: Elite = Lead time < 1h, CFR < 0.15, Recovery < 1h, Deploy >= 1/dia (7/semana)
        return (
            self.lead_time_hours < 1.0
            and self.cfr < 0.15
            and self.recovery_hours < 1.0
            and self.deployment_frequency_per_week >= 7.0
        )

    def high(self) -> bool | None:
        if any(v is None for v in (self.lead_time_hours, self.cfr, self.recovery_hours, self.deployment_frequency_per_week)):
            return None
        return (
            self.lead_time_hours < 24.0
            and self.cfr < 0.30
            and self.recovery_hours < 24.0
            and self.deployment_frequency_per_week >= 1.0
        )

    def category(self) -> str | None:
        if self.elite():
            return "Elite"
        if self.high():
            return "High"
        if all(v is not None for v in (self.lead_time_hours, self.cfr, self.recovery_hours, self.deployment_frequency_per_week)):
            return "Medium/Low"
        return None


def classify_dora(
    variant: DORAVariant,
    lead_time_a: float | None,
    lead_time_b: float | None,
    cfr: float | None,
    recovery_hours: float | None,
    deploy_freq_releases: float | None,
    deploy_freq_with_tags: float | None,
) -> DORAClassification:
    """Classifica conforme variante C1, C2 ou C3."""
    if variant == DORAVariant.C1:
        lt = lead_time_a
        df = deploy_freq_releases
    elif variant == DORAVariant.C2:
        lt = lead_time_a
        df = deploy_freq_with_tags
    else:  # C3
        lt = lead_time_b
        df = deploy_freq_with_tags

    return DORAClassification(
        variant=variant,
        lead_time_hours=lt,
        cfr=cfr,
        recovery_hours=recovery_hours,
        deployment_frequency_per_week=df,
    )