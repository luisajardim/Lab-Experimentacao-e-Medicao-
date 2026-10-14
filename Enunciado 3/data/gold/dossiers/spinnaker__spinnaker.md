# spinnaker/spinnaker

Repositório: https://github.com/spinnaker/spinnaker

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/spinnaker/spinnaker/releases/tag/spinnaker-release-2025.0.5
- Tag: `spinnaker-release-2025.0.5`
- Nome: Spinnaker 2025.0.5
- Publicada em: 2025-07-15
- Release anterior (cronológica): `spinnaker-release-2025.0.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  chore(build): Migrate from OSSRH to Central Portal (#7114) (#7123)
-  fix(publishing): Write all versions to Maven metadata (#7126) (#7127)
-  fix(build): Enable publishing for Gradle plugins (#7122) (#7128)
-  fix(retrofit2): fix query param encoding logic to accommodate repeating query params (#7133) (#7134)
-  chore(clouddriver/kubernetes): upgrade kind to 0.29.0 (#7138) (#7142)
-  test(clouddriver/kubernetes): test against a 1.30.13 k8s cluster (#7139) (#7141)

### Release 2

Link: https://github.com/spinnaker/spinnaker/releases/tag/spinnaker-release-2025.3.0
- Tag: `spinnaker-release-2025.3.0`
- Nome: Spinnaker 2025.3.0
- Publicada em: 2025-11-08
- Release anterior (cronológica): `spinnaker-release-2025.1.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 79

