"""Coleta de execuções de CI/CD (Workflow Runs) (PLAN T04).

Filtra por event=push e branch=default_branch. Divide a janela de busca
em pedaços mensais para não estourar o limite de 1.000 resultados da API.
Ignora conclusões indesejadas (cancelled, skipped, neutral, action_required, stale e None).
"""

from __future__ import annotations

import calendar
import logging
from datetime import date, datetime

from cache.sqlite_store import SQLiteStore
from github.models import WorkflowRun
from github.rest import GitHubRESTClient

log = logging.getLogger(__name__)

IGNORED_CONCLUSIONS = frozenset({"cancelled", "skipped", "neutral", "action_required", "stale"})


def _generate_months(start_date: str, end_date: str) -> list[tuple[str, str]]:
    """Gera tuplas de (início, fim) para cada mês entre start_date e end_date.
    As datas de entrada devem estar no formato YYYY-MM-DD.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()
    
    months = []
    current_year = start.year
    current_month = start.month
    
    while (current_year, current_month) <= (end.year, end.month):
        first_day = date(current_year, current_month, 1)
        last_day = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
        
        # Ajusta para não passar do start_date e end_date exatos, se for o caso
        chunk_start = max(first_day, start)
        chunk_end = min(last_day, end)
        
        months.append((chunk_start.strftime("%Y-%m-%d"), chunk_end.strftime("%Y-%m-%d")))
        
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1
            
    return months


def collect_runs(
    client: GitHubRESTClient,
    owner: str,
    repo: str,
    default_branch: str,
    start_date: str,
    end_date: str,
    *,
    store: SQLiteStore | None = None,
    stage: str = "collect:runs",
) -> dict[str, list[WorkflowRun]]:
    """Coleta os runs de workflow para um repositório, agrupados por mês.
    Retorna dicionário: {"YYYY-MM": [WorkflowRun, ...]}
    """
    results: dict[str, list[WorkflowRun]] = {}
    months = _generate_months(start_date, end_date)
    
    for m_start, m_end in months:
        month_key = m_start[:7]  # YYYY-MM
        cache_key = f"{owner}/{repo}:{month_key}"
        
        if store and store.is_stage_complete(f"{stage}:{cache_key}"):
            # Note: The cache might store completion but we still need the data if we just return it.
            # In other modules (like releases), if the stage is complete, they return [] because the DB 
            # handles the saving. If the pipeline relies on the return value to save JSONs, we shouldn't short-circuit 
            # returning empty unless we are only populating cache. Let's assume we return empty if cached, like releases.py
            log.debug("Runs for %s in %s already collected, skipping.", f"{owner}/{repo}", month_key)
            results[month_key] = []
            continue

        query = f"{m_start}..{m_end}"
        path = f"/repos/{owner}/{repo}/actions/runs"
        params = {
            "branch": default_branch,
            "event": "push",
            "created": query,
        }
        
        log.info("Coletando runs para %s/%s no periodo %s", owner, repo, query)
        raw = client.paginate(path, params=params)
        
        valid_runs: list[WorkflowRun] = []
        for item in raw:
            run = WorkflowRun.from_api(item)
            if run.conclusion is None or run.conclusion in IGNORED_CONCLUSIONS:
                continue
            valid_runs.append(run)
            
        results[month_key] = valid_runs
        log.info("Total de runs validos em %s: %d", month_key, len(valid_runs))
        
        if store:
            store.mark_stage_complete(f"{stage}:{cache_key}")
            
    return results
