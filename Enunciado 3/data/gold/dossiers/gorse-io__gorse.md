# gorse-io/gorse

Repositório: https://github.com/gorse-io/gorse

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/gorse-io/gorse/releases/tag/v0.2.0
- Tag: `v0.2.0`
- Nome: gorse v0.2.0
- Publicada em: 2021-06-05
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/gorse-io/gorse/releases/tag/v0.2.4
- Tag: `v0.2.4`
- Nome: gorse v0.2.4
- Publicada em: 2021-08-15
- Release anterior (cronológica): `v0.2.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  support Postgres
-  init mysql table engine innodb
-  redis password support (#218)
-  fixed division by zero (#221)
-  support ClickHouse as data storage
-  fix(#214): never distribute invalid model
-  disable popular/latest items under labels temporarily
-  find neighbors by similarity
-  trace stack of errors
-  support user import/export
-  implement task monitor
-  new task scheduler

### Release 3

Link: https://github.com/gorse-io/gorse/releases/tag/v0.2.8
- Tag: `v0.2.8`
- Nome: gorse v0.2.8
- Publicada em: 2021-11-06
- Release anterior (cronológica): `v0.2.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 14

-  remove redundant metrics
-  fix incompatibility of MariaDB (#294)
-  support modify users and items
-  fix invalid date in dashboard
-  chore: fix grammar (#296)
-  fix wrong documentation
-  support explore in recommendation
-  validate config values
-  skip empty list when inserting feedback (#300)
-  fix auto_insert_item = false (#301)
-  upgrade dashboard version (#302)
-  fix err logging in offline recommendation (#303)
-  pass exclude in explore (#304)
-  fix bug from bug fix (#305)

### Release 4

Link: https://github.com/gorse-io/gorse/releases/tag/v0.3.1
- Tag: `v0.3.1`
- Nome: gorse v0.3.1
- Publicada em: 2021-12-29
- Release anterior (cronológica): `v0.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 10

-  Fix concurrency write map panic (#338)
-  optimize deep copy (#337)
-  support total cold-start (#340)
-  optimize hidden items implementation (#341)
-  update latest in real time (#342)
-  update popular on server (#343)
-  cache item categories (#346)
-  fix race condition of map access (#347)
-  add bloom_filter index in ClickHouse (#349)
-  optimize fallback item-based recommender (#350)

### Release 5

Link: https://github.com/gorse-io/gorse/releases/tag/v0.4.11
- Tag: `v0.4.11`
- Nome: Gorse v0.4.11
- Publicada em: 2023-02-19
- Release anterior (cronológica): `v0.4.10`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  fix cors error with api key (#598)
-  polish Swagger docs (#601)
-  fix typo (#602)
-  support YAML/JSON configuration file format (#604)
-  worker: fix nil pointer in `refreshCache` (#611)
-  encode cursor by base64 (#612)
-  implement SVE2 vector multiplication (#614)
-  hide database config under managed mode (#616)
-  support Docker Windows images (#618)
-  change release archive file names (#619)
-  fix batch import feedback (#620)
-  support Windows log file sink (#621)
-  upgrade to Go 1.20 (#622)
-  support login by access token (#623)
-  allow empty feedback types in config (#624)
-  update DockerHub description (#625)
-  create temporary directory for scratch image (#627)
