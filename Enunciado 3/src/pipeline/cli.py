"""Interface de linha de comando do pipeline (entrada única).

Subcomandos: collect, metrics, report.
Lê config.toml, gerencia variável de ambiente GITHUB_TOKEN e configura logging estruturado.
"""

import argparse
import csv
import json
import logging
import os
import random
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any
from urllib.parse import unquote

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # Para compatibilidade com Python < 3.11, se necessário. O projeto usa 3.12+ (uv.lock)

from cache.sqlite_store import SQLiteStore
from collector.commits import collect_commits_between
from collector.releases import collect_releases
from collector.runs import collect_runs
from collector.search import collect_candidates, load_candidate_manifest
from collector.tags import collect_tags
from github.models import Release
from github.rest import GitHubRESTClient
from metrics import (
    DORAClassification,
    DORAVariant,
    censored_proportion,
    cfr_a,
    classify_dora,
    deployment_frequency,
    kaplan_meier_recovery,
    lead_time_by_commit,
    lead_time_by_release,
    median_recovery_hours,
    recovery_episodes,
    spearman_correlation,
)
from metrics.deployment_frequency import ReleaseInfo
from metrics.lead_time import ReleaseCommits
from metrics.recovery import WorkflowRunSample

log = logging.getLogger(__name__)


class TokenPool:
    """Pool rotativo de tokens GitHub para distribuir carga e aumentar quota."""

    def __init__(self, tokens: list[str]) -> None:
        if not tokens:
            raise ValueError("TokenPool requer pelo menos um token")
        self._tokens = tokens
        self._index = 0
        self._lock = threading.Lock()

    def get(self) -> str:
        with self._lock:
            token = self._tokens[self._index]
            self._index = (self._index + 1) % len(self._tokens)
            return token

    def __len__(self) -> int:
        return len(self._tokens)


def _create_token_pool(config: dict, env_token: str) -> TokenPool:
    """Cria pool de tokens a partir de config.toml ou variáveis de ambiente."""
    api_cfg = config.get("api", {})
    tokens: list[str] = []

    # 1. tokens do config.toml (array)
    if "tokens" in api_cfg and api_cfg["tokens"]:
        tokens.extend(api_cfg["tokens"])

    # 2. GITHUB_TOKENS do ambiente (separados por vírgula)
    env_tokens = os.getenv("GITHUB_TOKENS", "").strip()
    if env_tokens:
        tokens.extend([t.strip() for t in env_tokens.split(",") if t.strip()])

    # 3. GITHUB_TOKEN do ambiente (fallback)
    if env_token:
        tokens.append(env_token)

    if not tokens:
        raise ValueError("Nenhum token GitHub configurado. Defina GITHUB_TOKEN, GITHUB_TOKENS ou api.tokens no config.toml")

    log.info("Pool de tokens criado com %d token(s)", len(tokens))
    return TokenPool(tokens)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Pipeline de mineração de métricas DORA (Lab03).",
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help="Caminho do arquivo de configuração (padrão: config.toml)",
    )
    parser.add_argument(
        "--stage",
        choices=["collect", "collect-commits", "metrics", "report"],
        help="Estágio do pipeline (collect | collect-commits | metrics | report)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite de repositórios processados (para smoke tests)",
    )
    parser.add_argument("--candidate-manifest", help="CSV versionado que congela os candidatos.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignora o cache e força a reexecução da coleta",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logging detalhado (nível DEBUG)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos adicionais")
    subparsers.add_parser("doctor", help="Valida token, config, cache e dependências")

    return parser


def configure_logging(debug: bool) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _create_client(config: dict, token: str) -> GitHubRESTClient:
    api_cfg = config["api"]
    return GitHubRESTClient(
        token=token,
        base_url=api_cfg["base_url"],
        timeout=api_cfg["request_timeout_seconds"],
        max_retries=api_cfg["max_retries"],
        backoff_base=api_cfg["backoff_base_seconds"],
    )


def _create_client_from_pool(config: dict, token_pool: TokenPool) -> GitHubRESTClient:
    """Cria cliente REST usando o próximo token do pool."""
    return _create_client(config, token_pool.get())


def _save_repo_data(gold_dir: Path, owner: str, repo: str, data: dict) -> None:
    """Salva os dados coletados de um repositório em data/gold/{owner}/{repo}.json"""
    repo_dir = gold_dir / owner
    repo_dir.mkdir(parents=True, exist_ok=True)
    output_path = repo_dir / f"{repo}.json"
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log.info("Dados salvos em %s", output_path)


def _load_gold_repos(gold_dir: Path) -> list[dict]:
    """Carrega todos os repositórios salvos em data/gold/."""
    repos = []
    for owner_dir in gold_dir.iterdir():
        if not owner_dir.is_dir():
            continue
        for repo_file in owner_dir.glob("*.json"):
            data = json.loads(repo_file.read_text(encoding="utf-8"))
            repos.append(data)
    return repos


def _load_sampled_release_tags(template_path: Path) -> dict[str, set[str]]:
    """Lê as cinco releases sorteadas por repositório do template ouro."""
    sampled: dict[str, set[str]] = {}
    with template_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            full_name = row["full_name"]
            sampled[full_name] = {
                unquote(row[f"release_url_{number}"].rsplit("/tag/", 1)[1])
                for number in range(1, 6)
                if row.get(f"release_url_{number}")
            }
    return sampled


def _run_collect_commits(config_path: str, limit: int | None, token: str) -> int:
    """Atualiza somente os compares das releases sorteadas da amostra-ouro."""
    config_path = Path(config_path)
    with config_path.open("rb") as handle:
        cfg = tomllib.load(handle)

    base = config_path.parent.resolve()
    paths_cfg = cfg["paths"]
    gold_dir = base / Path(paths_cfg["gold_dir"])
    template_path = gold_dir / "labels_template.csv"
    if not template_path.exists():
        log.error("Template da amostra-ouro não encontrado: %s", template_path)
        return 1

    sampled = _load_sampled_release_tags(template_path)
    if limit is not None:
        sampled = dict(list(sorted(sampled.items()))[:limit])
    cache_db = base / Path(paths_cfg["cache_db"])
    token_pool = _create_token_pool(cfg, token)
    max_workers = min(int(cfg["api"].get("max_workers", 4)), len(token_pool))

    def process_repo(full_name: str, selected_tags: set[str]) -> tuple[str, int]:
        owner, repo = full_name.split("/", 1)
        path = gold_dir / owner / f"{repo}.json"
        if not path.exists():
            log.error("JSON ouro ausente para %s", full_name)
            return full_name, 0
        data = json.loads(path.read_text(encoding="utf-8"))
        releases = [
            Release(**item)
            for item in data.get("releases", [])
            if not item.get("draft", False) and not item.get("prerelease", False)
        ]
        by_tag = {release.tag_name: index for index, release in enumerate(releases)}
        client = _create_client_from_pool(cfg, token_pool)
        store = SQLiteStore(cache_db)
        try:
            updated: dict[str, dict[str, Any]] = {
                item["release"]: item for item in data.get("commits_between", [])
            }
            for tag in selected_tags:
                index = by_tag.get(tag)
                if index is None:
                    log.warning("Release %s não encontrada em %s", tag, full_name)
                    continue
                pair = releases[max(index - 1, 0) : index + 1]
                comparison = collect_commits_between(
                    client, owner, repo, pair, store=store, stage="collect:commits"
                )[-1]
                updated[tag] = {
                    "release": comparison.release,
                    "previous_release": comparison.previous_release,
                    "commits": [asdict(commit) for commit in comparison.commits]
                    if comparison.commits is not None
                    else None,
                    "ignored_reason": comparison.ignored_reason,
                }
            data["commits_between"] = [
                updated.get(release.tag_name, item)
                for release, item in zip(releases, data.get("commits_between", []), strict=False)
            ]
            _save_repo_data(gold_dir, owner, repo, data)
            return full_name, len(selected_tags)
        except Exception as exc:
            log.error("Erro ao recoletar commits de %s: %s", full_name, exc)
            return full_name, 0
        finally:
            client.close()
            store.close()

    updated = 0
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="commits") as pool:
        futures = {
            pool.submit(process_repo, full_name, tags): full_name
            for full_name, tags in sampled.items()
        }
        for future in as_completed(futures):
            _, count = future.result()
            updated += count
    log.info("Recoleta de commits concluída: %d releases da amostra atualizadas", updated)
    return 0


