# Runner de instalação (T04, #99)

`src/runner.py` produz `data/raw/<maquina>/runs.csv`, com uma linha por instalação medida (formato em
[schema.md](schema.md)). As métricas estão em `src/metrics.py`; o layout dos projetos-carga, em
[../projects/README.md](../projects/README.md).

```bash
uv run lab05 collect --machine bernardo --pilot --dry-run   # só mostra a sequência (182 instalações)
uv run lab05 collect --machine bernardo --pilot             # piloto: cold + warm-cache, 5 repetições
uv run lab05 collect --machine luisa --reps 10              # coleta completa (N vem da T09)
uv run python -m runner --help                              # mesmo programa, sem o cli
```

Opções: `--projects`, `--scenarios` e `--managers` (listas separadas por vírgula),
`--registry {local,public}`, `--warmup` (padrão 2), `--timeout` por instalação em segundos
(padrão 900) e `--out`. **Retomada:** rodar de novo continua de onde parou, pulando as
instalações já gravadas (mesmos máquina, projeto, cenário, gerenciador, repetição, registry e
aquecimento). Cada linha é gravada com `flush`/`fsync` assim que termina.

## O que acontece em cada instalação

1. **Diretório limpo.** O projeto é copiado para `$LAB05_WORKDIR/run/<projeto>--<gerenciador>/`
   (padrão: `Enunciado 5/.work/`; mude no `.env`, ver `.env.example`), junto com os arquivos de
   `lockfiles/<gerenciador>/`. Nunca use um `tmpfs` (o `/tmp` do WSL fica na RAM).
   O lockfile só entra nos cenários que o têm.
2. **Cenário.** O cache do gerenciador é **sempre apagado e reconstruído do zero**, para conter só
   os pacotes deste projeto (senão o `cache_mb` misturaria projetos).
   - `cold`: sem lockfile, cache vazio, sem `node_modules`.
   - `ci`: com lockfile, cache vazio, sem `node_modules`.
   - `warm-cache`: uma instalação preparatória **não medida** enche o cache; depois os artefatos
     (`node_modules`, `.pnp.*`, `.yarn/unplugged`…) são apagados.
   - `reinstall`: instalação preparatória não medida, e tudo fica no lugar.
3. **Instalação medida** (`metrics.run_measured`), sem shell e com a saída num log em
   `$LAB05_WORKDIR/logs/<maquina>/<run_id>.log`. Se passar do timeout, a árvore de processos
   inteira é morta e `exit_code = 124`.
4. **Disco e arquivos** (ver a definição abaixo).
5. **Build** (`<gerenciador> run build`, não cronometrado) → `build_ok`. Se a instalação falhou,
   o build não roda e `build_ok = false`. Falhas **não** param a coleta.

A versão do gerenciador (`<bin> --version`, rodado dentro do projeto para o Yarn Berry valer)
e a do Node são lidas uma vez por coleta.

## Comandos por tratamento

| Tratamento | cold | ci / warm-cache | reinstall |
|---|---|---|---|
| npm | `install --no-audit --no-fund` | `ci --no-audit --no-fund` | `install --no-audit --no-fund` |
| pnpm | `install` | `install --frozen-lockfile` | `install --frozen-lockfile` |
| Bun | `install` | `install --frozen-lockfile` | `install --frozen-lockfile` |
| Yarn Classic | `install` | `install --frozen-lockfile` | `install --frozen-lockfile` |
| Yarn Berry (nm/PnP) | `install` | `install --immutable` | `install --immutable` |

- **`--no-audit --no-fund` no npm:** o audit faz uma requisição extra ao registry, que o Verdaccio
  nem sempre atende, e nenhum outro gerenciador audita na instalação. É a configuração típica de CI.
- **Yarn Classic e Berry usam o mesmo binário `yarn`.** O Berry é escolhido pelo `yarnPath` do
  `.yarnrc.yml` do tratamento.
- O runner tira do ambiente as variáveis `CI`, `NODE_ENV`, `npm_config_production` e
  `YARN_ENABLE_IMMUTABLE_INSTALLS`, que mudariam o comportamento das ferramentas de uma máquina para outra.

## Cache isolado por gerenciador

Cada tratamento usa `$LAB05_WORKDIR/cache/<gerenciador>/`, definido **só por variáveis de ambiente**
(a configuração global do usuário não é tocada). O registry vem de `registry.registry_env` (T02).

