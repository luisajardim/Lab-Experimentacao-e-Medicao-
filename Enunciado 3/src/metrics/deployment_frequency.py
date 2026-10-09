"""Deployment frequency (ENUNCIADO §5, RQ 01).

Deploy = release não-draft (ENUNCIADO §3). Frequência = n_deploys / semanas_na_janela.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReleaseInfo:
    """Release com data de publicação."""
    published_at: str
    draft: bool = False


def deployment_frequency(
    releases: list[ReleaseInfo],
    window_weeks: float = 52.1,
) -> float | None:
    """Frequência de deploy = releases não-draft / semanas na janela.

    Retorna ``None`` se não houver releases não-draft.
    """
    non_draft = [r for r in releases if not r.draft]
    if not non_draft:
        return None
    return len(non_draft) / window_weeks