def _run_collect(
    config_path: str, limit: int | None, token: str, force: bool = False,
    candidate_manifest: str | None = None,
) -> int:
    """Executa o estágio de coleta (T04 + T05) com paralelismo e pool de tokens."""
    config_path = Path(config_path)
    with open(config_path, "rb") as handle:
        cfg = tomllib.load(handle)

    base = config_path.parent.resolve()
    paths_cfg = cfg["paths"]
    gold_dir = base / Path(paths_cfg["gold_dir"])
    gold_dir.mkdir(parents=True, exist_ok=True)

    filters_cfg = cfg["filters"]
    min_releases = filters_cfg["min_releases"]
    min_workflow_runs = filters_cfg["min_workflow_runs"]

    window_cfg = cfg["window"]
    start_date = window_cfg["start"]
    end_date = window_cfg["end"]

    api_cfg = cfg["api"]
    max_workers = int(api_cfg.get("max_workers", 4))

    cache_db = base / Path(paths_cfg["cache_db"])
    store = SQLiteStore(cache_db) if not force else None

    # Criar pool de tokens
    token_pool = _create_token_pool(cfg, token)

    # 1. Buscar candidatos (usa primeiro token do pool)
    manifest_path = candidate_manifest or paths_cfg.get("candidate_manifest_csv")
    if manifest_path:
        candidates = load_candidate_manifest(base / Path(manifest_path))
        log.info("Carregados %d candidatos do manifesto", len(candidates))
    else:
        log.info("Iniciando busca de candidatos...")
        search_client = _create_client_from_pool(cfg, token_pool)
        candidates = collect_candidates(search_client, config_path, limit=limit, store=store, stage="collect:search")
        search_client.close()

    if limit is not None:
        candidates = candidates[:limit]
        log.info("Limite aplicado: %d candidatos", limit)

    log.info("Total de candidatos: %d", len(candidates))
    log.info("Iniciando processamento paralelo com %d workers e %d token(s)", max_workers, len(token_pool))

    reports_dir = base / Path(paths_cfg.get("reports_dir", "reports"))
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Contadores thread-safe
    processed = 0
    skipped = 0
    funnel_stats = {
        "candidates": len(candidates),
        "few_releases": 0,
        "no_actions": 0,
        "few_runs": 0,
        "error": 0,
        "ok": 0,
    }
    counters_lock = threading.Lock()

    def process_repo(candidate) -> tuple[str, str, int, int, str]:
        """Processa um único repositório. Retorna (owner, repo, processed_delta, skipped_delta, reason)."""
        owner, repo = candidate.full_name.split("/", 1)
        repo_file = gold_dir / owner / f"{repo}.json"
        if repo_file.exists() and not force:
            log.info("Repositório %s/%s já coletado em %s (pulando re-coleta)", owner, repo, repo_file)
            return owner, repo, 1, 0, "ok"

        log.info("Processando %s/%s...", owner, repo)

        # Cada thread cria seu próprio cliente com token do pool
        repo_client = _create_client_from_pool(cfg, token_pool)
        local_store = SQLiteStore(cache_db) if not force else None

        try:
            # 2. Coletar releases
            releases = collect_releases(
                repo_client,
                owner,
                repo,
                store=local_store,
                stage="collect:releases",
            )

            principal_releases = [
                r for r in releases if not r.draft and not r.prerelease
            ]
            releases_in_window = [
                r for r in principal_releases if _eligible_release(r, start_date, end_date)
            ]
            if len(releases_in_window) < min_releases:
                log.info(
                    "Repositório %s/%s ignorado: apenas %d releases na janela (mínimo %d)",
                    owner, repo, len(releases_in_window), min_releases
                )
                return owner, repo, 0, 1, "few_releases"

            # 3. Coletar tags
            tags = collect_tags(
                repo_client,
                owner,
                repo,
                max_workers=4,
                store=local_store,
                stage="collect:tags",
            )

            # 4. Coletar workflow runs (ANTES dos commits - filtro barato)
            runs_by_month = collect_runs(
                repo_client,
                owner,
                repo,
                candidate.default_branch,
                start_date,
                end_date,
                store=local_store,
                stage="collect:runs",
            )

            # Contar total de runs válidos
            total_runs = sum(len(runs) for runs in runs_by_month.values())

            if total_runs == 0:
                log.info("Repositório %s/%s ignorado: sem runs válidos na janela", owner, repo)
                return owner, repo, 0, 1, "no_actions"

            if total_runs < min_workflow_runs:
                log.info(
                    "Repositório %s/%s ignorado: apenas %d runs válidos (mínimo %d)",
                    owner, repo, total_runs, min_workflow_runs
                )
                return owner, repo, 0, 1, "few_runs"

            # 5. Coletar commits entre releases consecutivas (só se passou no filtro)
            commits_between = collect_commits_between(
                repo_client,
                owner,
                repo,
                _commit_scope(principal_releases, start_date, end_date),
                store=local_store,
                stage="collect:commits",
            )

            # 6. Salvar dados em gold
            repo_data = {
                "repository": {
                    "full_name": candidate.full_name,
                    "stars": candidate.stars,
                    "language": candidate.language,
                    "default_branch": candidate.default_branch,
                    "created_at": candidate.created_at,
                },
                "releases": [asdict(r) for r in releases],
                "tags": [asdict(t) for t in tags],
                "commits_between": [
                    {
                        "release": cb.release,
                        "previous_release": cb.previous_release,
                        "commits": [asdict(c) for c in cb.commits] if cb.commits is not None else None,
                        "ignored_reason": cb.ignored_reason,
                    }
                    for cb in commits_between
                ],
                "runs_by_month": {
                    month: [asdict(r) for r in runs]
                    for month, runs in runs_by_month.items()
                },
            }

            _save_repo_data(gold_dir, owner, repo, repo_data)
            return owner, repo, 1, 0, "ok"

        except Exception as exc:
            log.error("Erro ao processar %s/%s: %s", owner, repo, exc)
            return owner, repo, 0, 1, "error"
        finally:
            repo_client.close()
            if local_store:
                local_store.close()

    # Processamento paralelo
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="collect") as pool:
        future_to_candidate = {pool.submit(process_repo, c): c for c in candidates}

        for future in as_completed(future_to_candidate):
            owner, repo, p_delta, s_delta, reason = future.result()
            with counters_lock:
                processed += p_delta
                skipped += s_delta
                funnel_stats[reason] += 1

            # Log de progresso periódico
            with counters_lock:
                total_done = processed + skipped
                if total_done % 10 == 0 or total_done == len(candidates):
                    log.info("Progresso: %d/%d concluídos (%d processados, %d ignorados)",
                             total_done, len(candidates), processed, skipped)

    log.info("Coleta concluída: %d repositórios processados, %d ignorados", processed, skipped)
    # Log da última execução do collect. O funil oficial (reports/funnel.md) é gerado
    # pelo estágio report a partir do snapshot versionado (ver snapshot_funnel).
    funnel_md = reports_dir / "funnel_collect.md"
    write_funnel_report(
        funnel_md,
        total_candidates=funnel_stats["candidates"],
        few_releases=funnel_stats["few_releases"],
        no_actions=funnel_stats["no_actions"],
        few_runs=funnel_stats["few_runs"],
        final_sample=funnel_stats["ok"],
    )
    log.info("Funil de seleção salvo em %s", funnel_md)
    store.close()
    return 0


