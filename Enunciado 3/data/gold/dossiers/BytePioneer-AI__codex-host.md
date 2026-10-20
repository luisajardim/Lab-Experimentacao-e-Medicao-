# BytePioneer-AI/codex-host

Repositório: https://github.com/BytePioneer-AI/codex-host

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/BytePioneer-AI/codex-host/releases/tag/v0.4.4
- Tag: `v0.4.4`
- Nome: codexhost 0.4.4
- Publicada em: 2026-09-03
- Release anterior (cronológica): `v0.4.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  fix: restore historical conversations
-  chore: prepare v0.4.4

### Release 2

Link: https://github.com/BytePioneer-AI/codex-host/releases/tag/v0.9.0
- Tag: `v0.9.0`
- Nome: codexhost 0.9.0
- Publicada em: 2026-09-16
- Release anterior (cronológica): `v0.8.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 120

-  fix: keep settings dialog below Windows titlebar
-  test: guard missing settings fixture bundle
-  test: drop unused Playwright titlebar e2e
-  fix(shim): 隔离计算机历史摘要进程
-  fix(deepseek): deduplicate repeated file changes
-  fix(host-runtime): keep a Subagent Thread active while its Subagent runs
-  fix(renderer): mount settings trigger before native header actions
-  fix(opencode): isolate managed server working directory
-  test(opencode): satisfy exact optional property types
-  fix(remote-control): recover native threads through POSIX relays
-  fix(remote-control): recover native threads through POSIX relays
-  fix(remote-control): narrow POSIX bridge fallback matching
-  fix(remote-control): narrow POSIX bridge fallback matching
-  merge origin/main into codex/verify-critical-open-issues
-  fix(macos): resolve CLI for sanitized node_repl sandbox launches
-  fix(desktop-control): route remote drafts through host registry
-  feat(adapters): add Qoder harness adapter and Desktop integration
-  fix(qoder): update sdk dependency, forward session options, and fix event projection
-  fix(qoder): provide permission mode catalog, dynamic models, cancel cleanup, and fix lint
-  fix(qoder): update host runtime plugin test, return empty catalog on error, and ensure query close
-  fix(qoder): use official Qoder icon asset
-  fix(renderer): wait for request route before harness probing
-  fix(desktop): include Qoder in production renderer agents
-  fix(qoder): restore authenticated model discovery
-  fix(qoder): preserve native model groups and BYOK
-  fix(renderer): distinguish Qoder model group headings
-  fix(qoder): provide nativeTurnRef on turn completion for thread persistence
-  fix(qoder): echo toolUseID in permissions and tag pre-tool text as commentary
-  feat(qoder): support thread fork and history snapshot
-  fix(protocol-core): normalize file paths and format git diff headers for file mutating tools
-  fix(protocol-core): coalesce multiple file changes for the same path in turn diff
-  fix(qoder): track context window, total tokens and informative usage metrics
-  feat(qoder): implement rollbackLastTurn to support editing previous messages
-  feat(qoder): enable model reasoning effort / thinking option selection
-  fix(protocol-core): emit raw file content for added and deleted files in item change to prevent extra git diff header lines
-  fix(qoder): omit sessionId in QoderOptions when resuming existing session
-  fix(qoder): enrich usage extraction from sdk context and usage info
-  fix(renderer): refresh request bridge for message editing
-  feat(qoder): add native slash command catalog and execution support
-  fix(qoder): dynamically map sdk commands and restrict headless execution to compact
- ... e mais 80 commits

### Release 3

