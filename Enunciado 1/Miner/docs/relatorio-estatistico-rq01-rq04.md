# Relatório estatístico — Maturidade dos repositórios (RQ01 e RQ04)

**Fonte:** `./data/1000_popular_repos.csv`
**Gerado em:** 2026-08-26T20:07:21.066Z
**Repositórios analisados:** 1000
**Critério de outlier:** limite de Tukey, `Q1 - 1,5×IQR` / `Q3 + 1,5×IQR`.

## Validação de consistência

| Verificação | Resultado |
|---|---:|
| Registros lidos | 1000 |
| Valores ausentes em `idade_anos` | 0 |
| Valores ausentes em `dias_desde_ultima_atualizacao` | 0 |
| Valores negativos em `idade_anos` | 0 |
| Valores negativos em `dias_desde_ultima_atualizacao` | 0 |

Valores negativos indicariam erro de extração (idade e tempo desde o último push não podem ser negativos); valores ausentes indicariam falha ao coletar `createdAt`/`pushedAt`.

## RQ01 — Idade do repositório (anos)

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR |
|---:|---:|---:|---:|---:|---:|---:|
| 0.02 | 3.5 | 7.74 | 7.66 | 11.35 | 18.36 | 7.85 |

Distribuição por faixa etária:

| Faixa | Repositórios | % |
|---|---:|---:|
| até 1 ano | 82 | 8.2% |
| 1-2 anos | 57 | 5.7% |
| 2-5 anos | 185 | 18.5% |
| 5-10 anos | 331 | 33.1% |
| 10-15 anos | 296 | 29.6% |
| 15+ anos | 49 | 4.9% |

Outliers (limite superior 23.13 anos): **0**

_Nenhum outlier acima do limite superior._

## RQ04 — Dias desde a última atualização

| Mínimo | Q1 | Mediana | Média | Q3 | Máximo | IQR |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 2 | 113.81 | 48.25 | 2452 | 48.25 |

Distribuição por faixa:

| Faixa | Repositórios | % |
|---|---:|---:|
| até 1 dia | 477 | 47.7% |
| 2-7 dias | 132 | 13.2% |
| 8-30 dias | 118 | 11.8% |
| 31-90 dias | 64 | 6.4% |
| 91-365 dias | 94 | 9.4% |
| mais de 365 dias | 115 | 11.5% |

Outliers (limite superior 120.63 dias): **196**

| Repositório | Dias sem push |
|---|---:|
| exacity/deeplearningbook-chinese | 2452 |
| GitSquared/edex-ui | 1765 |
| lib-pku/libpku | 1688 |
| adobe/brackets | 1529 |
| floodsung/Deep-Learning-Papers-Reading-Roadmap | 1361 |