def write_funnel_report(
    funnel_path: Path,
    total_candidates: int,
    few_releases: int,
    no_actions: int,
    few_runs: int,
    final_sample: int,
) -> None:
    """Gera tabela do funil de seleção de repositórios em Markdown com contagens reais."""
    funnel_path.parent.mkdir(parents=True, exist_ok=True)
    after_releases = max(0, total_candidates - few_releases)
    after_actions = max(0, after_releases - no_actions)
    after_runs = max(0, after_actions - few_runs)

    content = (
        "# Funil de Seleção de Repositórios\n\n"
        "Este documento registra as etapas do processo de seleção da amostra de repositórios para o cálculo das métricas DORA.\n\n"
        "| Etapa | Filtro Aplicado | Motivo de Descarte | Sobras (Contagem Real) |\n"
        "|---|---|---|---|\n"
        f"| **1. Candidatos Iniciais** | Repositórios open-source extraídos via Search API (agrupados por estrelas) | - | {total_candidates} |\n"
        f"| **2. ≥ 5 Releases** | Histórico mínimo de entregas (`config.toml: min_releases`) | Repositório possui menos de 5 releases publicadas na janela de observação ({few_releases} descartados). | {after_releases} |\n"
        f"| **3. Com Actions** | Filtragem de repositórios que utilizam o GitHub Actions (`/actions/runs`) | Repositório não possui workflow runs válidos na janela de observação ({no_actions} descartados). | {after_actions} |\n"
        f"| **4. ≥ 50 Runs** | Histórico mínimo de execuções de CI/CD (`config.toml: min_workflow_runs`) | Repositório possui menos de 50 execuções válidas de workflow disparadas por push no default branch ({few_runs} descartados). | {after_runs} |\n"
        f"| **5. Amostra Final** | Conjunto final validado para o cálculo das métricas DORA | (Nenhum, compõem o dataset final) | {final_sample} |\n"
    )
    funnel_path.write_text(content, encoding="utf-8")


