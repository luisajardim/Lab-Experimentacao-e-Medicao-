"""Interface de linha de comando do pipeline (entrada única).

Subcomandos: collect, metrics, report.
Lê config.toml, gerencia variável de ambiente GITHUB_TOKEN e configura logging estruturado.
"""

import argparse
import csv
import json
import logging
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # Para compatibilidade com Python < 3.11, se necessário. O projeto usa 3.12+ (uv.lock)

from cache.sqlite_store import SQLiteStore
from collector.commits import collect_commits_between
from collector.releases import collect_releases
from collector.runs import collect_runs
from collector.search import collect_candidates
from collector.tags import collect_tags
from github.rest import GitHubRESTClient
from metrics import (
    DORAClassification,
    DORAVariant,
    censored_proportion,
    classify_dora,
    cfr_a,
    deployment_frequency,
    kaplan_meier_recovery,
    lead_time_by_commit,
    lead_time_by_release,
    median_recovery_hours,
    recovery_episodes,
    spearman_correlation,
)

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
        choices=["collect", "metrics", "report"],
        help="Estágio do pipeline (collect | metrics | report)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limite de repositórios processados (para smoke tests)",
    )
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


def _run_collect(config_path: str, limit: int | None, token: str, force: bool = False) -> int:
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
    log.info("Iniciando busca de candidatos...")
    search_client = _create_client_from_pool(cfg, token_pool)
    candidates = collect_candidates(
        search_client,
        config_path,
        store=store,
        stage="collect:search",
    )
    search_client.close()

    if limit is not None:
        candidates = candidates[:limit]
        log.info("Limite aplicado: %d candidatos", limit)

    log.info("Total de candidatos: %d", len(candidates))
    log.info("Iniciando processamento paralelo com %d workers e %d token(s)", max_workers, len(token_pool))

    # Contadores thread-safe
    processed = 0
    skipped = 0
    counters_lock = threading.Lock()

    def process_repo(candidate) -> tuple[str, str, int, int]:
        """Processa um único repositório. Retorna (owner, repo, processed_delta, skipped_delta)."""
        owner, repo = candidate.full_name.split("/", 1)
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

            if len(releases) < min_releases:
                log.info(
                    "Repositório %s/%s ignorado: apenas %d releases (mínimo %d)",
                    owner, repo, len(releases), min_releases
                )
                return owner, repo, 0, 1

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

            if total_runs < min_workflow_runs:
                log.info(
                    "Repositório %s/%s ignorado: apenas %d runs válidos (mínimo %d)",
                    owner, repo, total_runs, min_workflow_runs
                )
                return owner, repo, 0, 1

            # 5. Coletar commits entre releases consecutivas (só se passou no filtro)
            commits_between = collect_commits_between(
                repo_client,
                owner,
                repo,
                releases,
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
                        "commits": [asdict(c) for c in cb.commits] if cb.commits else None,
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
            return owner, repo, 1, 0

        except Exception as exc:
            log.error("Erro ao processar %s/%s: %s", owner, repo, exc)
            return owner, repo, 0, 1
        finally:
            repo_client.close()
            if local_store:
                local_store.close()

    # Processamento paralelo
    with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="collect") as pool:
        future_to_candidate = {pool.submit(process_repo, c): c for c in candidates}

        for future in as_completed(future_to_candidate):
            owner, repo, p_delta, s_delta = future.result()
            with counters_lock:
                processed += p_delta
                skipped += s_delta

            # Log de progresso periódico
            with counters_lock:
                total_done = processed + skipped
                if total_done % 10 == 0 or total_done == len(candidates):
                    log.info("Progresso: %d/%d concluídos (%d processados, %d ignorados)",
                             total_done, len(candidates), processed, skipped)

    log.info("Coleta concluída: %d repositórios processados, %d ignorados", processed, skipped)
    store.close()
    return 0


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

    repos = _load_gold_repos(gold_dir)
    log.info("Carregados %d repositórios de %s", len(repos), gold_dir)

    if not repos:
        log.warning("Nenhum repositório encontrado em gold. Rode 'collect' primeiro.")
        return 0

    # Datasets para correlação
    all_lead_time_a: list[float] = []
    all_lead_time_b: list[float] = []
    all_cfr: list[float] = []
    all_recovery: list[float] = []
    all_deploy_freq: list[float] = []
    all_deploy_freq_tags: list[float] = []

    # Resultados por repositório
    repo_metrics: list[dict] = []

    for repo_data in repos:
        repo_info = repo_data["repository"]
        full_name = repo_info["full_name"]
        log.info("Calculando métricas para %s...", full_name)

        releases = repo_data["releases"]
        tags = repo_data["tags"]
        commits_between = repo_data["commits_between"]
        runs_by_month = repo_data["runs_by_month"]

        # Preparar dados para lead_time
        release_commits_a: list[dict] = []
        release_commits_b: list[dict] = []

        for cb in commits_between:
            if cb["ignored_reason"] is not None:
                continue  # Ignora primeira release ou compare 404
            if not cb["commits"]:
                continue  # Release sem commits novos
            release_commits_a.append({
                "release_published_at": next(
                    (r["published_at"] for r in releases if r["tag_name"] == cb["release"]),
                    None
                ),
                "commit_dates": [c["author_date"] for c in cb["commits"]],
            })
            release_commits_b.append({
                "release_published_at": next(
                    (r["published_at"] for r in releases if r["tag_name"] == cb["release"]),
                    None
                ),
                "commit_dates": [c["author_date"] for c in cb["commits"]],
            })

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
        runs_flat: list[dict] = []
        for runs in runs_by_month.values():
            runs_flat.extend(runs)
        episodes = recovery_episodes(runs_flat)
        recovery_hours = median_recovery_hours(episodes)
        censored_prop = censored_proportion(episodes)

        # Deployment frequency (releases only)
        deploy_freq = deployment_frequency(
            [{"published_at": r["published_at"], "draft": r["draft"]} for r in releases],
            window_weeks=window_weeks,
        )

        # Deployment frequency (releases + tags with dates)
        tags_with_dates = [{"published_at": t["date"], "draft": False} for t in tags if t.get("date")]
        deploy_freq_tags = deployment_frequency(
            [{"published_at": r["published_at"], "draft": r["draft"]} for r in releases] + tags_with_dates,
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
                "C1": asdict(dora_c1),
                "C2": asdict(dora_c2),
                "C3": asdict(dora_c3),
            },
            "survival": {
                "median_survival_hours": survival.median_survival,
                "confidence_interval": survival.confidence_interval,
                "n_events": survival.n_events,
                "n_censored": survival.n_censored,
                "n_total": survival.n_total,
            },
        }

        repo_metrics.append(repo_result)

        # Coletar para correlação
        if lt_a is not None:
            all_lead_time_a.append(lt_a)
        if lt_b is not None:
            all_lead_time_b.append(lt_b)
        if cfr is not None:
            all_cfr.append(cfr)
        if recovery_hours is not None:
            all_recovery.append(recovery_hours)
        if deploy_freq is not None:
            all_deploy_freq.append(deploy_freq)
        if deploy_freq_tags is not None:
            all_deploy_freq_tags.append(deploy_freq_tags)

    # Correlações (RQ 05 e RQ 06)
    correlations = {}

    # RQ 05: Lead Time (a) vs CFR(a)
    if len(all_lead_time_a) >= 2 and len(all_cfr) >= 2:
        min_len = min(len(all_lead_time_a), len(all_cfr))
        correlations["lead_time_a_vs_cfr_a"] = asdict(
            spearman_correlation(all_lead_time_a[:min_len], all_cfr[:min_len])
        )

    # RQ 05: Lead Time (b) vs CFR(a)
    if len(all_lead_time_b) >= 2 and len(all_cfr) >= 2:
        min_len = min(len(all_lead_time_b), len(all_cfr))
        correlations["lead_time_b_vs_cfr_a"] = asdict(
            spearman_correlation(all_lead_time_b[:min_len], all_cfr[:min_len])
        )

    # RQ 06: Deployment Frequency vs Recovery Time
    if len(all_deploy_freq) >= 2 and len(all_recovery) >= 2:
        min_len = min(len(all_deploy_freq), len(all_recovery))
        correlations["deploy_freq_vs_recovery"] = asdict(
            spearman_correlation(all_deploy_freq[:min_len], all_recovery[:min_len])
        )

    # RQ 06: Deployment Frequency (with tags) vs Recovery Time
    if len(all_deploy_freq_tags) >= 2 and len(all_recovery) >= 2:
        min_len = min(len(all_deploy_freq_tags), len(all_recovery))
        correlations["deploy_freq_tags_vs_recovery"] = asdict(
            spearman_correlation(all_deploy_freq_tags[:min_len], all_recovery[:min_len])
        )

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
    metrics_json = datasets_dir / "metrics_full.json"

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

        f.write("\n---\n*Gerado automaticamente pelo pipeline DORA Miner (Lab03).*\n")

    log.info("Relatório salvo em %s", report_md)

    # Gerar também um CSV resumo para fácil importação
    summary_csv = reports_dir / "summary.csv"
    df.to_csv(summary_csv, index=False)
    log.info("Resumo CSV salvo em %s", summary_csv)

    return 0


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
        return _run_collect(args.config, args.limit, env_token or "", args.force)

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
