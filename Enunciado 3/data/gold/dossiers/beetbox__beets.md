# beetbox/beets

Repositório: https://github.com/beetbox/beets

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/beetbox/beets/releases/tag/v1.2.2
- Tag: `v1.2.2`
- Nome: beets 1.2.2
- Publicada em: 2013-08-27
- Release anterior (cronológica): `v1.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 38

-  Added tag v1.2.1 for changeset bd7259ac13b5
-  Send a plug-in event when file is moved
-  Document new plug-in event item_moved
-  Add Item instance to item_moved event
-  Merge pull request #335 from dsedivec/master
-  changelog for #335, version bump
-  Don't consider text between parentheses when 
-  Some tweaking to yield better results by not 
-  Logging: remove match ratio, add source website name
-  Merge pull request #339 from KraYmer/lyrics-enh
-  changelog for #339
-  bpd: Use AnyFieldQuery when searching "any" fields
-  Merge pull request #340 from laarmen/fix_bpd_search
-  changelog for #340
-  travis: don't --use-mirrors with pip
-  docs/.../cli.rst: Add an `of` to the description of `update -p`
-  Merge pull request #342 from mineo/patch-2
-  Update index.rst
-  beets is now in the official Arch package repo
-  Beets is a music library manager, not a TARDIS
-  Merge pull request #352 from mineo/patch-3
-  pathformat.rst: Add back "track"
-  Merge pull request #353 from mineo/patch-4
-  fix regex (and other) queries in path field
-  guides/tagger: Make emailing Adrian less imperative
-  ref/cli.rst: Add a missing 'k'
-  ref/cli.rst: Remove a 'd'
-  plugins/zero.rst: Add a missing 'the'
-  plugins/zero.rst: Add a missing 'a'
-  docs/inline.rst: The ``[paths]`` section is now ``paths:``
-  Merge pull request #354 from mineo/docs-fixup-2
-  FetchArt plugin: Support grabbing album art from MB release group
-  Simplify fetching cover art from release group
-  changelog/thanks/tweaks for #355
-  fix homebrew gstreamer instructions
-  remove debug print that slipped in
-  fix import deletion race
-  changelog date/summary for 1.2.2

### Release 2

Link: https://github.com/beetbox/beets/releases/tag/v1.3.1
- Tag: `v1.3.1`
- Nome: beets 1.3.1
- Publicada em: 2013-10-13
- Release anterior (cronológica): `v1.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 106

-  fix outdated _record reference in web plugin
-  Added opus support, maybe.
-  Opus now passes basic tests.
-  Added tag v1.3.0 for changeset 87945a0e2175
-  Allow the convert plugin to convert to any format, not just mp3.
-  Removed reference to my testing plugin, oops.
-  Problem with unicode filenames sorted.
-  version bump: 1.3.1
-  Merge pull request #381 from rowan-lewis/opus
-  opus: sample rate is always 48kHz
-  opus: remove image from test file
-  opus: changelog/thanks/docs (closes #377, #381)
-  embedart: fix error message when imagehdr fails
-  docs: mention musicbrainz port config (closes #365)
-  Changed the configuration to allow for easier format selection.
-  It's called Vorbis, not OGG.
-  Reject lossy formats under a set bitrate.
-  Fixed validation, basically replace unfriendly errors with friendly errors.
-  Added more format presets, updated documentation.
-  Added 'quiet' operation mode, prevents start/finish announcements for each file.
-  merge
-  mbcollection: skip invalid MBIDs
-  Merge pull request #380 from rowan-lewis/convert-all
-  convert-any: changelog/thanks (closes #362, #380)
-  initial import of tags-from-filename plugin (#113)
-  fromfilename: python style, naming, comments
-  fromfilename: switch to declarative style
-  fromfilename: preserve case, apply in more cases
-  fromfilename: simplify
-  fromfilename: docs/changelog (closes #113)
-  info: eager error detection (closes #371)
-  echonest_tempo: ensure we have the right track
-  numeric query tests
-  filter wide integers (closes #348)
-  use track length over recording length
-  python 2.6 compatibility
-  add FAQ
-  FAQ: shorten questions
-  integrate FAQ links with the rest of the docs
-  FAQ: reorganize into sections
- ... e mais 66 commits

### Release 3

Link: https://github.com/beetbox/beets/releases/tag/v1.3.11
- Tag: `v1.3.11`
- Nome: beets 1.3.11
- Publicada em: 2015-04-06
- Release anterior (cronológica): `v1.3.10`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 615

-  Added the import_task_created event
-  Refactor ftintitle to extract the code to find the featured artist
-  Fix a bug in ftintitle with the order of album artist
-  Fix formatting to pass flake8 tests
-  Initialize feat_part as None
-  Removed some testing code which was checked in accidentally
-  Added the import_task_created event
-  Removed some testing code which was checked in accidentally
-  The new event changed the log so an old import test failed...
-  Merge remote-tracking branch 'origin/import-filefilter' into import-filefilter
-  Remove ArtistNotFoundException in favor of returning None for simplicity
-  Tests failed on windows
-  Simplified the configuration of the regular expressions for th ihate plugin
-  Rearranged regex config options to reduce hierarchies
-  Instead of emitting the import_task_created event using a pipeline stage, it is fired every time an import task was created.
-  Merge branch 'master' into import-filefilter
-  Modified the tests to match the new `--pretend` output.
-  Recent changes broke the flake8 rules...
-  All import tasks are now created by the ImportTaskFactory.
-  Event handler implemented in plugins may now return values.
-  Take care of None objects when dealing with tasks
-  Merge branch 'master' into import-filefilter
-  Offer new-style formatting for logging
-  Convert beets core to lazy logging
-  Convert beets plugins to lazy logging
-  Fix logging formatting string in duplicates plugin
-  Update logging imports: logging → beets.logging
-  Fix 4 tests by str()-ing a logged exception
-  Add tests for beets.logging
-  Make test/test_logging work on python 2.6
-  Fix docstring beets.logging.StrFormatLogger._log
-  Attain pep8-cleanliness
-  Silence flake8 on logging.* import
-  The return values of plugin event handlers are not flattened any more within the plugin class
-  Factory methods of ImportTaskFactory guaranty that a list is returned and the list does not contain a 'None'. That leads to much cleaner code where the methods are called.
-  Added documentation and tests
-  embedart: restore an apparent typo (which wasn't)
-  Port beets.logging to python 2.6
-  beets.logging: fix root logger access
-  Minor fix in beets.logging docstring
- ... e mais 575 commits

### Release 4

Link: https://github.com/beetbox/beets/releases/tag/v2.13.0
- Tag: `v2.13.0`
- Nome: Release v2.13.0
- Publicada em: 2026-07-27
- Release anterior (cronológica): `v2.12.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/beetbox/beets/releases/tag/v2.13.1
- Tag: `v2.13.1`
- Nome: Release v2.13.1
- Publicada em: 2026-07-29
- Release anterior (cronológica): `v2.13.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  reformat beatport/bpsync docs
-  Reformat beatport/bpsync docs (#6883)
-  Include uv.lock in changes docs files
-  It seems like the man folder was ignored as it is not part of our vcs.
-  Changelog entry
-  Removed unused doc sections. Preparing for hotfix.
-  fix: sdist should include man pages (#6884)
-  Increment version to 2.13.1
