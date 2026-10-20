"""Classificação DORA — variantes C1, C2, C3 (ENUNCIADO §5, RQ 07).

C1: lead_time_by_release + CFR(a) + median_recovery + deployment_frequency (releases)
C2: lead_time_by_release + CFR(a) + median_recovery + deployment_frequency (releases + tags com data)
C3: lead_time_by_commit  + CFR(a) + median_recovery + deployment_frequency (releases + tags com data)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


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

    def category(self) -> str | None:
        """Return the median of the four DORA tier scores, rounded down."""
        values = (
            self.deployment_frequency_per_week,
            self.lead_time_hours,
            self.cfr,
            self.recovery_hours,
        )
        if any(value is None for value in values):
            return None
        deployment_frequency, lead_time, cfr, recovery = values
        assert all(value is not None for value in values)
        scores = sorted(
            (
                4 if deployment_frequency >= 7 else 3 if deployment_frequency >= 1 else 2 if deployment_frequency >= 1 / 4.345 else 1,
                4 if lead_time < 24 else 3 if lead_time < 24 * 7 else 2 if lead_time < 24 * 30 else 1,
                4 if cfr <= 0.15 else 3 if cfr <= 0.30 else 2 if cfr <= 0.45 else 1,
                4 if recovery < 1 else 3 if recovery < 24 else 2 if recovery < 24 * 7 else 1,
            )
        )
        return {4: "Elite", 3: "High", 2: "Medium", 1: "Low"}[(scores[1] + scores[2]) // 2]


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
