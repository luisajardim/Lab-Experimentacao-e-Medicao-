# hashicorp/terraform-provider-azurerm

Repositório: https://github.com/hashicorp/terraform-provider-azurerm

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/hashicorp/terraform-provider-azurerm/releases/tag/v1.29.0
- Tag: `v1.29.0`
- Nome: v1.29.0
- Publicada em: 2019-05-26
- Release anterior (cronológica): `v1.28.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 87

-  Enable correlation request ID header in ARM API.
-  Cleanup after v1.28.0 release
-  Application Gateway: Rewrite Rules (#3423)
-  Update CHANGELOG.md to include #3423
-  Update CHANGELOG.md to include #3360
-  application gateway: add advanced ssl_policies (#3360)
-  Fix TestAccAzureRMStorageShare_disappears (#3467)
-  Fix TestAccAzureRMContainerGroup_windows (#3468)
-  Application Insights Webtests (#3331)
-  Update CHANGELOG.md to include #3331
-  Add initial implementation for Authentication Settings in read & update
-  Add initial active directory section
-  Add allowedAudiences to schema, flatten and expand
-  Add facebook auth settings schema
-  Add 'auth' to facebook schema function name
-  Add google auth settings schema
-  Make sure facebook app secret is required
-  Add microsoft auth settings schema
-  Add providers to main auth schema
-  Add twitter auth settings schema
-  Add remaining properties for main schema
-  Add facebook, google, microsoft and twitter to expand
-  Add facebook, google, microsoft and twitter to flatten
-  Add remaining main auth properties
-  Add remaining auth settings to flatten function
-  Add check for providers
-  Add acctest for Active Directory authentication
-  Add missing check for Active Directory authentication
-  Add acctest for Facebook authentication
-  Add acctest for Google authentication
-  Add acctest for Microsoft authentication
-  Add acctest for Twitter authentication
-  RandInt -> AccRandTimeInt
-  Check for nil interfaces in different auth settings
-  Add acc test for multiple authentication providers
-  Add acctests for remaining main auth settings
-  Add Authentication documentation
-  Add token_store_enabled setting
-  Fix linting error when updating auth settings in read
-  Add missing acceptance test for runtime version
- ... e mais 47 commits

### Release 2

Link: https://github.com/hashicorp/terraform-provider-azurerm/releases/tag/v2.9.0
- Tag: `v2.9.0`
- Nome: v2.9.0
- Publicada em: 2020-05-08
- Release anterior (cronológica): `v2.8.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 207

