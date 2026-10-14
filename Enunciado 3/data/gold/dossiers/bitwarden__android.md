# bitwarden/android

Repositório: https://github.com/bitwarden/android

## Metadados

- Linguagem: Kotlin

## Releases sorteadas

### Release 1

Link: https://github.com/bitwarden/android/releases/tag/v1.17.0
- Tag: `v1.17.0`
- Nome: Version 1.17.0
- Publicada em: 2018-06-20
- Release anterior (cronológica): `v1.16.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 43

-  Search Login URI as well
-  ignore "edit" fields on autofill
-  look for password fields from HtmlInfo attributes
-  bump android version
-  faceid description in info.plist
-  update fingerprint lib
-  version bump
-  adjust max_aspect ratio for samsung full screen
-  disable test nodes
-  add via to oreo trusted browsers
-  stub out yubico nfc support for ios
-  nfc updates
-  turn on nfc in plist
-  remove nfc from extension
-  clearup yubikey reading on ios
-  move nfc delegate to member of appdelegate class
-  cleanup
-  hide yubikey token cell for ios
-  try again button for ios yubikey
-  dont set key validity dates
-  previous 2017
-  Revert "previous 2017"
-  run cloc on install
-  checked for locked state on activity resume.
-  iphone yubikey images
-  update yubikey options for ios
-  appresources for ios yubikey
-  remove password generate event on disappear
-  add bromite autofill support
-  clear cache flag on disk
-  add pbkdf2 key stretching
-  Card Security Code masked (bitwarden/desktop issue 78) (#328)
-  monospace fonts for card code
-  shows both accessibility and autofill from tools
-  allow non-nfc keys on android
-  version bump
-  New Crowdin translations (#329)
-  update designer
-  add ko and fa languages
-  designer update
- ... e mais 3 commits

### Release 2

Link: https://github.com/bitwarden/android/releases/tag/v1.20.0
- Tag: `v1.20.0`
- Nome: Version 1.20.0
- Publicada em: 2018-11-27
- Release anterior (cronológica): `v1.19.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 29

-  back button should be white
-  bump version
-  os version checks on auth service apis
-  add minimum os version
-  bump version
-  formatting
-  ios < 12 fixes
-  bump version
-  null checks
-  version bump
-  dont try to fill unless has username and password
-  null ref check
-  target android sdk 26 with fixes to HybridWebView
-  New Crowdin translations (#389)
-  bump version
-  New Crowdin translations (#395)
-  New Crowdin translations (#398)
-  update packages
-  zh-HK gets traditional chinse
-  support attachment key, 100k iterations on regist.
-  New Crowdin translations (#411)
-  comment out keyboard dismissal
-  dont focus on cell tapped
-  Revert "dont focus on cell tapped"
-  Revert "comment out keyboard dismissal"
-  update libs
-  New Crowdin translations (#417)
-  bump version
-  deprecate mac checks on RSA decrypt

### Release 3

Link: https://github.com/bitwarden/android/releases/tag/v2.1.2
- Tag: `v2.1.2`
- Nome: Version 2.1.2
- Publicada em: 2019-07-25
- Release anterior (cronológica): `v2.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 32

-  register event service with container
-  log some events
-  process event uploads on ios
-  handle sleep event on ios manually
-  disable events funcionality for now
-  bump version
-  update autofill identities if needed
-  InitAppIfNeeded
-  fix lock checks on sleep of app
-  null checking
-  assign new messageCallback when subbing
-  rebuild same fingerprintName string
-  use fingerprintButtonText on extension unlock
-  fix no folder reference
-  more options button for ios on folder add/edit
-  a11y labeling
-  check yubico token length == 44
-  New Crowdin translations (#565)
-  log autofill events
-  * CredentialProviderViewController.cs:
-  formatting
-  version bump
-  don't allow device PIN fallback
-  event service func
-  check $LastExitCode
-  re-work hockeyapp init
-  visibility typo
-  New Crowdin translations (#567)
-  New Crowdin translations (#568)
-  null check on cipher when autofilling
-  null check on id
-  New Crowdin translations (#569)

### Release 4

Link: https://github.com/bitwarden/android/releases/tag/v2023.7.0
- Tag: `v2023.7.0`
- Nome: Version 2023.7.0
- Publicada em: 2023-07-13
- Release anterior (cronológica): `v2023.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 36

-  Add github actions to renovate (#2536)
-  [PM-2347] Refresh feature flags when environment urls change (#2538)
-  reset lock delay when returning from activity result (#2539)
-  Autosync the updated translations (#2540)
-  Bumped version to 2023.5.0 (#2553)
-  PM-2232 Fix api response not being read as string because the content was not being considered json when it was indeed. Now Netacea messages are shown on the UI. (#2541)
-  Bumped version to 2023.5.1 (#2554)
-  Autosync the updated translations (#2555)
-  PM-1798 Added accessibility names on entries on cipher add (#2550)
-  [PS-2558] Mobile Automation - Starting automationIDs additions to our codebase (#2558)
-  PM-1076 added warning on unlocking iOS extensions when the kdf type is argon2id and the memory is higher than 48MB, to let the user know that unlocking might crash the extension (#2560)
-  Autosync the updated translations (#2562)
-  add more comment to missing actions (#2567)
-  Update F-Droid listing author name (#2501)
-  Enhancement to login field detection for Android autofill (#2561)
-  PM-2575 Fixed extension freeze when using the return button on the keyboard when unlocking the extension. Also added way to prevent multiple executions of checking the password and logging exceptions. (#2568)
-  [PM-2544] Adding AutomationIDs for CipherAddEditViewPage elements (#2564)
-  Adding AutomationIDs on Generator page elements (#2569)
-  [PM-2645] Adding IDs for Account Switching elements (#2572)
-  Autosync the updated translations (#2570)
-  [PM-2611] Adding IDs for Cipher/Send search results (#2575)
-  [PM-2612] Adding AutomationIDs for LoginPasswordlessPage elements (#2574)
-  [PM-2545] Adding Automation IDs for CipherDetailsPage elements (#2576)
-  Adding IDs for AttachmentPage elements (#2577)
-  Autosync the updated translations (#2582)
-  [PM-2678] Adding IDs for Settings Page elements (#2584)
-  [PM-2748] Refactoring locator strategy for Cipher Details page (#2586)
-  [PM-2688] Adding IDs for Options and Folders pages (#2585)
-  [PM-192] Refactor forwarded email providers (#2579)
-  [PM-2737] Adding AutomationIDs for Send page elements (#2583)
-  [PM-2691] Adding AutomationIDs for Vault Page sections (#2580)
-  [PM-2798] Fixing Toolbar locators in FolderAddEditPage (#2592)
-  Autosync the updated translations (#2595)
-  Revert "reset lock delay when returning from activity result (#2539)" (#2597)
-  Bumped version to 2023.7.0 (#2612)
-  Fix Build Workflow (#2613)

### Release 5

Link: https://github.com/bitwarden/android/releases/tag/v2025.7.1-bwpm
- Tag: `v2025.7.1-bwpm`
- Nome: Password Manager 2025.7.1 (20513)
- Publicada em: 2025-08-01
- Release anterior (cronológica): `v2025.7.0-bwa`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  🍒 [BRE-831] migrate secrets akv (#5347) (#5595)
-  PM-24182: Fix crash in Android 13 (#5594)