def snapshot_funnel(
    gold_dir: Path,
    candidates_csv: Path,
    manifest_csv: Path | None,
    metrics_csv: Path,
    window_start: str,
    window_end: str,
    min_releases: int,
    min_workflow_runs: int,
) -> dict[str, int]:
    """Contagens do funil a partir do snapshot local (JSONs em gold + manifesto + metrics.csv).

    Ordem do ENUNCIADO §4/§7: usa Actions → ≥ min_releases → ≥ min_workflow_runs.
    Runs válidos: ``event=push`` no default branch (como em create_candidate_manifest).
    """
    def _rows(path: Path | None) -> int:
        if path is None or not path.exists():
            return 0
        with path.open(encoding="utf-8") as handle:
            return max(0, sum(1 for _ in handle) - 1)

    counts = {"no_actions": 0, "few_releases": 0, "few_runs": 0, "eligible": 0, "collected": 0}
    for path in gold_dir.rglob("*.json"):
        if path.parent == gold_dir or path.parent.name == "dossiers":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        repository = payload.get("repository", {})
        if not isinstance(repository.get("full_name"), str):
            continue
        counts["collected"] += 1
        branch = repository.get("default_branch")
        runs = [
            run
            for month in payload.get("runs_by_month", {}).values()
            for run in month
            if run.get("branch") == branch and run.get("event") == "push"
        ]
        releases = [
            r for r in payload.get("releases", []) if _eligible_release(r, window_start, window_end)
        ]
        if not runs:
            counts["no_actions"] += 1
        elif len(releases) < min_releases:
            counts["few_releases"] += 1
        elif len(runs) < min_workflow_runs:
            counts["few_runs"] += 1
        else:
            counts["eligible"] += 1
    counts["candidates"] = _rows(candidates_csv)
    counts["manifest"] = _rows(manifest_csv)
    counts["final"] = _rows(metrics_csv)
    return counts


def lead_time_coverage(
    gold_dir: Path, names: list[str], window_start: str, window_end: str
) -> dict[str, int]:
    """Quantas releases da janela entram no lead time e por que as demais ficam de fora.

    ENUNCIADO §11: releases com compare 404 são ignoradas e contadas.
    """
    counts: dict[str, int] = {"releases": 0, "used": 0, "no_new_commits": 0}
    for name in names:
        owner, repo = name.split("/", 1)
        path = gold_dir / owner / f"{repo}.json"
        if not path.exists():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        window = {
            r["tag_name"]
            for r in payload.get("releases", [])
            if _eligible_release(r, window_start, window_end)
        }
        for item in payload.get("commits_between", []):
            if item.get("release") not in window:
                continue
            counts["releases"] += 1
            reason = item.get("ignored_reason")
            if reason:
                counts[reason] = counts.get(reason, 0) + 1
            elif not item.get("commits"):
                counts["no_new_commits"] += 1
            else:
                counts["used"] += 1
    return counts


