# Dicionário de Dados — v1.0

Documentação de todas as colunas dos CSVs produzidos pelo pipeline (`python -m pipeline`).

**Convenções gerais**

- **Janela de observação:** `config.toml [window]`, de `2025-10-01` a `2026-09-30`, inclusive (52,1 semanas). Só entram no cálculo releases, tags e workflow runs **dentro da janela** (ENUNCIADO §3).
- **Critério mínimo de inclusão:** pelo menos 5 releases e 50 workflow runs na janela (`config.toml [filters]`). Os repositórios abaixo disso são descartados e contabilizados no funil (`reports/funnel.md`).
- **Valor vazio:** célula vazia significa que a métrica **não pôde ser calculada** (por exemplo, nenhuma release com commits comparáveis). Não equivale a zero.
- **Datas:** ISO-8601 em UTC (`AAAA-MM-DDTHH:MM:SSZ`).
- **Release válida:** `draft = false`, com `published_at` dentro da janela.
- **Workflow run válido:** `event = push` no default branch, criado na janela. As conclusões `cancelled`, `skipped`, `neutral`, `action_required`, `stale` e vazia são ignoradas.

---

## 1. `data/raw/candidates.csv`

Lista bruta de repositórios devolvida pela Search API, antes do funil (`src/collector/search.py`).

| Coluna | Tipo | Unidade | Fórmula / Origem na API | Exemplo |
|---|---|---|---|---|
| `full_name` | string | – | `full_name` (formato `owner/repo`) | `aeron-io/aeron` |
| `stars` | inteiro | estrelas | `stargazers_count` | `8901` |
| `language` | string | – | `language` (linguagem principal; pode vir vazia) | `Java` |
| `default_branch` | string | – | `default_branch` | `master` |
| `created_at` | datetime | ISO-8601 | `created_at` | `2014-04-29T21:29:05Z` |

---

## 2. `data/datasets/metrics.csv`

Uma linha por repositório da amostra final, com **todas** as métricas e as três classificações (`_run_metrics` em `src/pipeline/cli.py`).

| Coluna | Tipo | Unidade | Fórmula / Origem | Exemplo |
|---|---|---|---|---|
| `full_name` | string | – | `full_name` do repositório | `aeron-io/aeron` |
| `stars` | inteiro | estrelas | `stargazers_count` | `8901` |
| `language` | string | – | `language` | `Java` |
| `lead_time_a_hours` | float | horas | **Lead time (a), por release:** para cada release R da janela, `published_at(R) − author_date do commit mais antigo` em `compare/{anterior}...{R}`. Valor do repositório = **mediana** entre as releases. As releases sem anterior, com compare 404 ou sem commits novos são ignoradas. | `392.45` |
| `lead_time_b_hours` | float | horas | **Lead time (b), por commit:** `published_at(R) − author_date(c)` para **todo** commit c de toda release R. Valor = mediana de todos os commits. | `361.66` |
| `cfr_a` | float | proporção [0,1] | **CFR (a), proxy de CI:** `falhas / (falhas + sucessos)` dos workflow runs. Falha = `failure`, `timed_out` ou `startup_failure`; sucesso = `success`. | `0.1435` |
| `recovery_hours` | float | horas | **Tempo de recuperação:** um episódio começa na 1ª falha **após um sucesso** e termina no próximo sucesso **do mesmo workflow** (`updated_at` do sucesso − `run_started_at` da falha). Valor = mediana dos episódios **não censurados**. | `7.34` |
| `censored_proportion` | float | proporção [0,1] | Episódios que não se encerraram na janela ÷ total de episódios. Eles são registrados, não descartados (ENUNCIADO §3). | `0.0` |
| `deployment_frequency_per_week` | float | releases/semana | **Frequência de deploy:** nº de releases válidas na janela ÷ `window.weeks` (52,1). | `0.499` |
| `deployment_frequency_with_tags_per_week` | float | releases/semana | Igual à anterior, contando também as **tags com data** dentro da janela (variante da RQ 07). | `1.036` |
| `dora_c1_category` | string (categórica) | – | Classificação DORA na variante **C1** (ver seção 4). | `Medium/Low` |
| `dora_c2_category` | string (categórica) | – | Classificação DORA na variante **C2**. | `Medium/Low` |
| `dora_c3_category` | string (categórica) | – | Classificação DORA na variante **C3**. | `Medium/Low` |
| `survival_median_hours` | float | horas | Mediana do tempo de recuperação estimada por **Kaplan-Meier** (`lifelines.KaplanMeierFitter`). | `7.34` |
| `survival_n_events` | inteiro | episódios | Nº de episódios encerrados (recuperados) usados no Kaplan-Meier. | `149` |
| `survival_n_censored` | inteiro | episódios | Nº de episódios censurados usados no Kaplan-Meier. | `0` |
| `recovery_episodes` (`metrics_full.json`) | lista de objetos | horas + booleano | Duração de cada episódio de recovery e se foi censurado; permite refazer a curva Kaplan-Meier agregada sem consultar a API. | `[{"duration_hours": 7.34, "censored": false}]` |

