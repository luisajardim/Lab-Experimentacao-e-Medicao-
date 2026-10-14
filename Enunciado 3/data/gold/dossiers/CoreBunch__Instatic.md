# CoreBunch/Instatic

Repositório: https://github.com/CoreBunch/Instatic

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/CoreBunch/Instatic/releases/tag/v0.0.4
- Tag: `v0.0.4`
- Nome: Instatic 0.0.4
- Publicada em: 2026-06-13
- Release anterior (cronológica): `v0.0.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 42

-  ci/docs: standardize on GHCR, drop the Docker Hub mirror (#20)
-  Per-stylesheet import modes; remove generated import scope classes (#15)
-  Fix import fidelity: rgba color tokens and import-from-anywhere (#19)
-  Make var()/env() declarations engine-proof at the import boundary (#21)
-  Fix plugin useCanvasNodeRect: measure real canvas nodes, not admin chrome (#22)
-  perf: fix critical hot paths across publish pipeline, public serving, and editor store (#24)
-  fix(ai): derive credential auth from provider (#30)
-  perf: incremental site saves; hoist runtime builds out of the publish transaction (#27)
-  perf(canvas): kill per-node selector storms, per-frame DOM re-measures, and whole-site loop subscriptions (#28)
-  perf(plugins): handle-based VM dispatch, native base64, and indexed content-API lookups (#29)
-  Content Outlet availability + toast layering; close outlet invariant holes (#23)
-  Per-module published-JS channel; migrate the form runtime onto it (#26)
-  Inline text editing on the canvas (double-click to edit) (#25)
-  Clean up Style-rules review: drop ambient/class badges, fix CSS file marker, space the search (#31)
-  fix(canvas): scope the template read-only hint/open to chrome, not page content (#32)
-  feat(editor): user-saved layouts — save any subtree, re-insert it exactly (#33)
-  fix(canvas): live mode shows the shared frame skeleton while hydrating (#35)
-  feat(editor): remove inconsistent panel keyboard shortcuts from the rail (#36)
-  feat(canvas): open design mode at 50% zoom; pin live mode to 100% (#34)
-  fix(cms): make roster saves survive slug handoffs — homepage swap, swaps, revivals (#37)
-  refactor(publish): one-way layering — repositories never import the publish layer (#38)
-  refactor(publisher): single class-CSS emission engine for publish and canvas (#39)
-  fix(media): stop serving multi-MB originals to retina screens — variants-only srcset (#40)
-  refactor(explorer): one structural-row enumeration + shared dnd pointer math (#46)
-  docs(agents): document PR conventions (#50)
-  Add a "Not found" template target for designed 404 pages (#52)
-  refactor(vc): one slot-outlet collector — export it from @core/visualComponents (#44)
-  refactor(vc): split vcTreeOps out of visualComponentsSlice (#47)
-  Add double-click rename shortcuts (#49)
-  chore(cleanup): dead-code spring cleanup — knip reports zero unused surface (#41)
-  refactor(siteImport): one adapter contract, phase-decomposed pipeline, deduped helpers (#42)
-  refactor(siteImport): decompose conflict-resolution hotspots into named concerns (#43)
-  feat(publisher): derive <img sizes> from the layout — remove the manual Sizes field (#45)
-  fix(ai): tools inherit caller capabilities instead of ai.chat acting as a blanket read grant (#51)
-  fix(editor): apply node inline styles in read-only composed canvas content (#54)
-  fix(admin): redirect unknown admin URLs to the dashboard instead of a blank page (#55)
-  chore(release): prepare v0.0.4 (#56)
-  fix(test): wait on canvas frame readiness instead of fixed sleeps (#57)
-  refactor(canvas): mount breakpoint frames directly, drop progressive staggering (#58)
-  test(canvas): render CanvasTransformLayer directly in the no-staggering test (#59)
- ... e mais 2 commits

### Release 2

Link: https://github.com/CoreBunch/Instatic/releases/tag/v0.0.8
- Tag: `v0.0.8`
- Nome: Instatic 0.0.8
- Publicada em: 2026-07-01
- Release anterior (cronológica): `v0.0.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 14

