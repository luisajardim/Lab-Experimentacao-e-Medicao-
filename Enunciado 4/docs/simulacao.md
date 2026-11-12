# Resultados da simulação — formato dos arquivos

Gerados por [`src/simulate.py`](../src/simulate.py) (T08, #83) em `data/sim/`. O cenário e as situações
estão em [cenario.md](cenario.md).

| Item | Valor |
|---|---|
| Situações | `S-base`, `S-real`, `S-real-n10`, `S-outlier` (`config.SITUATIONS`) |
| Efeitos (ρ latente) | 0,0; 0,1; 0,2; 0,3; 0,4; 0,5; 0,6 (`config.EFFECT_GRID`) |
| Réplicas por célula | 10.000 (`config.REPS`) → 280.000 conjuntos simulados |
| Testes | Pearson e Spearman, bicaudais, p pela t com n − 2 g.l. (`stat_tests.py`) |
| α disponíveis | 0,05 e 0,01 (`config.ALPHAS`) |
| Tempo | ~50 s para tudo; com cache válido, ~1 s |

## Como gerar

```bash
uv run python -m simulate            # usa o cache se nada mudou
uv run python -m simulate --force    # re-simula do zero (resultado idêntico)
uv run lab04                         # o comando único também roda a simulação, com cache
uv run python scripts/parquet_to_csv.py   # exporta pvalues.parquet para data/sim/export/pvalues.csv
```

**Reprodutibilidade:** cada célula (situação × efeito) tem um gerador próprio derivado de `SEED = 42`
(`numpy.random.SeedSequence(SEED, spawn_key=(nome, efeito, finalidade))`, com o nome convertido em número por
CRC-32). Re-simular gera os mesmos números, e como a chave usa o nome e o valor do efeito (não a posição),
incluir, remover ou reordenar situações e efeitos não altera as células que continuam existindo.

**Cache:** `meta.json` guarda uma chave calculada a partir da semente, das réplicas, da grade de efeitos, das
situações, dos parâmetros da S-outlier, do SHA-256 de `data/real/params.json` e do SHA-256 do código que gera
os resultados (`generate.py`, `stat_tests.py` e `simulate.py`). Se algo disso mudar, a simulação roda de novo;
se não, os arquivos são reaproveitados.

## `pvalues.parquet` — uma linha por réplica (280.000 linhas)

| Coluna | Tipo | Descrição |
|---|---|---|
| `situation` | categoria | `S-base`, `S-real`, `S-real-n10` ou `S-outlier` |
| `rho` | float | ρ latente da célula (0,0 a 0,6) |
| `rep` | int | Índice da réplica dentro da célula (0 a 9.999) |
| `r` | float | Coeficiente de Pearson da amostra |
| `p_pearson` | float | p-valor bicaudal do teste de Pearson |
| `rho_s` | float | Coeficiente de Spearman da amostra |
| `p_spearman` | float | p-valor bicaudal do teste de Spearman |

Amostras em que X ou Y é constante (ex.: nenhum defeito na S-real-n10) têm coeficiente e p-valor `NaN`. Elas
contam como **"não rejeita H₀"** nas taxas.

Exemplo — taxa de rejeição com qualquer α:

```python
import pandas as pd
pv = pd.read_parquet("data/sim/pvalues.parquet")
taxa = (pv.assign(rej=pv["p_pearson"] < 0.05)
          .groupby(["situation", "rho"], observed=True)["rej"].mean())
```

## `summary.csv` — taxa de rejeição (112 linhas)

Uma linha por situação × efeito × α × teste. Com `rho == 0`, `reject_rate` é o **erro tipo I** (G3); com
`rho > 0`, é o **poder** (G4).

| Coluna | Descrição |
|---|---|
| `situation`, `rho` | Célula |
| `alpha` | 0,05 ou 0,01 |
| `test` | `pearson` ou `spearman` |
| `reject_rate` | Proporção de réplicas com p < α |
| `mc_se` | Erro padrão de Monte Carlo: √(taxa·(1 − taxa)/n_reps) (≈ 0,0022 em torno de 5%) |
| `n_reps` | Réplicas da célula (10.000) |
| `n_nan` | Réplicas com p-valor `NaN` (amostra constante) |

## `population.csv` — correlações "populacionais" (28 linhas)

r e ρₛ calculados numa amostra de 1.000.000 de classes de cada gerador. O erro de estimativa fica em torno de
±0,002 a 0,003 para o r (maior nas situações de cauda pesada) e ±0,0015 para o ρₛ. A população depende só do
gerador, então **S-real e S-real-n10 têm os mesmos valores**. Servem para anotar o eixo do G4: o mesmo ρ latente
corresponde a r e ρₛ diferentes em cada situação.

| Coluna | Descrição |
|---|---|
| `situation`, `rho` | Célula |
| `r_pop` | r de Pearson populacional |
| `rho_s_pop` | ρ de Spearman populacional |

Na S-outlier com ρ = 0, `r_pop` ≈ 0,18 e `rho_s_pop` ≈ 0,02: a associação vem só das classes extremas.

## `meta.json`

Chave de cache, configuração usada (`config`) e tempo de execução (`elapsed_seconds`).

## Extra: `sample_size.csv` — tamanho da amostra (#91)

Simulação opcional, para as perguntas da seção 6 do enunciado ("Para discutir: tamanho da amostra"). Gerada por
[`src/sample_size.py`](../src/sample_size.py) e mostrada no último gráfico do dashboard (poder e erro tipo I × tamanho da amostra).

```bash
uv run lab04 --sample-size              # roda a simulação extra (com cache) e abre o dashboard
uv run python -m sample_size [--force]  # só a simulação extra
```

| Item | Valor |
|---|---|
| Situações | `S-real` e `S-outlier` |
| n (classes) | 10, 20, 30, 50, 80, 120, 200 |
| Efeitos | `zero` (ρ = 0, erro tipo I), `moderado` (ρ latente = 0,3) e `observado` |
| Efeito observado | ρ latente calibrado para que o ρₛ populacional do gerador (em `population.csv`) seja igual ao ρₛ da amostra real de 30 classes (0,515): ≈ 0,60 na S-real e ≈ 0,58 na S-outlier |
| Réplicas | 10.000 por célula |
| Tempo | ~75 s; com cache válido, instantâneo |

Uma linha por situação × efeito × n × α × teste. A coluna `effect` substitui a grade de efeitos, e `n` é o
tamanho da amostra; as demais colunas (`rho`, `alpha`, `test`, `reject_rate`, `mc_se`, `n_nan`) têm o mesmo
significado do `summary.csv`.

O n para 80% de poder é interpolado por `sample_size.n80_table` (linear em log n) a partir dessas curvas; quando o poder não
chega a 80% dentro da grade, aparece como "mais de 200". O cache (`sample_size_meta.json`) considera também o
código de `sample_size.py` e o ρₛ da amostra real.
