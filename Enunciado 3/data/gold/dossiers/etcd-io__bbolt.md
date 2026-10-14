# etcd-io/bbolt

Repositório: https://github.com/etcd-io/bbolt

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/etcd-io/bbolt/releases/tag/v1.3.1-coreos.2
- Tag: `v1.3.1-coreos.2`
- Nome: v1.3.1-coreos.2
- Publicada em: 2017-09-27
- Release anterior (cronológica): `v1.3.1-coreos.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 28

-  README: explain purpose of bbolt fork
-  Merge pull request #32 from heyitsanthony/readme-fork
-  Add NoSync field to Options
-  Merge pull request #30 from tylertreat/nosync_option
-  add coverage reports
-  Merge pull request #33 from heyitsanthony/cov
-  Added support for no timeout locks on db files (#35)
-  Increase freelist.releaseRange unit test coverage.
-  Merge pull request #36 from jpbetz/freelist-tests
-  tx: use io.SeekStart in WriteTo function
-  Improve test coverage for releaseRange rollbacks.
-  Merge pull request #37 from jpbetz/tx-tests
-  db: add test in read-only mode
-  db: return t.Rollback directly in the end of View function
-  Merge pull request #43 from lorneli/bbolt_seek
-  Merge pull request #46 from lorneli/bbolt_db_test
-  Merge pull request #41 from lorneli/bbolt_db
-  tx: just close file once in WriteTo function
-  *: fix gofmt errors and makefile test
-  Merge pull request #48 from heyitsanthony/fix-fmt-test
-  Merge pull request #44 from lorneli/bbolt_tx
-  test tx.Check() on read only db
-  Fix bolt CLI tool print entire freelist, and to dump keys/value bytes of leaf elements.
-  Merge pull request #50 from jpbetz/page-kv-and-full-freelist
-  tx: load freelist on Check()
-  Merge pull request #52 from jpbetz/fix-readonly-check
-  Removed 'moribund' since some people think it's a bit derogatory towards the original developer.
-  Merge pull request #56 from virtualsue/master

### Release 2

Link: https://github.com/etcd-io/bbolt/releases/tag/v1.3.7
- Tag: `v1.3.7`
- Nome: v1.3.7
- Publicada em: 2023-01-30
- Release anterior (cronológica): `v1.3.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 169

