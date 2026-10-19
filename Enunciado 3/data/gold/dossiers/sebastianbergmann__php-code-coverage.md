# sebastianbergmann/php-code-coverage

Repositório: https://github.com/sebastianbergmann/php-code-coverage

## Metadados

- Linguagem: PHP

## Releases sorteadas

### Release 1

Link: https://github.com/sebastianbergmann/php-code-coverage/releases/tag/11.0.6
- Tag: `11.0.6`
- Nome: phpunit/php-code-coverage 11.0.6
- Publicada em: 2024-08-22
- Release anterior (cronológica): `10.1.16`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 39

-  Start development of next major version
-  Remove support for PHP-Parser 4
-  Use attributes
-  Use willReturn() instead of deprecated will(onConsecutiveCalls())
-  Update Psalm baseline
-  PHP-Parser 5 requires the ctype extension
-  Remove deprecated functionality
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Prepare release
-  Do not use implicitly nullable parameters and prepare release
-  Merge branch '10.1'
-  Prepare release
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Prepare release
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Update PHPUnit configuration
-  Do not use $class['package'] element (and its sub-elements)
-  Use PHPStan instead of Psalm
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Merge branch '10.1'
-  Update ChangeLog
-  Merge branch '10.1'
-  Prepare release
-  Prepare release
-  Update badge URL
-  Merge branch '10.1'
-  Update Codecov.io action(s)
-  Merge branch '10.1'
-  Prepare release

### Release 2

Link: https://github.com/sebastianbergmann/php-code-coverage/releases/tag/12.3.0
- Tag: `12.3.0`
- Nome: phpunit/php-code-coverage 12.3.0
- Publicada em: 2025-05-23
- Release anterior (cronológica): `12.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 31

-  Sync with CONTRIBUTING.md and CODE_OF_CONDUCT.md from sebastianbergmann/phpunit
-  Use CoversClassesThatExtendClass attribute
-  Make it obvious the code in the SebastianBergmann\CodeCoverage\Node namespace is currently not tested specifically
-  Ignore I/O error paths
-  Remove superfluous code
-  Also test the is-cached path
-  Add test
-  Revert "Make it obvious the code in the SebastianBergmann\CodeCoverage\Node namespace is currently not tested specifically"
-  Download https://raw.githubusercontent.com/openclover/clover/refs/tags/openclover-4.5.2/clover-core/src/main/resources/clover.xsd
-  Validate generated Clover XML against Clover XSD
-  Set clover attribute of <coverage> element to version identifier for phpunit/php-code-coverage
-  Perform validation after comparison with expectation
-  Remove superfluous type annotation
-  Make <metrics> element the first child of <project> and <file>
-  Set both name and path attributes on the <file> element
-  Rename method to reflect that we assert before we validate
-  Generate <package> element for global namespace
-  Ignore <testproject> for now, see https://github.com/sebastianbergmann/php-code-coverage/pull/1080#issuecomment-2900005969
-  Set complexity attribute on the <metrics> element under <project>
-  Narrow type
-  - Use consistent order for attributes on <metrics> elements
-  Remove namespace attribute from <class> element
-  Remove name and crap attributes from <line> element
-  Fix CS/WS issue
-  Set signature attribute on the <line> element (and reorder attributes to match XSD)
-  Set attributes of <metrics> element under <package> to actual values
-  Set attribute name of <class> element to unqualified class name
-  Keep Report\Clover as-is and introduce new Report\OpenClover for reporter that generates Clover XML that validates against OpenClover's XML schema definition
-  Reorganize
-  Bump
-  Prepare release

### Release 3

Link: https://github.com/sebastianbergmann/php-code-coverage/releases/tag/14.2.4
- Tag: `14.2.4`
- Nome: phpunit/php-code-coverage 14.2.4
- Publicada em: 2026-07-30
- Release anterior (cronológica): `14.2.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  Do not share a static analysis result cache between differently configured CodeCoverage objects
-  Prepare release

### Release 4

Link: https://github.com/sebastianbergmann/php-code-coverage/releases/tag/14.3.3
- Tag: `14.3.3`
- Nome: phpunit/php-code-coverage 14.3.3
- Publicada em: 2026-09-10
- Release anterior (cronológica): `14.3.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  Update dependency phpstan/phpstan to ^2.2.13
-  Update dependency phpunit/phpunit to ^13.3.3
-  Update tools
-  Closes #1314
-  Prepare release

### Release 5

Link: https://github.com/sebastianbergmann/php-code-coverage/releases/tag/12.5.8
- Tag: `12.5.8`
- Nome: phpunit/php-code-coverage 12.5.8
- Publicada em: 2026-10-03
- Release anterior (cronológica): `14.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Update dependency phpunit/phpunit to ^12.5.37
-  Merge the tests of another CodeCoverage instance into the ones merged so far in place instead of merging both into a new array, which made merging the code coverage of many processes quadratic
-  Update dependency phpunit/php-text-template to ^5.0.1
-  Prepare release
