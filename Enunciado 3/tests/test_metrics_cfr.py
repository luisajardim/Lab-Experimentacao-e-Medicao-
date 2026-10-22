"""Testes de CFR(a) e CFR(b) (ENUNCIADO RQ 03) — funções puras, sem rede."""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from metrics.cfr import cfr_a, cfr_b

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


END = datetime(2026, 9, 30, 23, 59, 59)


def _day(n: int) -> datetime:
    return datetime(2026, 9, 1) + timedelta(days=n)


def test_cfr_b_failure_within_seven_days():
    releases = [
        (_day(0), False),  # seguida por corretiva no dia 3 -> falha
        (_day(3), True),  # nenhuma corretiva até o dia 10 -> ok
        (_day(12), False),  # corretiva no dia 20 (8 dias depois) -> ok
        (_day(20), True),  # ok
    ]
    assert cfr_b(releases, END) == pytest.approx(1 / 4)


def test_cfr_b_exactly_seven_days_counts_as_failure():
    assert cfr_b([(_day(0), False), (_day(7), True)], END) == pytest.approx(1 / 2)


def test_cfr_b_censors_last_seven_days_of_window():
    releases = [(_day(0), False), (END - timedelta(days=2), True)]
    # a corretiva nos últimos 7 dias fica fora do denominador; a primeira é
    # avaliada e não falhou (a corretiva veio mais de 7 dias depois)
    assert cfr_b(releases, END) == 0.0
    assert cfr_b([(END - timedelta(days=1), False)], END) is None
    assert cfr_b([], END) is None
