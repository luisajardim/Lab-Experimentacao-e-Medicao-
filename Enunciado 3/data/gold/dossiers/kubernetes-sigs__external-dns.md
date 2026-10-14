# kubernetes-sigs/external-dns

Repositório: https://github.com/kubernetes-sigs/external-dns

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/kubernetes-sigs/external-dns/releases/tag/v0.5.14
- Tag: `v0.5.14`
- Nome: v0.5.14
- Publicada em: 2019-05-14
- Release anterior (cronológica): `v0.5.13`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 51

-  create missing DNS entry. fix https://github.com/kubernetes-incubator/external-dns/issues/964
-  proper field formatting
-  scratch - add Dockerfile.scratch
-  scratch - pin builder to specific image
-  scratch - add certs to scratch fs
-  Initial Skeleton From NS1 Provider
-  Add ns1 option for provider flag
-  Fix construction of record name in endpoint
-  Adds comments and fixes filtering
-  Wrap ns1 client with interface for easier testing
-  add comments
-  add acceptance tests for ns1 provider
-  Remove comment
-  Add boilerplate to ns1 provider and tests and simplfy code for inititializing provider
-  Add ns1-go to go.mod and go.sum
-  Update README with references to NS1 provider
-  Supress noisy logs from Kubernetes
-  Add tutorial for NS1 and link in README
-  Merge pull request #991 from njuettner/supress-k8s-logs
-  Merge pull request #963 from ns1/ns1-provider-ammended
-  Merge pull request #984 from yverbin/964-headless-dns-entry
-  Add flags for configuring custom NS1 endpoint and ignoring SSL verification for PrivateDNS support
-  Fix wording on flag description
-  add docker image faq
-  Merge pull request #1006 from Raffo/master
-  added TransIP provider
-  fixed linting issue
-  DNSimple: Support apex records
-  scratch - chnage from scratch to distroless
-  Update aws.md
-  Merge pull request #1009 from pawelprazak/patch-1
-  scratch - use gcr.io/distroless
-  add TransIP support to roadmap checklist
-  Merge pull request #1004 from jbowes/dnsimple-support-apex-domains
-  Merge pull request #1002 from ns1/ns1-add-endpoint-flag
-  tweaked transip provider tutorial
-  moved zoneForZoneName function into TransIPProvider struct
-  added test for TransIP provider flags
-  Merge branch 'master' of github.com:kubernetes-incubator/external-dns into transipSupport
-  Merge pull request #1007 from skoef/transipSupport
- ... e mais 11 commits

### Release 2

Link: https://github.com/kubernetes-sigs/external-dns/releases/tag/v0.7.0
- Tag: `v0.7.0`
- Nome: v0.7.0
- Publicada em: 2020-03-11
- Release anterior (cronológica): `v0.6.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 38

-  Fix updates of unchanged records for Azure Private DNS
-  Fix test
-  Add option to define minimum TTL for rfc2136 provider
-  Fixed issue to pass linting
-  Refactoring after review
-  Merge pull request #1377 from jasper-d/master
-  Adding issue templates
-  Updated minTTL variable type from int64 to Duration
-  Merge pull request #1424 from kubernetes-sigs/njuettner-patch-1
-  update docker image references of external-dns
-  Fix issue where headless services could return duplicate pod IP's
-  fix(azure): not use SPN to authenticate when clientid or secret is 'msi'
-  Merge pull request #1422 from norshtein/azure-msi
-  Merge pull request #1427 from tariq1890/upd_img
-  Use struct instead of bool
-  Headless service: retrieve endpoints via Endpoints resource; evaluate spec.publishNotReadyAddresses
-  Add CLI option to always publish not ready addresses of headless services
-  Fix typo
-  Update documentation to include RBAC permissions for endpoints resources
-  Address review comments
-  Merge pull request #1426 from thomasv314/dedup-targets
-  Merge pull request #1412 from ouzklcn/feature/rfc2136-min-ttl
-  Change DomainFilter to apply to records as well
-  fix broken links:https://community.exoscale.com/documentation/dns/api/ (#1451)
-  Merge pull request #1005 from devkid/feature/headless-services-publishnotreadyaddresses
-  fix: change test field to compile again
-  Merge pull request #1459 from linki/fix-build2
-  implement RouteGroup with similar feature set to ingress
-  docs: fix skipper routegroup flag in docs
-  Merge pull request #1444 from szuecs/feature/route-group
-  fix: return early if tokenfile could not be read
-  Merge pull request #1462 from szuecs/fix/nit-return-early
-  chore: add skipper routegroups to source flag documentation
-  Merge pull request #1465 from kubernetes-sigs/linki-patch-6
-  chore: add changelog for v0.7.0
-  Merge pull request #1442 from freenowtech/filter-record-creation
-  update changelog with latest addition
-  Merge pull request #1466 from linki/changelog-v0.7.0

### Release 3

Link: https://github.com/kubernetes-sigs/external-dns/releases/tag/v0.9.0
- Tag: `v0.9.0`
- Nome: v0.9.0
- Publicada em: 2021-08-05
- Release anterior (cronológica): `v0.8.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 138

