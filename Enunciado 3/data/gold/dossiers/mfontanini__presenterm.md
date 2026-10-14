# mfontanini/presenterm

Repositório: https://github.com/mfontanini/presenterm

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/mfontanini/presenterm/releases/tag/v0.2.1
- Tag: `v0.2.1`
- Nome: (sem nome)
- Publicada em: 2023-10-18
- Release anterior (cronológica): `0.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 10

-  Add link to layouts docs in features section
-  Add notes on enabling sixel support
-  Change wording in README
-  feat(ci,profiles): use github actions to release automated binaries // cargo profiles to test,bench,release binaries
-  feat(releaser): script to ease releasing process
-  feat(splash): show splashes if no args were provided
-  chore(clap-deps):use string feature to display splashes
-  Merge pull request #5 from pwnwriter/master
-  Add changelog
-  Bump version to 0.2.1

### Release 2

Link: https://github.com/mfontanini/presenterm/releases/tag/v0.4.0
- Tag: `v0.4.0`
- Nome: v0.4.0
- Publicada em: 2023-12-16
- Release anterior (cronológica): `v0.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 57

-  Update information on using the Nix package
-  Merge pull request #63 from MikaelFangel/patch-1
-  Pull in all of bat's syntect themes
-  Merge pull request #67 from mfontanini/more-themes
-  Reset colors before setting colors to respect terminal
-  Add support for named terminal colors
-  Add terminal dark/light themes
-  Merge pull request #68 from mfontanini/terminal-themes
-  Don't allow no background/foreground colors on PDF export
-  Merge pull request #69 from mfontanini/no-background-pdf
-  Allow providing custom syntect themes
-  Merge pull request #71 from mfontanini/custom-syntect-themes
-  Load themes under ~/.config/presenterm/themes
-  Merge pull request #73 from mfontanini/custom-themes
-  Create container for all themes
-  Create container for highlighting themes
-  Load default theme from dotfile
-  Merge pull request #74 from mfontanini/custom-configs
-  Allow rendering typst/latex formulas
-  Merge pull request #75 from mfontanini/render-formulas
-  Adjust themes' colors for typst rendering
-  Merge pull request #76 from mfontanini/formula-colors
-  Add syntax highlighting for nix
-  Generate PDF replacement images in presenterm directly
-  Merge pull request #79 from mfontanini/pdf-image-revamp
-  Merge pull request #78 from GaetanLepage/nix
-  Add script to verify bat assets
-  Fill shellcheck warnings for bat/update.sh
-  Add workflow to verify bat assets hash
-  Merge pull request #80 from mfontanini/verify-bat
-  Unify third party tool invocation
-  Validate the minimum presenterm-exporter version is installed
-  Merge pull request #81 from mfontanini/verify-exporter-version
-  Add syntax highlighting for diff
-  Fix typo in update.sh shebang
-  Merge pull request #82 from rmartine-ias/add-diff-syntax
-  Merge pull request #83 from rmartine-ias/patch-1
-  Edd .editorconfig for *.sh and format shell scripts
-  Merge pull request #85 from mfontanini/shfmt
-  Add comment command to jump to vertical middle
- ... e mais 17 commits

### Release 3

Link: https://github.com/mfontanini/presenterm/releases/tag/v0.8.0
- Tag: `v0.8.0`
- Nome: v0.8.0
- Publicada em: 2024-07-29
- Release anterior (cronológica): `v0.7.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 148

-  Update deps
-  Revert "Update deps"
-  feat(ruby-code-highlighting): added support for ruby code highlighting
-  Merge pull request #226 from pranavrao145/feat/ruby-code-highlighting
-  Allow having multiple authors
-  Merge pull request #227 from mfontanini/multiple-authors
-  chore(config): include strict_front_matter_parsing in default config
-  docs: CHANGELOG.md contains clickable links to issues
-  Merge pull request #230 from mikavilpas/changelog-includes-links-to-issues
-  Merge pull request #229 from mikavilpas/include-strict-front-matter-parsing-in-config
-  refactor: fix all clippy warnings
-  Merge pull request #231 from mikavilpas/fix-warnings
-  feat(config): generate JSON schema for the configuration file
-  Merge pull request #228 from mikavilpas/configuration-json-schema
-  Allow using image paths in typst
-  Rename schema.json to config-file-schema.json
-  Merge pull request #235 from mfontanini/typst-image-paths
-  Add script to validate config file schema
-  Run config file schema validation in CI
-  Point sample config file's YAML LSP schema to github
-  Merge pull request #236 from mfontanini/validate-config-file-schema
-  Allow explicitly disabling footer in certain slides
-  Merge pull request #239 from mfontanini/disable-footer
-  feat: allow jumping fast between slides
-  Merge pull request #244 from mfontanini/feat/jump-fast
-  fix: display background color behind '\t' in code exec output
-  Merge pull request #245 from mfontanini/fix/execution-style-tabs
-  chore: remove nix cache in CI
-  Merge pull request #246 from mfontanini/chore/remove-nix-cache
-  docs: Update install instructions for Arch Linux
-  Merge pull request #248 from orhun/docs/update_arch_instructions
-  chore: update dependencies
-  Merge pull request #249 from mfontanini/chore/update-dependencies
-  fix(code-exec): wait for code execution process to exit completely
-  Merge pull request #250 from dmackdev/fix/wait-for-code-exec-process-to-exit
-  include stderr output with os_pipe crate
-  add code execution examples to code.md presentation
-  add sleeps to stderr code example
-  read output line by line
-  remove man command from test since output is OS dependent
- ... e mais 108 commits

### Release 4

Link: https://github.com/mfontanini/presenterm/releases/tag/v0.11.0
- Tag: `v0.11.0`
- Nome: v0.11.0
- Publicada em: 2025-03-08
- Release anterior (cronológica): `v0.10.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 88