| Tratamento | Variáveis |
|---|---|
| npm | `npm_config_cache` |
| pnpm | `npm_config_store_dir` (store), `npm_config_cache_dir` (metadados), `npm_config_state_dir` |
| Bun | `BUN_INSTALL_CACHE_DIR` |
| Yarn Classic | `YARN_CACHE_FOLDER` |
| Yarn Berry | `YARN_ENABLE_GLOBAL_CACHE=true`, `YARN_GLOBAL_FOLDER` (o cache fica em `<global>/cache`), `YARN_CACHE_FOLDER` |

O cache fica **no mesmo disco** do diretório de trabalho. O pnpm e o Yarn só criam hard links
quando store e projeto estão no mesmo volume; em volumes diferentes eles copiam os arquivos e
o resultado muda. Não aponte `LAB05_WORKDIR` para outro disco no meio da coleta.

## Definição de disco (`disk_mb`, `cache_mb`, `n_files`)

- **`disk_mb`**: soma dos arquivos que a instalação cria **no projeto** (`node_modules`,
  `.pnp.cjs`, `.pnp.loader.mjs`, `.pnp.data.json`, `.yarn/unplugged`, `.yarn/cache`,
  `.yarn/install-state.gz`), contando cada inode uma vez.
- **`cache_mb`**: soma do cache/store do gerenciador, **excluindo os inodes já contados no
  projeto**. Assim, `disk_mb + cache_mb` é a pegada total da instalação, sem contar duas vezes o
  que o pnpm (ou o Bun e o Yarn) ligou por hard link entre o store e o `node_modules`.
- **`n_files`**: nº de arquivos (inodes distintos) criados no projeto.
- Links simbólicos e junctions (o pnpm usa junctions no Windows) **não** são seguidos nem
  contados. O tamanho é o tamanho aparente (`st_size`), não o espaço em blocos. MB = 1024².

Consequência para a análise: no pnpm, a maior parte dos bytes aparece em `disk_mb`, porque está
ligada nos dois lugares e conta no projeto. Comparações de pegada total devem usar
`disk_mb + cache_mb`.

## Ordem e aquecimento

A sequência de uma máquina tem as rodadas de aquecimento (`warmup = true`, `rep = 0`, células
sorteadas) e depois, para cada repetição, uma permutação aleatória de todas as células. A
semente é `SEED + sha256(nome da máquina)`, estável entre execuções (`hash()` do Python não serve,
porque muda a cada processo). `order` é a posição global na sequência e não muda na retomada.

## Limitações conhecidas

- **CPU e RAM por amostragem.** O psutil amostra a árvore de processos a cada 50 ms. Filhos que
  vivem menos que isso podem não entrar no pico de RSS nem na CPU. No Linux/WSL a CPU é
  complementada por `getrusage(RUSAGE_CHILDREN)` (maior dos dois valores); **no Windows a CPU é só
  a amostrada** e tende a subestimar. Por isso `wall_s` é a métrica principal e CPU/RAM são secundárias.
- **Windows:** os executáveis são resolvidos com `shutil.which` (`npm.cmd`, `pnpm.cmd`, `yarn.cmd`).
  A remoção usa caminhos `\\?\` (contorna o limite de 260 caracteres), limpa o atributo de somente
  leitura e tenta de novo quando o antivírus segura algum arquivo. O Defender fica no padrão,
  conforme o protocolo, e entra como ameaça à validade.
- **Instalação preparatória falhando** (warm-cache/reinstall): o runner avisa no terminal e mede
  mesmo assim. A falha aparece na instalação medida (`exit_code`/`build_ok`).
- O runner não aquece o Verdaccio: isso é a T02 (`uv run lab05 registry warm`).

## Checagem de versões antes da coleta

Antes da primeira instalação, `collect` confere se o Node e cada gerenciador estão na versão
esperada (`expected_version` em `src/config.py`, que bate com `scripts/windows_portable.ps1`) e
**aborta** se algum não estiver. O motivo principal: o Yarn Classic 1.22 obedece ao `yarnPath` de
um `.yarnrc.yml` em **qualquer pasta acima** do projeto (ou na home). Um arquivo esquecido
transformaria o tratamento `yarn-classic` em Berry sem aviso, com as linhas rotuladas errado
(conferido em 14/11: numa pasta isolada responde 1.22.22; abaixo de um `.yarnrc.yml` com
`yarnPath`, responde 4.18.1). `--skip-version-check` desliga a checagem, só para depurar.
