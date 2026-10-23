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
| `uv run python scripts/create_candidate_manifest.py --from-gold` | Congela a população local que passa os filtros oficiais |
| `uv run python -m pipeline --config config.toml --stage metrics` | Calcula métricas → `data/datasets/` |
| `uv run python -m pipeline --config config.toml --stage report` | Gera relatórios (`reports/`) |
| `uv run python -m pipeline doctor` | Verifica token, config, cache e dependências |
| `uv run gold --input-dir data/gold --population-csv data/datasets/metrics.csv --output-dir data/gold` | Gera o template CSV para a rotulagem manual |
| `uv run pytest --cov=metrics --cov-fail-under=80` | Testes + cobertura (mín. 80%) |

A flag `--limit N` restringe a coleta a N repositórios (smoke tests).

Para uma coleta reprodutível, versione `data/raw/candidates.csv` e
`data/raw/candidate_manifest.csv`. Quando `candidate_manifest_csv` está
configurado, o pipeline usa somente esse manifesto e não faz nova busca na
API; a amostra final tem 315 repositórios, selecionados deterministicamente.

## Replicação cruzada

Esta seção é o roteiro para outro grupo reproduzir o snapshot deste estudo.
Há dois modos: a reprodução **exata**, baseada nos JSONs e no manifesto
versionados, e uma **nova coleta** da API. A primeira é a indicada para a
avaliação: respostas da API do GitHub mudam com o tempo, portanto uma nova
coleta não deve ser esperada produzir números idênticos.

### 1. Preparar o ambiente

```bash
git clone https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-.git
cd Lab-Experimentacao-e-Medicao-/"Enunciado 3"
git checkout fix/dataset            # ou a tag/commit informado pelo grupo
uv sync
uv run pytest -q
```

Para consultar a API do GitHub, crie um token pessoal que possa ler
repositórios públicos e GitHub Actions. Nunca o registre no Git, em CSVs ou em
relatórios. O formato recomendado é:

```bash
cp .env.example .env
# Edite .env e defina uma única linha, sem aspas:
# GITHUB_TOKEN=github_pat_...  ou  GITHUB_TOKEN=ghp_...
set -a; source .env; set +a
```

Opcionalmente, use mais de um token para repartir a cota. A variável aceita
tokens separados por vírgula; mantenha-a somente no ambiente local:

```bash
export GITHUB_TOKENS='token_1,token_2,token_3'
```

Valide a instalação e o token antes de coletar:

```bash
uv run python -m pipeline --config config.toml doctor
```

### 2. Reprodução exata do snapshot

Este modo não exige token nem acesso à API, desde que o clone contenha
`data/gold/`, `data/raw/candidate_manifest.csv` e o código da mesma revisão.
O manifesto fixa 750 repositórios locais elegíveis; o estágio `metrics` faz um
corte determinístico de 315 com seed 42.

```bash
uv run python -m pipeline --config config.toml --stage metrics
uv run python -m pipeline --config config.toml --stage report
wc -l data/datasets/metrics.csv    # esperado: 316 (cabeçalho + 315)
./scripts/monitor_pipeline.sh all
```

Os artefatos a comparar com o snapshot são:

- `data/datasets/metrics.csv` e `metrics_full.json`;
- `data/datasets/dora_c1.csv`, `dora_c2.csv` e `dora_c3.csv`;
- `data/datasets/correlations.json`;
- `reports/funnel.md` e `reports/report.md`.

Diferenças nesse modo indicam uma mudança de código, dependência ou arquivo de
entrada e devem ser registradas como Issue com o comando executado e o diff.

### 3. Nova coleta da API

O manifesto impede uma nova busca e fixa a população-alvo. Assim, a coleta
abaixo atualiza ou preenche somente os 750 itens do manifesto; não percorre os
12.000 resultados brutos de busca.

```bash
uv run python -m pipeline --config config.toml --stage collect --limit 2
./scripts/monitor_pipeline.sh collect

# Coleta completa; --force atualiza também JSONs já existentes.
uv run python -m pipeline --config config.toml --stage collect --force

# Monitor contínuo, atualizando a cada 15 segundos.
./scripts/monitor_pipeline.sh all 15
```

Se a coleta for interrompida, execute novamente o mesmo comando. Cada JSON de
repositório é salvo individualmente; não apague `data/gold/` para retomar. Após
uma nova coleta completa, regenere métricas e relatórios conforme a seção 2.

Para reconstruir o manifesto a partir de um snapshot local validado, sem nova
busca, use o mesmo corte fixo:

```bash
uv run python scripts/create_candidate_manifest.py --from-gold --size 750 --seed 42
```

### 4. Validação manual e CFR(b)

Execute estes passos somente depois de congelar `metrics.csv`; gerar uma nova
planilha depois da rotulagem troca a população da amostra-ouro.

```bash
uv run gold --input-dir data/gold \
  --population-csv data/datasets/metrics.csv --output-dir data/gold
uv run python -m pipeline --config config.toml --stage collect-commits
uv run python scripts/build_dossiers.py --input-dir data/gold

# Cada avaliador executa independentemente sua própria planilha.
uv run python scripts/label_tool.py --member A
uv run python scripts/label_tool.py --member B
uv run python scripts/label_tool.py --member C
uv run python scripts/agreement.py
uv run python scripts/tune_cfr.py --input-dir data/gold
```

O consenso, o κ de Fleiss e a avaliação da heurística ficam em
`labels_consensus.csv`, `reports/agreement.md` e `cfr_metrics.json`.

### 5. Conclusão e análise

Com os datasets finais gerados, execute a T19 sem token e sem novas chamadas
à API:

```bash
uv run python analysis/rq01_rq04.py
uv run python analysis/recovery_survival.py
uv run python analysis/rq05_spearman.py
uv run python analysis/rq06_kruskal.py
uv run python analysis/rq07_sensitivity.py
uv run python analysis/rq08_bonus.py
uv run python analysis/figures.py      # figuras do relatório em analysis/output/figures/
```

Os comandos criam `analysis/output/rq01_rq04.md`, os CSVs de estatística e
distribuição C1, além de `recovery_survival.png` e seu resumo JSON. As
medianas e IQRs usam o repositório como unidade de análise; os ICs de 95% são
bootstrap BCa com 2.000 reamostragens (semente 42). A curva Kaplan--Meier usa
os episódios de recovery, inclusive os censurados.

Ao final da replicação, registre no Issue: hash do commit, versão do Python,
comandos usados, contagem de linhas de `metrics.csv`, conteúdo de
`reports/funnel.md` e diferenças encontradas. Não substitua esses scripts por
cálculos manuais ao reportar resultados reproduzidos.

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