def write_snapshot_funnel_report(
    funnel_path: Path, counts: dict[str, int], min_releases: int, min_workflow_runs: int
) -> None:
    """Escreve reports/funnel.md com as contagens de ``snapshot_funnel``."""
    after_actions = counts["collected"] - counts["no_actions"]
    after_releases = after_actions - counts["few_releases"]
    not_collected = counts["candidates"] - counts["collected"]
    rows = [
        ("1. Resultados da busca", "Search API, 12 faixas de estrelas (máx. 1.000 por consulta)",
         "—", counts["candidates"]),
        ("2. Coletados", "JSON de releases, tags, commits e runs salvo em `data/gold/`",
         f"{not_collected} não persistidos: descartados no collect (sem Actions, poucas releases "
         "ou poucos runs) ou não visitados; o snapshot não guarda o motivo por repositório",
         counts["collected"]),
        ("3. Com Actions", "≥ 1 workflow run `push` no default branch na janela",
         f"{counts['no_actions']} sem runs válidos", after_actions),
        (f"4. ≥ {min_releases} releases", "releases publicadas (não-draft, não-pré-release) na janela",
         f"{counts['few_releases']} com poucas releases", after_releases),
        (f"5. ≥ {min_workflow_runs} runs", "runs `push` no default branch na janela",
         f"{counts['few_runs']} com poucos runs", counts["eligible"]),
        ("6. Manifesto", "população congelada (`candidate_manifest.csv`, seed 42)",
         f"{counts['eligible'] - counts['manifest']} fora do corte", counts["manifest"]),
        ("7. Amostra final", "corte determinístico do estágio `metrics` (seed 42)",
         f"{counts['manifest'] - counts['final']} fora do corte", counts["final"]),
    ]
    lines = [
        "# Funil de seleção de repositórios",
        "",
        "Gerado por `python -m pipeline --stage report` a partir do snapshot versionado; não edite à mão.",
        "",
        "| Etapa | Critério | Descartados | Restantes |",
        "|---|---|---|---:|",
        *[f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows],
        "",
    ]
    funnel_path.parent.mkdir(parents=True, exist_ok=True)
    funnel_path.write_text("\n".join(lines), encoding="utf-8")


def _in_window(timestamp: str | None, start: str, end: str) -> bool:
    """True se a data (ISO-8601) está dentro da janela [start, end], inclusiva."""
    if not timestamp:
        return False
    return start <= timestamp[:10] <= end


def _eligible_release(release: Any, start: str, end: str) -> bool:
    """Return whether a release belongs to the principal DORA definition."""
    if isinstance(release, dict):
        published_at = release.get("published_at")
        draft = release.get("draft", False)
        prerelease = release.get("prerelease", False)
    else:
        published_at = getattr(release, "published_at", None)
        draft = getattr(release, "draft", False)
        prerelease = getattr(release, "prerelease", False)
    return not draft and not prerelease and _in_window(published_at, start, end)


def _commit_scope(releases: list, start: str, end: str) -> list:
    """Releases na janela mais a release anterior (necessária para o compare).

    A release anterior pode estar fora da janela (ENUNCIADO §5); se a primeira
    release da janela for a primeira da história, ela continua sendo ignorada.
    """
    in_window = [i for i, r in enumerate(releases) if _in_window(r.published_at, start, end)]
    if not in_window:
        return []
    return releases[max(in_window[0] - 1, 0): in_window[-1] + 1]


def _paired(rows: list[dict], x_key: str, y_key: str) -> tuple[list[float], list[float]]:
    """Pares (x, y) do MESMO repositório, descartando os que têm valor ausente."""
    pairs = [
        (row[x_key], row[y_key])
        for row in rows
        if row[x_key] is not None and row[y_key] is not None
    ]
    return [p[0] for p in pairs], [p[1] for p in pairs]


DORA_VARIANT_COLUMNS = [
    "full_name", "stars", "language",
    "lead_time_hours", "cfr", "recovery_hours",
    "deployment_frequency_per_week", "dora_category",
]


def _dora_to_dict(classification: DORAClassification) -> dict:
    """Serializa a classificação DORA incluindo a categoria (método, não campo)."""
    data = asdict(classification)
    data["variant"] = classification.variant.value
    data["category"] = classification.category()
    return data


