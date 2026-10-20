# monoscope-tech/monoscope

Repositório: https://github.com/monoscope-tech/monoscope

## Metadados

- Linguagem: Haskell

## Releases sorteadas

### Release 1

Link: https://github.com/monoscope-tech/monoscope/releases/tag/v0.4.1
- Tag: `v0.4.1`
- Nome: v0.4.1
- Publicada em: 2026-03-17
- Release anterior (cronológica): `v0.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  fix onboarding pricing: redirect after plan selection, fix button styling

### Release 2

Link: https://github.com/monoscope-tech/monoscope/releases/tag/v0.6.0
- Tag: `v0.6.0`
- Nome: v0.6.0 — Notification overhaul
- Publicada em: 2026-04-14
- Release anterior (cronológica): `v0.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 32

-  Auto-format code with fourmolu
-  Fix parser test expectations for to_jsonb(summary) change
-  Fix hasql enum casts and field order for error_patterns, formats, issues, monitors
-  sumary elements split
-  fix muted_until position which failwd integration tests
-  fix Endpoint DromRow in tests
-  Fix 6 integration test failures from extraction worker + hasql migration
-  Fix deadlocks, FK violations, and TOAST stress in prod DB
-  Auto-format code with fourmolu
-  Fix safety-net test timestamp and regenerate embedding golden files
-  Fix test DB log noise: orphaned jobs, type mismatches, scheduler errors
-  Auto-format code with fourmolu
-  Add trace session cache for cross-span identity propagation
-  Auto-format code with fourmolu
-  Add Sessions visualization with parameterized SQL queries
-  Auto-format code with fourmolu
-  Renumber session_user_indexes migration to 0069 to avoid conflict
-  Trigger CI rebuild
-  Improve sessions expand with trace trees, fix auth bypass and dedup lookups
-  Auto-format code with fourmolu
-  improve the sessions visualization to show errors and more valuable context
-  fmt: reorder derived instances
-  fix: strip dashes in test hexPad and add required summary column
-  fix: stop truncating session id in sessions-viz summary badge
-  feat: normalize browser error attributes to OTel exception semconv
-  improve replay observability: log missing keys, empty-result diagnostics
-  add session/user attributes to KQL autocomplete suggestions
-  Auto-format code with fourmolu
-  feat(sessions-viz): session-level header KPI strip + stacked bar chart
-  feat(span-summary): classify frontend spans; resource/url/action labels
-  Auto-format code with fourmolu
-  feat(notifications): denser, clearer Slack/Discord error alerts

### Release 3

Link: https://github.com/monoscope-tech/monoscope/releases/tag/v0.6.22
- Tag: `v0.6.22`
- Nome: v0.6.22
- Publicada em: 2026-05-05
- Release anterior (cronológica): `v0.6.21`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  Auto-format code with fourmolu
-  feat: track message size per row, surface in billing breakdown
-  Auto-format code with fourmolu
-  chore(deps): bump typescript from 5.9.3 to 6.0.3 in /web-components (#371)
-  chore(deps): bump jest from 29.7.0 to 30.3.0 (#369)
-  fix: strip summary badges in log pattern notifications
-  fix: strip summary badges from log pattern sample message too
-  fix: strip summary badges in remaining notification channels
-  fix(cli): preserve JSON types and clean summary in events search output

### Release 4

Link: https://github.com/monoscope-tech/monoscope/releases/tag/v0.6.25
- Tag: `v0.6.25`
- Nome: Monoscope v0.6.25
- Publicada em: 2026-08-07
- Release anterior (cronológica): `v0.6.24`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 240

-  fix(charts): don't advance query-cache watermark on failed delta fetch (#455)
-  fix(charts): don't advance query-cache watermark on failed delta fetch (#456)
-  Fix metric service name extraction (#454)
-  Auto-format code with fourmolu
-  Migrate dropdowns to native popover; rewrite facet sidebar; trim Log Explorer JS
-  Datadog-style field context menu: unify menus, add tooltips, fix clipping/truncation
-  Log Explorer: CSS-driven JSON-tree collapse, field-menu cleanup, fa-add tooling
-  Bound dead-socket hangs on all PG/TF pools: connect_timeout + tcp_user_timeout
-  Auto-format code with fourmolu
-  Log Explorer: CSS-driven detail-panel state, unified closeDetailPanel contract, mobile details-open
-  fa-add: fetch FontAwesome Pro API first, free CDN fallback
-  Log Explorer: fullscreen trace/details toggle, mobile back nav, Escape-to-close
-  Auto-format code with fourmolu
-  Log Explorer: split data/patterns/sessions into dedicated endpoints, fix column visibility URL sync
-  Merge origin/master (fourmolu auto-format)
-  fourmolu formatting
-  Trim verbose comments in Log Explorer, add minutes case to duration formatter
-  perf(ingest): column-oriented unnest bulk-insert; delete bisector + per-row poison
-  Auto-format code with fourmolu
-  fix(Parser): repair malformed splitTrailingAlias doctest (prose leaked into expected output; red on master, blocked deploys)
-  fix(ingest): per-engine SELECT casts for unnest insert (restore Postgres writes)
-  fix(dual-write): per-engine pg-type casts via timefusionUsesPgTypes config
-  Auto-format code with fourmolu
-  refactor(dual-write): move pg-type flag from EnvConfig to AuthContext
-  Auto-format code with fourmolu
-  fix(log-explorer): honor requested columns that alias-collide with defaults
-  refactor(log-explorer): inline sessions-header legend/kpis helpers
-  fix(ingest): cast unnest bind params so the TF bulk-insert leg can plan
-  fix(kafka): survive slow backlog batches — 30min max.poll.interval, drop static membership
-  fix(dlq): resolve ce-type on retry-tier topics — stop poisoning every retried message
-  Auto-format code with fourmolu
-  Add container HEALTHCHECK probing /status web listener
-  fix(incident 2026-07-06): idle-in-tx guard + stop attention-log flood
-  Make shutdown terminal + cap fire-and-forget tasks
-  Auto-format code with fourmolu
-  perf(ingest): cut hot-table lock contention on otel_logs_and_spans
-  test(session-backfill): verify propagation through the lagged 2–17 min window
-  feat(monitoring): pipeline-loss prevention after 2026-07-06 silent dual-write outage
-  Auto-format code with fourmolu
-  ci: exercise real TimeFusion in the regular test suite, drop the separate nightly
- ... e mais 200 commits

### Release 5

Link: https://github.com/monoscope-tech/monoscope/releases/tag/v0.6.27
- Tag: `v0.6.27`
- Nome: Monoscope v0.6.27
- Publicada em: 2026-09-07
- Release anterior (cronológica): `v0.6.26`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  Expand weekly emails into dense system reports (#509)
-  fix: return requested aggregates and columns in summary tables (#512)
-  fix: bound embedding requests and preserve long patterns (#511)
-  fix: keep ingestion parameters out of database exception logs (#513)
-  Record weekly report deployment and production storage failure
-  Fix CLI severity filters to match stored field and enum values (#514)
-  Resolve project caches for ID-only queued telemetry batches (#515)
-  Only render mobile sidebar controls when a sidebar exists (#516)
-  fix: pass project context to dashboard variable refresh (#519)
-  fix: align severity schema and examples with stored fields (#517)
-  fix: bound prefix length checks during error normalization (#520)
-  fix(cli): preserve pipelines when adding shorthand filters (#518)
