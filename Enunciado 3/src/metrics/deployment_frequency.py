"""Deployment frequency (ENUNCIADO §5, RQ 01).

Deploy = release publicada, não-draft e não-pré-release (ENUNCIADO §3).
Frequência = n_deploys / semanas_na_janela.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReleaseInfo:
    """Release com data de publicação."""
    published_at: str
    draft: bool = False
    prerelease: bool = False


def deployment_frequency(
    releases: list[ReleaseInfo],
    window_weeks: float = 52.1,
) -> float | None:
    """Frequência de deploy = releases publicadas, não-pré-release / semanas.

    Retorna ``None`` se não houver releases não-draft.
    """
    eligible = [r for r in releases if not r.draft and not r.prerelease]
    if not eligible:
        return None
    return len(eligible) / window_weeks
