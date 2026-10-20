# wger-project/flutter

Repositório: https://github.com/wger-project/flutter

## Metadados

- Linguagem: Dart

## Releases sorteadas

### Release 1

Link: https://github.com/wger-project/flutter/releases/tag/1.5.4
- Tag: `1.5.4`
- Nome: 1.5.4
- Publicada em: 2023-04-09
- Release anterior (cronológica): `1.5.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 36

-  Show ingredient images
-  Pass the base provider to the nutritional provider as an argument
-  Commit missing generated file
-  Add stub with nutrition provider tests
-  We don't use release branches anymore
-  Use CircleIconAvatar in the ingredient search
-  Don't show the ingredient ID
-  Merge branch 'master' into feature/ingredient-images
-  Recreate generated files
-  Translated using Weblate (Turkish)
-  Translated using Weblate (Ukrainian)
-  Update Gemfile.lock
-  Update pubspec.lock
-  Merge branch 'master' into feature/ingredient-images
-  Fix merge errors
-  Add switch to search for ingredients in English as well
-  Use paginated api when fetching log entries
-  Bump shared_preferences from 2.0.18 to 2.0.20
-  Merge pull request #368 from wger-project/dependabot/pub/shared_preferences-2.0.20
-  Bump cider from 0.1.4 to 0.1.5
-  Bump shared_preferences from 2.0.20 to 2.1.0
-  Bump mockito from 5.3.2 to 5.4.0
-  Merge pull request #372 from wger-project/dependabot/pub/mockito-5.4.0
-  Merge pull request #370 from wger-project/dependabot/pub/cider-0.1.5
-  Translated using Weblate (Spanish)
-  Translated using Weblate (Spanish)
-  Merge pull request #371 from wger-project/dependabot/pub/shared_preferences-2.1.0
-  Fix test
-  Merge pull request #214 from wger-project/feature/ingredient-images
-  Automatic linting
-  Update pubspec.lock
-  Fix typo
-  The ingredient ID is an integer, not a string
-  Link to ingredient product
-  Fix JSON response
-  Bump version to 1.5.4+31

### Release 2

Link: https://github.com/wger-project/flutter/releases/tag/1.7.3
- Tag: `1.7.3`
- Nome: 1.7.3
- Publicada em: 2024-05-29
- Release anterior (cronológica): `1.7.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 3

Link: https://github.com/wger-project/flutter/releases/tag/1.10.0
- Tag: `1.10.0`
- Nome: 1.10.0
- Publicada em: 2026-01-18
- Release anterior (cronológica): `1.9.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 4

Link: https://github.com/wger-project/flutter/releases/tag/1.10.2
- Tag: `1.10.2`
- Nome: 1.10.2
- Publicada em: 2026-02-28
- Release anterior (cronológica): `1.10.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 75

-  fixed ingredient weight validation
-  fix add time when log meal and nutrition
-  add sort datetime desc when showing ingredient suggestion
-  Merge pull request #1099 from cryptbrn/bugfix/fix-time-nutrition-log
-  Merge pull request #1106 from cryptbrn/feature/sort-ingredient-suggestion
-  Sort dependencies alphabetically
-  Bump build_runner from 2.10.5 to 2.11.0
-  Bump carousel_slider from 5.1.1 to 5.1.2
-  Bump drift from 2.30.1 to 2.31.0
-  Improve wording
-  Properly filter dayData entries
-  Merge pull request #1113 from wger-project/dependabot/pub/drift-2.31.0
-  Merge pull request #1111 from wger-project/dependabot/pub/carousel_slider-5.1.2
-  Merge pull request #1110 from wger-project/dependabot/pub/build_runner-2.11.0
-  Set the correct repetition unit object when saving logs
-  Refactor the log entry form in the gym mode.
-  Rename test
-  value can't be null here
-  Bump faraday from 1.10.4 to 1.10.5 in /ios
-  improves the pop up after a scan gives no result
-  adds the tests for the modified widget in this issue
-  apply dart format
-  Merge pull request #1117 from wger-project/dependabot/bundler/ios/faraday-1.10.5
-  Further increase the default timeout
-  Split up the widgets in log_page.dart file
-  Bump dependencies
-  Upgrade dependencies
-  Remove duplicated import
-  Also send the platform as the user agent
-  Update Podfile.lock
-  Update pull request template
-  Puts the dialog in a new column and changes style to default
-  Merge branch 'wger-project:master' into improve-product-not-found-dialog
-  Add logging when tne unawaited handleUpdateExerciseFromApi
-  Merge branch 'master' into fork/dhituval/issue721/fix-ingredient-weight
-  Fixed i18n
-  Merge pull request #1122 from alexisbirling-boop/improve-product-not-found-dialog
-  Bump actions/download-artifact from 7 to 8
-  Bump actions/upload-artifact from 6 to 7
-  Merge pull request #1126 from wger-project/dependabot/github_actions/actions/upload-artifact-7
- ... e mais 35 commits

### Release 5

Link: https://github.com/wger-project/flutter/releases/tag/2.0.0
- Tag: `2.0.0`
- Nome: 2.0.0
- Publicada em: 2026-06-16
- Release anterior (cronológica): `1.11.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 459

-  Update body weight provider to use riverpod
-  Start actually interacting with powersync
-  Start adding drift and using riverpod
-  Powersync seems to be working now
-  Consolidate body weight repositories and other providers, cleanup
-  Rename provider file
-  Test how feasible it is to load exercises via powersync as well
-  Use the powersync drift provider to show exercises
-  Also load the corresponding equipment
-  Use the new drift provider to load the exercises in their overview
-  Missing M2N table
-  Remove filters from old exercise provider
-  Move more usages to new exercise provider
-  Move more usages to new exercise provider
-  Add new network provider to check connectivity and disable options
-  Remove the json serializable decorators, not needed anymore
-  Read the powersync URL from the server's response
-  Add tables for workout sessions
-  Set foreign key relationships for the exercise tables
-  Set correct nullable attributes
-  Pre-load all exercises on opening the app
-  Use WarningCard to display offline mode
-  Remove the exercise cache settings tile
-  Remove unused methods from exercise provider
-  Move more widgets to use the new providers
-  Rework the base data providers, fix some tests
-  Fix test, remove unused mocks
-  Add tables and providers for weight and repetition units
-  Remove old exercise database
-  Fix some tests
-  Remove json serializable code for exercise models
-  Pass the exercises and workout units as parameters
-  Use directly the the weight unit providers
-  Fix some tests
-  Fix some more tests
-  Update session and log models
-  Fix test
-  Remove old exercises provider 🥲
-  Refactor the django powersync connector
-  Notes is nullable on the db
- ... e mais 419 commits
