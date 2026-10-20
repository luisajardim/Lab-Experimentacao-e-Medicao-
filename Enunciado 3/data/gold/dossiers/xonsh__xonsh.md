# xonsh/xonsh

Repositório: https://github.com/xonsh/xonsh

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/xonsh/xonsh/releases/tag/0.4.7
- Tag: `0.4.7`
- Nome: (sem nome)
- Publicada em: 2016-10-03
- Release anterior (cronológica): `0.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1366

-  fixed newline env issue
-  some test fixes
-  Sort results from globbing. Name misleading because glob, not iglob is used.
-  Introduce envvar True to control sorted globbing.
-  Add change log for sortglob.
-  Test sorted and unsorted globbing.
-  Return an interator from _iglobpath instead of a list.
-  PEP8 and fix wrong docstring.
-  'parametrize ftw'
-  'test_tools part1'
-  Merge branch 'master' into pytest_migration
-  newline
-  some cl cleanup
-  some cl cleanup
-  amalgamate fix
-  added amalgamate error
-  test_tools, almost complete
-  Merge branch 'amalfix'
-  version bump to 0.4.1
-  TODO list, conftest.py, some migrations
-  Merge branch 'master' into pytest_migration
-  'need more fixturesr'
-  'need more fixtures'
-  fixed conflict
-  newline fix
-  more docs
-  more doc hooks
-  Merge pull request #1313 from xonsh/nlp
-  stop autocomplete from autoselecting first entry
-  add changelog and note about forked code
-  'removed xenv ambiguity'
-  Merge branch 'master' into pytest_migration
-  Merge branch 'dont_select_first'
-  test_aliases/test_dirstack
-  add githash file to setup, manifest and gitignore
-  add git hash to platform and xonfig info
-  undo changes made to __init__.py during setup.py
-  add changelog and remove spurious MANIFEST entry
-  add minor fixes from review
-  manifest changes so that source dist can install anywhere
- ... e mais 1326 commits

### Release 2

Link: https://github.com/xonsh/xonsh/releases/tag/0.5.9
- Tag: `0.5.9`
- Nome: 0.5.9
- Publicada em: 2017-03-15
- Release anterior (cronológica): `0.5.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 539

