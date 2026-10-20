# guhcostan/mac-cleaner-cli

Repositório: https://github.com/guhcostan/mac-cleaner-cli

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/guhcostan/mac-cleaner-cli/releases/tag/v1.0.0
- Tag: `v1.0.0`
- Nome: v1.0.0
- Publicada em: 2025-12-04
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/guhcostan/mac-cleaner-cli/releases/tag/v1.1.0
- Tag: `v1.1.0`
- Nome: v1.1.0
- Publicada em: 2025-12-04
- Release anterior (cronológica): `v1.0.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 20

-  docs: update README to emphasize usage with npx, clarify installation options, and improve command examples
-  chore: remove ESLint configuration file and update dependencies; refactor inquirer usage to @inquirer/prompts in clean command
-  chore: update vitest configuration to increase branch coverage threshold to 80; add tests for Xcode Archives scanning and enhance Docker and Homebrew scanners with additional functionality and error handling
-  refactor: streamline test implementations by replacing child_process.exec with mockExecAsync in Docker, Homebrew, and other scanners; add new tests for nested directory scanning and permission handling in LargeFilesScanner
-  chore: remove package-lock.json; update Node.js engine requirement to >=20 in package.json; adjust CI workflow to target Node.js versions 20 and 22
-  feat: add uninstall and config commands; enhance backup management; introduce progress options for scan and clean commands; update version to 1.1.0
-  test: enhance category and scanner tests by adding 'node-modules' and 'duplicates'; update mock implementations for scanner retrieval
-  test: add mock implementation for removeItems in duplicates and node-modules scanner tests
-  chore: update README for improved clarity on usage and installation; streamline CLI commands for better user experience; bump version to 1.1.0
-  test: enhance uninstall, duplicates, node-modules, and backup utilities tests with additional scenarios and mock implementations
-  test: simplify NodeModulesScanner tests by removing unnecessary variable assignments in scan and clean methods
-  test: remove unnecessary variable assignment in DuplicatesScanner test for cleaner code
-  test: streamline DuplicatesScanner test by removing unnecessary variable assignment and verifying scan result directly
-  test: enhance uninstall and duplicates scanner tests with additional scenarios and improved mock implementations
-  test: remove unused import in DuplicatesScanner tests for cleaner code
-  test: add additional files to coverage exclusions in vitest configuration for improved test accuracy
-  test: improve DuplicatesScanner and NodeModulesScanner tests with enhanced mock implementations and additional scenarios
-  test: refine backup utilities tests by improving mock implementations, enhancing scenarios, and ensuring proper cleanup
-  ci: update CLI command in CI workflow from 'scan --list' to 'categories' for improved functionality
-  test: remove unused type import in dns-cache tests for cleaner code

### Release 3

Link: https://github.com/guhcostan/mac-cleaner-cli/releases/tag/v1.1.1
- Tag: `v1.1.1`
- Nome: v1.1.1 - Fix parallel scanner execution
- Publicada em: 2025-12-04
- Release anterior (cronológica): `v1.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  fix: parallel scanner execution losing results

### Release 4

Link: https://github.com/guhcostan/mac-cleaner-cli/releases/tag/v1.1.6
- Tag: `v1.1.6`
- Nome: v1.1.6
- Publicada em: 2025-12-05
- Release anterior (cronológica): `v1.1.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  chore: add new line for consistency in multiple files
-  chore: migrate to Bun as package manager and runtime
-  ci: update workflow to use Bun

### Release 5

Link: https://github.com/guhcostan/mac-cleaner-cli/releases/tag/v1.1.8
- Tag: `v1.1.8`
- Nome: v1.1.8 - Fix Node.js version requirement
- Publicada em: 2025-12-10
- Release anterior (cronológica): `v1.1.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 13

-  chore: add CodeQL security analysis workflow
-  docs: update README to include Windows availability
-  chore: migrate from tsup to tsdown
-  fix: mock child_process in maintenance tests to avoid sudo timeout
-  Delete TODO.md
-  Delete package-lock.json
-  chore(deps): bump github/codeql-action from 3 to 4
-  Merge pull request #20 from guhcostan/dependabot/github_actions/github/codeql-action-4
-  Merge pull request #17 from edgarberlinck/main
-  feat: change category selection to opt-in instead of opt-out
-  fix(ci): update CLI test to use .mjs extension
-  fix: add engines field requiring Node.js 20.12.0+ to fix 'Unexpected token with' error
-  v1.1.8 - Fix Node.js version requirement