---

## 3. `data/datasets/dora_c1.csv`, `dora_c2.csv`, `dora_c3.csv`

Um arquivo por variante de classificação (RQ 07), todos com **o mesmo schema**. Cada arquivo traz só as quatro métricas usadas naquela variante.

| Coluna | Tipo | Unidade | Fórmula / Origem | Exemplo (`dora_c3.csv`) |
|---|---|---|---|---|
| `full_name` | string | – | `full_name` do repositório | `aeron-io/aeron` |
| `stars` | inteiro | estrelas | `stargazers_count` | `8901` |
| `language` | string | – | `language` | `Java` |
| `lead_time_hours` | float | horas | C1 e C2: `lead_time_a_hours`; C3: `lead_time_b_hours` | `361.66` |
| `cfr` | float | proporção [0,1] | `cfr_a` (nas três variantes) | `0.1435` |
| `recovery_hours` | float | horas | `recovery_hours` (nas três variantes) | `7.34` |
| `deployment_frequency_per_week` | float | releases/semana | C1: `deployment_frequency_per_week`; C2 e C3: `deployment_frequency_with_tags_per_week` | `1.036` |
| `dora_category` | string (categórica) | – | Categoria DORA calculada com as quatro colunas acima (seção 4) | `Medium/Low` |

---

## 4. Regras da classificação DORA

Definidas em `src/metrics/dora_classification.py` (ENUNCIADO §5).

| Variante | Lead time | Frequência de deploy |
|---|---|---|
| **C1** | (a) por release | só releases |
| **C2** | (a) por release | releases + tags com data |
| **C3** | (b) por commit | releases + tags com data |

| Categoria | Condição (todas precisam ser verdadeiras) |
|---|---|
| `Elite` | lead time < 1 h **e** CFR < 0,15 **e** recuperação < 1 h **e** deploy ≥ 7/semana |
| `High` | lead time < 24 h **e** CFR < 0,30 **e** recuperação < 24 h **e** deploy ≥ 1/semana |
| `Medium/Low` | as quatro métricas existem, mas não atendem a `High` |
| *(vazio)* | pelo menos uma das quatro métricas não pôde ser calculada |

---

## 5. Arquivos auxiliares (não tabulares)

| Arquivo | Conteúdo |
|---|---|
| `data/datasets/correlations.json` | Spearman (`rho`, `p_value`, `significant` com α = 0,05) para: `lead_time_a_vs_cfr_a`, `lead_time_b_vs_cfr_a` (RQ 05), `deploy_freq_vs_recovery` e `deploy_freq_tags_vs_recovery` (RQ 06). Usa apenas pares do mesmo repositório em que os dois valores existem. |
| `data/datasets/metrics_full.json` | Versão detalhada do `metrics.csv` por repositório, incluindo o intervalo de confiança do Kaplan-Meier. |

---

*Histórico: v1.0 (S02). Revisar após a S03 caso surjam novas colunas.*
