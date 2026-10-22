"""Change failure rate (ENUNCIADO §5, RQ 03). Funções puras: sem I/O.

* variante (a), proxy de CI: classificação de ``conclusion`` dos workflow
  runs conforme a tabela da seção 3 do ENUNCIADO;
* variante (b), proxy de entrega: release seguida por release corretiva em
  até 7 dias (a classificação de corretiva vem de ``cfr_release``).
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta

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


FOLLOW_UP_DAYS = 7


def cfr_b(
    releases: Sequence[tuple[datetime, bool]],
    window_end: datetime,
    *,
    follow_up_days: int = FOLLOW_UP_DAYS,
) -> float | None:
    """CFR(b), proxy de entrega (ENUNCIADO §5, RQ 03 b).

    ``releases`` são os deploys da janela como ``(published_at, corretiva)``.
    Uma release R *falhou* se alguma release corretiva for publicada depois
    dela em até ``follow_up_days`` dias. Releases publicadas nos últimos
    ``follow_up_days`` dias da janela não podem ser avaliadas (censura) e
    ficam fora do denominador. ``None`` se nenhuma release puder ser avaliada.
    """
    follow_up = timedelta(days=follow_up_days)
    evaluated = [when for when, _ in releases if when + follow_up <= window_end]
    if not evaluated:
        return None
    corrective = [when for when, is_corrective in releases if is_corrective]
    failed = sum(
        any(when < fix <= when + follow_up for fix in corrective) for when in evaluated
    )
    return failed / len(evaluated)
