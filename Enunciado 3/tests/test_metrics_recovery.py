"""Testes de tempo de recuperação (ENUNCIADO RQ 04) — funções puras, sem rede."""

import json
from pathlib import Path

import pytest

from metrics.recovery import (
    WorkflowRunSample,
    censored_proportion,
    median_recovery_hours,
    recovery_episodes,
)

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def enunciado_example():
    return json.loads((FIXTURES / "recovery_example.json").read_text(encoding="utf-8"))


def _runs_from_fixture(data):
    return [
        WorkflowRunSample(
            workflow_id=item["workflow_id"],
            conclusion=item["conclusion"],
            run_started_at=item["run_started_at"],
            updated_at=item["updated_at"],
        )
        for item in data["runs"]
    ]


def test_episode_matches_enunciado_example(enunciado_example):
    runs = _runs_from_fixture(enunciado_example)
    episodes = recovery_episodes(runs)

    assert len(episodes) == 1
    episode = episodes[0]
    assert episode.failure_started_at == enunciado_example["expected_episode_failure_started_at"]
    assert episode.recovered_at == enunciado_example["expected_episode_recovered_at"]
    assert episode.censored is False
    assert episode.duration_hours == pytest.approx(
        enunciado_example["expected_episode_duration_hours"]
    )
    assert median_recovery_hours(episodes) == pytest.approx(
        enunciado_example["expected_episode_duration_hours"]
    )
    assert censored_proportion(episodes) == 0.0


def test_censored_episode_when_window_ends_mid_failure():
    """Caso de borda obrigatório: falha censurada (fim fora da janela)."""
    runs = [
        WorkflowRunSample(1, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),
        WorkflowRunSample(1, "failure", "2026-01-01T10:00:00Z", "2026-01-01T10:05:00Z"),
        # janela termina aqui: nenhum sucesso depois da falha
    ]
    episodes = recovery_episodes(runs)

    assert len(episodes) == 1
    assert episodes[0].censored is True
    assert episodes[0].recovered_at is None
    assert episodes[0].duration_hours is None
    assert median_recovery_hours(episodes) is None
    assert censored_proportion(episodes) == 1.0


def test_cancelled_runs_do_not_open_close_or_interrupt_episodes():
    """Caso de borda obrigatório: runs cancelled (ignorados)."""
    runs = [
        WorkflowRunSample(1, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),
        WorkflowRunSample(1, "cancelled", "2026-01-01T09:30:00Z", "2026-01-01T09:35:00Z"),
        WorkflowRunSample(1, "failure", "2026-01-01T10:00:00Z", "2026-01-01T10:05:00Z"),
        WorkflowRunSample(1, "cancelled", "2026-01-01T10:15:00Z", "2026-01-01T10:20:00Z"),
        WorkflowRunSample(1, "success", "2026-01-01T11:00:00Z", "2026-01-01T11:05:00Z"),
    ]
    episodes = recovery_episodes(runs)

    assert len(episodes) == 1
    assert episodes[0].failure_started_at == "2026-01-01T10:00:00Z"
    assert episodes[0].recovered_at == "2026-01-01T11:05:00Z"


def test_failure_without_prior_success_does_not_open_episode():
    runs = [
        WorkflowRunSample(1, "failure", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),
        WorkflowRunSample(1, "success", "2026-01-01T10:00:00Z", "2026-01-01T10:05:00Z"),
    ]
    assert recovery_episodes(runs) == []


def test_single_release_repo_has_no_episodes_and_no_median():
    """Caso de borda obrigatório: repo com 1 release / sem histórico de falha."""
    runs = [WorkflowRunSample(1, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z")]
    episodes = recovery_episodes(runs)
    assert episodes == []
    assert median_recovery_hours(episodes) is None
    assert censored_proportion(episodes) is None


def test_episodes_are_grouped_independently_per_workflow():
    runs = [
        WorkflowRunSample(1, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),
        WorkflowRunSample(1, "failure", "2026-01-01T10:00:00Z", "2026-01-01T10:05:00Z"),
        WorkflowRunSample(2, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),
        WorkflowRunSample(2, "failure", "2026-01-01T10:00:00Z", "2026-01-01T10:05:00Z"),
        WorkflowRunSample(2, "success", "2026-01-01T10:30:00Z", "2026-01-01T10:35:00Z"),
    ]
    episodes = recovery_episodes(runs)

    by_workflow = {1: [], 2: []}
    for episode in episodes:
        by_workflow[episode.workflow_id].append(episode)

    assert len(by_workflow[1]) == 1
    assert by_workflow[1][0].censored is True
    assert len(by_workflow[2]) == 1
    assert by_workflow[2][0].censored is False


def test_multiple_episodes_median_across_workflow():
    runs = [
        WorkflowRunSample(1, "success", "2026-01-01T00:00:00Z", "2026-01-01T00:05:00Z"),
        WorkflowRunSample(1, "failure", "2026-01-01T01:00:00Z", "2026-01-01T01:05:00Z"),
        WorkflowRunSample(1, "success", "2026-01-01T03:00:00Z", "2026-01-01T03:05:00Z"),  # 2h05
        WorkflowRunSample(1, "failure", "2026-01-01T05:00:00Z", "2026-01-01T05:05:00Z"),
        WorkflowRunSample(1, "success", "2026-01-01T09:00:00Z", "2026-01-01T09:05:00Z"),  # 4h05
    ]
    episodes = recovery_episodes(runs)
    assert len(episodes) == 2
    assert median_recovery_hours(episodes) == pytest.approx((2 + 5 / 60 + 4 + 5 / 60) / 2)
