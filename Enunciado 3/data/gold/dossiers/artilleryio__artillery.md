# artilleryio/artillery

Repositório: https://github.com/artilleryio/artillery

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/artilleryio/artillery/releases/tag/v2.0.0-7
- Tag: `v2.0.0-7`
- Nome: v2.0.0-7
- Publicada em: 2021-12-08
- Release anterior (cronológica): `v1.7.9`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 339

-  refactor: Track all metrics with generic histogram/counter methods
-  feat(metrics): Add support for serialization and HDR histograms
-  feat(console-reporter): Support table-formatted output
-  fix(multicore): Serialize/deserialize metrics objects
-  fix(metrics): Maintain backwards-compatibility with third-party code
-  chore(test): Remove unnecessary test
-  feat: Use new metric implementation in WS and HTTP engines
-  feat(core): Use standard prefixes for core metrics
-  feat(stats): Tweak HDR histogram settings
-  feat(metrics): Rename histograms to summaries
-  feat(metrics): Add support for tracking rate metrics
-  feat: Use new metric implementation in Socket.io engine
-  feat(ws): Track send rate
-  feat(stats): Add getRate method
-  feat(stats): Produce a backwards-compatible report
-  feat(stats): Default to adding one in counter()
-  feat(runner): Add ability to track summary and rate metrics
-  feat(runner): Track scenario metrics
-  feat(console-reporter): Use a line spinner
-  feat(console-reporter): Add new look for console reports
-  fix(http): Track response code counts
-  ci: Disable Docker layer caching on Circle
-  Merge branch 'master' into refactor/metrics
-  ci: Remove Travis CI
-  fix(test): Matches are deprecated in their current form
-  Merge pull request #709 from hassy/refactor/metrics
-  feat(http): Replace Request.js with Got
-  Merge pull request #803 from hassy/feat/request-to-got
-  docs: Update README
-  fix(stats): Calculate average rate over the whole recorded period
-  feat: Allow for config.ensure to be disabled
-  feat: Set recommended version to 10.19.0 (latest v10 Active LTS)
-  docs: Update README
-  docs: Update README
-  chore: Remove Request.js
-  test: Remove dev dependency on bcrypt
-  Correct documentation
-  feat(http): Make qs and gzip work with Got-based implementation
-  fix(tests): Prevent ECONNRESETs on tests that use think
-  chore: Upgrade Got.js to latest version (v11.0.2)
- ... e mais 299 commits

### Release 2

Link: https://github.com/artilleryio/artillery/releases/tag/v2.0.0-20
- Tag: `v2.0.0-20`
- Nome: v2.0.0-20
- Publicada em: 2022-07-04
- Release anterior (cronológica): `v2.0.0-19`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 13

-  fix(http): avoid multiple callbacks on redirects
-  dep: upgrade async to v2.6.4
-  test(ws): fix use of globals in WS test
-  fix: allow some properties to be numbers or strings
-  fix: allow zero-duration think steps
-  dep: upgrade dependencies
-  Merge pull request #1494 from artilleryio/dep/dependency-upgrades
-  fix: upgrade chalk from 2.0.0 to 2.4.2
-  Merge pull request #1495 from artilleryio/snyk-upgrade-2ad28616d3118b7fe941cb34193c3b15
-  fix: upgrade ip from 1.1.5 to 1.1.8
-  fix: upgrade socket.io-client from 4.4.1 to 4.5.1
-  fix: upgrade cli-table3 from 0.6.1 to 0.6.2
-  2.0.0-20

### Release 3

Link: https://github.com/artilleryio/artillery/releases/tag/v2.0.0-27
- Tag: `v2.0.0-27`
- Nome: v2.0.0-27
- Publicada em: 2022-11-16
- Release anterior (cronológica): `v2.0.0-26`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  fix: emit stats for sleeping workers on phaseStarted event
-  refactor: move new logic to isIdlePhase method
-  test: add new test for divideWork for multiple scenarios
-  test: test already known case
-  Merge pull request #1654 from artilleryio/hotfix/missing_report_when_no_phase_defined
-  Merge pull request #1657 from artilleryio/hotfix/flaky_ramp_test
-  feat(lambda): use arm64/Graviton by default
-  fix(console-reporter): count elapsed time from first recorded metric
-  feat: use a pool of SQS consumers
-  fix: make sure intermediates are flushed before done
-  2.0.0-27

### Release 4

