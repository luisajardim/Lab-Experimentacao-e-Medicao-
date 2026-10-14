# kata-containers/kata-containers

Repositório: https://github.com/kata-containers/kata-containers

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/kata-containers/kata-containers/releases/tag/1.9.4
- Tag: `1.9.4`
- Nome: Kata Containers 1.9.4
- Publicada em: 2020-01-16
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/kata-containers/kata-containers/releases/tag/1.10.7
- Tag: `1.10.7`
- Nome: Kata Containers 1.10.7
- Publicada em: 2020-09-01
- Release anterior (cronológica): `1.12.0-alpha1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 21

-  release: Kata Containers 1.10.0
-  Merge pull request #121 from jcvenegas/1.10.0-branch-bump
-  release: Kata Containers 1.10.1
-  Merge pull request #140 from amshinde/1.10.1-branch-bump
-  path-absolutize: version update
-  release: Kata Containers 1.10.2
-  Merge pull request #161 from bergwolf/1.10.2-branch-bump
-  release: Kata Containers 1.10.3
-  license: add license header
-  Merge pull request #185 from chavafg/topic/fix-license
-  Merge pull request #182 from chavafg/1.10.3-branch-bump
-  release: Kata Containers 1.10.4
-  Merge pull request #208 from katabuilder/1.10.4-branch-bump
-  release: actions: pin artifact to v1
-  Merge pull request #213 from jcvenegas/backport-1.10-fix-release
-  release: Kata Containers 1.10.5
-  Merge pull request #274 from amshinde/1.10.5-branch-bump
-  release: Kata Containers 1.10.6
-  Merge pull request #349 from bergwolf/1.10.6-branch-bump
-  release: Kata Containers 1.10.7
-  Merge pull request #632 from egernst/1.10.7-branch-bump

### Release 3

Link: https://github.com/kata-containers/kata-containers/releases/tag/2.2.1
- Tag: `2.2.1`
- Nome: Kata Containers 2.2.1
- Publicada em: 2021-09-24
- Release anterior (cronológica): `2.3.0-alpha1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 67

-  build_image: Fix error soft link about initrd.img
-  virtcontainers: clh: Upgrade to the openapi-generator v5.2.1
-  virtcontainers: clh: Re-generate the client code
-  virtcontainers: clh: Migrate to use the updated client APIs
-  virtcontainers: clh: Use constructors to ensure proper default value
-  virtcontainers: clh: Fix the unit test
-  virtcontainers: clh: Workaround incorrect default values
-  ci: Temporarily skip agent shutdown test on s390x
-  Merge pull request #2520 from Bevisy/stable-2.2-2503
-  Merge pull request #2531 from Jakob-Naucke/backport-s390x-skip-agent-shutdown-test
-  Merge pull request #2525 from likebreath/0827/backport_clh_generator
-  runtime: fix default hypervisor path
-  runtime: drop qemu-lite support
-  docs: remove mentioning of qemu-lite
-  Merge pull request #2533 from bergwolf/qemu-lite
-  release: Kata Containers 2.2.0
-  Merge pull request #2541 from fidencio/2.2.0-branch-bump
-  snap: Test variable instead of executing "branch"
-  sandbox: Add device permissions such as /dev/null to cgroup
-  Merge pull request #2588 from devimc/2021-09-07/backport/fixSnap
-  runtime: Fix README link
-  Merge pull request #2614 from sameo/stable-2.2
-  Merge pull request #2608 from Bevisy/main-2539-bp
-  versions: Upgrade to Cloud Hypervisor v18.0
-  virtcontainers: clh: Re-generate the client code
-  virtcontainers: clh: Revert the workaround incorrect default values
-  sandbox: Allow the device to be accessed,such as /dev/null and /dev/urandom
-  Merge pull request #2619 from likebreath/0913/backport_clh_v18.0
-  backport-2.2: remove default config for arm64.
-  Merge pull request #2642 from jongwu/qemu_mak_2.2
-  runtime: tracing: Use root context to stop tracing
-  runtime: tracing: Fix logger passed in newContainer
-  virtcontainers: fc: parse vcpuID correctly
-  virtiofs: Create shared directory with 0700 mode, not 0750
-  shimv2: add logging to shimv2 api calls
-  shimv2: add information to method comment
-  runtime: Add container field to logs
-  Merge pull request #2679 from c3d/backport/2527-adding-debugging-msgs
-  Merge pull request #2678 from nubificus/stable-2.2-fix_fc_vcpu_thread
-  ci: Call agent shutdown test only in the correspondent CI_JOB
- ... e mais 27 commits

### Release 4

