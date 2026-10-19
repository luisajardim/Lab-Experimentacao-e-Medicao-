# firezone/firezone

Repositório: https://github.com/firezone/firezone

## Metadados

- Linguagem: Elixir

## Releases sorteadas

### Release 1

Link: https://github.com/firezone/firezone/releases/tag/0.4.4
- Tag: `0.4.4`
- Nome: 0.4.4
- Publicada em: 2022-06-22
- Release anterior (cronológica): `0.4.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  Restart phoenix on setcap; only pick the latest erts path (#740)
-  set default MTU to 1280 (#742)
-  Add user_count, device_count, users_with_mfa_count (#741)

### Release 2

Link: https://github.com/firezone/firezone/releases/tag/0.6.14
- Tag: `0.6.14`
- Nome: 0.6.14
- Publicada em: 2022-12-24
- Release anterior (cronológica): `0.6.13`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Don't cache Elixir build in static_analysis workflow (#1227)
-  fix: endpoint migration when `EXTERNAL_URL` is not present (#1232)
-  Removes `hammer` and `hammer_plug` deps and their code references (#1230)
-  Change foreign key constraint to cascading delete (#1235)

### Release 3

Link: https://github.com/firezone/firezone/releases/tag/gui-client-1.3.5
- Tag: `gui-client-1.3.5`
- Nome: gui-client-1.3.5
- Publicada em: 2024-09-25
- Release anterior (cronológica): `gui-client-1.3.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 21

-  ci: Bump Apple and GUI versions (#6776)
-  docs(client/linux): document known issue with ZFS (#6756)
-  docs(contributing): corrections (#6760)
-  chore(rust/gui-client): Iced prototype (#6606)
-  fix(portal): Fallback to the user token if service account token is not available (#6764)
-  docs: Add known issue regarding macOS and SentinelOne agent (#6784)
-  fix(portal): Do not break Flowbite popovers on DOM patching (#6787)
-  fix(connlib): blackhole DNS HTTPS type queries for resources (#6788)
-  chore(codespell): tell codespell to ignore `rust/iced-client/target` (#6785)
-  fix(client/linux): bump `atomicwrites` to fix behavior on ZFS (#6780)
-  chore(infra): Add Microsoft TXT verification record (#6771)
-  fix(portal): Throttle reqs/sec and scheduled frequency on Okta sync jobs (#6794)
-  fix(portal): Fix order of desc and name (#6796)
-  test(rust/gui-client/auth): manual test for auto-sign-in with invalid token (#6792)
-  fix(portal): Update IDP sync error notification threshold (#6797)
-  fix(rust/gui-client/auth): destroy the connlib session on disconnect (#6795)
-  build(deps): Bump clap from 4.5.4 to 4.5.13 in /rust (#6800)
-  build(deps): Bump tauri-runtime from 0.14.4 to 0.14.5 in /rust (#6799)
-  chore(kotlin/android): add TODO comment (#6813)
-  docs(maintainers): suggest always keeping a draft entry open (#6790)
-  refactor(android): Fix Kotlin compile warnings (#6773)

### Release 4

Link: https://github.com/firezone/firezone/releases/tag/android-client-1.4.5
- Tag: `android-client-1.4.5`
- Nome: android-client-1.4.5
- Publicada em: 2025-03-17
- Release anterior (cronológica): `macos-client-1.4.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(nenhum commit novo)_

### Release 5

Link: https://github.com/firezone/firezone/releases/tag/apple-client-1.5.20
- Tag: `apple-client-1.5.20`
- Nome: apple-client-1.5.20
- Publicada em: 2026-09-15
- Release anterior (cronológica): `android-client-1.5.14`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 24

-  fix(ci): select store screenshots from the submission commit (#15137)
-  build(deps): bump jsonschema from 0.51.0 to 0.52.0 in /rust (#15111)
-  build(deps): bump lru from 0.18.2 to 0.18.4 in /rust (#15102)
-  build(deps): bump toml from 1.1.4+spec-1.1.0 to 1.1.5+spec-1.1.0 in /rust (#15099)
-  build(deps): bump mio from 1.2.2 to 1.2.3 in /rust (#15093)
-  build(deps): bump uuid from 1.25.0 to 1.26.0 in /rust (#15090)
-  fix(apple): refresh store screenshot selection and sizes (#15138)
-  fix(android): use the Intune track name for submissions (#15139)
-  build(deps): bump rcgen from 0.14.9 to 0.14.10 in /rust (#15107)
-  fix(android): update store assets only for production (#15140)
-  build(deps): bump tokio-rustls from 0.26.4 to 0.26.5 in /rust (#15105)
-  fix(portal): preserve conn state on request body errors (#15127)
-  fix(portal): return valid provisioned gateway token (#15142)
-  fix(android): report the user's device name to the portal (#15124)
-  build(deps): bump oban_web from 2.12.6 to 2.12.7 in /elixir (#15077)
-  fix(portal): serialize directory sync jobs without a lock (#15067)
-  fix(portal): render errors with the conn after a body read (#15147)
-  fix(portal): name the directory sync column Last Full Sync (#15148)
-  fix(portal): keep a synced actor's name and email current (#15146)
-  chore(gui-client): serve the Apple mock scenario (#15143)
-  chore(apple): collect MetricKit diagnostics (#15150)
-  ci(apple): photograph the macOS menu bar menu (#15141)
-  fix(gui-client): keep redirected stdout on console attach (#15116)
-  refactor(gui-client): flatten and hide the command tree (#15152)
