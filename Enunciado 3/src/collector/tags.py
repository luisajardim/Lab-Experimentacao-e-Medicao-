"""Coleta de tags de um repositório, com data resolvida via commit (PLAN T05).

Tags não trazem data própria na API (ENUNCIADO §4): a data de cada tag é a
``commit.author.date`` do commit que ela aponta, obtida com uma chamada
adicional a ``GET /repos/{owner}/{repo}/commits/{sha}`` por tag.

Usada como variante do "deploy" na classificação DORA (RQ 07, combinação
C3) — útil inclusive para repositórios sem releases publicadas.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from github.models import Commit, ResolvedTag, Tag
from github.rest import GitHubRESTClient


def _resolve_tag_date(
    client: GitHubRESTClient, owner: str, repo: str, tag: Tag
) -> ResolvedTag | None:
    if not tag.sha:
        return None
    commit_data = client.get_json(f"/repos/{owner}/{repo}/commits/{tag.sha}")
    commit = Commit.from_api(commit_data)
    return ResolvedTag(name=tag.name, sha=tag.sha, date=commit.author_date)


def collect_tags(
    client: GitHubRESTClient,
    owner: str,
    repo: str,
    *,
    max_workers: int = 4,
) -> list[ResolvedTag]:
    """Tags de ``owner/repo`` com a data do commit apontado resolvida."""
    raw = client.paginate(f"/repos/{owner}/{repo}/tags")
    tags = [Tag.from_api(item) for item in raw]

    resolved: list[ResolvedTag] = []
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="tags") as pool:
        futures = {
            pool.submit(_resolve_tag_date, client, owner, repo, tag): tag for tag in tags
        }
        for future in as_completed(futures):
            try:
                result = future.result()
                if result is not None:
                    resolved.append(result)
            except Exception:
                pass

    return resolved
