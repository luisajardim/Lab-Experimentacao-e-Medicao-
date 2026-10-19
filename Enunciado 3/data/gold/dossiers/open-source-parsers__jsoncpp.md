# open-source-parsers/jsoncpp

Repositório: https://github.com/open-source-parsers/jsoncpp

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/open-source-parsers/jsoncpp/releases/tag/0.10.4
- Tag: `0.10.4`
- Nome: minor bug fix
- Publicada em: 2015-07-12
- Release anterior (cronológica): `0.10.2-p1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 38

-  [Documentation][Markdown] Use correct help option for cmake.
-  make the unix make example work
-  fix compile error on android
-  Merge pull request #277 from gogo40/master
-  Merge pull request #275 from stefan-it/stefan/cmake-generator-fix
-  Fix custom includedir & libdir substitution in pkg-config
-  Clarify which parts of README for users vs devs
-  Merge pull request #280 from mgorny/pkg-config-fix
-  Merge pull request #282 from keithkml/patch-1
-  Merge pull request #276 from bmyerz/master
-  Merge pull request #291 from cdunn2001/0.y.z
-  fix doxybuild.py for Windows
-  Merge branch 'master' into 0.y.z
-  fix ,/. problem in reader
-  Merge pull request #294 from cdunn2001/master
-  Merge remote-tracking branch 'up/master' into 0.y.z
-  fix appveyor 32-bit windows build
-  Merge pull request #306 from cdunn2001/0.y.z
-  GCC warning removal for long long
-  Gcc warning unused "tokenStart"
-  Merge pull request #307 from cdunn2001/gaurav-fix-warnings
-  Allow an optional suffix on the debug library name in CMake.
-  Warn about implicit 64 to 32 bit conversions when using clang
-  Fix #296: Explicitly cast size_t results to unsigned when needed
-  Fix undefined name "sys"
-  0.10.3
-  Merge pull request #308 from cdunn2001/0.y.z
-  dockerize the Travis build
-  valgrind in Travis
-  gcc-4.6, clang-3.3
-  Merge pull request #310 from cdunn2001/0.y.z
-  -Wshadow
-  fix some warnings
-  fixed a bug found by -Wshadow
-  -Werror
-  0.6.4
-  Merge pull request #315 from cdunn2001/0.y.z
-  gcc-4.6 in Travis

### Release 2

Link: https://github.com/open-source-parsers/jsoncpp/releases/tag/0.10.5
- Tag: `0.10.5`
- Nome: Expose Exception classes
- Publicada em: 2015-07-23
- Release anterior (cronológica): `0.10.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 32

-  Allow an optional suffix on the debug library name in CMake.
-  Merge pull request #295 from martyngigg/master
-  fix appveyor 32-bit windows build
-  Merge pull request #303 from cdunn2001/appveyor-14.0
-  Warn about implicit 64 to 32 bit conversions when using clang
-  Fix #296: Explicitly cast size_t results to unsigned when needed
-  Merge pull request #304 from cdunn2001/297
-  Fix undefined name "sys"
-  Merge pull request #305 from cdunn2001/fix-fixeol-undefined-name-sys
-  minor doc fix, for #302
-  1.6.3
-  dockerize the Travis build
-  valgrind in Travis
-  Merge pull request #309 from cdunn2001/master
-  gcc-4.9, clang (3.0)
-  Merge pull request #312 from cdunn2001/master
-  -std=c++11 for gcc builds too
-  Merge pull request #313 from cdunn2001/master
-  auto-generated file with minor update
-  -Wconversion
-  drop -Wsign-conversion
-  fix some warnings
-  fixed a bug found by -Wshadow
-  -Werror
-  1.6.4
-  Merge pull request #314 from cdunn2001/master
-  Update json_tool.h
-  Merge pull request #316 from filipjs/master
-  correction for #316
-  Exceptions declared in header
-  1.6.5
-  merged from 1.6.5

### Release 3

Link: https://github.com/open-source-parsers/jsoncpp/releases/tag/1.7.2
- Tag: `1.7.2`
- Nome: Fix a clang warning
- Publicada em: 2016-03-25
- Release anterior (cronológica): `1.7.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  Fix a clang warning
-  Merge pull request #452 from cdunn2001/fix-451
-  1.7.2 <- 1.7.1

### Release 4

Link: https://github.com/open-source-parsers/jsoncpp/releases/tag/1.8.4
- Tag: `1.8.4`
- Nome: Minor fixes; update docs
- Publicada em: 2017-12-20
- Release anterior (cronológica): `1.8.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 41

