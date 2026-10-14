# prometheus-operator/prometheus-operator

Repositório: https://github.com/prometheus-operator/prometheus-operator

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.52.0
- Tag: `v0.52.0`
- Nome: 0.52.0 / 2021-11-04
- Publicada em: 2021-11-04
- Release anterior (cronológica): `v0.51.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 103

-  ThanosRulerSpec.labels: always set default replica label
-  test/framework: Remove context from framework struct
-  test/e2e: Update method calls to pass context
-  Add removed test case, move lines around
-  Update pkg/apis/monitoring/v1/thanos_types.go
-  Update pkg/apis/monitoring/v1/thanos_types.go
-  Merge pull request #4291 from simonpasquier/merge-release-0.51
-  regenerate
-  docs: Improve docs and error message for "smarthost" field
-  Update Pawel Krupa (paulfantom) Company
-  Merge pull request #4300 from prometheus-operator/paulfantom-patch-2
-  RELEASE.md: update instructions for kube-prometheus
-  tests/e2e: Update context parameter
-  test/e2e: Fix go-fmt
-  test/e2e: Fix tests and method calls
-  Setup mdox
-  Add mdox link checking and formatting
-  Update mdox to latest
-  docs: Regenerate docs/crd
-  format generate
-  Merge pull request #4196 from saswatamcode/add-mdox
-  CHANGELOG.md: fix typo
-  Merge pull request #4183 from slashpai/remove_ctx_struct
-  Merge pull request #4283 from r0bj/thanos_ruler_default_replica_label
-  Merge pull request #4305 from simonpasquier/fix-changelog
-  Merge pull request #4306 from prometheus-operator/release-0.51
-  Merge pull request #4293 from simonpasquier/update-kube-prometheus-instructions
-  docs: Regenerate Documentation/api.md
-  .github: automatically update dependencies
-  thanos: allow for injecting alert relabeling config to thanos ruler
-  Merge pull request #4303 from sjentzsch/thanos-rule-alert-relabeling
-  Merge pull request #4310 from paulfantom/dependabot-intro
-  *: pin to golang 1.17
-  *: Run make go-fmt with 1.17
-  *: Run make tidy
-  Merge pull request #4299 from mac-chaffee/master
-  .github/workflows: Update workflows to use go 1.17
-  Add .gitattributes
-  alertmanager: Support updated matching syntax in raw config for inhibit rules
-  Merge pull request #4313 from slashpai/go-1.17
- ... e mais 63 commits

### Release 2

Link: https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.56.3
- Tag: `v0.56.3`
- Nome: 0.56.3 / 2022-05-23
- Publicada em: 2022-05-24
- Release anterior (cronológica): `v0.56.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  *: fix support for new OpsGenie fields in Alertmanager config
-  Merge pull request #4797 from simonpasquier/fix-4755
-  pkg/prometheus: reduce the number of reconciliations
-  Merge pull request #4798 from simonpasquier/reduce-prometheus-syncs
-  pkg/prometheus: add generation to computed hash
-  Merge pull request #4806 from simonpasquier/fix-hash-computation
-  *: cut v0.56.3
-  Merge pull request #4805 from simonpasquier/release-0.56

### Release 3

Link: https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.64.1
- Tag: `v0.64.1`
- Nome: 0.64.1 / 2023-04-24
- Publicada em: 2023-04-25
- Release anterior (cronológica): `v0.64.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Fix panic when collecting metrics from Prometheus Agent controller
-  Merge pull request #5511 from ArthurSens/panic-collector
-  chore: cut v0.64.1
-  Merge pull request #5524 from simonpasquier/cut-0.64.1

### Release 4

Link: https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.84.1
- Tag: `v0.84.1`
- Nome: 0.84.1 / 2025-08-06
- Publicada em: 2025-08-06
- Release anterior (cronológica): `v0.84.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  Fix no-storage.tsdb.allow-overlapping-compaction argument
-  Fix test
-  Update CHANGELOG.md
-  Merge pull request #7747 from simonpasquier/fix-overlapping-compaction
-  fix: log only valid resources
-  fix: log only valid resources (#7749)
-  chore: cut v0.84.1
-  Merge pull request #7777 from slashpai/cut-0.84

### Release 5

Link: https://github.com/prometheus-operator/prometheus-operator/releases/tag/v0.94.0
- Tag: `v0.94.0`
- Nome: 0.94.0 / 2026-09-09
- Publicada em: 2026-09-09
- Release anterior (cronológica): `v0.93.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 100

-  fix json tag error
-  Merge pull request #8730 from kubeservice-stack/fix-tracingconfig-bug
-  build(deps): bump github.com/thanos-io/thanos from 0.42.2 to 0.42.3
-  build(deps): bump docker/login-action in the github-actions-deps group
-  Merge pull request #8731 from prometheus-operator/dependabot/go_modules/github.com/thanos-io/thanos-0.42.3
-  Merge pull request #8732 from prometheus-operator/dependabot/github_actions/github-actions-deps-6382876e44
-  build(deps): bump github.com/prometheus-community/prom-label-proxy
-  Merge pull request #8735 from prometheus-operator/dependabot/go_modules/github.com/prometheus-community/prom-label-proxy-0.15.0
-  chore: update prometheus to latest 3.13.2
-  Merge pull request #8736 from heliapb/chore/bump_prom_latest
-  chore: Update thanos version to v0.42.4 (#8734)
-  Merge pull request #8722 from nutmos/feat/add-operator-test-opsgenie
-  build(deps): bump github.com/prometheus/prometheus
-  Merge pull request #8738 from prometheus-operator/dependabot/go_modules/github.com/prometheus/prometheus-0.313.2
-  lint go header (#8737)
-  Feat: add test cases for Alertmanager Config validation for SNS Receiver (#8721)
-  alertmanager: add test case
-  fix: avoid panic when the kubelet service sync fails
-  fix: avoid panic when the kubelet service sync fails (#8743)
-  chore: embed timezone information
-  chore: update RELEASE.md
-  Merge pull request #8746 from simonpasquier/update-release
-  Merge pull request #8745 from simonpasquier/embed-tzdata
-  pkg/alertmanager: add URL validation for Mattermost receiver (#8225)
-  alertmanager: add test cases (#8744)
-  alertmanager: update test cases
-  alertmanager: update slack test cases
-  alertmanager: update test cases
-  alertmanager: update test cases
-  Merge pull request #8747 from nutmos/feat/validate-slack
-  Merge pull request #8741 from nutmos/feat/add-discord-operator-test
-  Merge remote-tracking branch 'origin/release-0.93' into merge-release-0.93
-  Merge pull request #8751 from simonpasquier/merge-release-0.93
-  Merge pull request #8727 from pujitha24/auto/issue-7579
-  ci: pin GitHub Actions to commit SHAs
-  ci: pin GitHub Actions to commit SHAs (#8753)
-  chore: remove use of wildcard verbs in ClusterRole
-  Merge pull request #8752 from simonpasquier/remove-wildcard-verbs
-  build(deps): bump google.golang.org/protobuf
-  Merge pull request #8755 from prometheus-operator/dependabot/go_modules/google.golang.org/protobuf-1.36.12
- ... e mais 60 commits
