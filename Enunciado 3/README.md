# Lab03 — Mineração de Métricas DORA

[![Testes](https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-/actions/workflows/testes.yml/badge.svg)](https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-/actions/workflows/testes.yml)

Pipeline de coleta e cálculo automático das métricas DORA (deployment frequency,
lead time for changes, change failure rate, tempo de recuperação) a partir de
repositórios open-source reais que usam GitHub Actions.

Disciplina: Laboratório de Experimentação de Software (6º período).
Grupo: Bernardo Alvim (A), Luísa Jardim (B), Pedro Seabra (C).

## Pré-requisitos

- **Python 3.12+** (recomendado: [`uv`](https://docs.astral.sh/uv/) como gerenciador de ambientes)
- **Token do GitHub** em variável de ambiente `GITHUB_TOKEN` (nunca commitado)

```bash
cp .env.example .env   # edite .env e cole o token
export $(grep -v '^#' .env | xargs)      # ou: source .env
```

## Começo rápido

```bash
uv sync                                   # instala dependências (gera .venv e uv.lock)
uv run pytest --cov=metrics --cov-report=term-missing   # testes das métricas
uv run python -m pipeline --config config.toml --stage collect --limit 2   # smoke test
```

## Comandos

| Comando | O que faz |
|---|---|
| `uv run python -m pipeline --config config.toml --stage collect` | Coleta da API (com cache/retomada) |
| `uv run python -m pipeline --config config.toml --stage metrics` | Calcula métricas → `data/datasets/` |
| `uv run python -m pipeline --config config.toml --stage report` | Gera relatórios (`reports/`) |
| `uv run python -m pipeline doctor` | Verifica token, config, cache e dependências |
| `uv run pytest --cov=metrics --cov-fail-under=80` | Testes + cobertura (mín. 80%) |

A flag `--limit N` restringe a coleta a N repositórios (smoke tests).

## Estrutura

Ver [`docs/architecture.md`](docs/architecture.md) para o layout completo, fluxo
de dados, decisões de arquitetura e rastreabilidade com o `PLAN.md`.

```
src/pipeline/    CLI e orquestração (entrada única: python -m pipeline)
src/github/      Clientes REST/GraphQL (httpx cru; sem PyGithub)
src/cache/       Cache SQLite content-addressed + retomada por estágio
src/collector/   Coleta: busca, releases, tags, commits, workflow runs
src/metrics/     Funções PURAS de cálculo das métricas (sem I/O)
tests/           Testes + fixtures (pytest)
scripts/         Ferramentas de validação manual e replicação
analysis/        Análises das RQ01-RQ08 (reexecutáveis a partir dos CSVs)
data/            raw/ (bruto, ignorado) · gold/ · datasets/ · cache/ (ignorado)
docs/            Arquitetura, dicionário de dados, protocolos
reports/         Funil de seleção, relatórios de replicação
```

## Notas

- Janela de observação: **2025-10-01 → 2026-09-30** (`config.toml`).
- Definições operacionais obrigatórias: ver `ENUNCIADO.md` §3.
- A coleta respeita o rate limit da API (`X-RateLimit-*`) e usa backoff
  exponencial em 429/5xx; respostas são cacheadas em `data/cache/`, o que
  permite retomar uma coleta interrompida sem repetir chamadas.
