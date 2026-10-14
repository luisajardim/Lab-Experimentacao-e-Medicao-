# cakephp/cakephp

Repositório: https://github.com/cakephp/cakephp

## Metadados

- Linguagem: PHP

## Releases sorteadas

### Release 1

Link: https://github.com/cakephp/cakephp/releases/tag/3.0.8
- Tag: `3.0.8`
- Nome: CakePHP 3.0.8 released
- Publicada em: 2015-06-28
- Release anterior (cronológica): `2.7.0-RC`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Renamed the app folder
-  Renamed the test app folder
-  Renamed the test case folder
-  Updated cake base files
-  Updated Cache folder
-  Updated Config folder
-  Updated Configure folder
-  Updated Console folder
-  Updated Controller folder
-  Updated Core folder
-  Updated Error folder
-  Updated Event folder
-  Updated I18n folder
-  Updated Log folder
-  Updated Model folder
-  Updated Network folder
-  Updated Routing folder
-  Updated Utility folder
-  Updated View folder
-  Updated TestSuite folder
-  Update test fixture folder
-  Update test case files folder
-  Update test case Cache folder
-  Update test case Configure folder
-  Update test case Console folder
-  Update test case Controller folder
-  Renaming CakePlugin test case
-  Update test case Core folder
-  Update test case Error folder
-  Update test case Event folder
-  Update test case I18n folder
-  Update test case Log folder
-  Update test case Model folder
-  Renaming Cake* files in network test case
-  Update test case Network folder
-  Update test case Routing folder
-  Update test case TestSuite folder
-  Update test case Utility folder
-  Update test case View folder
-  Renamed some files from TestApp
- ... e mais 210 commits

### Release 2

Link: https://github.com/cakephp/cakephp/releases/tag/3.3.10
- Tag: `3.3.10`
- Nome: CakePHP 3.3.10 released
- Publicada em: 2016-12-12
- Release anterior (cronológica): `2.9.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Mark belongsTo and count queries as not primary too.
-  Update Query::$primary and Query::primary() names.
-  More CS and doc fixes
-  Use more durable assertion.
-  Datetime tests in MySQL will return the time portion as well.
-  On some machines the de_DE locale is full of lies.
-  Merge branch '2.5' into 3.0
-  Merge pull request #3028 from ADmad/3.0
-  Plain entities cannot be used at this point as root in FormHelper
-  Marking entities with information containing the table they come from
-  More work towards marking entities with their source
-  Fixing some failing tests
-  Marking entities on save and fixing more tests
-  Unit testing Entity after adding the source() method
-  Adding test to Marshaller for showing that it adds the entity source
-  Small refactoring
-  Making EntityContext more intelligent by reading the entity source
-  Fixed failing test that was brought from 2.5 code
-  Make Request::addDetector() static.
-  Making Entity::source() just a string
-  Remove "mobile" detector.
-  Starting to make the base entity's properties accessible by default
-  Udating tests after chaing the accessible properties in Entity
-  Prevent HTML error pages being spewed in case of errors generated while running tests.
-  Merge pull request #3032 from cakephp/3.0-accessible-entity
-  Merge pull request #3034 from ADmad/3.0-cli-error
-  Re-implement fixtures in directories.
-  Check `validate` option before validating
-  Merge pull request #3035 from cakephp/3.0-fixture-dirs
-  Merge pull request #3025 from cakephp/3.0-validation-custom-messages
-  Fixing some refactoring artifacts
-  Merge pull request #3030 from cakephp/3.0-entity-context-fixes
-  Fix failing test case for `validate` option
-  Fix failing test.
-  Merge pull request #3036 from tigrang/bug-fix-validate
-  Make debug status boolean
-  Use semantic version for since doc block
-  Update ObjectRegistry since docblock to sem ver
-  Fix typo in method name.
-  Merge pull request #3046 from bcrowe/3.0-src-ver
- ... e mais 210 commits

### Release 3

Link: https://github.com/cakephp/cakephp/releases/tag/4.2.3
- Tag: `4.2.3`
- Nome: CakePHP 4.2.3 released
- Publicada em: 2021-01-25
- Release anterior (cronológica): `3.9.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Start 4.x branch.
-  Attempt to update appveyor build script for PHP 7.2
-  Change default return value of ServerRequest::getParam() to false.
-  Don't set session cookie name to CAKEPHP by default.
-  Move templates from "src/Template" to "templates".
-  Changes extension of templates files to ".php"
-  remove old classes for phpunit < 6
-  Prevent phpcs from running on template files.
-  Merge pull request #11930 from cakephp/issue-11584
-  Update extension version numbers.
-  Merge pull request #11929 from cakephp/4.x-request-getparam
-  Update php requirements for cache subsplit.
-  Remove deprecated code in Cache package.
-  Remove deprecated code in Collection package
-  Merge pull request #11933 from cakephp/phpunit6
-  Fix tests not running in 7.1
-  Merge branch '3.next' into 4.x
-  Fix error.
-  Remove phpstan warnings that no longer exist.
-  Merge pull request #11937 from cakephp/cache-deprecation
-  Add BaseType class.
-  Convert Database\Type to factory class.
-  Fix typehints and docblocks.
-  Fix test case.
-  Add Type::getMap().
-  Fix test case.
-  Remove unneeded base class check.
-  Use new method.
-  Remove deprecate and unused methods.
-  Merge branch 'master' into 4.x
-  add 4.x branch into appveyor
-  Merge pull request #11975 from cakephp/4.x-db-type
-  Merge branch '3.next' into 4.x
-  Remove dead code.
-  Use Type::getMap() as getter for individual types too.
-  Add Type::setMap() for setting complete map.
-  Removed unneeded "use" statements.
-  Fix docblock.
-  Fix typehint.
-  Update methods calls.
- ... e mais 210 commits