-  feat(editor): unify Core Framework into one tabbed panel with declarative management (#123)
-  feat(editor): consolidate left panels into one tabbed Explorer panel (#128)
-  fix(spotlight): keep highlighted row in view (#125)
-  fix(onboarding): open framework import ready to import (pre-select Full) (#129)
-  Fix AI token tool argument leniency (#121)
-  feat(editor): drag media assets onto canvas
-  fix(security): audit follow-ups — response headers, import SVG sanitization, MCP token expiry (#115)
-  fix(editor): retain pending site reloads through remount (#130)
-  fix(editor): make canvas mouse scroll use shift-wheel sideways
-  chore(release): prepare 0.0.8
-  chore(release): complete 0.0.8 notes
-  test(canvas): stabilize breakpoint dimming assertion
-  test(canvas): scope breakpoint dimming query
-  fix(docker): exclude tests from release image build

### Release 3

Link: https://github.com/CoreBunch/Instatic/releases/tag/v0.0.9
- Tag: `v0.0.9`
- Nome: Instatic 0.0.9
- Publicada em: 2026-07-01
- Release anterior (cronológica): `v0.0.8`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  fix(canvas): show body menu on empty canvas right-click (#139)
-  feat(agent): interactive AI assistant panel — tool-call rows, swatches, previews, titles (#133)
-  chore(release): prepare 0.0.9 (#140)

### Release 4

Link: https://github.com/CoreBunch/Instatic/releases/tag/v0.0.14
- Tag: `v0.0.14`
- Nome: Instatic 0.0.14
- Publicada em: 2026-07-28
- Release anterior (cronológica): `v0.0.13`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  fix(publisher): preserve window scroll container (#269)
-  fix(import): preserve preformatted text node newlines
-  fix(security): parse URL schemes instead of prefix-matching in isSafeUrl (#275)
-  fix(editor): remove redundant publish success callout (#278)
-  fix(mcp): advertise the open-workspace requirement on browser tools (#281)
-  feat(loops): support contextual entry field iteration (#299)
-  feat(editor): undock and resize sidebar panels (#293)
-  fix(data): keep the page-tree Open editor button enabled on system tables
-  feat(data): upgrade the Data workspace and add repeater authoring (#303)

### Release 5

Link: https://github.com/CoreBunch/Instatic/releases/tag/v0.0.17
- Tag: `v0.0.17`
- Nome: Instatic 0.0.17
- Publicada em: 2026-08-30
- Release anterior (cronológica): `v0.0.16`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 29

-  feat(editor): add TypeScript script tooling (#367)
-  docs(data): describe the built-in value lock that actually exists (#360)
-  fix(data): stop the field dialog crashing outside a secure context (#326)
-  test(harness): reset every app store before each test (#400)
-  fix(content): keep the stored title in the sidebar after a create (#401)
-  fix(mcp): stream editor bridges through reverse proxies (#282)
-  fix(ui): restore Escape dismissal in settings and while tooltips show (#272)
-  fix(admin): expose AI settings navigation (#346)
-  fix(framework): parse space-separated hsl() color values (#307)
-  chore(changelog): open 0.0.17 instead of an Unreleased bucket (#402)
-  feat(loops): filter and order data-row loops by a cell value (#348)
-  fix(mcp/oauth): coerce client_id_issued_at to number for Postgres (#381)
-  fix(publish): wire entry SEO title and description into the published <head> (#419)
-  fix(page-tree): map NULL to U+FFFD in escapeCssIdentifier (#309)
-  fix(server): let platform auto-detection survive an invalid PUBLIC_ORIGIN (#328)
-  fix(plugin-sdk): scaffold one SDK specifier, not two (#391)
-  fix(db): give DbClient a close() so test teardown releases the handle (#327)
-  fix(loops): read the loop endpoint from the tag, not currentScript (#437)
-  fix(data): let the New field dialog accept camelCase ids (#436)
-  fix(templates): strip backslash from escaped \{ in token interpolation (#308)
-  fix(templates): interpolate tokens inside htmlAttributes (#353)
-  docs(loops): document the server-rendered loop page query parameter (#396)
-  fix(spotlight): allow mouse click to select select-type arg options (#424)
-  fix(publish): interpolate entry tokens in page meta title and description (#337)
-  docs(server): record the rule that publish diagnostics established (#398)
-  fix(site-import): report asset references the archive cannot satisfy (#349)
-  feat(loops): let a loop carry custom HTML attributes (#350)
-  refactor(publisher): hoist resolveHtmlTag into core (#438)
-  chore(release): prepare 0.0.17 (#439)
