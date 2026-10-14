# gokcehan/lf

Repositório: https://github.com/gokcehan/lf

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/gokcehan/lf/releases/tag/r5
- Tag: `r5`
- Nome: r5
- Publicada em: 2018-06-16
- Release anterior (cronológica): `r4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  restart server when crashed
-  cleanup
-  add key mappings to the doc
-  cleanup
-  reload modified directories when loading cache
-  reload modified files when loading cache
-  keep cache when navigation is renewed
-  add 'period' option for periodic refresh
-  add 'load' command to load modified dirs and files
-  load all clients after running 'put' command
-  add tutorial link to readme
-  replace 'reload' with 'load' in documentaiton
-  handle command properly with 'cmd-word'back'
-  cleanup
-  find hidden parents when 'hidden' is changed
-  update preview when 'hidden' is changed
-  update readme

### Release 2

Link: https://github.com/gokcehan/lf/releases/tag/r8
- Tag: `r8`
- Nome: r8
- Publicada em: 2018-08-29
- Release anterior (cronológica): `r7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 16

-  add 'quit' command to server protocol
-  try to reconnect when server is not yet started
-  try to reconnect after sleep
-  export 'LF_LEVEL' variable for nested instances
-  handle removed directories during load
-  handle non-existent directories during reload
-  detach server on windows
-  add find commands to find as you type
-  add 'findlen' option to control number of chars
-  use zero value in findlen for arbitrary length
-  add 'anchorfind' option to control find start
-  keep reverse direction in find and search
-  keep index when selection is deleted
-  use load instead of reload after shell-pipe
-  check HOME and USER variables on startup
-  update documentation

### Release 3

Link: https://github.com/gokcehan/lf/releases/tag/r25
- Tag: `r25`
- Nome: r25
- Publicada em: 2021-10-09
- Release anterior (cronológica): `r24`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  Don't use the absolute path when saving bookmarks (#659)
-  implement dironly option (#669)
-  add an option to disable directory cache (#673)
-  update doc
-  add completion for dircache option
-  Added filter command (#667)
-  added pre-cd command (#685)
-  cmap now accepts all expressions (#686)
-  fixed bug, where ~ is not a absolute directory (#690)
-  Cmap fixes (#691)
-  fix crash when hidden is changed
-  update doc

### Release 4

Link: https://github.com/gokcehan/lf/releases/tag/r29
- Tag: `r29`
- Nome: r29
- Publicada em: 2023-04-30
- Release anterior (cronológica): `r28`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 57

-  Make `lfcd` examples safer for people who alias `lf` to `lfcd` (#1049)
-  Bind Ctrl+MouseWheel to scroll up/down (#1051)
-  Disallow exiting from `rename:` mode with backspace (#1060)
-  Add example to hiddenfiles documentation (#1073)
-  Refresh preview even if selection doesn't change (#1074)
-  Allow separate styles for cursor in normal and preview panes, simplify `tagfmt` and `errorfmt` (#1086)
-  Fix documentation for dironly/dirpreviews options (#1105)
-  Option to change look of cursors in parent dirs, rename an option. (#1106)
-  Navigate cmd history with up/down (#1112)
-  Add Winget Releaser workflow (#1107)
-  Bump actions/setup-go from 2 to 3 (#1126)
-  Bump dominikh/staticcheck-action from 1.2.0 to 1.3.0 (#1127)
-  Bump actions/checkout from 2 to 3 (#1129)
-  change go version from 1.17 to 1.18
-  remove older than go1.17 instructions from readme
-  `invert-below` command to substitute for visual mode (#1101)
-  Update the Go version in `go.mod` to 1.18 (#1132)
-  Bump github.com/gdamore/tcell/v2 (#1128)
-  Replace the obsolete Vue icon in the example file (#1123)
-  Bump golang.org/x/sys from 0.5.0 to 0.6.0 (#1136)
-  Bump golang.org/x/term from 0.5.0 to 0.6.0 (#1137)
-  Delete stale dircache entry during rename (#1138)
-  Remove commented code (#1141)
-  try to fix #916 (#1146)
-  Update file info after reload command (#1149)
-  Refactor code for printing directories (#1150)
-  Fix width used for line numbers (#1151)
-  add 'true/false' syntax for boolean options
-  cleanup
-  add errors for unexpected boolean option values
-  update doc
-  Avoid refreshing previews for async shell commands (#1164)
-  Enhance rename prompt (#1162)
-  Bump actions/setup-go from 3 to 4 (#1160)
-  Improve preview loading message flickering (#1154)
-  Use tcell constants for drawbox (#1170)
-  cleanup
-  Display zero when relativenumber is enabled (#1171)
-  Support custom line number colors (#1177)
-  Fix infinite loop in listMatches (#1183)
- ... e mais 17 commits

### Release 5

Link: https://github.com/gokcehan/lf/releases/tag/r30
- Tag: `r30`
- Nome: r30
- Publicada em: 2023-05-20
- Release anterior (cronológica): `r29`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  build diskfree on all platforms
-  Prevent scrolling to bottom when selecting files (#1222)
-  Separate filter from selections in the ui ruler (#1223)
-  Bump golang.org/x/sys from 0.7.0 to 0.8.0 (#1224)
-  Bump golang.org/x/term from 0.7.0 to 0.8.0 (#1225)
-  Minor cleanup of reflect code (#1229)
-  Add `jumps` command for displaying the jump list (#1233)
-  Fix count when parsing `bottom` command (#1240)
