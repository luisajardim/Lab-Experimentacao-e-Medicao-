# cberner/redb

Repositório: https://github.com/cberner/redb

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/cberner/redb/releases/tag/v0.11.0
- Tag: `v0.11.0`
- Nome: 0.11.0
- Publicada em: 2023-01-14
- Release anterior (cronológica): `v0.10.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/cberner/redb/releases/tag/v0.21.0
- Tag: `v0.21.0`
- Nome: 0.21.0
- Publicada em: 2023-06-09
- Release anterior (cronológica): `v0.20.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 3

Link: https://github.com/cberner/redb/releases/tag/v3.1.1
- Tag: `v3.1.1`
- Nome: 3.1.1
- Publicada em: 2026-03-08
- Release anterior (cronológica): `v3.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  Add additional information to the cache stats
-  Fix example in README
-  Fix ambiguity comparing against usize
-  Example of derived Key and Value
-  Bump dependencies: pyo3, rusqlite, rand
-  Fix panic inserting into fixed size key table
-  Update changelog
-  Bump version to 3.1.1

### Release 4

Link: https://github.com/cberner/redb/releases/tag/v4.0.0
- Tag: `v4.0.0`
- Nome: 4.0.0
- Publicada em: 2026-04-02
- Release anterior (cronológica): `v3.1.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  Remove Legacy type
-  Add Drop impl to AccessGuardMutInPlace
-  Add Drop impl to AccessGuardMut
-  Add a lifetime to PageMut
-  Update changelog
-  Bump version to 4.0.0

### Release 5

Link: https://github.com/cberner/redb/releases/tag/v4.3.0
- Tag: `v4.3.0`
- Nome: 4.3.0
- Publicada em: 2026-09-15
- Release anterior (cronológica): `v4.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 93

-  Store minimal key separators in branch nodes
-  Store minimal key separators for string keys
-  Update AGENTS.md
-  Reserve the repair commit's transaction id in check_integrity()
-  Stop read cursors from resuming past an unreadable page
-  Poison the transaction when a savepoint restore or catalog change fails partway
-  Take the file lock in the fallback file backend
-  Reclaim pages leaked by a write transaction dropped during a panic
-  Return a Cow from Key::separator()
-  Fail zero-byte writes on Windows instead of retrying forever
-  Stop derived Value implementations shadowing the struct's lifetimes
-  Make renaming a table to its current name a no-op
-  Keep savepoint bookkeeping from making the transaction savepoint-ineligible
-  Remove unnecessary code from benchmark
-  Shorten separators for Option keys
-  Split the benchmarks that compare against other engines into their own crate
-  Require a separator to be an encoding of the key type
-  Add Key::min_encoded_key()
-  Expose the io module whenever experimental-api-5 is enabled
-  Stop InMemoryBackend's Debug from printing the database
-  Fix broken doc links in the savepoint methods
-  Shorten separators for array keys
-  Shorten separators for tuple keys
-  Update design doc with design of multiprocess database access
-  Update multi-process design to a single file with range locks
-  Hold the multi-process byte ranges in the existing open modes
-  Simplify multi-process cache invalidation
-  Update multi-process design for Immutable mode protocol
-  Drop the whole-file lock where it shares a namespace with the ranges
-  Give the backends a locking interface of their own
-  Give Windows the byte-range locks it has always had
-  Take the range locks alone under the redb 5 API
-  Move file locking to core instead of the backend
-  Add the concurrency modes and the mode bytes they announce
-  Lock the header while a shared-mode process reads or writes it
-  Hold the writer byte for the duration of a write transaction
-  Hold a savepoint's transaction with a TransactionGuard
-  Refactor read transaction reference counting
-  Lock the active transaction a read transaction is reading
-  Read and lock a transaction under one header hold
- ... e mais 53 commits
