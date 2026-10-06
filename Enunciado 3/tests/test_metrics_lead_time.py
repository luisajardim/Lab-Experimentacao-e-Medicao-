"""Testes de lead time (ENUNCIADO RQ 02) — funções puras, sem rede."""

import json
from pathlib import Path

import pytest

from metrics.lead_time import ReleaseCommits, lead_time_by_commit, lead_time_by_release

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def enunciado_example():
    return json.loads((FIXTURES / "lead_time_example.json").read_text(encoding="utf-8"))


def _releases_from_fixture(data):
    return [
        ReleaseCommits(
            release_published_at=item["release_published_at"],
            commit_dates=item["commit_dates"],
        )
        for item in data["releases"]
    ]


def test_lead_time_by_release_matches_enunciado_example(enunciado_example):
    releases = _releases_from_fixture(enunciado_example)
    assert lead_time_by_release(releases) == enunciado_example["expected_lead_time_a_hours"]


def test_lead_time_by_commit_matches_enunciado_example(enunciado_example):
    releases = _releases_from_fixture(enunciado_example)
    assert lead_time_by_commit(releases) == enunciado_example["expected_lead_time_b_median_hours"]


def test_release_without_new_commits_is_ignored():
    """Caso de borda obrigatório: release sem commits novos."""
    releases = [
        ReleaseCommits("2026-01-10T00:00:00Z", []),
        ReleaseCommits("2026-01-20T00:00:00Z", ["2026-01-15T00:00:00Z"]),
    ]
    assert lead_time_by_release(releases) == 120.0
    assert lead_time_by_commit(releases) == 120.0


def test_single_release_with_no_eligible_entries_returns_none():
    """Caso de borda obrigatório: repo com 1 release (sem par anterior)."""
    assert lead_time_by_release([]) is None
    assert lead_time_by_commit([]) is None


def test_lead_time_by_release_uses_oldest_commit_per_release():
    releases = [
        ReleaseCommits(
            "2026-01-10T00:00:00Z",
            ["2026-01-05T00:00:00Z", "2026-01-08T00:00:00Z", "2026-01-01T00:00:00Z"],
        )
    ]
    # mais antigo é 01/01 -> 9 dias = 216h
    assert lead_time_by_release(releases) == 216.0


def test_lead_time_by_commit_uses_median_across_all_commits():
    releases = [
        ReleaseCommits("2026-01-11T00:00:00Z", ["2026-01-01T00:00:00Z"]),  # 240h
        ReleaseCommits("2026-01-21T00:00:00Z", ["2026-01-01T00:00:00Z"]),  # 480h
    ]
    assert lead_time_by_commit(releases) == 360.0