-  chore(build): dynamic version indexing in tag name based on type (#7202)
-  fix(orca/clouddriver): correct parameter order for requestOperations to avoid invalid cloudProvider errors (#7201)
-  fix(clouddriver/aws): align CredentialsParser types in AmazonCredentialsInitializer (#7207)
-  fix(halyard/retrofit2): fix daemon service getTask API definition (#7206)
-  fix(echo/rest): make it possible to send events to URLs with no trailing slash (#7212)
-  fix(google): Add retry and status polling logic (#7191)
-  chore(dependency): update bc version from 1.77 to 1.81 (#7211)
-  fix(gate/web): add Retrofit2SyncCall.execute to SubnetController.allByCloudProvider (#7219)
-  fix(orca/retrofit2): fix orca bakeservice api (#7224)
-  fix(gcp): Fix a number of potential NPEs around deploy handling for google builds.  Tied to groovy to java migration (#7227)
-  chore(deps): bump sha.js from 2.4.11 to 2.4.12 in /deck (#7213)
-  refactor(kubernetes): convert manifest actions modal components to react (#7223)
-  refactor(kubernetes): de-angularize services, and components (#7228)
-  refactor(kubernetes): convert load balancer details component to react (#7222)
-  chore(deps): bump tmp in /.github/actions/spinnaker-release (#7229)
-  fix(halyard/retrofit2): fix DaemonService's convertor factory (#7230)
-  chore(deps): bump tmp from 0.2.3 to 0.2.5 in /deck/test/functional (#7231)
-  fix(gcp): More NPE handling on some input (#7236)
-  fix(deck): Fix RunJob external logs when component is not mounted and interpolation is needed (#7163)
-  feat(clouddriver/aws): Implement the account API for aws accounts (#7238)
-  feat(clouddriver/aws): log aws sdk endpoints (#7239)
-  feat(clouddriver/aws): log the endpoint that aws sdk sts clients use (#7240)
-  fix(sql): Update account type column during upserts (#7242)
-  chore(graphql): Remove unused and legacy graphql libraries and sample endpoints (#7244)
-  feat(OAuth2): Current OAuth2 annotations are deprecated so using Java DSL way of configuring OAuth2 (#7052)
-  feat(echo/aws): upgrade echo from aws sdk v1 to v2 (#7243)
-  feat(clouddriver/ecs): Implement the account API for ecs accounts (#7247)
-  test(orca): add a test to verify clouddriver GET api to get CloudFormationStack (#7248)
-  fix(oracle): A few oracle operations call themselves google which can mess with class loading on class scans.  Fix them to be Oracle (#7249)
-  Various kork updates (secrets, utilities, prereqs for credentials updates) (#7245)
-  feat(front50/aws): upgrade front50 to aws sdk v2 (#7250)
-  fix(OAuth2, NPE): Map.copyOf is strict about nulls so use Collections.unmodifiableMap instead (#7246)
-  fix(oauth2): move tokenResponseClient bean to static inner config to avoid circular dependency (#7254)
-  chore(deps): bump actions/setup-go from 5 to 6 (#7257)
-  chore(deps): bump actions/setup-java from 4 to 5 (#7258)
-  chore(deps): bump actions/checkout from 4 to 5 (#7259)
-  chore(deps): bump google-github-actions/auth from 2 to 3 (#7260)
-  chore(deps): bump google-github-actions/upload-cloud-storage from 2 to 3 (#7261)
-  feat(healthcheck): Add GRPC and HTTP/2 support for GCP load balancers (#7253)
-  fix(orca/clouddriver/retrofit): fix wildcard in the retrofit method parameter (#7264)
- ... e mais 39 commits

### Release 3

Link: https://github.com/spinnaker/spinnaker/releases/tag/spinnaker-release-2025.4.1
- Tag: `spinnaker-release-2025.4.1`
- Nome: Spinnaker 2025.4.1
- Publicada em: 2026-02-03
- Release anterior (cronológica): `spinnaker-release-2025.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  fix(orca/web): properly deserialize webhook status code (#7367) (#7368)
-  test(orca/web): reproduce anonymous pipeline trigger user (#7369) (#7374)
-  fix(OAuth2): Remove quotes as it is causing URI issues while redirecting. (#7380) (#7383)
-  fix(npm): Fix npm publishing (#7398) (#7408)
-  fix(build): actually publish compiled deck-kayenta code (#7389) (#7417)
-  fix(deck): Attempt two of fixing deck publishing (backport #7406) (#7410)
-  chore(build): migrate to trusted npm publishing (#7379) (#7414)
-  fix(publishing): Fix image publishing for deck due to NPM trusted publishing change (#7422) (#7423)
-  fix(gcp): Fix missing pagination token on accelerator lookups (#7420) (#7434)
-  fix(validation): Fixes some url validation handling on underscores (backport #7428) (#7440)
-  fix(publishing): Fix deck kayenta had duplicate package block (#7444) (#7445)

### Release 4

Link: https://github.com/spinnaker/spinnaker/releases/tag/spinnaker-release-2026.1.1
- Tag: `spinnaker-release-2026.1.1`
- Nome: Spinnaker 2026.1.1
- Publicada em: 2026-06-12
- Release anterior (cronológica): `spinnaker-release-2026.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  fix(echo): GitHub status conversion exception (#7701) (#7706)
-  Merge commit from fork (#7711)
-  fix(tests): Add tests around retrofit incorrect call handling from previous PR (#7710) (#7722)
-  fix(echo): Fix Microsoft Teams webhook URL doubling in Retrofit2 migration (#7718) (#7719)

### Release 5

Link: https://github.com/spinnaker/spinnaker/releases/tag/spinnaker-release-2026.1.3
- Tag: `spinnaker-release-2026.1.3`
- Nome: Spinnaker 2026.1.3
- Publicada em: 2026-09-25
- Release anterior (cronológica): `spinnaker-release-2026.2.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 24

-  fix(echo): GitHub status conversion exception (#7701) (#7706)
-  Merge commit from fork (#7711)
-  fix(tests): Add tests around retrofit incorrect call handling from previous PR (#7710) (#7722)
-  fix(echo): Fix Microsoft Teams webhook URL doubling in Retrofit2 migration (#7718) (#7719)
-  fix(build): Defer publishing configuration until -bom subproject evaluation (#7727) (#7728)
-  fix(build): Use default resolution for javaPlatform (#7732) (#7733)
-  fix(packer): pass through Boolean false and numeric 0 -var values (#7806) (#7813)
-  fix(libdiffs): order versions of differing component counts correctly (#7805) (#7816)
-  fix(build): Set group name on all root projects (backport #7834) (#7858)
-  fix(parsing):  Fixes the issue reported in https://github.com/spinnaker/spinnaker/pull/7686 and adds some null checks and blank handling (#7856) (#7861)
-  feat(lambdaInvoke): Opt-In in resolving in Orca the Invoke payload artifact (#7867) (#7869)
-  fix(trigger): Fixes docker UI trigger on expected artifacts to use docker UI not the helm UI (#7824) (#7907)
-  fix(artifacts): prevent SSRF via HTTP redirect in Helm and Jenkins artifact accounts (#7756) (#7909)
-  fix(sql): qualify GROUP BY columns so getAllByApplication works on PostgreSQL (#7902) (#7905)
-  fix(entity-store): Fix a UI bug with entity store references and a few stages which didn't work with it (#7913) (#7915)
-  fix(front50): filter pipelines by application, not pipeline name, in PostFilter (backport #7945) (#7949)
-  fix(echo): populate telemetry spinnakerVersion from resolved service version (#7966) (#7978)
-  fix(rosco): reject helmfile hooks/postRenderers by default (backport #8015) (#8018)
-  chore(tests): Remove deprecated tests from legacy versions (#7984) (#8021)
-  test(aws): replace MinIO and LocalStack with MiniStack in AWS integration tests (backport #8010) (#8013)
-  fix(rosco): close remaining helmfile gaps on some operations (backport #8034) (#8037)
-  fix(kubernetes): retain empty cache entries for kinds with zero live resources (#8054) (#8057)
-  fix(k8s):  K8s caching is kind of broken with SQL  (backport #8059) (#8082)
-  fix(front50): repair dormant pipeline staleCheck optimistic-concurrency check (backport #8022) (#8087)
