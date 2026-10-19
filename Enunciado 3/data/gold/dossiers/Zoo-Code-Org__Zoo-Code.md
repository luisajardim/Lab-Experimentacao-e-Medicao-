# Zoo-Code-Org/Zoo-Code

Repositório: https://github.com/Zoo-Code-Org/Zoo-Code

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/Zoo-Code-Org/Zoo-Code/releases/tag/v3.54.1
- Tag: `v3.54.1`
- Nome: Zoo Code v3.54.1
- Publicada em: 2026-05-16
- Release anterior (cronológica): `v3.54.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 18

-  chore(deps): update node.js to v20.20.2 (#65)
-  test(e2e): add DeepSeek V4 coverage (#72)
-  fix: upgrade isbinaryfile to ^5.0.7 (#88)
-  fix: centralize Zoo Code support links (#77)
-  [Chore] Use repo collaborators as default code owners (#96)
-  [Docs] Refresh Zoo Code branding across docs and metadata (#85)
-  [Improve] Keep settings regression coverage in webview-ui tests (#95)
-  [Fix] Setup announcement shows the wrong origin and LM Studio misses models on first load (#97)
-  Clarify Zoo Code migration messaging in README (#99)
-  fix: update Zoo Code Discord invite links (#107)
-  [Fix] Settings and marketplace stay inaccessible after importing Roo Router settings (#109)
-  Update dependency @dotenvx/dotenvx to v1.66.0 (#61)
-  Update dependency lint-staged to v16.4.0 (#64)
-  [Chore] Clean up skipped extension package tests (#110)
-  fix: keep onboarding provider setup top-aligned (#113)
-  [Fix] Anthropic Opus 4.7 fails when reasoning is enabled (#111)
-  [Chore] Use a single PR flow for extension releases (#142)
-  [Chore] Prepare v3.54.1 release (#143)

### Release 2

Link: https://github.com/Zoo-Code-Org/Zoo-Code/releases/tag/v3.78.0
- Tag: `v3.78.0`
- Nome: Zoo Code v3.78.0
- Publicada em: 2026-08-15
- Release anterior (cronológica): `v3.76.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 38

