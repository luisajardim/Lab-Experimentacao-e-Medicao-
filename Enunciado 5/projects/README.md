# Projetos-carga (T03, #98)

Os três projetos Node que servem de **carga** do experimento. A regra do enunciado é que o
objeto de estudo seja o *gerenciador em funcionamento*, não um repositório de terceiros: por isso
os projetos são gerados aqui, pelos **templates oficiais**, e não clonados.

Os nomes das pastas são os de `src/config.py` (`PROJECTS`): `express-api`, `react-vite`,
`next-app`.

## Os três projetos

| Projeto | Origem | `build` | Diretas | Transitivas | Total no lockfile | Instalados no Windows x64 |
|---|---|---|---:|---:|---:|---:|
| `express-api` | escrito à mão (não há template oficial para um servidor Express) | `node scripts/build.cjs` | 4 | 82 | 86 | 86 |
| `react-vite` | `npm create vite@9.3.4 -- --template react-ts` | `vite build` | 9 | 88 | 97 | 28 |
| `next-app` | `npx create-next-app@16.4.6 --ts --app --no-eslint --no-tailwind --no-src-dir --no-import-alias` | `next build --webpack` | 7 | 53 | 60 | 27 |

- **Diretas** = `dependencies` + `devDependencies` do `package.json`; **transitivas** = o resto das
  entradas do `lockfiles/npm/package-lock.json`. Contagens conferidas em 16/11/2026, com o
  Verdaccio ligado.
- **Total no lockfile × instalados:** o lockfile lista os binários de *todas* as plataformas
  (`vite` 8 e `oxlint` trazem um pacote por SO/arquitetura; o `next`, o SWC). No Windows x64 só
  um de cada é instalado — daí 97 → 28 e 60 → 27 (`npm ls --all --parseable`). Os três projetos
  dão um contraste útil: a API tem **muitos pacotes pequenos**, os dois front-ends têm **poucos
  pacotes grandes**.

Dependências diretas, todas com **versão exata** (sem `^` ou `~`):

- `express-api`: `express` 5.3.0, `cors` 2.8.6, `morgan` 1.12.1, `compression` 1.8.2.
- `react-vite`: `react` e `react-dom` 19.3.1; dev: `vite` 8.3.8, `@vitejs/plugin-react` 6.3.0,
  `typescript` 7.0.2, `oxlint` 1.94.0, `@types/node` 24.19.2, `@types/react` e
  `@types/react-dom` 19.3.0.
- `next-app`: `next` 16.4.6, `react` e `react-dom` 19.3.0; dev: `typescript` 5.9.3,
  `@types/node` 20.19.43, `@types/react` e `@types/react-dom` 19.3.0.

O `build` é o critério de **instalação válida** (`build_ok` no CSV): não é cronometrado, só
precisa provar que o que foi instalado funciona. Nos front-ends é o build de produção do próprio
template; na API, `scripts/build.cjs` sobe o app numa porta efêmera e bate nas rotas.

### Dois ajustes no `build` por causa do Yarn PnP

O `build` tem de ser **o mesmo nos 6 tratamentos**, e os templates, como saem da caixa, não
constroem sob `nodeLinker: pnp`. Os dois ajustes abaixo valem para todos os tratamentos (não só
o PnP), justamente para não comparar builds diferentes entre si:

| Projeto | Template | Aqui | Por quê |
|---|---|---|---|
| `react-vite` | `tsc -b && vite build` | `vite build` (o `tsc -b` virou o script `typecheck`) | O `tsc` resolve a opção `types` do tsconfig (`vite/client`, `node`) por `node_modules/@types`, que não existe no PnP: dá `TS2688`. O `vite build` transpila o TypeScript do mesmo jeito, e é ele que prova que a instalação serve. |
| `next-app` | `next build` | `next build --webpack` | O Next 16 constrói com Turbopack por padrão, e o Turbopack resolve direto no filesystem, sem a API do PnP: `Could not find the Next.js package (next/package.json)`. Com o webpack o build passa nos 6 — e o type-check do próprio Next, que entende PnP, continua rodando. |

Nos dois casos a limitação é do PnP, não dos lockfiles: a **instalação** do PnP conclui sem erro
em todos os projetos. O Vite 8, inclusive, avisa na saída que "Using Yarn PnP with Vite is
discouraged" — vale como achado para a discussão do artigo (T17/T21).

## Contrato de layout

```
projects/<projeto>/
├── package.json              # versões EXATAS (sem ^ ou ~), com script "build"
├── <código do projeto>       # src/, index.html, next.config.* etc.
└── lockfiles/
    ├── npm/package-lock.json
    ├── pnpm/
    │   ├── pnpm-lock.yaml
    │   └── pnpm-workspace.yaml            # minimumReleaseAge: 0
    ├── bun/bun.lock
    ├── yarn-classic/yarn.lock                 # lockfile v1
    ├── yarn-berry-nm/
    │   ├── yarn.lock                          # lockfile do Yarn 4
    │   ├── .yarnrc.yml                        # nodeLinker: node-modules + yarnPath
    │   └── .yarn/releases/yarn-4.18.1.cjs
    └── yarn-berry-pnp/
        ├── yarn.lock
        ├── .yarnrc.yml                        # nodeLinker: pnp + yarnPath
        └── .yarn/releases/yarn-4.18.1.cjs
```

