"""Sessão HTTP com cache SQLite content-addressed (T03 + T04/T05/T06).

Encapsula um ``httpx.Client`` real e intercepta ``request()`` para
servir respostas em cache ou graválas após a chamada de rede.
"""

from __future__ import annotations

import logging
from typing import Any

from github.rest import BaseGitHubClient, GitHubHTTPError
from cache.sqlite_store import SQLiteStore

log = logging.getLogger(__name__)


class CachedSession:
    """Proxy de sessão HTTP que adiciona cache SQLite a qualquer cliente."""

    def __init__(
        self,
        wrapped: Any,
        store: SQLiteStore,
        stage: str,
    ) -> None:
        self._wrapped = wrapped
        self._store = store
        self._stage = stage

    def request(self, method: str, url: str, params=None, json=None, **kwargs):
        key_body = None
        if json is not None:
            key_body = str(json)
        cached = self._store.get(method, url, key_body)
        if cached is not None:
            log.debug("cache hit: %s %s", method, url)
            return _response_from_cache(cached)

        log.debug("cache miss: %s %s", method, url)
        response = self._wrapped.request(method, url, params=params, json=json, **kwargs)
        try:
            response_body = response.text
        except Exception:
            response_body = ""
        self._store.put(
            method,
            url,
            key_body,
            response.status_code,
            response_body,
            stage=self._stage,
        )
        return response

    def close(self) -> None:
        self._wrapped.close()


def _response_from_cache(cached: Any) -> Any:
    """Reconstrói um objeto response mínimo a partir do cache."""
    import httpx

    return httpx.Response(
        status_code=cached.status,
        text=cached.response_body,
        request=httpx.Request(cached.method, cached.url),
    )
