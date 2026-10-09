"""Funções PURAS de cálculo das métricas DORA (sem I/O).

Regras operacionais: ENUNCIADO §3 e §5. Todas as funções recebem
dados já coletados e devolvem valores numéricos, para teste com
fixtures (tests/fixtures/).
"""

from .cfr import cfr_a
from .deployment_frequency import deployment_frequency
from .dora_classification import DORAClassification, DORAVariant, classify_dora
from .lead_time import lead_time_by_commit, lead_time_by_release
from .recovery import RecoveryEpisode, censored_proportion, median_recovery_hours, recovery_episodes
from .survival import SurvivalResult, kaplan_meier_recovery
from .correlation import SpearmanResult, spearman_correlation

__all__ = [
    "cfr_a",
    "deployment_frequency",
    "DORAClassification",
    "DORAVariant",
    "classify_dora",
    "lead_time_by_commit",
    "lead_time_by_release",
    "RecoveryEpisode",
    "censored_proportion",
    "median_recovery_hours",
    "recovery_episodes",
    "SurvivalResult",
    "kaplan_meier_recovery",
    "SpearmanResult",
    "spearman_correlation",
]
