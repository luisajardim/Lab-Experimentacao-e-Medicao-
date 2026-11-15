# Projetos-carga (T03, #98)

Contrato de layout que o runner (T04, #99) espera. Cada projeto é uma pasta com o nome usado em
`src/config.py` (`PROJECTS`): `express-api`, `react-vite`, `next-app`.

```
projects/<projeto>/
├── package.json              # versões EXATAS (sem ^ ou ~), com script "build"
├── <código do projeto>       # src/, index.html, next.config.* etc.
└── lockfiles/
    ├── npm/package-lock.json
    ├── pnpm/pnpm-lock.yaml
    ├── bun/bun.lock
    ├── yarn-classic/yarn.lock                 # lockfile v1
    ├── yarn-berry-nm/
    │   ├── yarn.lock                          # lockfile v4 (Berry)
    │   ├── .yarnrc.yml                        # nodeLinker: node-modules + yarnPath
    │   └── .yarn/releases/yarn-4.x.y.cjs
    └── yarn-berry-pnp/
        ├── yarn.lock
        ├── .yarnrc.yml                        # nodeLinker: pnp + yarnPath
        └── .yarn/releases/yarn-4.x.y.cjs
```

## Como o runner usa isto

1. Copia `projects/<projeto>/` para um diretório de trabalho, **sem** `lockfiles/`,
   `node_modules/`, `.pnp.*`, `dist/`, `.next/` e `.turbo/`.
2. Copia por cima o conteúdo de `lockfiles/<gerenciador>/`:
   - os **lockfiles** (`package-lock.json`, `pnpm-lock.yaml`, `bun.lock`, `yarn.lock`) só entram
     nos cenários com lockfile (`ci`, `warm-cache`, `reinstall`). No `cold` ficam de fora;
   - **todo o resto** (`.yarnrc.yml`, `.yarn/releases/`, `.npmrc` do projeto etc.) entra sempre.
3. Instala, mede, roda `<gerenciador> run build` e apaga tudo antes da próxima instalação.

## Regras

- **Mesmo `package.json` para os 6 tratamentos.** O que muda entre eles fica em `lockfiles/<gerenciador>/`.
- **Yarn Classic × Berry:** os dois usam o mesmo binário `yarn` (1.22, instalado global). O Berry
  é ativado pelo `yarnPath` do `.yarnrc.yml`, apontando para o release versionado em
  `.yarn/releases/` (o Yarn 1.22 respeita o `yarnPath`). **Não** use o campo `packageManager` do
  `package.json`, porque ele valeria para todos os tratamentos e acionaria o Corepack.
- **Não ponha registry nem cache no `.yarnrc.yml`/`.npmrc`.** O runner define os dois por
  variáveis de ambiente (Verdaccio local ou registry público, e um cache isolado por gerenciador).
- **Gere os lockfiles contra o registry local** (`uv run lab05 registry up`), para que todos
  resolvam as mesmas versões e o Verdaccio já tenha os pacotes no cache.
- O `build` precisa provar que a instalação funciona (ex.: `vite build`, `next build`,
  `node -e "require('express')"` na API). Ele **não** é cronometrado: só vira `build_ok`.
- Nada de `postinstall` próprio no projeto: o tempo medido deve ser só do gerenciador.

Para conferir o layout antes da coleta: `uv run lab05 collect --machine teste --dry-run`
mostra a sequência, e uma rodada curta com `--reps 1 --scenarios cold --projects <projeto>`
mostra se os 6 tratamentos instalam e passam no build.
