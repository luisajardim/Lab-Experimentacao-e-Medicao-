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

`schema.load_runs()` junta os `data/raw/<maquina>/runs.csv` da coleta completa. Por padrão, ele
**ignora o sintético (`synthetic/`), o piloto (`pilot/`) e as rodadas de aquecimento**. O piloto
fica de fora porque roda numa das máquinas da coleta, com outros cenários e outro N: misturado, ele
duplicaria repetições do mesmo bloco. Para desenvolver antes da coleta completa, use
`include_pilot=True` ou `include_synthetic=True`.

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
| `disk_mb` | real | razão | Disco dos artefatos que a instalação criou no projeto: `node_modules`, `.pnp.*`, `.yarn/*` (MB) |
| `cache_mb` | real | razão | Disco do cache/store do gerenciador **sem** os arquivos já contados no projeto (MB) |
| `n_files` | inteiro | razão | Nº de arquivos criados no projeto |
| `build_ok` | booleano | nominal | O `build` do projeto passou após a instalação (instalação válida) |
| `exit_code` | inteiro | nominal | Código de saída da instalação (`124` = timeout) |

### Disco: como ler `disk_mb` e `cache_mb`

Cada arquivo é contado uma vez por inode (hard links), e links simbólicos/junctions não são
seguidos. O pnpm (e o Yarn com cache global) cria hard links entre o store e o `node_modules`;
esses arquivos entram em `disk_mb`, e o `cache_mb` fica só com o que está exclusivamente no
cache. Assim **`disk_mb + cache_mb` é a pegada total sem dupla contagem**, e é essa soma que a
análise usa para comparar o espaço ocupado. Detalhes da medição em [docs/runner.md](runner.md).

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
