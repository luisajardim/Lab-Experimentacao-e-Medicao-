# Arquitetura do Pipeline — Lab03 (Mineração de Métricas DORA)

> Documento vivo. Atualize via Issues do GitHub Projects quando decisões mudarem.
> Rastreável ao `PLAN.md` (seção "Rastreabilidade" ao final).

---

## 1. Objetivo

Pipeline reprodutível que (a) **coleta** dados públicos de repositórios
GitHub (releases, tags, commits, workflow runs), (b) **calcula** as métricas
DORA em todas as variantes obrigatórias do ENUNCIADO §3–§5, e (c) **alimenta**
análises estatísticas (RQ 01–08) e a validação manual (amostra-ouro).

Na entrega final, **outro grupo** executa este pipeline seguindo apenas o
README (replicação cruzada, ENUNCIADO §9).

## 2. Princípios

1. **Métricas puras.** `src/metrics/` não faz I/O: recebe dados, devolve
   números. Toda a lógica de negócio é testável com fixtures, sem rede
   (requisito ENUNCIADO §7: cobertura ≥ 80% com pytest).
2. **Nenhum cliente GitHub de terceiros.** Proibido PyGithub/Octokit
   (ENUNCIADO §observação). Acesso via `httpx` cru: REST (paginação pelo
   cabeçalho `Link`) e GraphQL (requisições em lote com aliases).
3. **Cache-first e retomada.** Toda resposta da API é persistida em SQLite
   (chave = hash de método+URL+body). Uma coleta interrompida (rate limit,
   rede, Ctrl+C) retoma do último estágio completo sem repetir chamadas.
4. **Configuração explícita.** Janela, fatias de busca, filtros e caminhos
   vivem em `config.toml`; o token vive **apenas** em `GITHUB_TOKEN`.
5. **Análise desacoplada.** Scripts em `analysis/` leem somente os CSVs
   finais (`data/datasets/*.csv`): as RQs são reexecutáveis sem tocar na API.

## 3. Layout de diretórios

```
Enunciado 3/
├── config.toml               # janela, fatias, filtros, paths
├── pyproject.toml            # dependências, ruff, pytest, hatchling
├── .python-version           # 3.12 (uv)
├── .env.example              # template do GITHUB_TOKEN (sem valores reais)
├── .github/workflows/testes.yml
├── docs/
│   ├── architecture.md       # este arquivo
│   ├── data_dictionary.md    # T10/T17: colunas, tipos, unidades, fórmulas
│   └── consensus_protocol.md # T13: protocolo de desempate da amostra-ouro
├── src/
│   ├── pipeline/             # CLI (python -m pipeline) e orquestração por estágio
│   ├── github/               # gql.py (lote), rest.py (paginação), models.py
│   ├── cache/                # sqlite_store.py: get/put/get_stale/clear_stage
│   ├── collector/            # search, releases, tags, commits, runs
│   └── metrics/              # lead_time, cfr, recovery, dora (funções puras)
├── tests/                    # pytest + fixtures/ (dados de entrada conhecidos)
├── scripts/                  # generate_gold, agreement, diff_datasets (T11-T16)
├── analysis/                 # rq01_rq04.py … rq08_bonus.py (S03) + output/
├── data/
│   ├── raw/        [gitignored] JSON por repo+endpoint, candidates.csv
│   ├── gold/       rótulos dos 3 avaliadores + consenso (commitados)
│   ├── datasets/   dora_c1.csv, dora_c2.csv, dora_c3.csv (commitados)
│   └── cache/      [gitignored] api_responses.db
├── meta/                     # search_queries/ usadas + manifest.json (SHA256)
├── reports/                  # funnel.md, replication_run.md, replication_diff.md
└── templates/                # issue_replicacao.md
```

## 4. Pacotes e responsabilidades

| Pacote | Responsabilidade | Depende de |
|---|---|---|
| `github` | Clientes REST (paginação `Link`) e GraphQL (lote por aliases); `BaseGitHubClient` com retry/backoff/rate limit; modelos de dados | httpx |
| `cache` | Persistência content-addressed, staleness, retomada por estágio | — |
| `collector` | Orquestra endpoints por recurso (search/releases/tags/commits/runs) | github, cache |
| `metrics` | Cálculo puro das métricas e classificação DORA | — (sem I/O) |
| `pipeline` | CLI, leitura de `config.toml`, estágios collect/metrics/report/doctor | todos |

## 5. Fluxo de dados