-  chore: prepare v3.76.0 release (#1173)
-  [Refactor] Add shared test utilities and pilot refactors (#1171)
-  refactor(cli): canonicalize provider identifiers (#1110)
-  [Refactor] Reuse shared API options in provider tests (#1178)
-  refactor: reuse shared XAI response client mock (#1182)
-  refactor: reuse shared CustomModesManager test helpers (#1190)
-  fix(telemetry): record tool usage once centrally, sanitize raw tool names (#1073)
-  refactor: reuse code-index reset helpers (#1194)
-  refactor: reuse shared config test helpers (#1195)
-  refactor: reuse terminal test reset helpers (#1197)
-  refactor: reuse webview chat render helper (#1196)
-  fix(task): skip saveClineMessages when history task aborts before messages load (#1181)
-  refactor: reuse shared test helpers in config import/export spec (#1198)
-  refactor(webview): complete provider identifier migration (#1141)
-  chore(deps): update dependency mermaid to v11.16.1 [security] (#1193)
-  chore(deps): update dependency undici to v6.28.0 [security] (#1161)
-  refactor: reuse shared reset helper in code-index specs (#1199)
-  refactor: reuse shared reset helper in remaining code-index specs (#1200)
-  refactor(webview): use provider identifiers in ApiOptions (#1146)
-  refactor: reuse webview render helper in chat and settings specs (#1203)
-  refactor: reuse shared reset helper in provider specs (#1202)
-  refactor: reuse webview render helper in remaining settings specs (#1204)
-  refactor: reuse shared reset helper in semble and terminal specs (#1201)
-  refactor(webview): canonicalize provider model config identifiers (#1147)
-  [Fix] Azure OpenAI returns 404 with resource endpoint (#1192)
-  feat: add DCG support for macOS x86_64 (#1213)
-  refactor(webview): migrate provider identifiers in UI hooks (#1148)
-  refactor(providers): reuse retired Roo identifier (#1166)
-  fix(kimi-code): correct maxTokens defaults and add server-side override (#1217)
-  refactor(types): canonicalize shared provider settings identifiers (#1109)
-  [Feat] Add GLM 5.3 support to Z AI and OpenCode Go (#1244)
-  [Feat] Add Gemini 3.7 Flash support (#1241)
-  [Feat] Add Qwen3.8 Max to OpenCode Go (#1245)
-  [Fix] DeepSeek V4 costs are underestimated after pricing changes (#1237)
-  fix: update deepseek-v4-pro reasoning efforts and mappings (#1236)
-  feat(api): add NanoGPT provider support (#1239)
-  fix(config): use zoo-code-settings.json for settings export/import (#1177)
-  chore: prepare v3.78.0 release

### Release 3

Link: https://github.com/Zoo-Code-Org/Zoo-Code/releases/tag/v3.80.0
- Tag: `v3.80.0`
- Nome: Zoo Code v3.80.0
- Publicada em: 2026-08-22
- Release anterior (cronológica): `v3.78.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 27

-  chore: prepare v3.78.0 release (#1249)
-  fix(task): recover stale delegated children after restart (#1210)
-  fix(webview): throttle state pushes to prevent gray screen OOM (#1078)
-  refactor(webview): canonicalize provider and model message identifiers (#1143)
-  feat(api): support official GLM-5.3 Z.ai release (#1284)
-  feat(api): introduce RequestConfigBuilder for SDK-agnostic abort signal support (#1008)
-  fix(shell): delegate VS Code profile reads to Terminal methods (issue #634) (#1033)
-  [Fix] Mermaid labels are unreadable in light IDE themes (#1285)
-  refactor(providers): canonicalize model-router calls (#1165)
-  fix: stream reasoning_content in LM Studio provider (#1175)
-  lint(providers): enforce canonical identifiers (#1297)
-  fix(semble): increase archive download limit (#1306)
-  fix(task-history): atomic per-task merge and drop shared index file (#1231) (#1261)
-  [Fix] Chat controls fade into light IDE themes (#1298)
-  [Fix] Remaining chat controls fade into light IDE themes (#1312)
-  fix(telemetry): default telemetry to opt-out with explicit consent UI (#1069)
-  feat(models): add Gemini 3.5 Flash Lite and 3.1 Flash Lite to Gemini API provider (#1334)
-  [Chore] Enforce safe async handling in core tools (#1255)
-  fix(zoo-gateway): stop inventing UI cost from default model prices (#1339)
-  [Improve] Keep shared controls legible across IDE themes (#1333)
-  ci: upload test VSIX for pull requests (#1314)
-  feat: Add Read+Write allowlists (#1274)
-  fix(openai-codex): complete prompts over the streaming transport (#1243)
-  [Fix] NanoGPT Muse Spark fails during tool use (#1310)
-  fix(task): mark interrupted tool calls as errors in persisted history (#1323)
-  fix(config): await settings import persistence (#1340)
-  chore: prepare v3.80.0 release

### Release 4

Link: https://github.com/Zoo-Code-Org/Zoo-Code/releases/tag/v3.82.1
- Tag: `v3.82.1`
- Nome: Zoo Code v3.82.1
- Publicada em: 2026-09-12
- Release anterior (cronológica): `v3.82.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 24

-  chore: prepare v3.82.0 release (#1533)
-  ci: bump GitHub Actions to node24 runtimes (fixes Node 20 deprecation warnings) (#1534)
-  [Fix] Commits fail after users interrupt mutation tests (#1525)
-  [Fix] Tasks stall when interrupted subtasks resume (#1470)
-  [Fix] Task history disappears when user reopens a task (#1319)
-  [Fix] Reasoning models stop thinking after model selection (#1349)
-  [Fix] Provider settings contact unselected model services (#1425)
-  [Fix] Task history can disappear when users restart after completion (#1452)
-  fix(webview): ignore blank or missing follow-up suggestion answers (#1286)
-  [Chore] Refine CodeRabbit review checks (#1571)
-  [Chore] Clarify CodeRabbit approval checks (#1577)
-  Update dependency mammoth to v1.12.2 (#1472)
-  Update dependency globals to v16.5.0 (#1474)
-  Update dependency i18next to v25.10.10 (#1475)
-  Update dependency ink to v6.8.0 (#1477)
-  [Fix] MCP OAuth registration fails for servers advertising unsupported grants (#1532)
-  [Fix] Nested subtask tool calls no longer stall (#1494)
-  [Fix] OpenCode Go context meter shows incorrect limits (#1428)
-  fix(nanogpt): preserve optional tool parameters (#1590)
-  refactor(providers): finish canonical identifier audit (#1493)
-  test(code-index,tools): cover lines left uncovered by #1297 (#1317)
-  test(e2e): add LM Studio reasoning_content e2e guard (#1322)
-  [Fix] Review labels disappear after base updates (#1584)
-  chore: prepare v3.82.1 release

### Release 5

Link: https://github.com/Zoo-Code-Org/Zoo-Code/releases/tag/v3.88.0
- Tag: `v3.88.0`
- Nome: Zoo Code v3.88.0
- Publicada em: 2026-10-10
- Release anterior (cronológica): `v3.86.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_
