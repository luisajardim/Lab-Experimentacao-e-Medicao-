"""Coleta de commits entre releases consecutivas (PLAN T05).

Para cada release (exceto a primeira da história, que não tem release
anterior para comparar), chama ``compare/{base}...{head}`` paginando
``per_page=250`` e registra os commits inclusos — usados no cálculo de
lead time (ENUNCIADO §5, RQ 02).

Dois casos são registrados e **ignorados no cálculo de lead time**, sem
interromper a coleta dos demais:

- a release é a primeira da história do repositório (sem release anterior);
- o ``compare`` devolve 404 (tag apagada ou reescrita — ENUNCIADO §11).
"""

from __future__ import annotations

from dataclasses import dataclass

from cache.sqlite_store import SQLiteStore
from github.models import Commit, Release
from github.rest import GitHubHTTPError, GitHubRESTClient

NO_PREVIOUS_RELEASE = "no_previous_release"
COMPARE_NOT_FOUND = "compare_404"


@dataclass(frozen=True)
class CommitsBetween:
    """Commits incluídos em uma release frente à release anterior.

    ``commits`` é ``None`` (e ``ignored_reason`` explica o motivo) quando a
    comparação não pôde ser feita; nesse caso a release é registrada mas
    ignorada no cálculo de lead time, conforme o critério de aceitação.
    """

    release: str
    previous_release: str | None
    commits: list[Commit] | None
    ignored_reason: str | None = None

    @property
    def ignored(self) -> bool:
        return self.ignored_reason is not None


def _compare_commits(
    client: GitHubRESTClient, owner: str, repo: str, base: str, head: str, *, per_page: int
) -> list[Commit] | None:
    """Commits de ``base...head``, ou ``None`` se o ``compare`` devolver 404."""
    path = f"/repos/{owner}/{repo}/compare/{base}...{head}"
    try:
        raw_commits = list(
            client.paginate_field(path, "commits", per_page=per_page)
        )
    except GitHubHTTPError as error:
        if error.status == 404:
            return None
        raise
    return [Commit.from_api(item) for item in raw_commits]


def collect_commits_between(
    client: GitHubRESTClient,
    owner: str,
    repo: str,
    releases: list[Release],
    *,
    per_page: int = 250,
    store: SQLiteStore | None = None,
    stage: str = "collect:commits",
) -> list[CommitsBetween]:
    """Commits entre cada par de releases consecutivas (ordem ascendente).

    ``releases`` deve vir ordenada por ``published_at`` (ver
    ``collector.releases.collect_releases``) — a primeira release da lista
    é tratada como a primeira da história e não gera comparação.
    """
    results: list[CommitsBetween] = []
    previous: Release | None = None

    for release in releases:
        if previous is None:
            results.append(
                CommitsBetween(
                    release=release.tag_name,
                    previous_release=None,
                    commits=None,
                    ignored_reason=NO_PREVIOUS_RELEASE,
                )
            )
            previous = release
            continue

        cache_key = f"compare:{owner}/{repo}:{previous.tag_name}...{release.tag_name}"
        if store and store.is_stage_complete(f"{stage}:{cache_key}"):
            results.append(
                CommitsBetween(
                    release=release.tag_name,
                    previous_release=previous.tag_name,
                    commits=None,
                    ignored_reason=COMPARE_NOT_FOUND,
                )
            )
            previous = release
            continue

        commits = _compare_commits(
            client,
            owner,
            repo,
            previous.tag_name,
            release.tag_name,
            per_page=per_page,
        )
        results.append(
            CommitsBetween(
                release=release.tag_name,
                previous_release=previous.tag_name,
                commits=commits,
                ignored_reason=None if commits is not None else COMPARE_NOT_FOUND,
            )
        )

        if store:
            store.mark_stage_complete(f"{stage}:{cache_key}")

        previous = release

    return results
