"""Coleta de tags de um repositório, com data resolvida via commit (PLAN T05).

Tags não trazem data própria na API (ENUNCIADO §4): a data de cada tag é a
``commit.author.date`` do commit que ela aponta, obtida com uma chamada
adicional a ``GET /repos/{owner}/{repo}/commits/{sha}`` por tag.

Usada como variante do "deploy" na classificação DORA (RQ 07, combinação
C3) — útil inclusive para repositórios sem releases publicadas.
"""

from __future__ import annotations

from github.models import Commit, ResolvedTag, Tag
from github.rest import GitHubRESTClient


def collect_tags(client: GitHubRESTClient, owner: str, repo: str) -> list[ResolvedTag]:
    """Tags de ``owner/repo`` com a data do commit apontado resolvida."""
    raw = client.paginate(f"/repos/{owner}/{repo}/tags")
    tags = [Tag.from_api(item) for item in raw]

    resolved: list[ResolvedTag] = []
    for tag in tags:
        if not tag.sha:
            continue
        commit_data = client.get_json(f"/repos/{owner}/{repo}/commits/{tag.sha}")
        commit = Commit.from_api(commit_data)
        resolved.append(ResolvedTag(name=tag.name, sha=tag.sha, date=commit.author_date))
    return resolved