-  First pass - based on global flag
-  Change to an annotation-based approach, based on feedback
-  Merge remote-tracking branch 'origing/master' into dansimone/support-prefer-ingress-annotations
-  Resolve differences
-  Fix unit test
-  FAQ changes based on feedback
-  Merge remote-tracking branch 'origing/master' into dansimone/support-prefer-ingress-annotations
-  Tidy up the logic that constructs the final list of ingresses based on the hostname source annotation
-  Merge remote-tracking branch 'origing/master' into dansimone/support-prefer-ingress-annotations
-  Merge FAQ line
-  Tidy up newline
-  Merge remote-tracking branch 'kubernetes-sigs/master'
-  Fix CNAME update for hetzner provider
-  update TransIP's Go client to v6
-  Add Gandi provider
-  Address remove comments
-  Add clarifying comment about ingressHostnameSourceKey
-  Merge remote-tracking branch 'kubernetes-sigs/master'
-  Merge remote-tracking branch 'kubernetes-sigs/master' into godaddy
-  Reduce AWS Route53 API calls
-  Provide example of multiple values for "in" filter
-  Keep copied structs to module
-  Use constants in tests for uris
-  Merge pull request #2025 from skoef/transipv6
-  Update controller/controller.go
-  bluecat: support getting credentials from environment variables
-  Update kustomization.yaml
-  Merge pull request #2072 from KohlsTechnology/bluecat-cred-from-env
-  Merge pull request #2073 from kubernetes-sigs/raffo/update-kustomize-080
-  docs: update bluecat tutorial
-  Merge remote-tracking branch 'kubernetes-sigs/master' into godaddy
-  Merge pull request #2074 from KohlsTechnology/bc-docs
-  Fix managed-record-types
-  Merge remote-tracking branch 'kubernetes-sigs/master'
-  Merge branch 'master' into godaddy
-  Updated k8s manifest for Azure DNS provider #2082
-  FEAT: Support DryRun
-  FEAT: Declare error response model
-  FEAT: Use the new Delete GoDaddy API
-  Delete record first and create record in last.
- ... e mais 98 commits

### Release 4

