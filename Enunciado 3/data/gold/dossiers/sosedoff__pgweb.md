# sosedoff/pgweb

Repositório: https://github.com/sosedoff/pgweb

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/sosedoff/pgweb/releases/tag/v0.8.0
- Tag: `v0.8.0`
- Nome: 0.8.0
- Publicada em: 2016-01-11
- Release anterior (cronológica): `v0.7.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 27

-  Update changelog
-  Update dockerfile to use golang 1.5 image
-  Encode bigints as strings
-  Automatically call PrepareBigints for all queries
-  Format big floats as well
-  Merge pull request #109 from sosedoff/bigint-to-string
-  Move query export buttons to the right, add xml export button
-  Do not record duplicate queries into history
-  Add support for offset in table rows endpoint, dry up code
-  Implement pagination and simple filtering
-  Reset filters before loading table data
-  Filtering bugfixes
-  Do not show bindata.go in the git diff log
-  Merge pull request #110 from sosedoff/filter-and-pagination
-  Make pgweb to use multiple sessions at once [wip]
-  Make sessions optional via --sessions CLI flag
-  Move api middleware into its own file
-  Only expose sessions data in debug mode, otherwise return just a count of sessions
-  Allow enabling sessions via SESSIONS env var
-  Merge pull request #111 from sosedoff/sessions
-  Update readme
-  Change icon on sequences items on the sitebar
-  Update screenshots
-  Godeps go 1.5.1
-  Bump go to 1.5.2
-  Update bindata
-  Version bump: 0.8.0

### Release 2

Link: https://github.com/sosedoff/pgweb/releases/tag/v0.9.10
- Tag: `v0.9.10`
- Nome: 0.9.10
- Publicada em: 2017-11-04
- Release anterior (cronológica): `v0.9.9`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 34

-  Update changelog
-  Fix formatting
-  Update docker image version
-  Correction on idle timeout
-  Fix panics when sshinfo is not set on bookmarks
-  Add an extra test to verify SSHinfoIsEmpty does not panic
-  Merge pull request #296 from sosedoff/ssh-hotfix
-  Dot now allow using startup bookmark in multi-session mode
-  Tweak wording
-  Merge pull request #300 from sosedoff/disable-bookmark-on-startup
-  added simple copy to clipboard from data-id prop
-  #282: added timeout flags & tuned client.IsIdle()
-  #282 fix disabled state per idle timeout
-  #301: change rexexp to String.split()
-  Merge pull request #302 from ldinc/issue#301
-  Regenerated bindata
-  Search for database with autocomplete
-  UI and design tweaks
-  Merge branch 'EyesBear-master'
-  Merge branch 'master' into issue#282
-  #282: updated bindata
-  #282: set flag idle logic to cli-run phase
-  #282: cleared bindata
-  Merge pull request #303 from ldinc/issue#282
-  Rename disable connection timeout cli option
-  Fix broken bindata
-  Trigger CI failure if bindata contains any dev links
-  Add asset check script
-  Remove bindata check from test-all script
-  Merge pull request #305 from sosedoff/assets-ci-guard
-  Update README
-  Merge pull request #311 from krlevkirill/patch-1
-  Rebuild bindata
-  Release 0.9.10

### Release 3

Link: https://github.com/sosedoff/pgweb/releases/tag/v0.11.1
- Tag: `v0.11.1`
- Nome: 0.11.1
- Publicada em: 2019-01-28
- Release anterior (cronológica): `v0.11.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 16

-  Update changelog/dockerfile
-  Fix typo
-  Add custome base64 encode to handle special character
-  Fix: missing base64.js in index.html and remove blank space
-  Fix startup error when DATABASE_URL is set
-  Merge pull request #406 from sosedoff/fix-startup-error-with-db-url
-  Merge pull request #405 from Nhat002/fix_encode_query_to_base64_in_export
-  Remove apt cache when building docker container
-  Update license years
-  Fix error when automatic user detection fails
-  Add extra note
-  Merge pull request #408 from sosedoff/fix-auto-user-detection
-  Switch to github.com/go-bindata/go-bindata fork
-  Regenerate bindata
-  Merge pull request #409 from sosedoff/switch-bindata-dep
-  Release 0.11.1

### Release 4

Link: https://github.com/sosedoff/pgweb/releases/tag/v0.16.2
- Tag: `v0.16.2`
- Nome: 0.16.2
- Publicada em: 2024-11-02
- Release anterior (cronológica): `v0.16.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Update changelog
-  Update references from master branch to main branch (#750)
-  Try running checks against pg 17 (#758)
-  Version bump: 0.16.2

### Release 5

Link: https://github.com/sosedoff/pgweb/releases/tag/v0.17.0
- Tag: `v0.17.0`
- Nome: 0.17.0
- Publicada em: 2025-11-22
- Release anterior (cronológica): `v0.16.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 23

-  Update changelog
-  Update changelog formatting
-  Fix typos (#764)
-  add exec time of empty queries (#763)
-  Add server settings view (#768)
-  Shorten git revision printed in the --version output (#770)
-  Bump rack in /config/examples/connect_backend_ruby (#777)
-  Fix typo in the list of env vars (#786)
-  Bump rack from 2.2.11 to 2.2.14 in /config/examples/connect_backend_ruby (#792)
-  Update connect backend code to work on latest ruby version
-  Connect backend refactor (#801)
-  Bump golangci-linter to 1.62.2 (#772)
-  Add PostgreSQL 18 support to Github Actions (#816)
-  Add extra test for verifiying ssh connection options (#817)
-  Bump golangci-lint version in CI to v1.64.8 (#819)
-  Use go1.24 in CI and scripts (#818)
-  Update dockerfile to use golang 1.24 image (#821)
-  Bump go crypto package to 0.44.0 (#820)
-  Minor session manager code cleanup and refactor (#822)
-  Bump golang.org/x/crypto from 0.44.0 to 0.45.0 (#823)
-  Fix ENV reference in Dockerfile
-  Remove obsolete  reference from docker compose file
-  Version bump: 0.17.0