Link: https://github.com/kata-containers/kata-containers/releases/tag/2.5.2
- Tag: `2.5.2`
- Nome: # Release 2.5.2
- Publicada em: 2022-09-30
- Release anterior (cronológica): `3.0.0-rc1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 52

-  action: extend commit message line limit to 150 bytes
-  versions: Update Cloud Hypervisor to v25.0
-  Merge pull request #4643 from fidencio/topic/stable-2.5-bump-clh-to-v25.0-release
-  clh: Don't crash if no network device is set by the upper layer
-  Merge pull request #4653 from fidencio/topic/stable-2.5-fix-clh-crash-when-booting-up-with-no-network-device
-  versions: Update Firecracker version to v1.1.0
-  Merge pull request #4807 from nubificus/backport-2.5-fc-v1.1
-  runtime: add unlock before return in sendReq
-  nydus: upgrade nydus/nydus-snapshotter version
-  container: kill all of the processes in this container
-  runtime: Fix DisableSelinux config
-  build: Fix clh source build as normal user
-  release: Adapt kata-deploy for 2.5.0
-  release: Kata Containers 2.5.0
-  Merge pull request #4910 from bergwolf/2.5.0-branch-bump
-  versions: Upgrade to Cloud Hypervisor v26.0
-  runtime: clh: Re-generate the client code
-  runtime: clh: Use the new 'payload' interface
-  Merge pull request #4955 from likebreath/0818/backport_clh_v26.0
-  dep: update nix dependency
-  agent/runk: update regex dependency
-  agent-ctl/trace-forwarder: udpate thread_local dependency
-  versions: Update kernel to 5.15.63
-  versions: Upgrade rust supported version to 1.59.0
-  agent-ctl: Get rid of compiler warning
-  Merge pull request #5059 from amshinde/bump-rust-version
-  Merge pull request #5052 from fidencio/topic/stable-2.5-update-kernel-before-release
-  Merge pull request #5049 from bergwolf/github/backport-stable-2.5
-  agent: do some rollback works if case of do_create_container failed
-  runtime: tracing: End root span at end of trace
-  kernel: Add CONFIG_CGROUP_HUGETLB=y as part of the cgroup fragments
-  release: Adapt kata-deploy for 2.5.1
-  release: Kata Containers 2.5.1
-  Merge pull request #5047 from amshinde/2.5.1-branch-bump
-  kernel: Add CONFIG_CGROUP_HUGETLB=y as part of the cgroup fragments
-  hypervisor: Add GetTotalMemoryMB to interface
-  sandbox: don't hotplug too much memory at once
-  sandbox_test: Add test to verify memory hotplug behavior
-  kernel: fix for set_kmem_limit error
-  kernel: upgrade guest kernel support to 5.19.2
- ... e mais 12 commits

### Release 5

Link: https://github.com/kata-containers/kata-containers/releases/tag/3.23.0
- Tag: `3.23.0`
- Nome: Kata Containers 3.23.0
- Publicada em: 2025-11-18
- Release anterior (cronológica): `3.22.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 193

-  ci: Add NVIDIA CUDA vectoradd test
-  ci: Refactor NVIDIA NIM test
-  kata-deploy: Automatically deploy NodeFeatureRules for TEEs
-  actions: Remove unused USING_NFD
-  runtime-rs: pass the tuntap fds down to Cloud Hypervisor
-  runtime-rs: supporting the CLH VMM process running in non-root mode
-  kata-types: add VM template and factory configuration
-  runtime-rs: add factory, template and vm modules for VM template lifecycle
-  runtime-rs: boot vm from template
-  Merge pull request #11862 from StevenFryto/rootless_clh
-  Merge pull request #11828 from jiuyi123/rs-vm-template-runtime-rs
-  gpu: Add libs for CC
-  gpu: Remove unneeded libraries
-  readme: install: Drop outdated documentation
-  Merge pull request #11933 from kata-containers/topic/kata-deploy-nfd-dependency-part-I
-  libs: Fix formatting issue
-  Merge pull request #11993 from zvonkok/vectorAdd
-  dragonball: Bump kvm-ioctls to fix security issue
-  Merge pull request #11867 from spectator333/update-rust-vmm-deps
-  kata-ctl: add factory subcommands for VM template management
-  docs: add guide on VM templating usage in runtime-rs
-  Merge pull request #11816 from jiuyi123/rs-vm-template-kata-ctl-merge
-  tests: k8s: Remove tests running on GitHub provided runner
-  webhook: allow privileged containers
-  gpu: Handle VFIO and IOMMUFD
-  osbuilder: nvrc: Consume NVRC release instead of building it
-  kata-deploy: Add more per-arch options
-  kata-deploy: Allow setting the default runtime class name
-  kata-deploy: Add NFD as a dependency
-  tests: Use NFD as part of the tests
-  tests: Do not enable NFD on cbl-mariner
-  tests: Do not enable NFD on s390x
-  scripts: release: Run helm dependencies update
-  tests: k8s: run QoS tests on a bigger instance
-  tests: k8s: parallel: Increase timeout
-  Merge pull request #12014 from fidencio/topic/release-ensure-helm-dependencies-update
-  tests: policy-pod: detect create container errors early
-  tests: policy-deployment-sc: reduced redundancy
-  tests: policy-deployment-sc: detect create container errors early
-  tests: policy-job: detect create container errors early
- ... e mais 153 commits
