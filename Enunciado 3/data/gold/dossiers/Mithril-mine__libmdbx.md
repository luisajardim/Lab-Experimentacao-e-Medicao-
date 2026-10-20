# Mithril-mine/libmdbx

Repositório: https://github.com/Mithril-mine/libmdbx

## Metadados

- Linguagem: C

## Releases sorteadas

### Release 1

Link: https://github.com/Mithril-mine/libmdbx/releases/tag/v0.13.10_github_workaround
- Tag: `v0.13.10_github_workaround`
- Nome: v0.13.10 "Gloss of Glory" (Блеск Славы)
- Publicada em: 2025-12-21
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/Mithril-mine/libmdbx/releases/tag/v0.13.11
- Tag: `v0.13.11`
- Nome: libmdbx v0.13.11 "A7A5" (just as Stable)
- Publicada em: 2026-01-30
- Release anterior (cronológica): `v0.13.10_github_workaround`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 19

-  mdbx: sigma note about new distribution approach.
-  mdbx: add `COPYRIGHT` file to the distribution (backport).
-  mdbx-cmake: hotfix of build error due two version info sources (backport).
-  mdbx: backport fixes from the `master` branch.
-  mdbx: avoid using `ERROR_UNHANDLED_ERROR` on Windows (backport).
-  mdbx: explicitly clearing dbi-handles opened inside an aborted nested transaction (backport).
-  mdbx: provide initial `ut_and_examples` within a distribution (backport).
-  mdbx-doc: clarification and addition of documentation (v0.13.10-23-g1ee6a154).
-  mdbx: add public-visible CI on Github (backport).
-  mdbx: adding packages and the minimal C++ API example (v0.13.10-36-g834438ea).
-  mdbx++: workaround for MinGW build failures (v0.13.10-37-g3d10d4df).
-  mdbx-doc: add link to NodeJS bindings and update ChangeLog (v0.13.10-39-g12c7912f).
-  mdbx: fix extra-flush regression (v0.13.10-48-gade27cfc).
-  mdbx: avoid extra-growth of DB instead of GC-reclaiming in a rare specific cases (v0.13.10-55-g0e259437).
-  mdbx: minor fix `iov_callback4dirtypages()` for Valgrind/ASAN (v0.13.10-58-g77f8c54e).
-  mdbx: fix cursor(s) finalization after ones explicitly closed in a nested transactions (v0.13.10-62-g644ef70e).
-  mdbx-make: fix `LDFLAGS` regression for tools (v0.13.10-65-ge413d8b7).
-  mdbx-ci: add ci-script caption.
-  mdbx: release v0.13.11 "A7A5" (just as Stable).

### Release 3

Link: https://github.com/Mithril-mine/libmdbx/releases/tag/v0.13.12
- Tag: `v0.13.12`
- Nome: libmdbx v0.13.12 "Аврора" (Aurora)
- Publicada em: 2026-04-30
- Release anterior (cronológica): `v0.13.11`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 13

-  mdbx: fix counting of nested trees for multi-values/dupsort hives (v0.13.11-2-gea86a7d3).
-  mdbx: mdbx: fix dump/load tools (v0.13.11-5-gf6cf8d3f).
-  mdbx: fix `SIGSEGV` in the case when all meta pages are not entirely usable (v0.13.11-8-g7b53a155).
-  mdbx: a few fixes via github pull-requests (v0.13.11-14-ga1c58703).
-  mdbx: cutoff `packages` into the aside repository.
-  mdbx: a few fixes via github pull-requests (v0.13.11-18-gfbd7c62a).
-  mdbx-ci: cutoff CI-related stuff into the aside repository.
-  mdbx: a few minor bug fixes backported from the `master` branch.
-  mdbx: Create SECURITY.md (backport).
-  mdbx: fix minor regression in case minimal page-size and huge RAM (v0.13.11-24-g53b010b4).
-  mdbx: fix wrong/uninitialized `ms_psize` field when using `mdbx_enumerate_tables()` (backport).
-  mdbx: fix adjusting neighbor nested cursors after dupsort item deletion (v0.13.11-30-gb8bc0bb2).
-  mdbx: release v0.13.12 "Аврора" (Aurora).

### Release 4

Link: https://github.com/Mithril-mine/libmdbx/releases/tag/v0.14.2
- Tag: `v0.14.2`
- Nome: libmdbx v0.14.2 "Буревестник" (Stormy Petrel)
- Publicada em: 2026-05-14
- Release anterior (cronológica): `v0.13.12`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/Mithril-mine/libmdbx/releases/tag/v0.14.3
- Tag: `v0.14.3`
- Nome: libmdbx v0.14.3 "Китов" (Kitov)
- Publicada em: 2026-08-09
- Release anterior (cronológica): `v0.14.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 35

-  mdbx-doc: minor clarify/refine README.
-  mdbx: minor fix/refine assertions triggering in a specific scenarios of creating and renaming tables within nested transactions (v0.14.2-4-gf1208edf).
-  mdbx: minor fixes by ai suggestions (v0.14.2-8-gcfb319f8).
-  mdbx: introduce `DBI_SLAIN` for deferred closing of the dropped dbi during txn commit (v0.14.2-13-g7030afca).
-  mdbx: fix `ERROR_LOCK_VIOLATION` during defrag on Windows.
-  mdbx: support for building with Embarcadero C++ Builder.
-  mdbx: allows to use cursors binded with the same DBI, but different ro-txns, in the API with multiple cursors in a parameters (v0.14.2-224-g8f756694).
-  mdbx: set of minor refines mostly by AI suggestions.
-  mdbx: fix `env_owned_wrtxn()` to avoid by-pass locking in the `MDBX_NOSTICKYTHREADS` mode.
-  mdbx: add `MDBX_opt_presync_threshold`.
-  mdbx: code quality fixes.
-  fix: V-001 security vulnerability
-  mdbx-load: re-fix potential buffer overread by `fgets()`.
-  mdbx: set of fixes based by AI suggestions.
-  mdbx++: provide copy content for move-assignment of `mdbx::buffer` for non-equal allocators case.
-  mdbx-windows: rework/fix `MDBX_WITHOUT_MSVC_CRT=ON` for SEH.
-  mdbx: fix MDBX_opt_presync_threshold using min_unsigned() instead of max_unsigned()
-  mdbx: resource leak fixes.
-  mdbx: `mdbx_defrag` utility fixes.
-  Honor documented presync threshold maximum
-  mdbx: v0.14.3 release candidate.
-  mdbx-chk: fix wrong function name in env sync error reporting.
-  mdbx: fix mincore_cache shift to iterate from the end.
-  mdbx++: fix F4 UTF-8 continuation range to 80..8F.
-  mdbx: more fixes.
-  mdbx: fix missing headroom reservation and other cleanups.
-  mdbx: refine project directories, CI on github, set of fixes.
-  mdbx: the set of fixes.
-  mdbx: checkpoint of July bug fixing party.
-  mdbx: rework cursor's stack with introducing the `stash`.
-  mdbx: workaround MSVC C11-atomics and fix spilling internal accounting for `MDBX_AVOID_MSYNC=ON`.
-  mdbx: regression/bug in the copy-without-compaction code, which leads to produce a copy without a payload.
-  mdbx: more fix `copy_asis()` regression for case destination is a pipe.
-  mdbx-windows: fix loosing of global init and tls-destructors in static library build by MinGW toolchain in particular cases.
-  mdbx: release v0.14.3 "Китов" (Kitov).
