# tektoncd/pipeline

Repositório: https://github.com/tektoncd/pipeline

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/tektoncd/pipeline/releases/tag/v0.17.2
- Tag: `v0.17.2`
- Nome: Tekton Pipeline release v0.17.2 "Raas Rapbot"
- Publicada em: 2020-10-26
- Release anterior (cronológica): `v0.17.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  Fix json annotations in WhenExpression
-  Fix TaskRunSpec overrides when empty 🗜
-  tekton: port koparse fix to release-0.17.x

### Release 2

Link: https://github.com/tektoncd/pipeline/releases/tag/v0.43.1
- Tag: `v0.43.1`
- Nome: Tekton Pipeline release v0.43.1 "British-Shorthair Jarvis"
- Publicada em: 2023-01-06
- Release anterior (cronológica): `v0.43.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Use the golangci-lint configured in Makefile in build tests
-  Register informers for v1 TaskRun and PipelineRun
-  ChildReference status helper functions should support both CustomRuns and Runs
-  tekton: fix KO_CONFIG_PATH on release pipeline

### Release 3

Link: https://github.com/tektoncd/pipeline/releases/tag/v0.62.6
- Tag: `v0.62.6`
- Nome: Tekton Pipeline release v0.62.6 "Ragamuffin Reventlov"
- Publicada em: 2024-11-20
- Release anterior (cronológica): `v0.65.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  Refine check if the result is from a matrix task
-  pkg/taskrunmetrics/fake shouldn't be imported…
-  {taskrun,pipelinerun}metrics: make sure config is up-to-date
-  check namespace config for node throttle metric
-  apply default-container-resource-requirements before LimitRange transformer
-  Fix Artifact type to a pointer
-  Fix isolated workspaces ignored when using StepTemplate
-  Mark steps as deleted when TaskRun fails
-  Backport release "scripts" changes from main…
-  Expose Resolvers Controller performance tuning configurations
-  Run finally pipeline even if task is failed at the validation
-  Resolve review comments 1
-  Exit reconcilation and markfailed if finally is not present
-  Remove permanent error and improve skip logic
-  Fix number of completed and failed task in case of ValidationFailed
-  fix(pipelinerun): resolve issue with PipelineRun not timing out successfully
-  Use io.ReadFull to read the bundle content

### Release 4

Link: https://github.com/tektoncd/pipeline/releases/tag/v1.9.5
- Tag: `v1.9.5`
- Nome: Tekton Pipeline release v1.9.5 "Devon Rex Dreadnought"
- Publicada em: 2026-06-23
- Release anterior (cronológica): `v1.13.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 60

-  fix(pipelines): allow pipeline param defaults to use non-param variables
-  tekton: update plumbing ref to include full image references fix
-  ci: add CI summary fan-in job for branch protection
-  tekton: update plumbing ref to latest commit
-  Fix panic in GenerateDeterministicNameFromSpec with long resolver names
-  fix: prevent path traversal in git resolver pathInRepo parameter
-  Re-enable pipeline-api.md generation
-  fix: Align cache configstore with framework implementation
-  fix: resolve cache race with singleflight
-  fix: remove corrupted cache entries on type error
-  fix: use TextParser struct directly for prometheus/common v0.62.0 compatibility
-  fix: bump Go to 1.24.13 to fix CVE-2025-61728, CVE-2025-61726, CVE-2025-61729
-  fix: pin registry image and relax log-based cache assertion
-  fix(e2e): replace ubuntu with busybox in dind-sidecar test Dockerfile
-  Fix running_taskruns metric overcounting TaskRuns with no condition
-  Security: reject system API token with user-controlled serverURL
-  fix: prevent git argument injection via revision parameter (GHSA-94jr-7pqp-xhcq)
-  fix: normalize VolumeMount paths before /tekton/ restriction check
-  fix: strip resolver prefixes and use non-capturing group for pattern anchoring
-  fix: limit HTTP resolver response body size to prevent OOM DoS
-  fix: trim whitespace from source URI before pattern matching
-  build(deps): bump k8s.io/api from 0.32.11 to 0.32.13
-  build(deps): bump k8s.io/client-go from 0.32.11 to 0.32.13
-  build(deps): bump k8s.io/apiextensions-apiserver from 0.32.11 to 0.32.13
-  build(deps): bump k8s.io/apimachinery from 0.33.7 to 0.33.11
-  build(deps): bump github.com/go-jose/go-jose/v3 from 3.0.4 to 3.0.5
-  build(deps): bump github.com/spiffe/spire-api-sdk from 1.14.0 to 1.14.6
-  build(deps): bump actions/cache from 4.2.3 to 4.2.4
-  build(deps): bump tj-actions/changed-files from 47.0.1 to 47.0.6
-  build(deps): bump github/codeql-action from 4.32.0 to 4.32.6
-  build(deps): bump the all group in /tekton with 4 updates
-  build(deps): bump step-security/harden-runner from 2.14.1 to 2.14.2
-  fix: surface clear errors when completed tasks miss referenced results
-  build(deps): bump github.com/tektoncd/pipeline
-  build(deps): bump the all group across 1 directory with 4 updates
-  build(deps): bump chainguard-dev/actions from 1.5.13 to 1.5.16
-  build(deps): bump actions/dependency-review-action from 4.8.2 to 4.8.3
-  [cherry-pick: release-v1.9.x] fix: bump google.golang.org/grpc to 1.79.3 (CVE-2026-33186)
-  build(deps): bump github.com/google/go-containerregistry
-  build(deps): bump k8s.io/apimachinery from 0.33.11 to 0.33.12
- ... e mais 20 commits