-  docs: fix code to image conversion example
-  docs: restructure docs mdbook
-  docs: restructure docs mdbook (#436)
-  docs: link speaker notes example
-  docs; fix latex image link
-  feat: add support for kitty's font size spec
-  docs: add redirects from old routes
-  docs: move notes around external code highlighting via bat
-  feat: add support for kitty's font size protocol (#438)
-  perf: avoid cloning strings when styling them
-  perf: avoid cloning strings when styling them (#440)
-  chore: use fastrand instead of rand
-  chore: don't pull in getrandom via tempfile
-  chore: remove `rayon` feature in `image`
-  chore: use fastrand instead of rand (#441)
-  feat!: sanitize theme footer
-  feat!: sanitize theme footer's templates (#442)
-  chore: create trait out of `Terminal`
-  chore: add tests for margins/columns handling in engine
-  chore: restructure `Terminal` code and add test for margins/layouts (#443)
-  fix: don't squash image if font is not 2:1
-  fix: don't squash image if font is not 2:1 (#446)
-  feat: add support for wikilinks
-  feat: add support for wikilinks (#448)
-  feat: support images in footer
-  feat: support images in footer (#450)
-  Update introduction.md
-  Update introduction.md (#451)
-  chore: bump sixel-rs version
-  chore: bump sixel-rs version (#452)
-  fix: don't err if auto_render_languages isn't set
-  fix: don't err if auto_render_languages isn't set (#454)
-  chore: add release notes for 0.10.1
-  fix: don't get stuck if tmux doesn't passthrough
-  fix: don't get stuck if tmux doesn't passthrough (#456)
-  docs: mention tmux passthrough in docs
-  feat: allow specifying font size in comment command
-  feat: allow specifying font size in comment command (#458)
-  fix: respect lists that start at non 1 indexes
-  fix: respect lists that start at non 1 indexes (#459)
- ... e mais 48 commits

### Release 5

Link: https://github.com/mfontanini/presenterm/releases/tag/v0.12.0
- Tag: `v0.12.0`
- Nome: v0.12.0
- Publicada em: 2025-03-25
- Release anterior (cronológica): `nightly`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 25

-  feat: allow specifying export dimensions in config file
-  ci: export PDF during merge checks
-  feat: allow specifying export dimensions in config file (#511)
-  fix: center lists correctly
-  ci: build with sixel enabled
-  fix: center lists correctly (#512)
-  ci: build with sixel enabled (#513)
-  Revert "ci: build with sixel enabled"
-  ci: revert build with sixel enabled (#514)
-  fix: respect line height when jumping lines when rendering PDF
-  fix: respect line height when jumping lines when rendering PDF (#517)
-  chore: allow specifying path for temporary export files
-  chore: allow specifying path for temporary export files (#518)
-  chore: cleanup text attributes
-  chore: cleanup text attributes (#519)
-  fix: display inline code colors when in list
-  fix: display inline code colors when in list (#520)
-  fix: respect font size in lists
-  fix: respect font size in lists (#522)
-  fix: show error if sixel mode is selected but disabled
-  fix: show error if sixel mode is selected but disabled (#525)
-  chore: add changelog notes for 0.12.0
-  chore: add docs for 0.12.0
-  chore: bump version to 0.12.0
-  chore: prepare for 0.12.0 changes (#523)
