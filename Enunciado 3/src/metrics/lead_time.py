"""Lead time for changes — variantes (a) e (b) (ENUNCIADO §5, RQ 02).

Funções puras: sem I/O, sem import de ``github``/``collector``. Recebem
apenas as datas já extraídas (strings ISO 8601) — quem monta
``ReleaseCommits`` a partir das respostas da API é o chamador (pipeline).

Todos os tempos são retornados em **horas** (ver ``metrics.recovery`` para
a mesma convenção).
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from datetime import datetime


def _parse(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def _hours_between(start: str, end: str) -> float:
    return (_parse(end) - _parse(start)).total_seconds() / 3600


@dataclass(frozen=True)
class ReleaseCommits:
    """Uma release e as datas (``commit.author.date``) dos commits nela.

    ``commit_dates`` vazio representa o caso de borda obrigatório
    "release sem commits novos": a release é ignorada nas duas variantes.
    Releases sem release anterior (primeira da história) não devem ser
    incluídas na lista de entrada — o chamador já as filtra a partir do
    ``ignored_reason`` de ``collector.commits.CommitsBetween``.
    """

    release_published_at: str
    commit_dates: list[str]


def lead_time_by_release(releases: list[ReleaseCommits]) -> float | None:
    """Variante (a): mediana, por repo, de ``published_at - commit mais antigo``.

    ``None`` se não houver nenhuma release elegível (ex.: repo com uma
    única release, ou todas as releases sem commits novos).
    """
    values = [
        _hours_between(min(release.commit_dates), release.release_published_at)
        for release in releases
        if release.commit_dates
    ]
    return statistics.median(values) if values else None


def lead_time_by_commit(releases: list[ReleaseCommits]) -> float | None:
    """Variante (b): mediana de todos os commits de todas as releases."""
    values = [
        _hours_between(commit_date, release.release_published_at)
        for release in releases
        for commit_date in release.commit_dates
    ]
    return statistics.median(values) if values else None
