"""Cliente GraphQL do GitHub com requisições em lote (aliases).

Várias operações são combinadas em um único documento
``query { alias0: ... alias1: ... }`` e enviadas numa só
requisição, reduzindo round-trips e consumo de cota (PLAN T02).
"""

from __future__ import annotations

import logging
import re
from collections.abc import Iterator
from typing import Any

import httpx

from .rest import (
    BaseGitHubClient,
    GitHubError,
    GitHubHTTPError,
    Sleeper,
    WallClock,
)

log = logging.getLogger(__name__)

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_DEFAULT_VARIABLE_TYPE = "String!"

REPO_METADATA_SELECTION = """
    nameWithOwner
    url
    stargazerCount
    primaryLanguage { name }
    defaultBranchRef { name }
    createdAt
    pushedAt
"""


class GraphQLResponseError(GitHubError):
    """A API devolveu erros (HTTP 200 com campo ``errors``)."""

    def __init__(self, errors: list[dict[str, Any]]) -> None:
        details = "; ".join(str(error.get("message", error)) for error in errors)
        super().__init__(f"GraphQL errors: {details}")
        self.errors = errors


def _chunks(items: list[Any], size: int) -> Iterator[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _uses_variable(selection: str, name: str) -> bool:
    return re.search(rf"\${re.escape(name)}\b", selection) is not None


class GitHubGraphQLClient(BaseGitHubClient):
    """Cliente GraphQL que agrupa operações por aliases (batching)."""

    def __init__(
        self,
        token: str,
        *,
        url: str = "https://api.github.com/graphql",
        batch_size: int = 20,
        timeout: float = 30.0,
        max_retries: int = 5,
        backoff_base: float = 1.0,
        session: httpx.Client | None = None,
        sleeper: Sleeper | None = None,
        wall_clock: WallClock | None = None,
    ) -> None:
        super().__init__(
            token,
            base_url=url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_base=backoff_base,
            session=session,
            sleeper=sleeper,
            wall_clock=wall_clock,
        )
        self._url = url
        self._batch_size = batch_size

    def query(
        self,
        operations: dict[str, str],
        variables: dict[str, Any] | None = None,
        variable_types: dict[str, str] | None = None,
        *,
        strict: bool = False,
    ) -> dict[str, Any]:
        """Executa operações em lote; devolve ``{chave_original: dados}``.

        Cada valor de ``operations`` é o corpo de seleção (sem o
        wrapper ``query { ... }``); todas as operações compartilham
        ``variables``. Operações além de ``batch_size`` são divididas
        em requisições adicionais. Com ``strict=False`` (padrão),
        falhas de operações individuais viram ``None`` no resultado e
        são registradas em log; com ``strict=True`` levantam
        ``GraphQLResponseError``.
        """
        results: dict[str, Any] = {}
        variables = variables or {}
        variable_types = variable_types or {}
        for chunk in _chunks(list(operations.items()), self._batch_size):
            results.update(self._query_chunk(chunk, variables, variable_types, strict=strict))
        return results

    def _query_chunk(
        self,
        chunk: list[tuple[str, str]],
        variables: dict[str, Any],
        variable_types: dict[str, str],
        *,
        strict: bool,
    ) -> dict[str, Any]:
        aliases: dict[str, str] = {}
        parts: list[str] = []
        for index, (key, selection) in enumerate(chunk):
            alias = key if _IDENTIFIER_RE.match(key) else f"op{index}"
            aliases[alias] = key
            parts.append(f"{alias}: {selection}")

        used_variables = {
            name: value
            for name, value in variables.items()
            if any(_uses_variable(selection, name) for _, selection in chunk)
        }
        definitions = ""
        if used_variables:
            rendered = ", ".join(
                f"${name}: {variable_types.get(name, _DEFAULT_VARIABLE_TYPE)}"
                for name in used_variables
            )
            definitions = f"({rendered})"
        document = f"query{definitions} {{ {' '.join(parts)} }}"

        response = self._request_with_retry(
            "POST",
            self._url,
            json_body={"query": document, "variables": used_variables},
        )
        if response.status_code >= 400:
            raise GitHubHTTPError(response.status_code, response.text[:500])
        body = response.json()
        errors = body.get("errors") or []
        if errors and strict:
            raise GraphQLResponseError(errors)
        if errors:
            first = errors[0].get("message", errors[0])
            log.warning("GraphQL devolveu %d erro(s); modo leniente: %s", len(errors), first)
        data = body.get("data") or {}
        return {original: data.get(alias) for alias, original in aliases.items()}

    def repositories(
        self,
        full_names: list[str],
        *,
        selection: str = REPO_METADATA_SELECTION,
    ) -> dict[str, Any]:
        """Metadados de repositórios em lotes; chave: ``full_name``."""
        operations: dict[str, str] = {}
        variables: dict[str, Any] = {}
        for index, full_name in enumerate(full_names):
            owner, _, name = full_name.partition("/")
            operations[full_name] = (
                f"repository(owner: $owner{index}, name: $name{index}) {{ {selection} }}"
            )
            variables[f"owner{index}"] = owner
            variables[f"name{index}"] = name
        return self.query(operations, variables)
