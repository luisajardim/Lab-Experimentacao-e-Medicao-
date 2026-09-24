# Consolidação de Qualidade de Código (RQ3)

A análise inclui os artefatos `metrics.json` com status válido no log de trials. Foram incluídos 12 de 12 artefatos; 0 foram excluídos.

## Estatísticas descritivas

| Métrica | COM_IA (mediana; média +/- DP) | SEM_IA (mediana; média +/- DP) |
|---|---:|---:|
| LOC | 21.00; 21.67 +/- 7.20 (n=6) | 23.50; 35.33 +/- 35.61 (n=6) |
| Complexidade ciclomática | 5.50; 4.83 +/- 2.71 (n=6) | 7.00; 6.72 +/- 1.48 (n=6) |
| Halstead volume | 547.90; 469.07 +/- 222.60 (n=6) | 601.42; 555.52 +/- 286.91 (n=6) |
| Halstead difficulty | 18.61; 17.64 +/- 9.46 (n=6) | 21.84; 21.12 +/- 11.22 (n=6) |
| Halstead effort | 10886.33; 9388.07 +/- 5157.06 (n=6) | 14175.77; 13189.50 +/- 6976.18 (n=6) |
| Duplicação (%) | 0.00; 0.00 +/- 0.00 (n=6) | 0.00; 0.94 +/- 2.31 (n=6) |

## Testes inferenciais

| Métrica | Wilcoxon (p; r) | Mann-Whitney (p; Cliff's delta) |
|---|---:|---:|
| LOC | 0.3438; -0.39 | 0.8721; -0.08 |
| Complexidade ciclomática | 0.1250; -0.63 | 0.1445; -0.53 |
| Halstead volume | 0.1250; -0.63 | 0.4225; -0.31 |
| Halstead difficulty | 0.0625; -0.76 | 0.4225; -0.31 |
| Halstead effort | 0.0625; -0.76 | 0.1994; -0.47 |
| Duplicação (%) | 1.0000; 0.00 | 0.4047; -0.17 |

## Texto para resultados

Foram analisados 12 artefatos de qualidade, com 6 katas pareados entre COM_IA e SEM_IA. As diferenças foram avaliadas pelo teste de Wilcoxon pareado por kata e, como análise complementar, pelo teste de Mann-Whitney U sobre as distribuições agregadas. Os resultados devem ser interpretados com cautela devido ao tamanho amostral reduzido; o sinal de Cliff's delta positivo indica valores maiores em COM_IA.

## Exclusões

Nenhum artefato foi excluído.
