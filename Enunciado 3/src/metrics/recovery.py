"""Tempo de recuperação após falha de CI (ENUNCIADO §5, RQ 04).

Um episódio de falha começa na primeira falha **após um sucesso** e
termina na próxima execução bem-sucedida *do mesmo workflow*. Episódios
que nunca fecham dentro da janela de execuções fornecida são censurados
(``censored=True``): são registrados, não descartados, mas não entram no
cálculo da mediana.

Função pura: sem I/O.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import datetime

from .cfr import FAILURE_CONCLUSIONS, IGNORED_CONCLUSIONS, SUCCESS_CONCLUSIONS


def _parse(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def _hours_between(start: str, end: str) -> float:
    return (_parse(end) - _parse(start)).total_seconds() / 3600


@dataclass(frozen=True)
class WorkflowRunSample:
    """Entrada mínima de um workflow run usada por ``recovery_episodes``."""

    workflow_id: int
    conclusion: str | None
    run_started_at: str
    updated_at: str


@dataclass(frozen=True)
class RecoveryEpisode:
    """Um episódio de falha->recuperação de um workflow."""

    workflow_id: int
    failure_started_at: str
    recovered_at: str | None
    censored: bool

    @property
    def duration_hours(self) -> float | None:
        if self.censored or self.recovered_at is None:
            return None
        return _hours_between(self.failure_started_at, self.recovered_at)


def recovery_episodes(runs: list[WorkflowRunSample]) -> list[RecoveryEpisode]:
    """Episódios de falha->recuperação, agrupados por ``workflow_id``.

    Runs com conclusão ignorada (``cancelled``, ``skipped``, ``neutral``,
    ``action_required``, ``stale``, vazia) são descartados antes do
    agrupamento: não abrem, não fecham e não interrompem um episódio — o
    caso de borda obrigatório "runs cancelled (ignorados)".
    """
    by_workflow: dict[int, list[WorkflowRunSample]] = {}
    for run in runs:
        if run.conclusion in IGNORED_CONCLUSIONS:
            continue
        by_workflow.setdefault(run.workflow_id, []).append(run)

    episodes: list[RecoveryEpisode] = []
    for workflow_id, workflow_runs in by_workflow.items():
        ordered = sorted(workflow_runs, key=lambda run: run.run_started_at)
        has_seen_success = False
        open_failure_start: str | None = None

        for run in ordered:
            is_success = run.conclusion in SUCCESS_CONCLUSIONS
            is_failure = run.conclusion in FAILURE_CONCLUSIONS

            if is_failure and has_seen_success and open_failure_start is None:
                open_failure_start = run.run_started_at
            elif is_success and open_failure_start is not None:
                episodes.append(
                    RecoveryEpisode(
                        workflow_id=workflow_id,
                        failure_started_at=open_failure_start,
                        recovered_at=run.updated_at,
                        censored=False,
                    )
                )
                open_failure_start = None

            if is_success:
                has_seen_success = True

        if open_failure_start is not None:
            episodes.append(
                RecoveryEpisode(
                    workflow_id=workflow_id,
                    failure_started_at=open_failure_start,
                    recovered_at=None,
                    censored=True,
                )
            )

    return episodes


def median_recovery_hours(episodes: list[RecoveryEpisode]) -> float | None:
    """Mediana, por repo, das durações dos episódios **não censurados**."""
    values = [episode.duration_hours for episode in episodes if not episode.censored]
    return statistics.median(values) if values else None


def censored_proportion(episodes: list[RecoveryEpisode]) -> float | None:
    """Proporção de episódios censurados (ENUNCIADO §3: nunca descartar)."""
    if not episodes:
        return None
    return sum(1 for episode in episodes if episode.censored) / len(episodes)
