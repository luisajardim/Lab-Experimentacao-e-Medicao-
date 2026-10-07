"""Coleta de candidatos a repositórios via ``GET /search/repositories`` (PLAN T04).

Fatia a busca por faixa de estrelas e, opcionalmente, por linguagem,
respeitando o limite de 1.000 resultados por query do GitHub. Para cada
query o paginador do ``GitHubRESTClient`` percorre todas as páginas
automaticamente. A coleta para quando atinge ``max_candidates``.

Resultados são salvos em ``candidates_csv`` e cada query usada é
registrada em ``meta/search_queries/``.
"""

from __future__ import annotations

import csv
import logging
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cache.cached_session import CachedSession
from cache.sqlite_store import SQLiteStore
from github.rest import GitHubRESTClient

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Candidate:
    """Repositório candidato retornado pela busca de repositórios."""

    full_name: str
    stars: int
    language: str | None
    default_branch: str
    created_at: str


def _build_queries(star_slices: list[str], languages: list[str]) -> list[str]:
    queries: list[str] = []
    for slice_ in star_slices:
        base = f"stars:{slice_}"
        if languages:
            for lang in languages:
                queries.append(f"{base}+language:{lang}")
        else:
            queries.append(base)
    return queries


def _item_to_candidate(item: dict[str, Any]) -> Candidate:
    return Candidate(
        full_name=item["full_name"],
        stars=int(item["stargazers_count"]),
        language=item.get("language"),
        default_branch=item.get("default_branch", "main"),
        created_at=item.get("created_at", ""),
    )


def _ensure_dirs(paths: dict[str, Path]) -> None:
    for key in ("raw_dir", "meta_dir"):
        paths[key].mkdir(parents=True, exist_ok=True)


def _write_csv(candidates: list[Candidate], csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["full_name", "stars", "language", "default_branch", "created_at"],
        )
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "full_name": candidate.full_name,
                    "stars": candidate.stars,
                    "language": candidate.language or "",
                    "default_branch": candidate.default_branch,
                    "created_at": candidate.created_at,
                }
            )


def _record_query(queries_dir: Path, idx: int, query: str, count: int) -> None:
    queries_dir.mkdir(parents=True, exist_ok=True)
    path = queries_dir / f"query_{idx:03d}.txt"
    path.write_text(f"query={query}\ncount={count}\n", encoding="utf-8")


def _collect_one_query(
    query: str,
    per_page: int,
    max_candidates: int,
    session: Any,
    queries_dir: Path,
    idx: int,
) -> list[Candidate]:
    """Coleta uma query de busca e retorna a lista de candidatos encontrados."""
    local_seen: set[str] = set()
    local_candidates: list[Candidate] = []
    count = 0
    for item in session.paginate(
        "/search/repositories",
        params={"q": query, "per_page": per_page},
    ):
        if not item:
            continue
        full_name = item.get("full_name", "")
        if full_name in local_seen:
            continue
        local_seen.add(full_name)
        local_candidates.append(_item_to_candidate(item))
        count += 1
        if len(local_candidates) >= max_candidates:
            break
    _record_query(queries_dir, idx, query, count)
    return local_candidates


def collect_candidates(
    client: GitHubRESTClient,
    config_path: str | Path = "config.toml",
    *,
    store: SQLiteStore | None = None,
    stage: str = "collect:search",
    max_workers: int = 4,
) -> list[Candidate]:
    """Busca repositórios candidatos seguindo ``config.toml``.

    Args:
        client: cliente REST autenticado.
        config_path: caminho do ``config.toml`` (default: atual).
        store: cache SQLite opcional.
        stage: nome do estágio para cache/resumo.
        max_workers: threads paralelas para queries.

    Returns:
        Lista de ``Candidate`` única (deduplicada por ``full_name``),
        limitada a ``max_candidates``.
    """
    config_path = Path(config_path)
    with open(config_path, "rb") as handle:
        cfg = tomllib.load(handle)

    base = config_path.parent.resolve()
    search_cfg = cfg["search"]
    star_slices: list[str] = search_cfg["star_slices"]
    languages: list[str] = search_cfg.get("languages", [])
    max_candidates: int = int(search_cfg.get("max_candidates", 4000))
    per_page: int = int(search_cfg.get("per_page", 100))

    paths_cfg = cfg["paths"]
    raw_dir = base / Path(paths_cfg["raw_dir"])
    meta_dir = base / Path(paths_cfg["meta_dir"])
    candidates_csv = base / Path(paths_cfg["candidates_csv"])

    _ensure_dirs({"raw_dir": raw_dir, "meta_dir": meta_dir})

    if store and store.is_stage_complete(stage):
        log.info("%s já concluído; pulando coleta", stage)
        _write_csv([], candidates_csv)
        return []

    queries = _build_queries(star_slices, languages)
    seen: set[str] = set()
    candidates: list[Candidate] = []
    queries_dir = meta_dir / "search_queries"

    if store:
        client = GitHubRESTClient(
            token=client._session.headers.get("Authorization", "").replace("Bearer ", ""),
            session=CachedSession(client._session, store, stage),
            max_retries=client._max_retries,
            backoff_base=client._backoff_base,
            sleeper=client._sleep,
            wall_clock=client._wall_clock,
        )

    query_results: list[list[Candidate]] = [[] for _ in queries]
    future_to_idx: dict[Any, int] = {}
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="search") as pool:
        for idx, query in enumerate(queries):
            if len(candidates) >= max_candidates:
                break
            future = pool.submit(
                _collect_one_query,
                query,
                per_page,
                max_candidates,
                client,
                queries_dir,
                idx,
            )
            future_to_idx[future] = idx

        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                query_results[idx] = future.result()
            except Exception as exc:
                log.error("query %d (%s) falhou: %s", idx, queries[idx], exc)

    for query_candidates in query_results:
        for candidate in query_candidates:
            if candidate.full_name in seen:
                continue
            seen.add(candidate.full_name)
            candidates.append(candidate)
            if len(candidates) >= max_candidates:
                break
        if len(candidates) >= max_candidates:
            break

    if store:
        for candidate in candidates:
            store.record_signature(stage, candidate.full_name, str(candidate.stars))
        store.mark_stage_complete(stage)
        store.write_staleness_report(
            base / paths_cfg["reports_dir"] / "staleness_search.json",
            stage,
            {c.full_name: str(c.stars) for c in candidates},
        )

    _write_csv(candidates, candidates_csv)
    return candidates
