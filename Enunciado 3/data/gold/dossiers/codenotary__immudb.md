# codenotary/immudb

Repositório: https://github.com/codenotary/immudb

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/codenotary/immudb/releases/tag/v0.7.0
- Tag: `v0.7.0`
- Nome: Multidatabase
- Publicada em: 2020-08-10
- Release anterior (cronológica): `v0.6.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 228

-  feat: add multiple databases support
-  test: add corruption_checker test
-  chore: add options to tuning corruption checking frequency, iteration and single iteration
-  chore: enhance immudb server messages during start
-  chore: capitalize immudb stop log message for consistency reasons
-  chore: log immudb user messages during start to file if a logfile is specified
-  fix: use the correct server logger and use a dedicated logger with warning level for the db store
-  fix: use dedicated logger for store
-  chore: use debug instead of info for some log messages that are not relevant to the user
-  fix: fix compilation error in corruption checker test
-  fix: race condition in token eviction
-  fix: skip loading databases from disk when in memory is requested
-  test: add homedir tests
-  test: add timestamp tests
-  test: add batch_request tests
-  test: add timestamp service test
-  test(pkg/client): add root_service test
-  test(pkg/client/cache): add file and history_file cache tests
-  chore: add auditor single run mode
-  test: add auditor tests
-  fix(pkg/store): fix count method using a proper NewKeyIterator
-  test: add client sdk tests
-  chore: add unit tests for zip and tar
-  test(pkg/fs): add copy_test and extract duplicated test code into functions
-  doc: update README
-  tests(pkg/server): consinstency checker
-  fix(pkg/server/server): change user pass , old password check
-  tests(pkg/server): mtlsoptions
-  tests(pkg/server): uuid, pid
-  tests(pkg/server):  add server tests. refactor database close
-  chore: fix test
-  test(pkg/server/corruption_checker): corruption checker tests
-  tests(pkg/auth): user , tokens test
-  tests(pkg/auth): clientinterceptor, passwords, permissions, tokenkeys
-  chore: change insert user to use safeset instead of set
-  chore: remove sleep from tests
-  chore(pkg/server): make DevMode default false and cleanup call to action message shwon right after immudb start
-  fix: if custom port is <= 0 use default port for both immudb and immugw
-  chore: use 0.0.0.0 instead of 127.0.0.1 as default address for both immudb and immugw
-  test(pkg/gw): add and replace unit tests for all immu gateway handlers
- ... e mais 188 commits

### Release 2

Link: https://github.com/codenotary/immudb/releases/tag/v0.9.0-RC1
- Tag: `v0.9.0-RC1`
- Nome: immustore
- Publicada em: 2020-12-22
- Release anterior (cronológica): `v0.8.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  doc: 0.8.0 release documentation integrations (#500)
-  Fix admin password (#501)
-  test: Added automatic after-build tests (#504)
-  chore: update readme with SDKs urls (#506)
-  chore: include github stars over time chart (#509)
-  refactor(pkg/client): decoupled immuclient from rootService
-  test(pkg/client/rootservice): add uuid provider unit test
-  chore: fix naming conventions
-  fix(pkg/client): handle rootservice error inside constructor
-  Fix/#510 (#511)
-  doc: update consistency diagram (#512)
-  feat: expose CountAll through gRPC
-  fix: add permissions for the new CountAll gRPC method
-  test(pkg/auth): add test for CountAll permissions
-  Added a not on the file limit in the FAQ (#515)
-  test(pkg/server): add a vanilla grpc server used inside tests
-  chore(pkg/client/timestamp): fix naming convention
-  chore: export uwrap and wrap value method to be used in nimmu
-  chore(pkg/client/clienttest): add mock service client constructor
-  fix(pkg): handle expired token error
-  chore(pkg/client/clienttest): add missing method inside service client mock
-  test(pkg/auth): increase  client interceptors test coverage
-  chore(pkg/auth): fix get batch permissions
-  feat: configurable max incomming msg size (#526)
-  Fix various typos (#524)
-  Fix ineffectual assignments (#525)
-  test: add unit-test for db dump (#527)
-  chore: link to immuchallenge repo (#528)
-  feat: extend sorted set to support multiple equals key
-  chore(pkg/store): add consistency check on zadd and safezadd index reference method and tests
-  change immudb introductory paragraph (#530)
-  feat: enhance auditor to publish tampering details at a specified URL (optional)
-  fix(pkg/store): scan item now contains immudb index, not badger timestamp
-  Some minor refactoring to increase testing and readability for packages server and client (#534)
-  feat(pkg/client/auditor): enhance auditor to always send audit notification (even when no tampering was detected) if a notification URL is specified
-  Testing store (#537)
-  test(pkg/client): validate connection status (#539)
-  test(pkg/sservice): use delayed task for sequential actions (#538)
-  test(pkg/auth): test cases for client and server interceptors (#540)
-  chore: fix typo in cmd help (#541)
- ... e mais 210 commits

### Release 3

Link: https://github.com/codenotary/immudb/releases/tag/v1.2.4
- Tag: `v1.2.4`
- Nome: v1.2.4
- Publicada em: 2022-04-28
- Release anterior (cronológica): `v1.2.4-RC1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  release: v1.2.4

### Release 4

Link: https://github.com/codenotary/immudb/releases/tag/v1.3.0
- Tag: `v1.3.0`
- Nome: v1.3.0
- Publicada em: 2022-05-23
- Release anterior (cronológica): `v1.3.0-RC1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  fix(pkg/client): enhance client-side validations in verified methods
-  fix(embedded/sql): return invalid value when using aggregated col selector in temporal queries
-  release: v1.3.0

### Release 5

Link: https://github.com/codenotary/immudb/releases/tag/v1.9.4
- Tag: `v1.9.4`
- Nome: (sem nome)
- Publicada em: 2024-07-25
- Release anterior (cronológica): `v1.9.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 16

-  Update README.md
-  Remove license badge
-  fix: set mattermost payload
-  Log request information as transaction metadata
-  Add support for JSON type
-  Add table of contents and projects section to README
-  Add CreatedAt and CreatedBy to DatabaseInfo
-  Implement CHECK constraints
-  Update go.sum
-  Update README.md
-  Prohibite changing transiency of keys
-  Fix startup failure when remote identifier is not present
-  Implement SQL permissions
-  Refactor SQL privileges
-  Implement CSV import/export of tables
-  release v1.9.4
