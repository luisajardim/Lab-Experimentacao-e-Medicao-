# Auditoria de Consistência e Outliers — RQ02 e RQ03

**Fonte auditada:** `../../../data/github-rq2-rq3-v2_1787148677023.csv`  
**Data de execução:** 2026-08-20T04:09:30.388Z  
**Critério de outlier:** limite superior de Tukey, `Q3 + 1,5 × IQR`.

## Integridade dos dados

| Verificação | Resultado |
| --- | ---: |
| Registros lidos | 1000 |
| Registros válidos | 1000 |
| Valores inválidos em total_pr_aceitas | 0 |
| Valores inválidos em total_releases | 0 |
| Nomes de repositório duplicados | 0 |
| Repositórios com zero releases | 286 (28.60%) |

Valores inválidos incluem campos vazios, null, undefined, não inteiros, negativos ou não numéricos. Repositórios sem releases são válidos: representam projetos que não usam o mecanismo de Releases do GitHub.

## Estatísticas descritivas

| Métrica | Mínimo | Q1 | Mediana | Média | Q3 | Máximo |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PRs aceitas | 0 | 175 | 768 | 4236.77 | 3415.75 | 103349 |
| Releases | 0 | 0 | 39 | 126.61 | 147 | 1000 |

## Outliers

| Métrica | IQR | Limite superior | Quantidade de outliers |
| --- | ---: | ---: | ---: |
| PRs aceitas | 3240.75 | 8276.88 | 124 |
| Releases | 147 | 367.50 | 93 |

### Dez maiores valores de PRs aceitas

| Repositório | PRs aceitas |
| --- | ---: |
| firstcontributions/first-contributions | 103349 |
| llvm/llvm-project | 97096 |
| elastic/elasticsearch | 95522 |
| getsentry/sentry | 91170 |
| home-assistant/core | 90122 |
| rust-lang/rust | 73601 |
| grafana/grafana | 69443 |
| ClickHouse/ClickHouse | 69143 |
| kubernetes/kubernetes | 65650 |
| python/cpython | 62670 |

### Dez maiores valores de releases

| Repositório | Releases |
| --- | ---: |
| langchain-ai/langchain | 1000 |
| vercel/next.js | 1000 |
| ggml-org/llama.cpp | 1000 |
| electron/electron | 1000 |
| storybookjs/storybook | 1000 |
| home-assistant/core | 1000 |
| zed-industries/zed | 1000 |
| lobehub/lobehub | 1000 |
| ruvnet/ruflo | 1000 |
| withastro/astro | 1000 |

## Conclusão da auditoria

Os valores passaram pelas regras de consistência acima. Os outliers foram preservados, pois são observações reais de repositórios populares; entretanto, tornam a média sensível a poucos projetos muito ativos. Por isso, a mediana deve ser a medida central prioritária na análise das RQs 02 e 03, acompanhada da distribuição e da discussão dos valores extremos.