Link: https://github.com/artilleryio/artillery/releases/tag/v2.0.0-37
- Tag: `v2.0.0-37`
- Nome: Artillery v2.0.0-37
- Publicada em: 2023-09-11
- Release anterior (cronológica): `artillery-2.0.0-36`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 42

-  chore: post slack notifications only on failures in main (#2063)
-  chore: change mockingjay port to 9099 (#2071)
-  fix(types): implies default "http" engine, fixes request "cookies" and "match" (#2054)
-  fix(publish-metrics): fix operator in honeycomb reporter
-  Merge pull request #2075 from artilleryio/fix-honeycomb-fail
-  ci: release v0.1.4 @artilleryio/types (#2072)
-  feat(ensure): add colored output to checks (#2074)
-  feat: add support for app keys to Datadog reporter (#2067)
-  feat(cloud): show test run url at the end of the run too (#2070)
-  docs: point to Playwright engine docs in the README
-  chore(artillery): change repeated test names
-  Merge pull request #2081 from artilleryio/change-duplicated-test-name
-  fix(types): support array of expectation metrics (#2077)
-  feat(core): allow multiple time formats in duration and pauses
-  fix(types): correct phase types
-  chore(types): add ms link to tip on pause and duration
-  Merge pull request #2084 from artilleryio/bernardobridge/art-1081-support-multiple-time-formats-in-artillery-cli
-  dep(publish-metrics): update Honeycomb client (#2076)
-  fix(cloud): display api key error when invalid key is set (#2078)
-  test(artillery): increase timeout
-  Merge pull request #2088 from artilleryio/bernardobridge/increase-cli-test-timeout
-  fix(types): rename "followRedirects" to "followRedirect" (#2089)
-  fix(types): annotate "config.http.defaults" (#2090)
-  ci: release v0.1.5 (#2091)
-  refactor(examples): make playwright smoke example have more interaction (#2103)
-  fix: calculate common prefix taking directory separators into account (#2106)
-  dep(playwright): update playwright version to 1.37.1 (#2105)
-  ci(test): change to better formatted slack notification github action (#2107)
-  fix(examples): artillery cli using data from csv example (#2108)
-  ci(examples): make gh action examples report to artillery cloud (#2109)
-  dep(artillery): update ci-info to get more up-to-date telemetry (#2116)
-  feat(publish-metrics): add OpenTelemetry tracing support (#2073)
-  feat(publish-metrics): implement sending metrics with OpenTelemetry (#2113)
-  fix(publish-metrics): remove undefined prefix from rate names (#2121)
-  ci: release v0.3.2 of artillery-engine-playwright
-  docs: update README
-  ci: release v1.2.0 of artillery-plugin-ensure
-  ci: release v2.7.0 of artillery-plugin-publish-metrics
-  ci: release v2.1.0 of @artilleryio/int-core
-  dep(artillery): update platform-fargate to 2.1.0
- ... e mais 2 commits

### Release 5

Link: https://github.com/artilleryio/artillery/releases/tag/artillery-2.0.24
- Tag: `artillery-2.0.24`
- Nome: Artillery v2.0.24
- Publicada em: 2025-08-11
- Release anterior (cronológica): `artillery-2.0.23`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 23

-  fix(azure): process AQS messages faster
-  fix(azure): decrease delay between starting batches of workers
-  fix: Azure message processing throughput (#3542)
-  fix: take distributed phases into account in TypeScript scripts (#3548)
-  dep: upgrade Playwright to v1.53.0 (#3556)
-  fix: Slack plugin not reporting duration and status correctly (#3555)
-  dep(apdex): move tap to devDependencies (#3573)
-  ci: run tests on Node.js 22 and 24 (#3572)
-  dep: upgrade outdated dependencies
-  chore: update package-lock.json
-  dep: upgrade Playwright to v1.54.0
-  chore: update package-lock.json
-  Merge pull request #3574 from artilleryio/dep/playwright-v1.54.0
-  test: skip tests for suggested commands
-  refactor: exit from the main Oclif callback
-  refactor: handle prepareTestExecutionPlan errors
-  Merge pull request #3568 from artilleryio/dep/upgrade
-  feat: remove Lightstep integration via lightstep-tracer (#3575)
-  test: increase amount of memory for memory use stress test (#3576)
-  test: increase resources for both configs (#3578)
-  fix: apdex score not showing (#3579)
-  dep: upgrade to Playwright v1.54.2 (#3593)
-  ci: release v2.0.24 of artillery (#3594)
