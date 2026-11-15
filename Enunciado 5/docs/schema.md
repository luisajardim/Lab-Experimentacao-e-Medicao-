# Schema dos dados — `runs.csv`

Contrato entre a coleta (T04 #99, T05 #100, T12 #107–#109), a validação (T13 #110), a
estatística (T08 #103, T09 #104) e o dashboard (T10 #105). A fonte da verdade é
[`src/schema.py`](../src/schema.py): se este documento e o código divergirem, vale o código.

## Onde ficam os arquivos

```
data/raw/<maquina>/runs.csv     # uma pasta por bloco (bernardo, luisa, pedro, pilot, registry_real)
data/raw/<maquina>/specs.json   # specs da máquina (T07, #102)
data/raw/synthetic/runs.csv     # CSV SINTÉTICO, números inventados (T01) — só para desenvolver
data/processed/runs_all.csv     # dataset final validado (T13, #110)
```

`schema.load_runs()` junta todos os `data/raw/*/runs.csv`. Por padrão, ele **ignora o
sintético e as rodadas de aquecimento**; use `include_synthetic=True` enquanto não houver coleta.

## Colunas

Uma linha = **uma instalação medida** (gerenciador × cenário × projeto × máquina × repetição).

| Coluna | Tipo | Escala | Descrição |
|---|---|---|---|
| `machine` | texto | nominal | Bloco: identificador da máquina (ex.: `bernardo`) |
| `run_id` | texto | nominal | Identificador único da instalação |
| `timestamp` | texto | intervalar | Início da instalação, ISO 8601 com fuso |
| `project` | texto | nominal | `express-api`, `react-vite`, `next-app` |
| `scenario` | texto | nominal | `cold`, `ci`, `warm-cache`, `reinstall` |
| `manager` | texto | nominal | `npm` (controle), `pnpm`, `bun`, `yarn-classic`, `yarn-berry-nm`, `yarn-berry-pnp` |
| `manager_version` | texto | nominal | Versão exata do gerenciador |
| `node_version` | texto | nominal | Versão exata do Node.js |
| `registry` | texto | nominal | `local` (Verdaccio) ou `public` (checagem da T19) |
| `rep` | inteiro | ordinal | Repetição (1..N) da célula; `0` no aquecimento |
| `order` | inteiro | ordinal | Posição na sequência aleatorizada do bloco (1..total) |
| `warmup` | booleano | nominal | Rodada de aquecimento: registrada, mas descartada na análise |
| `wall_s` | real | razão | Tempo de relógio da instalação (s) |
| `cpu_s` | real | razão | CPU (usuário + sistema) da árvore de processos (s) |
| `peak_rss_mb` | real | razão | Pico de memória residente da árvore de processos (MB) |
| `disk_mb` | real | razão | Disco do projeto após instalar: `node_modules` ou `.yarn`/`.pnp` (MB, hard links contados uma vez) |
| `cache_mb` | real | razão | Disco do cache/store global do gerenciador após a instalação (MB) |
| `n_files` | inteiro | razão | Nº de arquivos criados no projeto |
| `build_ok` | booleano | nominal | O `build` do projeto passou após a instalação (instalação válida) |
| `exit_code` | inteiro | nominal | Código de saída do comando de instalação |

## Regras de validação (`schema.validate`)

- Todas as colunas presentes, sem colunas a mais, com os tipos acima.
- `manager`, `scenario`, `project` e `registry` só aceitam os valores de `src/config.py`.
- Métricas (`wall_s`, `cpu_s`, `peak_rss_mb`, `disk_mb`, `cache_mb`, `n_files`) não negativas.
- `machine`, `run_id`, `project`, `scenario`, `manager`, `rep` e `wall_s` sem vazios.
- `run_id` único.

Instalações que falham **não são apagadas**: ficam com `build_ok = false` ou `exit_code ≠ 0`,
porque a compatibilidade também é resultado (ex.: Yarn PnP).

## Escalas e estatísticas permitidas

- **Razão** (tempo, disco, arquivos, memória): todas as estatísticas; como as distribuições são
  assimétricas, o grupo reporta mediana/IQR e usa testes não paramétricos e razões (speedup).
- **Nominal** (gerenciador, cenário, projeto, `build_ok`): contagens e proporções.
- **Ordinal** (`rep`, `order`): só ordenação. `order` serve para checar efeito de ordem/aquecimento.

## CSV sintético

`uv run lab05 synthetic` gera `data/raw/synthetic/runs.csv`, com 3 máquinas fictícias
(`sint-a`, `sint-b`, `sint-c`), o desenho completo (6 × 4 × 3 células), 5 repetições e 2
aquecimentos por bloco, semente fixa. **Os números são inventados** (ver os fatores em
[`src/synthetic.py`](../src/synthetic.py)). Não são hipóteses do grupo e não entram em nenhum resultado.
