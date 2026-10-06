"""Coleta de releases válidas de um repositório (PLAN T05).

Filtra ``draft=false`` e ordena por ``published_at`` ascendente — a ordem
que ``collector.commits`` espera para montar os pares consecutivos usados
no cálculo de lead time (ENUNCIADO §5, RQ 02).

Pré-releases (``prerelease=true``) **não** são filtradas aqui: elas entram
como unidade de deploy apenas na variante C2/C3 da classificação DORA
(ENUNCIADO §5, RQ 07), então o chamador decide se as inclui ou não.
"""

from __future__ import annotations

from github.models import Release
from github.rest import GitHubRESTClient


def collect_releases(client: GitHubRESTClient, owner: str, repo: str) -> list[Release]:
    """Releases não-draft de ``owner/repo``, ordenadas por ``published_at``."""
    raw = client.paginate(f"/repos/{owner}/{repo}/releases")
    releases = [Release.from_api(item) for item in raw if not item.get("draft")]
    releases.sort(key=lambda release: release.published_at or "")
    return releases
