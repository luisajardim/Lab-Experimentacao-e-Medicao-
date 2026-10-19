# gitkraken/vscode-gitlens

Repositório: https://github.com/gitkraken/vscode-gitlens

## Metadados

- Linguagem: TypeScript

## Releases sorteadas

### Release 1

Link: https://github.com/gitkraken/vscode-gitlens/releases/tag/v8.2.0
- Tag: `v8.2.0`
- Nome: v8.2.0
- Publicada em: 2018-03-31
- Release anterior (cronológica): `v8.1.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 29

-  Updates vscode & dependencies
-  Fixes #312 - simplify date style switching
-  Fixes #314 - Toggle line annotation doesn't work
-  Fixes #310 - quote path
-  Switches to cd rather than git -C
-  Fixes #309 - comparision commands terminology
-  Fixes issue with paths that contain `.git`
-  Adds remote merge-base indicator
-  Fixes issues with image & binary files
-  Updates dependencies
-  Removes open working file when unneeded
-  Refactors current line tracking
-  Adds scrollable setting to the current line annotation
-  Fixes issue with active repo not updating
-  Adds rich tooltips to views
-  Adds notification for conflicting shortcuts
-  Updates dependencies
-  Preps v8.2.0-beta
-  Updates dependencies
-  Adds settings to the settings editor
-  Fixes backwards indicator
-  Fixes inaccurate count
-  Updates screenshots
-  Adds many new settings to the UI
-  Adds tracking branch into indicator
-  Adds history explorer
-  Fixes build issues with minification
-  Updates backers and sponsors
-  Preps v8.2.0

### Release 2

Link: https://github.com/gitkraken/vscode-gitlens/releases/tag/v8.5.1
- Tag: `v8.5.1`
- Nome: v8.5.1
- Publicada em: 2018-07-18
- Release anterior (cronológica): `v8.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 47

-  Add the gitlens.hovers.avatars configuration option
-  Adds recognition for Segev Finer's contribution
-  Adds hovers.avatars setting to the interactive settings editor
-  Updates dependencies
-  Resolves #436 - Copy to clipboard not working
-  Adds languageId to debug code lens
-  Removes "configuration" from config title
-  Prettier all-the-things
-  Renames history explorer to file history explorer
-  Adds ability to show explorers in a GitLens view
-  Fixes #442 - File status fails if name (or path) starts with -
-  Fixes issue where changed files count was wrong when behind upstream
-  Fixes issue where file history wasn't auto updated
-  Fixes issue with editor focus and compare commands
-  Fixes empty scope box
-  Fixes missing image from package
-  Updates backers
-  Update dependencies
-  Removes unneeded tslint disables
-  Closes #431 - adds tag annotations to tooltips
-  Fixes #440 - Increases max buffer to 100MB
-  Fixes issue with diff with previous and renames
-  Consolidates gitlens:active* contexts into gitlens:activeFileStatus
-  Changes file history to always be the full history
-  Fixes compare with prev/next with renames (especially case only renames)
-  Removes space before ellipsis for consistency
-  Closes #316 - Show file history from another branch or tag
-  Enables the new GitLens sidebar view by default
-  Adds alt command to compare with previous toolbar command
-  Reorders imports (via tslint) and moves some files for better structure
-  Moves getHistoryNode to History explorer
-  Preps v8.5.0
-  Replace `--` with `—` in package.json
-  Adds recognition for korigod's contribution
-  Fixes #444 - Resizes activity bar icon
-  Updates github issue templates
-  Updates dependencies
-  Replaces encoded chars with unicode (stops fighting with npm)
-  Closes #446 - Adds ability to compare arbitrary file revisions
-  Fixes refresh issue on config change
- ... e mais 7 commits

### Release 3

Link: https://github.com/gitkraken/vscode-gitlens/releases/tag/v9.0.0
- Tag: `v9.0.0`
- Nome: v9.0.0
- Publicada em: 2018-12-02
- Release anterior (cronológica): `v8.5.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 223

-  Prettiers more things
-  Updates dependencies & more
-  Adds logging for finding a new repository
-  Switches to use new git extension api (for git path)
-  Fixes issue with log cache (exact match miss)
-  Fixes incorrect status when parsing logs with diffs
-  Adds the current user e-mail when uncommitted
-  Changes mm Gravatar fallback to mp (since Gravatar renamed it)
-  Reworks git commands a bit to reduce rethrows
-  Add support to filter logs by author
-  Fixes #430 - Use content provider instead of tmp files (for text docs)
-  Adds diffWithWorking to editor toolbar when diffing
-  Closes #493 - Adds changes to commits in explorers
-  Defaults compact to false in getFormattedDiffStatus
-  Fixes path formatting & adds optional suffix
-  Closes #388 - Adds git mailmap support
-  Adds another git warning
-  Adds explore repo from here command (wip)
-  Moves gitService into git folder & renames a couple of git files
-  Bundles node_modules directly into extension.js
-  Fixes floating promises
-  Renames a few interfaces to remove I prefix
-  Consolidates error messaging to show output channel button
-  Removes docked history view (wip)
-  Reworks explorers (wip)
-  Adds new repository commands (fetch, pull, push) (wip)
-  Shows explorer when adding revision workspace folder
-  Bumps version to eventual 9.0.0-alpha
-  Updates config types to better match
-  Fixes issue with line history refreshing on all selection changes
-  Adds progress notification to fetch, pull, push ops
-  Fixes issues with comparing added/deleted files
-  Saves children to avoid losing state on tree update
-  Adds parent links to all nodes
-  Only await if we need to
-  Renames GitLens explorer to Repositories explorer
-  Adds pull all command to repos explorer
-  Adds changes into commit format in explorers
-  Removes dead code
-  Renames CodeLensController to GitCodeLensController
- ... e mais 183 commits

### Release 4

Link: https://github.com/gitkraken/vscode-gitlens/releases/tag/v11.0.2
- Tag: `v11.0.2`
- Nome: v11.0.2
- Publicada em: 2020-11-20
- Release anterior (cronológica): `v11.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 13

-  Fixes #1166 - Bad size for GitHub fallback avatars
-  Fixes #1187 - adds missing escape in regexp
-  Updates dependencies
-  Fixes #1151 - missing codicons
-  Updates regex to not be positional
-  Removes unneeded debug logging
-  Adds shortcut keys to rebase buttons
-  Reduces padding on rebase entries
-  Adds debug logging for sync'd settings
-  Hides the show line history command unless enabled
-  Adds range support to compare refs
-  Refines rebase editor
-  Bumps to v11.0.1

### Release 5

Link: https://github.com/gitkraken/vscode-gitlens/releases/tag/v12.0.3
- Tag: `v12.0.3`
- Nome: v12.0.3
- Publicada em: 2022-03-10
- Release anterior (cronológica): `v12.0.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  Reset octokit on logging change to enable logging
-  Avoids unhelpful gate
-  Starts handling rate limits (wip)
-  Fixes #1897 avoid messages on 500 errors
-  Bumps to v12.0.3
