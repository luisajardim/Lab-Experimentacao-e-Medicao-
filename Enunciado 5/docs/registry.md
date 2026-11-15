# Registry local (Verdaccio) — T02 (#97)

## Por que

- **Isolar o efeito do gerenciador.** Se a instalação baixasse do registry público, o tempo
  misturaria a velocidade do gerenciador com a internet de cada casa (ameaça à validade interna).
  Com um registry local, a rede vira `localhost` e é igual para os 6 tratamentos.
- **Ética.** A coleta faz centenas de instalações. Com o Verdaccio fazendo cache, cada pacote é
  baixado do `registry.npmjs.org` **uma única vez** e depois servido do storage local
  (`registry/storage/`, fora do git).
- A checagem de validade externa contra o registry real fica na T19 (#116).

Versão fixada: **Verdaccio 7.1.0** (`VERDACCIO_VERSION` em `src/registry.py`), executado via
`npx`, sem instalação global. Configuração em [`registry/config.yaml`](../registry/config.yaml):
storage local, uplink `npmjs` com cache, leitura liberada, publicação bloqueada, interface web desligada.

## Comandos

```bash
uv run lab05 registry up       # sobe em segundo plano em http://localhost:4873/ (idempotente)
uv run lab05 registry status   # checa /-/ping
uv run lab05 registry warm     # pré-aquece o cache com os projetos de projects/ (T03, #98)
uv run lab05 registry down     # encerra (idempotente)
```

(Equivalente: `uv run python -m registry <ação>`.) Log em `registry/verdaccio.log`.

## Como cada gerenciador é apontado para o registry

Só por **variáveis de ambiente** (`registry_env(manager, registry)`). Nada é escrito nos
`.npmrc`/`.yarnrc` globais do usuário.

| Gerenciador | Variáveis |
|---|---|
| npm, pnpm | `npm_config_registry=http://localhost:4873/` |
| Bun | `BUN_CONFIG_REGISTRY` + `npm_config_registry` |
| Yarn Classic | `YARN_REGISTRY` + `npm_config_registry` |
| Yarn Berry (nm e PnP) | `YARN_NPM_REGISTRY_SERVER=http://localhost:4873` + `YARN_UNSAFE_HTTP_WHITELIST=localhost` (o Berry recusa http sem isso) |

Com `registry="public"`, as mesmas variáveis apontam para `https://registry.npmjs.org/`, e o
Yarn Berry fica sem a whitelist de http.

**Atenção aos lockfiles:** o lockfile guarda a URL de onde cada pacote veio (`resolved`). Os
lockfiles dos projetos-carga (T03) devem ser gerados **com o Verdaccio** para que a instalação no
cenário `ci` não volte a buscar no registry público.

## Critério de aceitação: instalação offline

1. `uv run lab05 registry up` e depois `uv run lab05 registry warm`.
2. Desligue a internet (ou o Wi-Fi).
3. Num diretório temporário, instale um projeto aquecido com cada tratamento usando as variáveis
   acima e um cache vazio. A instalação deve concluir sem erro. Quem conclui sem rede está, de
   fato, lendo do Verdaccio.

Checagem rápida feita na T02 (Linux/WSL): `up` → `npm install is-number` com
`npm_config_registry` local e cache temporário → o `package-lock.json` registrou
`"resolved": "http://localhost:4873/is-number/-/is-number-7.0.0.tgz"` → `down` sem processos órfãos.