Link: https://github.com/kubernetes-sigs/external-dns/releases/tag/v0.14.2
- Tag: `v0.14.2`
- Nome: v0.14.2
- Publicada em: 2024-05-16
- Release anterior (cronológica): `external-dns-helm-chart-1.14.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 168

-  test: controller run() should do somthing and successfully shutdown
-  refactor: as suggested
-  test: #4059 detect no change necessary with provider specific config
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Adding feature for #4209
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Fix provider/dnsimple/dnsimple_test.go: Add the missing call to NewDnsimpleProvider for testing its behavior when the DNSIMPLE_OAUTH environment variable is not set
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Group By Endpoint names per Hosted Zone on AWS
-  Group By Endpoint names per Hosted Zone on AWS
-  Group By Endpoint names per Hosted Zone on AWS
-  Group By Endpoint names per Hosted Zone on AWS
-  Going back to endpoint.go
-  Fix format on aws and endpoint files
-  Fix Lint
-  Add const to avoid Lint
-  Revert "Fix Lint"
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Allow for DNSimple User API tokens to be used by implementing the DNSIMPLE_ACCOUNT_ID and DNSIMPLE_ZONES environment variables
-  Update endpoint.go with Key function
-  Fix lint
-  Merge branch 'kubernetes-sigs:master' into bugfix/group-endpoints-per-hosted-zone-for-aws
-  Fix Lint
-  Removing comments and clean up
-  Add IPv6 AAAA record support to PiHole provider
-  feat(azure): add zone name filter for Azure Private DNS
-  test(azure): Azure Private DNS zone name filter
-  test(azure): Azure Private DNS apply change with zone name filter
-  docs(azure): describe --zone-name-filter behavior
-  Merge remote-tracking branch 'origin/master' into bugfix/group-endpoints-per-hosted-zone-for-aws
-  Fix for duplicated endpoints and unit tests
-  chore: alphabetical order on providers
- ... e mais 128 commits

### Release 5

Link: https://github.com/kubernetes-sigs/external-dns/releases/tag/v0.17.0
- Tag: `v0.17.0`
- Nome: v0.17.0
- Publicada em: 2025-05-14
- Release anterior (cronológica): `external-dns-helm-chart-1.16.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 81

-  fix(log testing): fix logs
-  fix cloudflare regional hostnames
-  add tests & fixes for dataLocalizationRegionalHostnamesChanges()
-  Merge pull request #5175 from vflaux/fix_cf_regional_hostname
-  fix(zonefinder): handle underscores in dns records
-  changes to goccy yaml
-  use json to unmarshal json
-  Merge pull request #5292 from kubernetes-sigs/raffo/change-yaml-dep
-  chore(dependencies): update toools versions (#5252)
-  chore(source): code cleanup
-  chore(go): build with go 1.24.2
-  Merge pull request #5273 from gofogo/fix-flakey-test-logging
-  Merge pull request #5281 from arthlr/fix/zone-finder
-  Merge pull request #5306 from mloiseleur/chore/toolchain
-  fix(helm): update helm schema (#5297)
-  chore(deps): bump the dev-dependencies group across 1 directory with 2 updates
-  Merge pull request #5301 from kubernetes-sigs/dependabot/github_actions/dev-dependencies-a128ef9c40
-  chore(deps): bump the dev-dependencies group across 1 directory with 21 updates (#5313)
-  chore(refactore): added lint checks
-  Merge pull request #5318 from gofogo/chore-refactoring-v0
-  feat(pihole): add support for IPv6 Dual format (#5253)
-  feat(helm): allow extraArgs to also be a map enabling overrides of individual values (#5293)
-  chore(code-quality): linter warnings fixes
-  RFC2136: Update flags documentation to be more clear about multiple zones.
-  RFC2136: Update tutorial to show Helm example with TSIG in secret
-  Update flags doc in correct location
-  Merge pull request #5325 from BasJ93/docs-update-rfc2136
-  Merge pull request #5320 from gofogo/chore-code-quality-v1
-  test(source): fix data race on node_test
-  Merge pull request #5334 from mloiseleur/chore/fix-data-race
-  chore(code): improve some tests + re-order sources flags CLI (#5288)
-  chore(providers): rename custom TTL constants to defaultTTL (#5312)
-  chore(code-quality): webhook increase code coverage
-  Merge pull request #5337 from gofogo/chore-bump-backoff-deps
-  chore(deps): code cleanup, do not use pkg/errors (#5335)
-  chore(webhook): bump cenkalti/backoff version (#5342)
-  chore(deps): bump the dev-dependencies group across 1 directory with 14 updates
-  chore(deps): bump the dev-dependencies group across 1 directory with 2 updates
-  fix: check that parent generation matches current generation.
-  fix: add unit tests for generation check
- ... e mais 41 commits
