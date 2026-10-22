# T22 — RQ07: sensibilidade da classificação DORA

Fonte: `metrics.csv` (315 repositórios). κ de Cohen ponderado linear (`sklearn.metrics.cohen_kappa_score`, `weights='linear'`), interpretado pela escala de Landis & Koch (1977).

## Variantes comparadas

| variante | definição |
|---|---|
| C1 | deploy = release; lead time (a) por release; CFR (a) |
| C2 | deploy = release + tags com data; lead time (a) por release; CFR (a) |
| C3 | deploy = release + tags com data; lead time (b) por commit; CFR (a) |

## Distribuição por variante

| categoria | C1 | C2 | C3 |
|---|---:|---:|---:|
| Elite | 22 | 26 | 25 |
| High | 113 | 133 | 135 |
| Medium | 97 | 81 | 81 |
| Low | 14 | 6 | 5 |
| Não classificável | 69 | 69 | 69 |

## Concordância entre pares

| par | n comparado | excluídos | mudaram | % mudou | melhoraram | pioraram | saltos ≥ 2 níveis | κ linear | interpretação |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C1×C2 | 246 | 69 | 36 | 14.6% | 36 | 0 | 0 | 0.802 | quase perfeita |
| C1×C3 | 246 | 69 | 58 | 23.6% | 47 | 11 | 1 | 0.673 | substancial |
| C2×C3 | 246 | 69 | 27 | 11.0% | 14 | 13 | 0 | 0.840 | quase perfeita |

"Melhoraram"/"pioraram" referem-se à segunda variante do par em relação à primeira (melhorar = mais perto de Elite). Excluídos = não classificáveis em pelo menos uma das duas variantes (alguma métrica ausente).

## Matrizes de transição

Linhas = primeira variante, colunas = segunda. A diagonal (negrito) são os repositórios que mantiveram a categoria.

### C1 × C2

| C1 \ C2 | Elite | High | Medium | Low | total |
|---|---:|---:|---:|---:|---:|
| Elite | **22** | 0 | 0 | 0 | 22 |
| High | 4 | **109** | 0 | 0 | 113 |
| Medium | 0 | 24 | **73** | 0 | 97 |
| Low | 0 | 0 | 8 | **6** | 14 |
| total | 26 | 133 | 81 | 6 | 246 |

### C1 × C3

| C1 \ C3 | Elite | High | Medium | Low | total |
|---|---:|---:|---:|---:|---:|
| Elite | **17** | 5 | 0 | 0 | 22 |
| High | 7 | **100** | 6 | 0 | 113 |
| Medium | 1 | 30 | **66** | 0 | 97 |
| Low | 0 | 0 | 9 | **5** | 14 |
| total | 25 | 135 | 81 | 5 | 246 |

### C2 × C3

| C2 \ C3 | Elite | High | Medium | Low | total |
|---|---:|---:|---:|---:|---:|
| Elite | **20** | 6 | 0 | 0 | 26 |
| High | 5 | **122** | 6 | 0 | 133 |
| Medium | 0 | 7 | **73** | 1 | 81 |
| Low | 0 | 0 | 2 | **4** | 6 |
| total | 25 | 135 | 81 | 5 | 246 |
