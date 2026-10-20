# mvanhorn/cli-printing-press

Repositório: https://github.com/mvanhorn/cli-printing-press

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/mvanhorn/cli-printing-press/releases/tag/v1.3.1
- Tag: `v1.3.1`
- Nome: v1.3.1
- Publicada em: 2026-04-11
- Release anterior (cronológica): `v1.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  fix(cli): address Kalshi retro findings — --name flag, sync keys, primary key detection (#163) (#164)
-  chore(main): release 1.3.1 (#165)

### Release 2

Link: https://github.com/mvanhorn/cli-printing-press/releases/tag/v4.8.0
- Tag: `v4.8.0`
- Nome: v4.8.0
- Publicada em: 2026-05-16
- Release anterior (cronológica): `v4.7.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  fix(cli): use Chrome User-Agent for synthetic/cookie/composed/session_handshake CLIs (#1479)
-  fix(cli): probe nested path-param leaves so verify catches `args[]` index bugs (#1434)
-  fix(ci): switch queue update_method to merge so fork PRs can queue (#1492)
-  fix(cli): doctor preserves configured User-Agent when API uses UA as auth credential (#1361)
-  fix(cli): expand pm_stale timestamp-field list for non-updated_at APIs (#1461)
-  feat(cli): add ElevenLabs generation support (#1307)
-  fix(cli): short-circuit sync on dry-run sentinel response (#1471)
-  chore(main): release 4.8.0 (#1491)

### Release 3

Link: https://github.com/mvanhorn/cli-printing-press/releases/tag/v4.18.1
- Tag: `v4.18.1`
- Nome: v4.18.1
- Publicada em: 2026-05-27
- Release anterior (cronológica): `v4.18.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  chore(cli): ignore built cli-printing-press binary and .clawpatch (#2391)
-  fix(cli): apply store SQLite pragmas via modernc _pragma= DSN syntax (#2399)
-  fix(cli): gofmt Go source after publish-time module-path rewrite (#2405)
-  chore(main): release 4.18.1 (#2401)

### Release 4

Link: https://github.com/mvanhorn/cli-printing-press/releases/tag/v4.20.1
- Tag: `v4.20.1`
- Nome: v4.20.1
- Publicada em: 2026-06-01
- Release anterior (cronológica): `v4.20.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  fix(patches): emit per-patch directory layout (generator + skills) (#2581)
-  ci(ci): shard full-test and shallow-clone work jobs to cut merge-queue time (#2584)
-  chore(main): release 4.20.1 (#2583)

### Release 5

Link: https://github.com/mvanhorn/cli-printing-press/releases/tag/v4.31.3
- Tag: `v4.31.3`
- Nome: v4.31.3
- Publicada em: 2026-08-30
- Release anterior (cronológica): `v4.31.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  fix(cli): fail workflow archive when every resource errors (#4410)
-  fix(cli): use non-ticker alias fixture in learn teach test (#4409)
-  fix(cli): seed POST-query sync first page with id-walk filter (#4411)
-  fix(cli): recognize camelCase stemUid as resource primary key (#4412)
-  fix(cli): normalize hyphenated parent FK for typed-table sync (#4413)
-  fix(cli): chmod rewritten cache files to 0600 and skip multipart file IO on --dry-run (#4429)
-  fix(cli): apply --limit after HTML extraction, not on raw markup (#4432)
-  fix(cli): expose a queryable bare id for parent-keyed typed tables (#4434)
-  fix(cli): derive manifest, MCPB, and SKILL auth env vars from the credentials the binary reads (#4431)
-  fix(cli): stop --force reprint from keeping stale generated bodies (#4430)
-  chore(main): release 4.31.3 (#4415)