```
GET /search/repositories (fatias de stars)        → data/raw/candidates.csv
        │  (funil: com Actions → ≥5 releases → ≥50 runs)
        ▼
por repositório: releases, tags, compare, runs    → data/raw/{repo}.json  (cache SQLite)
        ▼
ESTÁGIO metrics: funções puras de src/metrics/    → data/datasets/dora_c{1,2,3}.csv
        ▼
ESTÁGIO report / analysis/: RQ01-RQ08             → reports/, analysis/output/
```

Estágios são retomáveis: `pipeline --stage collect` só baixa o que não está
em cache; `metrics` e `report` regeneram saídas a partir dos dados brutos.

## 6. Decisões (ADR)

| # | Decisão | Contexto / alternativa rejeitada |
|---|---|---|
| D1 | `src/` layout com 5 pacotes | Testabilidade e clara separação I/O vs. lógica; flat layout misturaria responsabilidades |
| D2 | `httpx` cru para REST + GraphQL | Obrigatório pelo ENUNCIADO; PyGithub proibido |
| D3 | GraphQL em lote (aliases) para metadados; REST paginado para runs/compare | GraphQL reduz round-trips; REST é necessário onde GraphQL é limitado (1.000 runs) |
| D3a | `BaseGitHubClient` compartilhada por REST e GraphQL | Retry/backoff/rate-limit em um só lugar; sessão, `sleeper` e `wall_clock` injetáveis para testes sem rede |
| D4 | SQLite content-addressed como cache | Retomada por estágio + staleness; alternativa (JSON por arquivo) não indexa nem expira |
| D5 | `config.toml` + `tomllib` (stdlib) | Sem dependência extra; TOML legível; token só via `GITHUB_TOKEN` |
| D6 | `argparse` (stdlib) em vez de `typer` | Uma dependência a menos; CLI tem 4 subcomandos simples |
| D7 | `uv` + hatchling + `.python-version` 3.12 | Lock reprodutível (`uv.lock`) e CI em 3.12/3.13 (PLAN T01/T09) |
| D8 | `analysis/` lê apenas CSVs | RQs reexecutáveis sem API (ENUNCIADO §10); replicação compara CSVs |
| D9 | Smoke test no CI (`--limit 2`) | Prova que a coleta funciona end-to-end; consome cota mínima do token do Actions |

## 7. Governança: o que entra no git

| Caminho | No git? | Motivo |
|---|---|---|
| `data/datasets/*.csv`, `data/gold/` | **Sim** | Entregáveis: dataset e amostra-ouro rotulada |
| `meta/`, `reports/`, `docs/` | **Sim** | Reprodutibilidade e documentação |
| `data/raw/` | Apenas `.gitkeep` | Conteúdo regenerável; candidatos e JSONs ficam locais |
| `data/cache/` | **Não** | Criado em runtime; cache local nunca é commitado (ENUNCIADO §7) |
| `.env`, `.env.*` | **Não** | Segredos (`.env.example` é a exceção, sem valores) |

`data/manifest.json` (SHA256 das respostas brutas por repo+endpoint) será
commitado ao fim de cada coleta: permite auditar se o dataset foi gerado a
partir das mesmas respostas de API.

## 8. Rastreabilidade PLAN → artefatos

| Tarefa | Artefatos principais |
|---|---|
| T01 | `pyproject.toml`, `config.toml`, `README.md`, `.github/workflows/testes.yml`, este doc |
| T02 | `src/github/{gql,rest,models}.py` |
| T03 | `src/cache/sqlite_store.py` + `staleness_report.json` |
| T04 | `src/collector/search.py` → `data/raw/candidates.csv`, `meta/search_queries/` |
| T05 | `src/collector/{releases,tags,commits}.py` → JSON por repo |
| T06 | `src/collector/runs.py` (divisão mensal da janela) |
| T07 | `src/metrics/{lead_time,cfr,recovery}.py` + `tests/fixtures/` |
| T08 | `src/pipeline/cli.py` (collect/metrics/report/doctor, `--limit`) |
| T09 | `.github/workflows/testes.yml` (este scaffold) |
| T10 | `reports/funnel.md`, `docs/data_dictionary.md` |
| T11-T17 | `scripts/`, `data/gold/`, `data/datasets/`, `docs/` |
| T19-T23 | `analysis/*.py` + `analysis/output/` |
| T25-T28 | `reports/replication_*.md`, `templates/issue_replicacao.md`, `docs/threats.md` |