## Como o runner usa isto

1. Copia `projects/<projeto>/` para um diretório de trabalho, **sem** `lockfiles/`,
   `node_modules/`, `.pnp.*`, `dist/`, `.next/` e `.turbo/`.
2. Copia por cima o conteúdo de `lockfiles/<gerenciador>/`:
   - os **lockfiles** (`package-lock.json`, `pnpm-lock.yaml`, `bun.lock`, `yarn.lock`) só entram
     nos cenários com lockfile (`ci`, `warm-cache`, `reinstall`). No `cold` ficam de fora;
   - **todo o resto** (`.yarnrc.yml`, `.yarn/releases/`, `pnpm-workspace.yaml` etc.) entra sempre.
3. Instala, mede, roda `<gerenciador> run build` e apaga tudo antes da próxima instalação.

## Regras

- **Mesmo `package.json` para os 6 tratamentos.** O que muda entre eles fica em `lockfiles/<gerenciador>/`.
- **Yarn Classic × Berry:** os dois usam o mesmo binário `yarn` (1.22, instalado global). O Berry
  é ativado pelo `yarnPath` do `.yarnrc.yml`, apontando para o release versionado em
  `.yarn/releases/` (o Yarn 1.22 respeita o `yarnPath`). **Não** use o campo `packageManager` do
  `package.json`, porque ele valeria para todos os tratamentos e acionaria o Corepack.
  Como o Yarn 1.22 procura o `.yarnrc.yml` também nas **pastas acima** do projeto, não pode
  existir nenhum `.yarnrc.yml` em `projects/` nem na raiz do repositório (o runner confere as
  versões antes de coletar e aborta se o Yarn Classic responder como Berry).
- **Não ponha registry nem cache nas configs dos tratamentos.** O runner define os dois por
  variáveis de ambiente (Verdaccio local ou registry público, e um cache isolado por gerenciador).
- **Política de idade das versões desligada no pnpm e no Yarn Berry.** Dois dos seis
  gerenciadores recusam, por padrão, pacotes publicados há menos de 24 h: o Yarn 4.18
  (`npmMinimalAgeGate`, "quarantined") e o pnpm 12 (`minimumReleaseAge`, que só aceita a opção
  pelo `pnpm-workspace.yaml` — o `.npmrc` é ignorado). O npm, o Bun e o Yarn Classic não têm
  nada parecido. Com a política ligada, esses dois falham em instalações que os outros quatro
  concluem — foi o que aconteceu com o `oxlint` 1.94.0, publicado no dia em que os lockfiles
  foram gerados — e a diferença medida deixaria de ser o gerenciador. Pior: durante a coleta,
  qualquer dependência transitiva publicada nas últimas 24 h derrubaria células só nesses dois
  tratamentos. Por isso o valor é 0 nos dois, e essa é a **única** opção nesses arquivos além de
  `yarnPath` e `nodeLinker`.
- Nada de `postinstall` próprio no projeto: o tempo medido deve ser só do gerenciador.
- O `build` do `next-app` manda uma telemetria anônima. Para evitar essa chamada de rede durante
  a coleta, deixe `NEXT_TELEMETRY_DISABLED=1` no `.env` (está no `.env.example`): o runner repassa
  o ambiente do processo para o build.

## Como os lockfiles foram gerados

Com o **Verdaccio ligado** (`uv run lab05 registry up`) e com as versões fixadas em
`scripts/windows_portable.ps1`: Node 24.22.3, npm 11.19.1, pnpm 12.21.0, Yarn Classic 1.22.22,
Bun 1.4.4 e Yarn Berry 4.18.1 (o release em `lockfiles/yarn-berry-*/.yarn/releases/`).

Gerar com o registry local importa porque o lockfile guarda a URL de onde cada pacote veio:
`package-lock.json`, `bun.lock` e o `yarn.lock` v1 trazem `http://localhost:4873/...`. O
`pnpm-lock.yaml` e o `yarn.lock` do Berry guardam só o nome, a versão e o hash de integridade —
nesses dois o registry vem das variáveis de ambiente do runner, em qualquer cenário.

Para refazer um lockfile: com o Verdaccio de pé, copie `projects/<projeto>/` (sem `lockfiles/`)
e os arquivos de `lockfiles/<gerenciador>/` que **não** são lockfile para uma pasta de trabalho
fora do repo, rode a instalação daquele gerenciador com as variáveis de `src/runner.py`
(`build_env`) e traga só o lockfile de volta.

## Conferir antes da coleta

```bash
uv run lab05 registry up
uv run lab05 collect --machine teste --dry-run                       # a sequência
uv run lab05 collect --machine teste --reps 1 --warmup 0 \
  --scenarios cold --out <pasta temporária>/runs.csv                 # 6 tratamentos × 3 projetos
```

A segunda rodada gera um `runs.csv` de verdade (não commite esse teste): `exit_code = 0` e
`build_ok = True` nas 18 linhas é o critério de aceitação desta tarefa.
