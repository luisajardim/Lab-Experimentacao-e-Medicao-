"""Cliente REST do GitHub: paginação, rate limit e backoff exponencial.

Nenhuma biblioteca pronta de acesso à API do GitHub é usada (ENUNCIADO §4):
todo o tráfego passa por ``httpx`` cru. Este módulo também abriga
``BaseGitHubClient``, a máquina de transporte compartilhada pelos clientes
REST e GraphQL (retry, backoff exponencial e pausa por rate limit).
"""

from __future__ import annotations

import logging
import re
import time
from collections.abc import Callable, Iterator
from typing import Any

import httpx

from .models import RateLimitStatus

log = logging.getLogger(__name__)

_RETRYABLE_STATUSES = frozenset({429})
_LINK_RE = re.compile(r"<(?P<url>[^>]+)>;\s*rel=\"(?P<rel>[^\"]+)\"")
_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "dora-miner-lab03",
}

Sleeper = Callable[[float], None]
WallClock = Callable[[], float]


class GitHubError(Exception):
    """Base para erros da API do GitHub."""


class GitHubHTTPError(GitHubError):
    """Erro HTTP não recuperável (ou erro de transporte após retries)."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"HTTP {status}: {message}")
        self.status = status


def parse_link_header(header: str) -> dict[str, str]:
    """Extrai ``{rel: url}`` de um cabeçalho ``Link``."""
    links: dict[str, str] = {}
    for match in _LINK_RE.finditer(header):
        links[match.group("rel")] = match.group("url")
    return links


class BaseGitHubClient:
    """Transporte compartilhado: retry com backoff e respeito ao rate limit."""

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://api.github.com",
        timeout: float = 30.0,
        max_retries: int = 5,
        backoff_base: float = 1.0,
        session: httpx.Client | None = None,
        sleeper: Sleeper | None = None,
        wall_clock: WallClock | None = None,
    ) -> None:
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._sleeper: Sleeper = sleeper or time.sleep
        self._wall_clock: WallClock = wall_clock or time.time
        self._session = session or httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={**_HEADERS, "Authorization": f"Bearer {token}"},
        )

    def close(self) -> None:
        self._session.close()

    def _sleep(self, seconds: float) -> None:
        if seconds > 0:
            log.debug("aguardando %.2fs", seconds)
            self._sleeper(seconds)

    def _wait_for_rate_limit(self, headers: Any) -> None:
        """Pausa até o reset da cota quando ``X-RateLimit-Remaining`` zera."""
        remaining = headers.get("X-RateLimit-Remaining")
        reset = headers.get("X-RateLimit-Reset")
        if remaining is None or reset is None:
            return
        if int(remaining) > 0:
            return
        wait = int(reset) + 1.0 - self._wall_clock()
        log.warning("rate limit atingido; pausando %.0fs até o reset da cota", max(wait, 0.0))
        self._sleep(max(wait, 0.0))

    @staticmethod
    def _retry_after(response: Any) -> float | None:
        """Espera indicada pelo servidor (``Retry-After``), se houver."""
        retry_after = response.headers.get("Retry-After")
        if retry_after is None:
            return None
        try:
            return float(retry_after)
        except ValueError:
            return None

    @staticmethod
    def _is_retryable(response: Any) -> bool:
        if response.status_code in _RETRYABLE_STATUSES or response.status_code >= 500:
            return True
        return response.status_code == 403 and response.headers.get("Retry-After") is not None

    def _request_with_retry(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Efetua a requisição com retry em 429/5xx e pausa por rate limit."""
        attempt = 0
        while True:
            try:
                response = self._session.request(method, url, params=params, json=json_body)
            except httpx.TransportError as exc:
                if attempt >= self._max_retries:
                    raise GitHubHTTPError(0, f"erro de transporte: {exc}") from exc
                wait = self._backoff_base * (2**attempt)
                log.warning(
                    "erro de transporte (%s); retry %d/%d em %.1fs",
                    exc,
                    attempt + 1,
                    self._max_retries,
                    wait,
                )
                self._sleep(wait)
                attempt += 1
                continue
            self._wait_for_rate_limit(response.headers)
            if not self._is_retryable(response):
                return response
            if attempt >= self._max_retries:
                raise GitHubHTTPError(response.status_code, response.text[:500])
            wait = self._retry_after(response)
            if wait is None:
                wait = self._backoff_base * (2**attempt)
            log.warning(
                "HTTP %d; retry %d/%d em %.1fs",
                response.status_code,
                attempt + 1,
                self._max_retries,
                wait,
            )
            self._sleep(wait)
            attempt += 1


class GitHubRESTClient(BaseGitHubClient):
    """Cliente REST com paginação automática pelo cabeçalho ``Link``."""

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = self._request_with_retry("GET", path, params=params)
        if response.status_code >= 400:
            raise GitHubHTTPError(response.status_code, response.text[:500])
        return response.json()

    def paginate(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """Itera por todas as páginas seguindo ``Link: rel="next"``."""
        request_params: dict[str, Any] | None = dict(params or {})
        request_params.setdefault("per_page", per_page)
        url: str | None = path
        while url is not None:
            response = self._request_with_retry("GET", url, params=request_params)
            if response.status_code >= 400:
                raise GitHubHTTPError(response.status_code, response.text[:500])
            body = response.json()
            items = body.get("items", []) if isinstance(body, dict) else body
            yield from items
            url = parse_link_header(response.headers.get("Link") or "").get("next")
            request_params = None

    def paginate_field(
        self,
        path: str,
        field: str,
        params: dict[str, Any] | None = None,
        per_page: int = 100,
    ) -> Iterator[dict[str, Any]]:
        """Itera por ``body[field]`` em respostas que são objeto, não lista.

        Necessário para endpoints como ``compare/{base}...{head}``, cujo
        corpo é ``{"commits": [...], ...}`` em vez de um array no topo.
        Segue ``Link: rel="next"`` como ``paginate``.
        """
        request_params: dict[str, Any] | None = dict(params or {})
        request_params.setdefault("per_page", per_page)
        url: str | None = path
        while url is not None:
            response = self._request_with_retry("GET", url, params=request_params)
            if response.status_code >= 400:
                raise GitHubHTTPError(response.status_code, response.text[:500])
            body = response.json()
            yield from body.get(field, [])
            url = parse_link_header(response.headers.get("Link") or "").get("next")
            request_params = None

    def rate_limit(self) -> RateLimitStatus:
        """Consulta ``GET /rate_limit`` (não consome cota)."""
        body = self.get_json("/rate_limit")
        core = body["resources"]["core"]
        return RateLimitStatus(
            limit=int(core["limit"]),
            remaining=int(core["remaining"]),
            reset_epoch=int(core["reset"]),
            resource="core",
        )

    @staticmethod
    def rate_limit_from_headers(headers: Any) -> RateLimitStatus | None:
        """Lê a cota dos cabeçalhos de qualquer resposta autenticada."""
        if "X-RateLimit-Remaining" not in headers:
            return None
        return RateLimitStatus(
            limit=int(headers["X-RateLimit-Limit"]),
            remaining=int(headers["X-RateLimit-Remaining"]),
            reset_epoch=int(headers["X-RateLimit-Reset"]),
        )