def _run_metrics(config_path: str) -> int:
    """Executa o estágio de cálculo de métricas."""
    config_path = Path(config_path)
    with open(config_path, "rb") as handle:
        cfg = tomllib.load(handle)

    base = config_path.parent.resolve()
    paths_cfg = cfg["paths"]
    gold_dir = base / Path(paths_cfg["gold_dir"])
    datasets_dir = base / Path(paths_cfg["datasets_dir"])
    datasets_dir.mkdir(parents=True, exist_ok=True)

    window_cfg = cfg["window"]
    window_weeks = window_cfg["weeks"]
    window_start = window_cfg["start"]
    window_end = window_cfg["end"]
    min_releases = cfg["filters"]["min_releases"]
    min_workflow_runs = cfg["filters"]["min_workflow_runs"]
    final_sample_size = int(cfg["filters"].get("final_sample_size", 0))

    repos = _load_gold_repos(gold_dir)
    manifest_path = paths_cfg.get("candidate_manifest_csv")
    if manifest_path:
        manifest = load_candidate_manifest(base / Path(manifest_path))
        allowed_names = {candidate.full_name for candidate in manifest}
        repos = [repo for repo in repos if repo["repository"]["full_name"] in allowed_names]
    log.info("Carregados %d repositórios de %s", len(repos), gold_dir)

    if not repos:
        log.warning("Nenhum repositório encontrado em gold. Rode 'collect' primeiro.")
        return 0

    discarded = 0

    # Resultados por repositório
    repo_metrics: list[dict] = []

    for repo_data in repos:
        repo_info = repo_data["repository"]
        full_name = repo_info["full_name"]
        log.info("Calculando métricas para %s...", full_name)

        # Só entram releases, tags e runs publicados dentro da janela (ENUNCIADO §3)
        releases = [
            r for r in repo_data["releases"]
            if _eligible_release(r, window_start, window_end)
        ]
        tags = [
            t for t in repo_data["tags"]
            if _in_window(t.get("date"), window_start, window_end)
        ]
        window_tags = {r["tag_name"] for r in releases}
        commits_between = [
            cb for cb in repo_data["commits_between"] if cb["release"] in window_tags
        ]
        runs_by_month = repo_data["runs_by_month"]

        total_runs = sum(len(runs) for runs in runs_by_month.values())
        if len(releases) < min_releases or total_runs < min_workflow_runs:
            log.info(
                "Repositório %s descartado: %d releases e %d runs na janela (mínimos %d/%d)",
                full_name, len(releases), total_runs, min_releases, min_workflow_runs,
            )
            discarded += 1
            continue

        # Preparar dados para lead_time
        release_commits_a: list[ReleaseCommits] = []
        release_commits_b: list[ReleaseCommits] = []

        for cb in commits_between:
            if cb["ignored_reason"] is not None:
                continue  # Ignora primeira release ou compare 404
            if not cb["commits"]:
                continue  # Release sem commits novos
            published_at = next(
                (r["published_at"] for r in releases if r["tag_name"] == cb["release"]),
                None,
            )
            if published_at is None:
                continue
            release_commit = ReleaseCommits(
                release_published_at=published_at,
                commit_dates=[c["author_date"] for c in cb["commits"]],
            )
            release_commits_a.append(release_commit)
            release_commits_b.append(release_commit)

        # Lead time variante (a) e (b)
        lt_a = lead_time_by_release(release_commits_a)
        lt_b = lead_time_by_commit(release_commits_b)

        # CFR(a) - coletar conclusões de todos os runs
        all_conclusions: list[str | None] = []
        for runs in runs_by_month.values():
            for run in runs:
                all_conclusions.append(run.get("conclusion"))
        cfr = cfr_a(all_conclusions)

        # Recovery episodes
        runs_flat: list[WorkflowRunSample] = []
        for runs in runs_by_month.values():
            for run in runs:
                if not run.get("run_started_at") or not run.get("updated_at"):
                    continue
                runs_flat.append(WorkflowRunSample(
                    workflow_id=run["workflow_id"],
                    conclusion=run.get("conclusion"),
                    run_started_at=run["run_started_at"],
                    updated_at=run["updated_at"],
                ))
        episodes = recovery_episodes(runs_flat, censor_at=f"{window_end}T23:59:59Z")
        recovery_hours = median_recovery_hours(episodes)
        censored_prop = censored_proportion(episodes)

        # Deployment frequency (releases only)
        release_infos = [
            ReleaseInfo(
                published_at=r["published_at"],
                draft=r.get("draft", False),
                prerelease=r.get("prerelease", False),
            )
            for r in releases
        ]
        deploy_freq = deployment_frequency(release_infos, window_weeks=window_weeks)

        # Deployment frequency (releases + tags with dates)
        tags_with_dates = [
            ReleaseInfo(published_at=t["date"], draft=False) for t in tags if t.get("date")
        ]
        deploy_freq_tags = deployment_frequency(
            release_infos + tags_with_dates,
            window_weeks=window_weeks,
        )

        # DORA classification C1, C2, C3
        dora_c1 = classify_dora(
            DORAVariant.C1, lt_a, lt_b, cfr, recovery_hours, deploy_freq, deploy_freq_tags
        )
        dora_c2 = classify_dora(
            DORAVariant.C2, lt_a, lt_b, cfr, recovery_hours, deploy_freq, deploy_freq_tags
        )
        dora_c3 = classify_dora(
            DORAVariant.C3, lt_a, lt_b, cfr, recovery_hours, deploy_freq, deploy_freq_tags
        )

        # Kaplan-Meier survival
        durations = [e.duration_hours for e in episodes if e.duration_hours is not None]
        censored = [e.censored for e in episodes if e.duration_hours is not None]
        survival = kaplan_meier_recovery(durations, censored)

        repo_result = {
            "repository": repo_info,
            "metrics": {
                "lead_time_a_hours": lt_a,
                "lead_time_b_hours": lt_b,
                "cfr_a": cfr,
                "recovery_hours": recovery_hours,
                "censored_proportion": censored_prop,
                "deployment_frequency_per_week": deploy_freq,
                "deployment_frequency_with_tags_per_week": deploy_freq_tags,
            },
            "dora_classification": {
                "C1": _dora_to_dict(dora_c1),
                "C2": _dora_to_dict(dora_c2),
                "C3": _dora_to_dict(dora_c3),
            },
            "survival": {
                "median_survival_hours": survival.median_survival,
                "confidence_interval": survival.confidence_interval,
                "n_events": survival.n_events,
                "n_censored": survival.n_censored,
                "n_total": survival.n_total,
            },
            # Mantém a unidade mínima necessária para refazer a Kaplan--Meier
            # agregada sem nova chamada à API (T19). Datas e mensagens não são
            # replicadas aqui porque já não são necessárias à análise.
            "recovery_episodes": [
                {"duration_hours": episode.duration_hours, "censored": episode.censored}
                for episode in episodes
                if episode.duration_hours is not None
            ],
        }

        repo_metrics.append(repo_result)

    if final_sample_size:
        if len(repo_metrics) < final_sample_size:
            raise ValueError(
                f"manifesto produziu {len(repo_metrics)} repositórios elegíveis; "
                f"mínimo fixado: {final_sample_size}"
            )
        repo_metrics = sorted(
            random.Random(42).sample(repo_metrics, final_sample_size),
            key=lambda item: item["repository"]["full_name"].casefold(),
        )

    log.info(
        "Funil (metrics): %d repositórios lidos, %d descartados, %d na amostra final",
        len(repos), discarded, len(repo_metrics),
    )

    # Correlações (RQ 05 e RQ 06): pares do mesmo repositório, sem valores ausentes
    correlations = {}
    metric_rows = [m["metrics"] for m in repo_metrics]
    for name, x_key, y_key in (
        ("lead_time_a_vs_cfr_a", "lead_time_a_hours", "cfr_a"),
        ("lead_time_b_vs_cfr_a", "lead_time_b_hours", "cfr_a"),
        ("deploy_freq_vs_recovery", "deployment_frequency_per_week", "recovery_hours"),
        ("deploy_freq_tags_vs_recovery", "deployment_frequency_with_tags_per_week", "recovery_hours"),
    ):
        xs, ys = _paired(metric_rows, x_key, y_key)
        if len(xs) >= 2:
            correlations[name] = asdict(spearman_correlation(xs, ys))

    # Salvar datasets
    datasets_dir.mkdir(parents=True, exist_ok=True)

    # metrics.csv
    metrics_csv = datasets_dir / "metrics.csv"
    with open(metrics_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "full_name", "stars", "language",
            "lead_time_a_hours", "lead_time_b_hours",
            "cfr_a", "recovery_hours", "censored_proportion",
            "deployment_frequency_per_week", "deployment_frequency_with_tags_per_week",
            "dora_c1_category", "dora_c2_category", "dora_c3_category",
            "survival_median_hours", "survival_n_events", "survival_n_censored",
        ])
        writer.writeheader()
        for m in repo_metrics:
            r = m["repository"]
            mt = m["metrics"]
            dc = m["dora_classification"]
            sv = m["survival"]
            writer.writerow({
                "full_name": r["full_name"],
                "stars": r["stars"],
                "language": r["language"] or "",
                "lead_time_a_hours": mt["lead_time_a_hours"],
                "lead_time_b_hours": mt["lead_time_b_hours"],
                "cfr_a": mt["cfr_a"],
                "recovery_hours": mt["recovery_hours"],
                "censored_proportion": mt["censored_proportion"],
                "deployment_frequency_per_week": mt["deployment_frequency_per_week"],
                "deployment_frequency_with_tags_per_week": mt["deployment_frequency_with_tags_per_week"],
                "dora_c1_category": dc["C1"]["category"],
                "dora_c2_category": dc["C2"]["category"],
                "dora_c3_category": dc["C3"]["category"],
                "survival_median_hours": sv["median_survival_hours"],
                "survival_n_events": sv["n_events"],
                "survival_n_censored": sv["n_censored"],
            })
    log.info("Dataset salvo em %s", metrics_csv)

    # dora_c1.csv, dora_c2.csv, dora_c3.csv (um CSV por variante de classificação)
    for variant in ("C1", "C2", "C3"):
        variant_csv = datasets_dir / f"dora_{variant.lower()}.csv"
        with open(variant_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=DORA_VARIANT_COLUMNS)
            writer.writeheader()
            for m in repo_metrics:
                r = m["repository"]
                dc = m["dora_classification"][variant]
                writer.writerow({
                    "full_name": r["full_name"],
                    "stars": r["stars"],
                    "language": r["language"] or "",
                    "lead_time_hours": dc["lead_time_hours"],
                    "cfr": dc["cfr"],
                    "recovery_hours": dc["recovery_hours"],
                    "deployment_frequency_per_week": dc["deployment_frequency_per_week"],
                    "dora_category": dc["category"],
                })
        log.info("Dataset %s salvo em %s", variant, variant_csv)

    # correlations.json
    corr_json = datasets_dir / "correlations.json"
    corr_json.write_text(
        json.dumps(correlations, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log.info("Correlações salvas em %s", corr_json)

    # metrics_full.json (detalhado)
    metrics_json = datasets_dir / "metrics_full.json"
    metrics_json.write_text(
        json.dumps(repo_metrics, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    log.info("Métricas completas salvas em %s", metrics_json)

    return 0


def _run_report(config_path: str) -> int:
    """Executa o estágio de geração de relatórios."""
    config_path = Path(config_path)
    with open(config_path, "rb") as handle:
        cfg = tomllib.load(handle)

    base = config_path.parent.resolve()
    paths_cfg = cfg["paths"]
    datasets_dir = base / Path(paths_cfg["datasets_dir"])
    reports_dir = base / Path(paths_cfg["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    metrics_csv = datasets_dir / "metrics.csv"
    corr_json = datasets_dir / "correlations.json"

    if not metrics_csv.exists():
        log.error("Arquivo %s não encontrado. Rode 'metrics' primeiro.", metrics_csv)
        return 1

    # Carregar dados
    import pandas as pd
    df = pd.read_csv(metrics_csv)
    correlations = json.loads(corr_json.read_text(encoding="utf-8")) if corr_json.exists() else {}

    # Gerar relatório Markdown
    report_md = reports_dir / "report.md"
    with open(report_md, "w", encoding="utf-8") as f:
        f.write("# Relatório de Métricas DORA\n\n")
        f.write(f"Total de repositórios analisados: {len(df)}\n\n")

        # Sumário
        f.write("## Sumário das Métricas\n\n")
        for col in ["lead_time_a_hours", "lead_time_b_hours", "cfr_a", "recovery_hours",
                    "deployment_frequency_per_week", "deployment_frequency_with_tags_per_week"]:
            if col in df.columns:
                vals = df[col].dropna()
                if not vals.empty:
                    f.write(f"- **{col}**: mediana={vals.median():.2f}, "
                            f"média={vals.mean():.2f}, min={vals.min():.2f}, max={vals.max():.2f}\n")

        f.write("\n## Classificação DORA\n\n")
        for variant in ["C1", "C2", "C3"]:
            col = f"dora_{variant.lower()}_category"
            if col in df.columns:
                counts = df[col].value_counts()
                f.write(f"### Variante {variant}\n")
                for cat, count in counts.items():
                    f.write(f"- {cat}: {count}\n")
                f.write("\n")

        # Correlações
        f.write("## Correlações (Spearman)\n\n")
        for name, result in correlations.items():
            f.write(f"- **{name}**: ρ={result['rho']:.3f}, p={result['p_value']:.4f}, "
                    f"{'significativo' if result['significant'] else 'não significativo'}\n")

        coverage = lead_time_coverage(
            base / Path(paths_cfg["gold_dir"]),
            list(df["full_name"]),
            cfg["window"]["start"],
            cfg["window"]["end"],
        )
        f.write("\n## Lead time: releases usadas e ignoradas\n\n")
        f.write("| Situação | Releases | % |\n|---|---:|---:|\n")
        total = coverage["releases"] or 1
        for key, count in sorted(coverage.items(), key=lambda kv: -kv[1]):
            if key != "releases":
                f.write(f"| `{key}` | {count} | {count / total:.1%} |\n")
        f.write(f"| **total na janela** | {coverage['releases']} | 100% |\n")

        f.write("\n---\n*Gerado automaticamente pelo pipeline DORA Miner (Lab03).*\n")

    log.info("Relatório salvo em %s", report_md)

    manifest_cfg = paths_cfg.get("candidate_manifest_csv")
    counts = snapshot_funnel(
        gold_dir=base / Path(paths_cfg["gold_dir"]),
        candidates_csv=base / Path(paths_cfg["candidates_csv"]),
        manifest_csv=base / Path(manifest_cfg) if manifest_cfg else None,
        metrics_csv=metrics_csv,
        window_start=cfg["window"]["start"],
        window_end=cfg["window"]["end"],
        min_releases=cfg["filters"]["min_releases"],
        min_workflow_runs=cfg["filters"]["min_workflow_runs"],
    )
    funnel_md = reports_dir / "funnel.md"
    write_snapshot_funnel_report(
        funnel_md, counts, cfg["filters"]["min_releases"], cfg["filters"]["min_workflow_runs"]
    )
    log.info("Funil de seleção salvo em %s", funnel_md)

    # Gerar também um CSV resumo para fácil importação
    summary_csv = reports_dir / "summary.csv"
    df.to_csv(summary_csv, index=False)
    log.info("Resumo CSV salvo em %s", summary_csv)

    return 0


def _load_env_file(env_path: Path) -> None:
    """Carrega variáveis do arquivo .env para os.environ se existir."""
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    # Se nenhum argumento for passado, exibe o help
    if argv is None and len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    configure_logging(args.debug)

    # Se nenhum stage nem command for especificado, exibe o help
    if not args.stage and not args.command:
        parser.print_help()
        return 0

    _load_env_file(Path(".env"))
    _load_env_file(Path(args.config).parent / ".env")

    # Token pode vir de GITHUB_TOKEN, GITHUB_TOKENS ou config.toml
    env_token = os.getenv("GITHUB_TOKEN")
    # Não exigimos mais GITHUB_TOKEN obrigatório se houver GITHUB_TOKENS ou config.tokens

    try:
        with open(args.config, "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo de configuração '{args.config}' não encontrado.")
        return 1
    except Exception as e:
        print(f"Erro ao ler configuração: {e}")
        return 1

    # Validar que temos pelo menos um token
    api_cfg = config.get("api", {})
    has_config_tokens = "tokens" in api_cfg and api_cfg["tokens"]
    has_env_tokens = bool(os.getenv("GITHUB_TOKENS", "").strip())
    has_single_token = bool(env_token)

    if not (has_config_tokens or has_env_tokens or has_single_token):
        print("Erro: Nenhum token GitHub configurado.")
        print("Opções:")
        print("  1. export GITHUB_TOKEN='seu_token'")
        print("  2. export GITHUB_TOKENS='token1,token2,token3'")
        print("  3. Adicionar 'tokens = [\"token1\", \"token2\"]' em [api] no config.toml")
        return 1

    if args.command == "doctor":
        log.info("Ambiente validado com sucesso. Token e config presentes.")
        return 0

    if args.stage == "collect":
        log.info("Iniciando pipeline, estágio: collect")
        if args.limit:
            log.info("Limite ativado: processando no máximo %d repositório(s).", args.limit)
        if args.force:
            log.info("Modo --force ativado: ignorando cache.")
        return _run_collect(args.config, args.limit, env_token or "", args.force, args.candidate_manifest)

    if args.stage == "collect-commits":
        log.info("Iniciando pipeline, estágio: collect-commits")
        return _run_collect_commits(args.config, args.limit, env_token or "")

    if args.stage == "metrics":
        log.info("Iniciando pipeline, estágio: metrics")
        return _run_metrics(args.config)

    if args.stage == "report":
        log.info("Iniciando pipeline, estágio: report")
        return _run_report(args.config)

    # TODO: Implementar estágios adicionais
    print(f"[pipeline] estágio '{args.stage}' configurado e pronto (implementação pendente).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