Link: https://github.com/BytePioneer-AI/codex-host/releases/tag/v0.9.1
- Tag: `v0.9.1`
- Nome: codexhost 0.9.1
- Publicada em: 2026-09-19
- Release anterior (cronológica): `v0.9.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 94

-  ci: trim duplicate platform checks
-  fix: allow installer-only release recovery
-  feat: allow model and thinking selection during active turns
-  fix(omp): preserve native question details and timeout semantics
-  docs(omp): leave capability matrix updates to consolidated audit
-  ci: skip incremental Rust state on fresh runners
-  feat(hermes): project native diffs and context commands
-  feat: add native CodeBuddy commands and delegation discovery
-  fix: 透传原生任务分组排序请求 (#316)
-  fix: preserve large native thread history responses (#315)
-  docs(omp): keep the interaction index independently mergeable
-  feat: add Cursor thinking commands and outbound delegation
-  fix(codebuddy): preserve native compaction outcomes
-  fix(cursor): honor explicit native command input metadata
-  test: remove constant-only package checks
-  feat(codebuddy): derive native fork and revision sessions
-  feat(hermes): add verified native gateway sessions and precise history
-  docs: align harness capability matrix with native support
-  fix(hermes): stop opening sessions after adapter closes
-  fix(codebuddy): prevent derivation after adapter shutdown
-  fix(hermes): align slash history with native dispatch
-  fix(harness-discovery): preserve selected Node runtime in PATH
-  fix(hermes): remove version-based compatibility gates
-  ci: publish npm with trusted publishing instead of NPM_TOKEN
-  chore: prepare v0.9.1-test.1
-  fix(hermes): isolate delegation skill registration
-  fix(codebuddy): clean up native derivation copies
-  merge: integrate OMP capability improvements locally
-  merge: integrate CodeBuddy capabilities locally
-  merge: integrate Cursor capabilities locally
-  merge: integrate Hermes capabilities locally
-  merge: integrate harness capability documentation locally
-  docs: align integrated harness capability notes
-  chore: prepare v0.9.1-test.2
-  fix(omp): enable native ask through rpc-ui mode
-  merge: enable OMP native ask in local test build
-  fix(codebuddy): expose command catalog to Desktop menu
-  merge: fix CodeBuddy command menu locally
-  fix(codebuddy): expose commands through broker plugin
-  fix(cursor): expose native command menu metadata
- ... e mais 54 commits

### Release 4

Link: https://github.com/BytePioneer-AI/codex-host/releases/tag/v0.10.0
- Tag: `v0.10.0`
- Nome: codexhost 0.10.0
- Publicada em: 2026-09-23
- Release anterior (cronológica): `v0.9.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 71

-  feat: add Kimi Code harness adapter and Desktop integration
-  fix: align Desktop readiness agents and lock Kimi workspace
-  fix: publish Kimi native session identity
-  fix: read Kimi ACP text content
-  fix: project Kimi ACP tool fields
-  fix: confirm Kimi session configuration
-  fix: preserve Kimi approval context
-  fix: retain Kimi session commands
-  fix: correlate Kimi native turns
-  fix: surface Kimi history read failures
-  fix: stabilize Kimi identity and add runtime logs
-  fix: finalize Kimi textual items cleanly and complete reasoning on transition
-  fix(kimi-code): preserve canonical tool names and align native turn folding order
-  fix(kimi-code): complete agent message cleanly without commentary phase
-  fix(kimi-code): align native turn folding with reasoning envelope and clean final answer
-  fix(kimi-code): emit reasoning text update before completion to align with projector contract
-  fix(kimi-code): extract and emit token usage from native wire log and context window
-  fix(kimi-code): unify turn process fold and eliminate correlation freeze
-  fix(kimi-code): resolve native turn correlation timeout and handle delayed wire log flush
-  fix(kimi-code): eliminate synthetic reasoning cards and restore native folding phase lifecycle
-  feat(kimi-code): support session fork and attach turn checkpoints
-  feat(kimi-code): support rollbackLastTurn for revising previous message
-  feat(kimi-code): add dynamic slash command discovery, sync, and execution
-  fix(kimi-code): provide baseline slash command catalog for composer availability
-  feat(kimi-code): format command outputs as structured markdown and strip ansi
-  style(kimi-code): clean thinking option labels by removing Thinking prefix
-  fix(kimi-code): preserve native history and turn lifecycle contracts
-  fix(kimi-code): restore native head fork support
-  fix(kimi-code): align upstream integration and regression checks
-  style: format upstream ZCode compatibility regression
-  fix(kimi-code): restore last-message revision with native undo
-  fix(kimi-code): resolve upstream conflicts and review findings
-  fix(kimi-code): settle turns after usage projection failures
-  chore: remove obsolete OpenCodex attribution
-  feat: quieter update affordances in the title bar and Updates page
-  fix: point failed update requests to GitHub Releases instead of retrying
-  fix: keep sidebar agent icons on the title line when Desktop wraps titles (#362)
-  fix: reject mismatched npm platform payloads (#365)
-  fix(desktop-control): stop re-injecting the Renderer on Agent list order drift (#369)
-  Merge remote-tracking branch 'origin/main' into feat/quieter-update-ui
- ... e mais 31 commits

### Release 5

Link: https://github.com/BytePioneer-AI/codex-host/releases/tag/v0.13.1
- Tag: `v0.13.1`
- Nome: codexhost 0.13.1
- Publicada em: 2026-10-08
- Release anterior (cronológica): `v0.13.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_
