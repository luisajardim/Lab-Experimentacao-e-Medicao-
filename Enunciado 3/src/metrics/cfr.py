"""Change failure rate — variante (a), proxy de CI (ENUNCIADO §5, RQ 03).

Classificação de ``conclusion`` dos workflow runs conforme a tabela da
seção 3 do ENUNCIADO. Função pura: sem I/O.
"""

from __future__ import annotations

FAILURE_CONCLUSIONS = frozenset({"failure", "timed_out", "startup_failure"})
SUCCESS_CONCLUSIONS = frozenset({"success"})
IGNORED_CONCLUSIONS = frozenset(
    {"cancelled", "skipped", "neutral", "action_required", "stale", "", None}
)


def cfr_a(conclusions: list[str | None]) -> float | None:
    """CFR(a) = falhas / (falhas + sucessos) a partir das ``conclusion``.

    Runs com conclusão em ``IGNORED_CONCLUSIONS`` (inclui execuções ainda
    em andamento, representadas por ``None``/string vazia) não entram no
    denominador. ``None`` se não houver nenhum sucesso nem falha.
    """
    failures = sum(1 for conclusion in conclusions if conclusion in FAILURE_CONCLUSIONS)
    successes = sum(1 for conclusion in conclusions if conclusion in SUCCESS_CONCLUSIONS)
    total = failures + successes
    if total == 0:
        return None
    return failures / total