-  implement echo in python
-  implement pwd
-  implement echo and pwd the right way
-  better name?
-  add cat
-  improvements to cat
-  pep8 fixes
-  add tty to the list
-  small change to built_ins (hopefully won't break anything)
-  big-time fixes for cat
-  small refactor
-  small refactor
-  update the way PWD is handled internally
-  update pwd command
-  fix where help string is printed
-  add tee command
-  modify tests for new pwd info
-  use new built-ins for capturing STDIN
-  new procproxy controller; should make routing signals to procproxy objects possible
-  temporarily give up on allowing procproxy to be backgrounded; only killed for now
-  treat waiting for procproxies just the same as waiting for actual subprocs
-  modify xoreutils funcs to use new semantics
-  small bugfixes for timing, etc
-  some cleanups for cat
-  small test change
-  slightly different interface for the (now 4) different ways of specifying procproxies
-  echo and pwd don't need the controller
-  flesh out implementation of tty
-  another small test fix
-  tty small fix (not sure why necessary)
-  implement yes in python
-  add built-in commands, move which to xoreutils
-  add 'enable' command
-  reverting some choice files to old form
-  woops; bad merge
-  working proof of concept.  still need to figure out stream redirects
-  controllableprocproxy working...almost
-  other passthroughs
-  update more to xoreutils
-  pep8 fixes
- ... e mais 499 commits

### Release 3

Link: https://github.com/xonsh/xonsh/releases/tag/0.6.2
- Tag: `0.6.2`
- Nome: 0.6.2
- Publicada em: 2018-04-24
- Release anterior (cronológica): `0.6.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 45

-  Include Metadata in release tarballs
-  include license and docs: fix issues raised in PR
-  remove docs from tarballs
-  some removal
-  Merge branch 'master' into noconf
-  fixed foreign shells for no config
-  added file inserter to wizard
-  some updates
-  add command name
-  foreign shell writer
-  wrote dumpers
-  remove extra paren
-  fixed some other startup bugs
-  fixed tests for no conf
-  fixed StateVistor.flatten() bug
-  many small fixes
-  added noconf news
-  flake8 and doc fixes
-  removed lazyobject from _XONFIG_SOURCE_FOREIGN_SHELL_COMMAND
-  have to push tags up
-  Add `#` to chars that need autoquotes
-  Merge pull request #2612 from xonsh/escape_pound
-  Remove "Try xonsh" and fix doctr release deploy
-  Merge pull request #2615 from xonsh/fix_docs
-  change doc repo url
-  Merge branch 'master' of github.com:xonsh/xonsh
-  resolved conflicts
-  unused import
-  added deprecation warning
-  Remove extraneous colon
-  environ
-  Merge branch 'noconf' of github.com:xonsh/xonsh into noconf
-  Merge pull request #2567 from xonsh/noconf
-  Remove references to static config file from xontrib docs
-  Merge pull request #2620 from xonsh/static_conf_doc_clean
-  Merge pull request #2551 from sebix/inc-license
-  Trim excess whitespace
-  Add section on configuring the path helper.
-  Merge pull request #2622 from jaraco/docs/macos-path_helper
-  print() rather than print_color()
- ... e mais 5 commits

### Release 4

Link: https://github.com/xonsh/xonsh/releases/tag/0.6.4
- Tag: `0.6.4`
- Nome: 0.6.4
- Publicada em: 2018-05-17
- Release anterior (cronológica): `0.6.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 20

-  Fixes spaces in readline tab completer
-  Merge branch 'master' into aspace
-  Completions for quotes in readline, more complex than I thought
-  Merge branch 'master' into aspace
-  readline completions list all options correctly
-  fix bash completion prefix length computation
-  indents
-  Merge branch 'master' into aspace
-  fixed typos
-  Fix typo in error message
-  Avoid referencing ASYNC and AWAIT on Python 3.7.0b4 and later. Fixes #2638.
-  Add news entry. Ref #2638.
-  Bring back PYTHON_VERSION_INFO and rely on it to filter ASYNC/AWAIT variables. Ref #2638.
-  Merge pull request #2639 from jaraco/bugfix/issue-2638
-  source-foreign error improvement
-  Merge branch 'master' into srcerror
-  typo fix
-  Merge pull request #2642 from xonsh/srcerror
-  bumped version to 0.6.4
-  Updated CHANGELOG for 0.6.4

### Release 5

Link: https://github.com/xonsh/xonsh/releases/tag/0.22.2
- Tag: `0.22.2`
- Nome: v0.22.2
- Publicada em: 2026-02-03
- Release anterior (cronológica): `0.22.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 70

-  Enhance on_chdir docstring with usage example
-  Revert adding example
-  fix: Revert "Fix for completer issue with file name containing backslash" because of a regress (#6052)
-  fix(docs): Update ErrorString import handling in cmdhelp.py (#6054)
-  Add example to on_chdir
-  Reduce env updating 
-  Refactor next_command handling in prompt logic
-  Update xonsh installation instructions in README
-  Update installation and cheatsheet links in README
-  Enhance documentation for on_ptk_create event
-  Revise tutorial on xonsh events and usage examples
-  Delete docs/advanced_events.rst
-  Remove advanced_events from documentation index
-  Fix typo in README regarding xonsh compilation
-  Update title of install_mamba.rst to 'Mamba Install Xonsh'
-  Update activation command for mamba to use -e flag
-  fix(mamba-installer): Rename xmamba to xmamba.xsh (#6059)
-  Change code block syntax from console to bash
-  fix(procs): Fix ioctl windowsize buffer size to reduce issues in the future python 3.14 (#6061)
-  fix: Raise an error in case of redirect without command (#6060)
-  fix: Fixed `xcontext` error in case `xpip` has complex command (#6063)
-  Fix typo in 'Cheat sheet' link in README
-  Simplify xonsh AppImage README by adding the link
-  Update environment variable access in activate.xsh
-  Refactor environment variable checks in activate.xsh
-  Add example for changing variable value in tutorial
-  Change xonsh shell prompt to include a symbol
-  Tag 'kash' entry from README
-  fix(startup): Fix crash on built-in readline, print compatibility message on uv pythons (#6069)
-  Update installation guide with wording fixes
-  feat(prompt): Added $XONSH_PROMPT_NEXT_CMD_SUGGESTION to set the text of the next command suggestion (#6048)
-  feat(xcontext): Report current xonsh session executable in `xcontext` (#6071)
-  Update command from 'xpython -V' to 'which xpython'
-  Update docs/aliases to provide more examples
-  Fix codeblock
-  Update wording
-  Update table marks
-  Fix symbols in Xonsh installation options table
-  Update table mark
-  Fix typo
- ... e mais 30 commits
