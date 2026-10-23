# Dicionário de Dados — v1.1

Documentação de todas as colunas dos CSVs produzidos pelo pipeline (`python -m pipeline`).

**Convenções gerais**

- **Janela de observação:** `config.toml [window]`, de `2025-10-01` a `2026-09-30`, inclusive (52,1 semanas). Só entram no cálculo releases, tags e workflow runs **dentro da janela** (ENUNCIADO §3).
- **Critério mínimo de inclusão:** pelo menos 5 releases e 50 workflow runs na janela (`config.toml [filters]`). Os repositórios abaixo disso são descartados e contabilizados no funil (`reports/funnel.md`, gerado pelo estágio `report`).
- **Valor vazio:** célula vazia significa que a métrica **não pôde ser calculada** (por exemplo, nenhuma release com commits comparáveis). Não equivale a zero.
- **Datas:** ISO-8601 em UTC (`AAAA-MM-DDTHH:MM:SSZ`).
- **Release válida (deploy):** `draft = false` e `prerelease = false`, com `published_at` dentro da janela.
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
| `dora_c1_category` | string (categórica) | – | Classificação DORA na variante **C1** (ver seção 4). | `High` |
| `dora_c2_category` | string (categórica) | – | Classificação DORA na variante **C2**. | `High` |
| `dora_c3_category` | string (categórica) | – | Classificação DORA na variante **C3**. | `Medium` |
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
| `dora_category` | string (categórica) | – | Categoria DORA calculada com as quatro colunas acima (seção 4) | `Medium` |

---

## 4. Regras da classificação DORA

Definidas em `src/metrics/dora_classification.py` (ENUNCIADO §5).

| Variante | Lead time | Frequência de deploy |
|---|---|---|
| **C1** | (a) por release | só releases |
| **C2** | (a) por release | releases + tags com data |
| **C3** | (b) por commit | releases + tags com data |

Cada métrica recebe uma nota pelos cortes fixos do ENUNCIADO §5 (RQ 07):

| Métrica | Elite (4) | High (3) | Medium (2) | Low (1) |
|---|---|---|---|---|
| Deployment frequency | ≥ 7/semana | ≥ 1 e < 7/semana | ≥ 1/mês (1/4,345 por semana) e < 1/semana | < 1/mês |
| Lead time (mediana) | < 24 h | 24 h a < 7 dias | 7 a < 30 dias | ≥ 30 dias |
| CFR | ≤ 0,15 | > 0,15 e ≤ 0,30 | > 0,30 e ≤ 0,45 | > 0,45 |
| Tempo de recuperação (mediana) | < 1 h | 1 h a < 24 h | 1 a < 7 dias | ≥ 7 dias |

A categoria geral é a **mediana das quatro notas, arredondada para baixo** (com quatro
notas ordenadas, `(n₂ + n₃) // 2`). Ex.: notas (4, 3, 3, 1) → mediana 3 → `High`.
Se alguma das quatro métricas não pôde ser calculada, a categoria fica **vazia**
("não classificável").

---

## 5. Saídas das análises (`analysis/output/`)

Geradas pelos scripts de `analysis/` a partir de `metrics.csv` e dos JSONs em `data/gold/`, sem chamadas à API.

| Arquivo | Coluna | Tipo | Unidade | Fórmula / Origem |
|---|---|---|---|---|
| `rq05_cfr_b.csv` | `releases_window` | inteiro | releases | Releases válidas (deploys) na janela |
| | `corrective_releases` | inteiro | releases | Releases marcadas como corretivas pela heurística escolhida em `data/gold/cfr_metrics.json` (`best`) |
| | `releases_evaluated` | inteiro | releases | Releases da janela com ≥ 7 dias de acompanhamento antes do fim (as dos últimos 7 dias são censuradas) |
| | `releases_failed` | inteiro | releases | Releases avaliadas seguidas por uma release corretiva em até 7 dias |
| | `cfr_b` | float | proporção [0,1] | **CFR (b), proxy de entrega:** `releases_failed / releases_evaluated` |
| `rq05_metrics.csv` | `variant`, `n`, `rho`, `p_value`, `ci_low`, `ci_high` | misto | – | Spearman entre `deployment_frequency_per_week` e CFR (a) ou (b); IC 95% bootstrap BCa pareado (2.000 réplicas, seed 42) |
| `rq04_hypothesis.csv` | `valid_runs` | inteiro | runs | Runs `push` no default branch com `success` ou falha, na janela (denominador do CFR (a)) |
| `rq06_tests.csv` | `factor`, `metric`, `test`, `statistic`, `p_value`, `p_holm`, `effect_name`, `effect` | misto | – | Kruskal-Wallis por fator × métrica; `p_holm` corrigido por Holm sobre todos os testes; efeito ε² = H / (n − 1) |
| `rq07_sensitivity.csv` | `pair`, `n_compared`, `pct_changed`, `kappa_linear` | misto | %, κ | Por par de variantes: repositórios classificáveis nas duas, % que mudou de categoria e κ de Cohen ponderado linear |
| `rq08_rework_rate.csv` | `corrective_releases_window` | inteiro | releases | Mesma heurística e mesmos deploys de `rq05_cfr_b.csv` |
| | `rework_rate_window` | float | proporção [0,1] | **Rework rate:** `corrective_releases_window / total_releases_window` |
| `rq08_summary.csv` | `increasing`, `decreasing`, `negligible` (+ `pct_*`) | inteiro / proporção | repositórios | Resultado do Mann-Kendall (α = 0,05) por métrica e escala (trimestral, mensal); CFR (a) por período segue a tabela de `conclusion` do ENUNCIADO §3 |

## 6. Arquivos auxiliares (não tabulares)

| Arquivo | Conteúdo |
|---|---|
| `data/datasets/correlations.json` | Spearman exploratório gerado pelo estágio `metrics` (`lead_time_*_vs_cfr_a`, `deploy_freq*_vs_recovery`). **Não** é a RQ 05 oficial; esta fica em `analysis/output/rq05_metrics.csv`. |
| `data/datasets/metrics_full.json` | Versão detalhada do `metrics.csv` por repositório, incluindo o intervalo de confiança do Kaplan-Meier. |
| `data/gold/cfr_metrics.json` | Resultado do tuning da heurística de release corretiva (`best`, melhor por versão, validação cruzada). |
| `reports/funnel.md` | Funil de seleção a partir do snapshot versionado (estágio `report`). |

---

*Histórico: v1.0 (S02); v1.1 (S03): regra de classificação corrigida, CFR (b), rework rate e saídas das análises.*