### Release 4

Link: https://github.com/cakephp/cakephp/releases/tag/3.9.10
- Tag: `3.9.10`
- Nome: CakePHP 3.9.10 released
- Publicada em: 2021-05-31
- Release anterior (cronológica): `4.2.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Fix trace/context for errors wrapped by debug kit
-  Update MockBuilder.php
-  Merge pull request #14098 from cakephp/3.x-mockbuilder
-  Add test cases to demonstrate issue 13666
-  Fix dirty associations that use formatResults
-  Remove tests that weren't failing before the fix.
-  Merge pull request #14107 from cakephp/bug/translate-dirty-parent
-  Added 4.x backport for Client/Response->isSuccess() and tests.
-  Added 4.x backport for CspMiddleware and tests.
-  Merge pull request #14121 from Tiborhajos/ticket-13493-backport-response-is-success
-  Fixed version comment and a typo in CspMiddleWare.
-  Merge pull request #14090 from cakephp/fix-debug-kit-trace
-  Merge pull request #14122 from Tiborhajos/ticket-13493-backport-csp-middleware
-  Align frame offset key to what debugkit is using.
-  Fix tests.
-  Only try to clean entities
-  Merge pull request #14133 from Zuluru/3.x
-  Don't map() when we don't need to.
-  Merge pull request #14134 from cakephp/optimize-association-format
-  Fixed contain() BelongsToMany association restricting fields with 'fields' option
-  Fix element cache key generation.
-  Remove PHP7 syntax from backport.
-  Fix failing tests from 4.x backport
-  Backport from 4.x: Fix docblocks around bool false.
-  Backport from 4.x: Typos and exceptions.
-  Backport from 4.x
-  Merge pull request #14154 from cakephp/3.x-docblocks
-  Correct & clarify length parameter of File::read()
-  Skip writing POT file if not changed
-  Merge pull request #14170 from cakephp/3.x-file-read-length-param
-  Only check for existing files
-  Check if password hasher is called exactly once in all cases.
-  Remove typehints.
-  Fix Notice Error: Trying to access array offset on value of type null
-  Merge pull request #14173 from cakephp/3.x-i18n-extract-skip-unchanged
-  Always use / as fallback layout title
-  Merge pull request #14195 from cakephp/3.next-default-title
-  Use substr and string cast instead.
-  Merge pull request #14181 from cakephp/3.x-assetUrl-null-path
-  Update version number to 3.8.9
- ... e mais 210 commits

### Release 5

Link: https://github.com/cakephp/cakephp/releases/tag/5.0.2
- Tag: `5.0.2`
- Nome: CakePHP 5.0.2
- Publicada em: 2023-10-29
- Release anterior (cronológica): `4.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Require php 8.0 and bump package dependency versions to 5.0
-  Re-generate php 8 phpstan baseline
-  Re-generate php 8 psalm baseline
-  Merge pull request #15591 from cakephp/require-php8
-  Merge branch '4.next' into 5.0
-  Update version to 5.0.0-dev
-  Remove deprecated AuthComponent and related files.
-  Merge pull request #15599 from cakephp/remove-authcomponent
-  Update return types.
-  Merge pull request #15600 from cakephp/5.0-stan
-  Remove deprecated code from View package.
-  Remove database-related deprecated code
-  Remove deprecated code from Validation package
-  Merge pull request #15603 from cakephp/5.0-deprecated
-  Merge pull request #15602 from cakephp/deprecated-database
-  Remove http-related deprecated code
-  Merge pull request #15604 from cakephp/deprecated-http
-  Merge branch '4.next' into 5.0
-  Remove various deprecations
-  Remove reference to Email file
-  Merge pull request #15605 from cakephp/remove-deprecations
-  Regenerate psalm-baseline
-  Merge pull request #15607 from cakephp/regen-psalmbaseline
-  Remove deprecated shells.
-  Merge pull request #15608 from cakephp/5.0-deprecated-shells
-  Use `null` instead of `false` to disable log scopes.
-  Require array event payload
-  Update stan config/baseline.
-  Merge pull request #15612 from cakephp/5.0-stan
-  Remove deprecated syslog formatter
-  Merge pull request #15613 from cakephp/deprecated-formatter
-  Merge pull request #15611 from cakephp/event-array
-  Remove Wincache support
-  Merge pull request #15621 from cakephp/remove-wincache
-  Merge pull request #15610 from cakephp/issue-15544
-  Merge branch '4.next' into 5.0
-  Remove deprecated whitelist config
-  Remove deprecated underscored special view vars
-  Merge pull request #15625 from cakephp/deprecated-viewvars
-  Merge pull request #15624 from cakephp/paginator-whitelist
- ... e mais 210 commits
