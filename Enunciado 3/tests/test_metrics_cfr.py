"""Testes de CFR(a) (ENUNCIADO RQ 03a) — funções puras, sem rede."""

import json
from pathlib import Path

import pytest

from metrics.cfr import cfr_a

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def enunciado_example():
    return json.loads((FIXTURES / "cfr_a_example.json").read_text(encoding="utf-8"))


def test_cfr_a_matches_fixture_example(enunciado_example):
    assert cfr_a(enunciado_example["conclusions"]) == enunciado_example["expected_cfr_a"]


def test_cfr_a_all_success_is_zero():
    assert cfr_a(["success", "success", "success"]) == 0.0


def test_cfr_a_all_failure_is_one():
    assert cfr_a(["failure", "timed_out", "startup_failure"]) == 1.0


def test_cancelled_runs_are_ignored():
    """Caso de borda obrigatório: runs cancelled (ignorados)."""
    assert cfr_a(["success", "cancelled", "cancelled"]) == 0.0
    assert cfr_a(["cancelled", "skipped", "neutral", "action_required", "stale"]) is None


def test_cfr_a_empty_or_none_conclusions_are_ignored():
    assert cfr_a(["success", None, ""]) == 0.0


def test_cfr_a_returns_none_when_no_success_or_failure():
    assert cfr_a([]) is None