-  Fixed swiched parameters in install
-  Fixed compile bug
-  Merge pull request #660 from SloCompTech/master
-  Try adding python-3.5 in TravisCI
-  Do not write to stderr
-  Merge pull request #667 from cdunn2001/foo
-  Generated new footer.html
-  Generated new header.html
-  Update header.html
-  rsync less
-  Drop timestamp from HTML doxygen
-  Link classes and namespace
-  Drop TITLE from Doxygen docs
-  Update writer.h
-  More VS warning prevention
-  Merge pull request #669 from cdunn2001/avoid-redundant-depreciation-warnings
-  Try Travis support suggestion for py3
-  Merge pull request #670 from cdunn2001/fix-travis
-  Add value_type to improve integration with boost
-  Merge pull request #675 from wolframroesler/patch-1
-  Use move ctor in append()
-  Merge pull request #678 from open-source-parsers/append-move
-  Fix unknown pragma warnings with clang
-  Fix meson.build to allow using jsoncpp as a subproject
-  Merge pull request #680 from jasonszang/master
-  Merge pull request #679 from hughbe/clang-warnings
-  Use non-deprecated removeMember()
-  Serialize UTF-8 string with Unicode escapes (#687)
-  Un-deprecate removeMember overloads, return void (#693)
-  Add comment to README giving instructions on how to install to a directory other than /usr/local (#694)
-  rm unused func
-  MSVC warning fixes in tests
-  Merge pull request #699 from MarcelRaad/msvc_warnings
-  Suppress implicit-fallthrough warnings from GCC 7 (#697)
-  Spelling (#703)
-  Fix sign mismatch in `valueToString`
-  Merge pull request #707 from remyjette/valuetostring-sign-mismatch
-  Allow Json::Value to be used in a boolean context (#695)
-  pyenv install (#713)
-  replace code point in range(0xD800, 0xDFFF) to replacement mark (#714)
- ... e mais 1 commits

### Release 5

Link: https://github.com/open-source-parsers/jsoncpp/releases/tag/1.9.7
- Tag: `1.9.7`
- Nome: 1.9.7: Bugfixes, build system cleanups
- Publicada em: 2026-03-19
- Release anterior (cronológica): `1.9.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 50

-  Fixes PreventInSourceBuilds.cmake to work with add_subdirectory (#1383)
-  json_value.cpp bug in the edges of uint/int (#1519)
-  Release 1.9.6 and move versions to 1.9.7 (#1566)
-  Fix deallocate for working on old compiers (#1478)
-  Fix typo in JSONCPP_USE_SECURE_MEMORY vs JSONCPP_USING_SECURE_MEMORY (#1567)
-  fix(build): remove `check_required_components` for meson build (#1570)
-  the cgi module was removed from Python3.13 (#1578)
-  Fix name of static library when targeting MinGW. (#1579)
-  Fix comparison warnings caused by 54fc4e2 (#1575)
-  Drop pre-C++11 alternatives (#1593)
-  feat: support std::string_view in Value API (#1584)
-  Added Value::findType with String key (#1574)
-  Set up for Bazel module builds. (#1597)
-  Add a BUILD.bazel file for //example. (#1602)
-  Fix "include what you use" issue (#1625)
-  Make the build configuration under Bazel more correct. (#1600)
-  Add Bazel tests (#1601)
-  Return false in Reader::readValue when stack limit is exceeded (#1619)
-  Remove deprecated/removed clang-tidy key AnalyzeTemporaryDtors (#1614) (#1615)
-  [docs] Consuming JSONCpp via Conan package manager (#1622)
-  Cleanup README.md, fix broken link. (#1633)
-  Add gcovr.cfg to fix CI coverage merge errors (#1635)
-  Remove build directory exclusion from gcovr config (#1640)
-  Add workflow for version bumping
-  Add version-bump workflow configuration
-  Rename version-bump.yml to update-project-version.yml
-  Refactor version bump workflow for clarity and functionality
-  Rename workflow and update descriptions
-  Enhance version update workflow with input validation
-  Update version input descriptions and handling
-  Update version descriptions and improve sed commands
-  Update versioning logic in workflow configuration
-  Update versioning in update-project-version.yml
-  Clarify version update comments in workflow script
-  Add test for allowDroppedNullPlaceholders (#1648)
-  prevent test colision when running in parallel via RESOURCE_LOCK (#1637)
-  fixup project version updater (#1649)
-  Update README with project status and focus (#1639)
-  Adding a cmake option to exclude the jsoncpp files from install. (#1596)
-  Change stack depth limit to 256 (#1657)
- ... e mais 10 commits