-  Support for external Hive metastore
-  Fix formatting
-  Support for Oozie and Ambari
-  Make metastores optional
-  Fix
-  Fix doc
-  Merge remote-tracking branch 'upstream/master' into hdi/external_metastore
-  Fix update scenario for network interface
-  Merge remote-tracking branch 'upstream/master' into fix_nic
-  provider: update terrafmt checks with make terrafmt command (#6567)
-  provider: pin golangci to 1.24 (#6577)
-  provider tests: removes the requires import feature flag [L-W] (#6573)
-  `azurerm_function_app` - Added `storage_account_id` and `storage_account_access_key` (#6304)
-  update for #6304
-  `azurerm_iothub_dps` - fix crash when path isn't cased correctly #6570
-  Update for #6570
-  `azurerm_linux_virtual_machine_scale_set` - fixes crash with `boot_diagnositics` #6569
-  Update for #6569
-  provider: upgrade API Management to 2019-12-01 (#6479)
-  update CHANGELOG.md to include #6479
-  `azurerm_private_endpoint`: Add support for tags (#6574)
-  `azurerm_public_ip_prefix`: Update `prefix_length` validation to accept all valid IPv4 address ranges (#6589)
-  updating to include #6574 and #6589
-  Updating instead of foo to example (#6591)
-  Revert "CDN Endpoint: make origin_host_header required " (#6583)
-  ...
-  ...
-  Merge branch 'fix_nic' of https://github.com/microsoft/terraform-provider-azurerm into fix_nic
-  Fix typo
-  Added test for hive only and check in reading code
-  Update tests
-  Merge branch 'hdi/external_metastore' of github.com:kosinsky/terraform-provider-azurerm into hdi/external_metastore
-  add name and priority to ip_restriction for app_service
-  make priority computed
-  added recovery capabilty for secrets
-  added key soft-delete recovery support
-  added certificate soft-delete recovery support
-  simplified recovery logic
-  Cleanup after v2.8.0 release
-  acctests: boosting the default concurrency to 20
- ... e mais 167 commits

### Release 3

Link: https://github.com/hashicorp/terraform-provider-azurerm/releases/tag/v2.12.0
- Tag: `v2.12.0`
- Nome: v2.12.0
- Publicada em: 2020-05-28
- Release anterior (cronológica): `v2.11.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 73

-  Align azurerm_sql_virtual_network_rule name validation with azure validation
-  minor test fixes
-  Test fix - name too short error returned for empty name
-  Cleanup after v2.11.0 release
-  Add note about certificate format (#7054)
-  OMS Agent Identity Export
-  Clarify the content of the parameters_body argument (#7060)
-  azurern_[linux|windows]_virtual_machine - Correctly check the length of the rsa ssh `public_key` property (#7061)
-  update CHANGELOG.md to include #7061
-  Fix `azurerm_orchestrated_virtual_machine_scale_set` - `azurerm_linux|windows_virtual_machine` should allow to assign `virtual_machine_scale_set_id` in non-zonal deployment (#7057)
-  update CHANGELOG.md to include #7057
-  Update Resource: `azurerm_eventgrid_event_subscription` (#6860)
-  update CHANGELOG.md to include #6860
-  Fix validation for serivce bus topic name
-  Update code
-  azurerm_batch_pool - support `container_image_names` property (#6689)
-  update CHANGELOG.md to include #6689
-  New resource: azurerm_dev_test_global_shutdown_schedule (#5536)
-  update CHANGELO.md to include #5536
-  Fixed 'Unknown' issuer not working
-  Update code
-  Update code
-  Update code
-  Merge pull request #7056 from aristosvo/oms-agent-identity
-  updating to include #7056
-  Merge pull request #6968 from robselway/hotfix/sql-vnet-rule-validation
-  updating to include #6968
-  Merge pull request #6979 from ThomasZeman/master
-  updating to include #6979
-  Use address_prefixes in azurerm_application_gateway (#7072)
-  r/api_management_api_version_set: handling changes to the Azure Resource ID (#7071)
-  update CHANGELOG.md to include #7071
-  d/azurerm_kubernetes_cluster extended with kubelet_identity and identity (#6527)
-  update CHANGELOG.md to include #6527
-  Update doc for access_tier of storage account
-  Update code
-  Update code
-  acctest: updating the build config definition to 2020.1
-  acctest: using teamcity-go-test for service packages
-  acctest: moving off the built-in test parser for now
- ... e mais 33 commits

### Release 4

Link: https://github.com/hashicorp/terraform-provider-azurerm/releases/tag/v4.23.0
- Tag: `v4.23.0`
- Nome: v4.23.0
- Publicada em: 2025-03-13
- Release anterior (cronológica): `v4.22.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/hashicorp/terraform-provider-azurerm/releases/tag/v5.7.0
- Tag: `v5.7.0`
- Nome: v5.7.0
- Publicada em: 2026-09-24
- Release anterior (cronológica): `v5.6.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 37

-  Attributes added `azurerm_signalr_service ` - add support for `connectivity_logs_enabled + 9 attributes` (#33372)
-  typos: check spelling in CI and fix existing typos (#33388)
-  linting: add lychee link checking for docs; fix all broken links (#33327)
-  fix: link check errors (#33461)
-  actions: add changelog action (#33378)
-  add changelog to ignore (#33465)
-  workflow: changelog workflow fixes + improvements (#33462)
-  workflow: fix pagination (#33466)
-  Workflow: changelog fixes (#33469)
-  actions: scan workflows for security problems with zizmor, and fix what it found (#33468)
-  workflow: use service account instead of default (#33474)
-  workflow: migrate token to more granular permissions (#33475)
-  workflow: bump cli version + update comment template (#33476)
-  workflows: changelog (#33482)
-  Attributes added `data.azurerm_service_plan` - add missing attributes to match resource (#33300)
-  helpers: remove wrappers that duplicate the standard library and our own validators (#33478)
-  Data Source: `azurerm_kubernetes_cluster` - fix panics on `agent_pool_profile` flatten (#33488)
-  Attributes added `data.public_ip` - add missing attributes to match resource (#33193)
-  `data.network_interface` - add missing attributes to match resource (#33204)
-  Attributes added `data.linux_web_app` - add missing attributes to match resource (#33316)
-  Attributes added `data.azurerm_storage_blob` - add missing attributes to match resource (#33318)
-  Attribiutes added `data.azurerm_traffic_manager_profile ` - add missing attributes to match resource (#33346)
-  Attributes added `azurerm_web_pubsub ` - add missing attributes to match resource (#33373)
-  helpers: move the ISO8601 and regex validators, drop the TitleCase and QuotedStringSlice wrappers (#33490)
-  dependencies - Update `go-azure-sdk` to `v0.20260917.1142820` (#33495)
-  workflows: run govulncheck on main and weekly (#33491)
-  containers/kubernetes: add `Windows2025` OS SKU for AKS node pools (#33463)
-  update network sdk API version to 2025-07-01: `appservice`, `cognitive`, `compute`, `databricks`, `firewall`, `legacy`, `network`, `paloalto`, `qumulo`, `resource` (#33441)
-  update network sdk API version to 2025-07-01: `loadbalancer`, `databricks` (#33438)
-  `windows_virtual_machine` - add List Resource support (#33332)
-  `private_dns_resolver_forwarding_rule` - Add list support (#33313)
-  update network sdk API version to 2025-07-01: `cdn`, `mssql`, `recoveryservices` (#33439)
-  update network sdk API version to 2025-07-01: `containers`, `datafactory`, `servicenetworking`, `signalr` (#33440)
-  `CI` - update terraform core version to `1.16` for latest actions feature support (#33506)
-  postgresql_flexible_server: fix perpetual replace of replica caused by cluster drift (#33082)
-  fix 5.0 upgrade guide (#33508)
-  5.7.0 release changelog (#33509)