### Release 5

Link: https://github.com/tektoncd/pipeline/releases/tag/v1.3.6
- Tag: `v1.3.6`
- Nome: Tekton Pipeline release v1.3.6 "Maine Coon Melfina"
- Publicada em: 2026-06-23
- Release anterior (cronológica): `v1.6.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 92

-  Fix tini-git image to be multi-arch
-  fix: exclude pending PipelineRuns from tekton_pipelines_controller_running_pipelineruns metric
-  Disable the Gitea e2e tests temporarily to unblock
-  check initContainers for kubernetes sidecar implementation
-  Do not fail PipelineRun if pvc creation error is because of exceeded quotas
-  Refactor CreatePVCFromVolumClaimTemplate condition logic
-  fix: allow finalizer updates on completed TaskRuns
-  fix: allow finalizer updates on completed PipelineRuns
-  fix: update tests after cherrypicking from PR 9011
-  fix(#8940): Fix token-authentication header in git resolver
-  chore: fix unit test action name
-  tests: pdate csi-node-driver-registrar image reference
-  Pin actions by commit SHA or image digest
-  test/e2e: remove data race on global variable requireAlphaFeatureFlag
-  test/e2e: remove prow from env-file names
-  Add comments on ignore to highlight why they are here
-  examples: make sure we use the same image for sidecar and step
-  test: reduce the number of examples tests running in parallel
-  Migrate tests images out of dockerhub.
-  test: limit examples test parallelism to 2 to prevent timeouts
-  test(e2e): move flaky retry/matrix tests to no-ci temporarily
-  ci: Ensure e2e setup errors fail tests, add retries during e2e setup
-  e2e: give more time for dind-sidecar to start
-  Add hostUsers field support to PodTemplate
-  chore(pipelinerun): remove cmpopts.SortSlices from pkg/reconciler/pipelinerun/pipelinerun_updatestatus_test.go
-  Add missing sort.Slice for childRefs ordering
-  tekton: update plumbing ref to include full image references fix
-  tekton: update plumbing ref to latest commit
-  ci: add CI summary fan-in job for branch protection
-  fix: panic in v1beta1 matrix validation for invalid result refs
-  fix: Prevent excessive reconciliation when timeout disabled
-  chore: centralize ko base image configuration
-  Fix tekton/publish sed for combined-based-image digest replacement
-  feat: upload release manifests to oracle cloud
-  chore(release-pipeline): update references to oci bucket
-  Fix panic in GenerateDeterministicNameFromSpec with long resolver names
-  fix: prevent path traversal in git resolver pathInRepo parameter
-  fix(ci): fix e2e test failures on release-v1.3.x
-  fix: add signal handling in sidecarlogresults for native k8s sidecars
-  Re-enable pipeline-api.md generation
- ... e mais 52 commits
