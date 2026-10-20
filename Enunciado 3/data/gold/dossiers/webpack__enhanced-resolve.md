# webpack/enhanced-resolve

Repositório: https://github.com/webpack/enhanced-resolve

## Metadados

- Linguagem: JavaScript

## Releases sorteadas

### Release 1

Link: https://github.com/webpack/enhanced-resolve/releases/tag/v5.4.0
- Tag: `v5.4.0`
- Nome: (sem nome)
- Publicada em: 2020-12-02
- Release anterior (cronológica): `v5.3.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  chore(deps): remove unused graceful-fs
-  fix: actual use graceful-fs, per review comment
-  Merge pull request #262 from AviVahl/remove-unused-graceful-fs
-  remove fullySpecified when resolving a module request with PnP
-  Merge pull request #266 from webpack/bugfix/pnp-fully-specified
-  5.4.0

### Release 2

Link: https://github.com/webpack/enhanced-resolve/releases/tag/v4.4.0
- Tag: `v4.4.0`
- Nome: (sem nome)
- Publicada em: 2021-01-11
- Release anterior (cronológica): `v5.4.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  Setup github actions
-  add test case to test fatal errors in root path resolving
-  add workaround to ignore fatal errors during root paths resolving to avoid a breaking change
-  Merge pull request #274 from webpack/bugfix/error-in-root-path
-  4.4.0

### Release 3

Link: https://github.com/webpack/enhanced-resolve/releases/tag/v5.16.0
- Tag: `v5.16.0`
- Nome: v5.16.0
- Publicada em: 2024-03-11
- Release anterior (cronológica): `v5.15.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 4

Link: https://github.com/webpack/enhanced-resolve/releases/tag/v5.21.0
- Tag: `v5.21.0`
- Nome: v5.21.0
- Publicada em: 2026-04-23
- Release anterior (cronológica): `v5.20.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 76

-  fix(ExportsFieldPlugin): prevent fallback to parent node_modules when exports target is missing (#495)
-  chore(deps-dev): bump flatted from 3.4.1 to 3.4.2 (#497)
-  chore(deps-dev): bump memfs from 4.56.11 to 4.57.1 in the dependencies group (#498)
-  chore(deps): bump codecov/codecov-action from 5.5.2 to 5.5.3 in the dependencies group (#499)
-  chore(deps-dev): bump picomatch from 2.3.1 to 2.3.2 (#501)
-  fix(TsconfigPathsPlugin): gracefully handle missing tsconfig.json (#502)
-  fix(imports): prevent chained resolution of non-relative imports targets (#503)
-  chore(deps): bump the dependencies group with 2 updates (#504)
-  chore(deps): bump the dependencies group with 2 updates (#506)
-  chore(deps-dev): bump eslint-config-webpack from 4.9.4 to 4.9.5 in the dependencies group (#508)
-  chore(deps-dev): bump lodash from 4.17.23 to 4.18.1 (#511)
-  chore(deps-dev): bump cspell from 9.7.0 to 10.0.0 (#509)
-  chore(deps-dev): bump typescript from 5.9.3 to 6.0.2 (#505)
-  chore(deps-dev): bump tooling from v1.25.0 to v1.26.0 (#510)
-  chore(deps-dev): bump prettier from 3.8.1 to 3.8.2 in the dependencies group (#513)
-  chore(deps): bump the dependencies group with 2 updates (#515)
-  chore(deps-dev): bump tooling from v1.26.0 to v1.26.1 (#514)
-  chore(bench): add tinybench-based performance benchmark suite (#512)
-  test: add benchmarks cases
-  chore(deps-dev): bump follow-redirects from 1.15.11 to 1.16.0 (#517)
-  test: more benchmarks cases
-  fix: move join/dirname/basename caches to Resolver instance to prevent memory leak (#507)
-  ci: improve time (#522)
-  feat: add promise API for resolve (#520)
-  test: improve coverage (#521)
-  perf: cache stripJsonComments + JSON.parse result in readJson via WeakMap (#524)
-  fix: avoid OOM in CachedInputFileSystem when duration is Infinity (#527)
-  perf: singly-linked StackEntry for resolver stack with Set-like API (#526)
-  test: added stack perf case
-  test: add node-compare benchmark + perf: Promise.withResolvers in resolvePromise (#525)
-  perf(alias): avoid per-resolve split("*") in AliasUtils scan (#529)
-  perf: precompile AliasPlugin options to speed up huge alias lists (#528)
-  test: document multi-target alias watch-mode fallback (#395) (#531)
-  perf: some improvements
-  test: more performance cases
-  docs: document built-in plugins and custom plugin authoring (#537)
-  feat(Resolver): allow optional context and resolveContext on resolve* (#536)
-  Fix use basename helper everywhere (#538)
-  chore(deps): bump the dependencies group with 3 updates (#540)
-  chore(deps): bump the dependencies group with 9 updates (#539)
- ... e mais 36 commits

### Release 5

Link: https://github.com/webpack/enhanced-resolve/releases/tag/v5.22.2
- Tag: `v5.22.2`
- Nome: v5.22.2
- Publicada em: 2026-06-03
- Release anterior (cronológica): `v5.22.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  chore(deps): bump CodSpeedHQ/action from 4.15.1 to 4.17.0 in the dependencies group (#599)
-  chore(deps-dev): bump the dependencies group with 4 updates (#598)
-  fix: fall back when an exports target is filtered out by restrictions (#600)
-  chore(release): new release (#601)