-  ignore goland ide generated files
-  Ignore IntelliJ/GoLand generated files.
-  Add Rain torrent library to projects section in README (#232)
-  remove unreachable code
-  Use madvise syscall wrapper from golang.org/x/sys/unix
-  fix etcd-io/bbolt#247 move compact logic
-  ignore .idea folder, go to 1.15
-  bucket,cursor: clarify sort order and seek algorithm
-  Add Chestnut to os projects in README.md
-  Merge pull request #248 from andrewpmartinez/expose.compact
-  Merge pull request #259 from jrapoport/patch-1
-  Use WriteTo() instead
-  Merge pull request #264 from zouyee/instead
-  test: add buffer to a channel to avoid the goroutine leak
-  Merge pull request #254 from lzhfromustc/12_9_GL
-  Merge pull request #243 from tklauser/madvise-x-sys-unix
-  tx: remove outdated comment (#271)
-  Avoid unnecessary conversions (#270)
-  Add `Mlock` flag.
-  Skip few long running tests in `-short` mode
-  Merge pull request #274 from wpedrak/speed-up-short-tests
-  `Mlock` flag tests
-  Add BoltDB Viewer to projects section in README (#255)
-  remove dead links (#242)
-  Merge branch 'master' into patch
-  Make sure failed tests report their exit code (#240)
-  replace buf[:] with buf (#238)
-  Replace bolt with bbolt in command line usage (#235)
-  cmd/bbolt: pagesCommand no need db.Update (#226)
-  Merge pull request #273 from wpedrak/mlock-flag
-  Merge pull request #223 from huahang/patch
-  Clean and simplify some code (#279)
-  Use golang.org/x/sys/windows for FileLockEx/UnlockFileEx
-  Merge pull request #283 from tklauser/lock-unlock-x-sys-windows
-  Update README.md
-  fix lmdb link (#300)
-  compact: open src file readonly (#292)
-  Add support for loong64 arch. (#303)
-  upgrade golang to 1.17 and replace iouitl with io and os (#297)
-  support sub buckets in get+keys (#295)
- ... e mais 129 commits

### Release 3

Link: https://github.com/etcd-io/bbolt/releases/tag/v1.4.0
- Tag: `v1.4.0`
- Nome: v1.4.0
- Publicada em: 2025-02-05
- Release anterior (cronológica): `v1.4.0-beta.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 40

-  Update release date for v1.4.0-beta.0
-  Merge pull request #852 from ahrtr/changelog_20241104
-  chore/docs: installing document description should use bbolt
-  Merge pull request #855 from caicancai/docs
-  Bump go toolchain to 1.23.3 Signed-off-by: Samuel Bartels <bartelssamuel20@gmail.com>
-  Merge pull request #856 from samuelbartels20/go/1.23.3
-  build(deps): Bump golang.org/x/sync from 0.8.0 to 0.9.0
-  Merge pull request #860 from etcd-io/dependabot/go_modules/golang.org/x/sync-0.9.0
-  build(deps): Bump golang.org/x/sys from 0.26.0 to 0.27.0
-  Merge pull request #861 from etcd-io/dependabot/go_modules/golang.org/x/sys-0.27.0
-  build(deps): Bump github.com/stretchr/testify from 1.9.0 to 1.10.0
-  Merge pull request #865 from etcd-io/dependabot/go_modules/github.com/stretchr/testify-1.10.0
-  Updated Go toolchain to 1.23.4
-  Merge pull request #867 from deanurag/main
-  build(deps): Bump golang.org/x/sync from 0.9.0 to 0.10.0
-  Merge pull request #869 from etcd-io/dependabot/go_modules/golang.org/x/sync-0.10.0
-  build(deps): Bump golang.org/x/sys from 0.27.0 to 0.28.0
-  Merge pull request #870 from etcd-io/dependabot/go_modules/golang.org/x/sys-0.28.0
-  docs: remove repetitive words
-  Merge pull request #871 from RiceChuan/main
-  build(deps): Bump actions/setup-go from 5.1.0 to 5.2.0
-  Merge pull request #874 from etcd-io/dependabot/github_actions/actions/setup-go-5.2.0
-  Update buildtags
-  Merge pull request #879 from x3c3/go-fix-fixes
-  build(deps): Bump golang.org/x/sys from 0.28.0 to 0.29.0
-  Merge pull request #880 from etcd-io/dependabot/go_modules/golang.org/x/sys-0.29.0
-  bbolt: update golang toolchain to 1.23.5
-  Merge pull request #884 from ajaysundark/bump-bbolt-golang-toolchain-1.23.5
-  build(deps): Bump golangci/golangci-lint-action from 6.1.1 to 6.2.0
-  Merge pull request #886 from etcd-io/dependabot/github_actions/golangci/golangci-lint-action-6.2.0
-  build(deps): Bump actions/stale from 9.0.0 to 9.1.0
-  build(deps): Bump actions/setup-go from 5.2.0 to 5.3.0
-  Merge pull request #888 from etcd-io/dependabot/github_actions/actions/setup-go-5.3.0
-  Merge pull request #887 from etcd-io/dependabot/github_actions/actions/stale-9.1.0
-  build(deps): Bump github.com/spf13/pflag from 1.0.5 to 1.0.6
-  Merge pull request #889 from etcd-io/dependabot/go_modules/github.com/spf13/pflag-1.0.6
-  Remove changelog from release-1.4
-  Merge pull request #890 from ahrtr/remove_changelog_20250204
-  update goland toolchain to 1.23.6
-  Merge pull request #893 from ArkaSaha30/bump-go-1.23.6

### Release 4

Link: https://github.com/etcd-io/bbolt/releases/tag/v1.4.1
- Tag: `v1.4.1`
- Nome: v1.4.1
- Publicada em: 2025-06-10
- Release anterior (cronológica): `v1.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 19

-  Update version to 1.4.0
-  Merge pull request #895 from ahrtr/version_20250207
-  Fix debug sync log line
-  Merge pull request #905 from k8s-infra-cherrypick-robot/cherry-pick-904-to-release-1.4
-  Bump release 1.4 go toolchain to v1.23.7
-  Merge pull request #921 from tcchawla/release-1.4-bump-go-to-1.23.7
-  bump go 1.23.8
-  Merge pull request #938 from joshjms/release-1.4
-  Clarify the effect of InitialMmapSize on Windows platform
-  Merge pull request #943 from ahrtr/1.4_initial_mmap_size_20240409
-  [release-1.4] Bump Go to 1.23.9
-  Merge pull request #957 from Elbehery/1.4_20250507-bump-go-1.23.9
-  db: drop unused txs list
-  Merge pull request #969 from nspcc-dev/drop-unused-txs
-  Revert "Merge pull request #969 from nspcc-dev/drop-unused-txs"
-  Merge pull request #974 from Elbehery/20250609-revert-drop-unused-txs-list
-  Move MaxMapSize and MaxAllocSize into internal common
-  Merge pull request #978 from ahrtr/20250610_panick_1.4
-  Bump version to 1.4.1

### Release 5

Link: https://github.com/etcd-io/bbolt/releases/tag/v1.5.0
- Tag: `v1.5.0`
- Nome: v1.5.0
- Publicada em: 2026-06-21
- Release anterior (cronológica): `v1.4.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  update goland toolchain to 1.23.6
-  Merge pull request #891 from marcelfranca/issue/19333-main
-  Update changelog for v1.4.0
-  Merge pull request #894 from ahrtr/changelog_20250205
-  build(deps): Bump golang.org/x/sys from 0.29.0 to 0.30.0
-  build(deps): Bump golangci/golangci-lint-action from 6.2.0 to 6.3.2
-  Merge pull request #899 from etcd-io/dependabot/go_modules/golang.org/x/sys-0.30.0
-  build(deps): Bump golang.org/x/sync from 0.10.0 to 0.11.0
-  Merge pull request #901 from etcd-io/dependabot/github_actions/golangci/golangci-lint-action-6.3.2
-  Merge pull request #900 from etcd-io/dependabot/go_modules/golang.org/x/sync-0.11.0
-  Fix debug sync log line
-  Merge pull request #904 from ivanvc/fix-debug-log-line
-  Add code of conduct
-  Merge pull request #906 from spzala/addcoc
-  Bump go linter 1.24
-  build(deps): Bump github.com/spf13/cobra from 1.8.1 to 1.9.1
-  Merge pull request #909 from Elbehery/20250216-bump-go-linter-1.24
-  build(deps): Bump golangci/golangci-lint-action from 6.3.2 to 6.5.0
-  chore: setup golangci-lint config file
-  Merge pull request #911 from etcd-io/dependabot/github_actions/golangci/golangci-lint-action-6.5.0
-  Merge pull request #912 from etcd-io/dependabot/go_modules/github.com/spf13/cobra-1.9.1
-  bump golangci-lint v1.64.5
-  Merge pull request #915 from Elbehery/20250221-bump-go-linter-1.24
-  bump golangci-lint v1.64.5-win
-  Merge pull request #916 from Elbehery/20250221-bump-go-linter-1.24-win
-  Merge pull request #913 from mmorel-35/golangci-lint
-  build(deps): Bump golang.org/x/sync from 0.11.0 to 0.12.0
-  build(deps): Bump golang.org/x/sys from 0.30.0 to 0.31.0
-  Merge pull request #924 from ivanvc/update-golang-x-dependencies
-  Bump go 1.24.0
-  Merge pull request #907 from Elbehery/20250216-bump-go1.24.0
-  Bump go 1.24.1
-  Merge pull request #925 from Elbehery/20250311-bump-go1.24.1
-  github/workflows: use ARM64 runners for robustness tests
-  github/workflows: add ARM64 tests
-  Merge pull request #926 from ivanvc/use-github-runners-for-arm64-robustness-tests
-  build(deps): Bump golangci/golangci-lint-action from 6.5.0 to 6.5.1
-  Merge pull request #927 from etcd-io/dependabot/github_actions/golangci/golangci-lint-action-6.5.1
-  build(deps): Bump actions/setup-go from 5.3.0 to 5.4.0
-  Merge pull request #933 from etcd-io/dependabot/github_actions/actions/setup-go-5.4.0
- ... e mais 210 commits
