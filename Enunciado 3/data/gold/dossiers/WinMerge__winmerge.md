# WinMerge/winmerge

Repositório: https://github.com/WinMerge/winmerge

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/WinMerge/winmerge/releases/tag/2.14.0%2B-jp-118
- Tag: `2.14.0+-jp-118`
- Nome: WinMerge 2.14.0 + (3-way merge, image compare/merge) +-jp-118
- Publicada em: 2016-09-25
- Release anterior (cronológica): `2.14.0+-jp-117`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 13

-  Added tag 2.14.0+-jp-117 for changeset 573d8dbb6181
-  CompareMSExcelFiles.sct: Remove trailing spaces and make setting window size larger
-  CompareMSExcelFiles.sct: Add 'Update external references(links)' checkbox to plugin settings window
-  Plugins.cpp: Ignore *.sct~ files
-  Fix to display the Left|Right EOL column correctly. close #53. (Merge from WinMerge2011)
-  Installer: Make Plugins option checked by default
-  OptionsInit.cpp: Make Tree Mode checked by default
-  OptionsInit.cpp: Disable mlang.dll on non-CJK environment
-  Update WiX installer project
-  Bump revision to 2.14.0+-jp-118
-  Added tag 2.14.0+-jp-118 for changeset b0fb758b8bae
-  Forget to merge from WinMerge2011
-  Removed tag 2.14.0+-jp-118

### Release 2

Link: https://github.com/WinMerge/winmerge/releases/tag/v2.16.16
- Tag: `v2.16.16`
- Nome: v2.16.16
- Publicada em: 2021-10-28
- Release anterior (cronológica): `ShellExtension-1.18.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 25

-  DlowloadDeps.cmd: Update ShellExtension to 1.18.2.0
-  ImgMergeFrm.cpp: Fix an issue where drag-and-drop of file would only work once.
-  Fix an issue where filters are not applied correctly when opening a project file containing multiple items with different filters. (#995)
-  Resource.h: Increase the maximum number of unpacker plugins from 40 to 200.
-  ShellFileOperations_test.cpp: Fix failed test
-  PropShell.cpp: Fix the problem that the "Register Shell Extension for Windows 11 or later" button is not enabled when another user has registered ShellExtension for Windows 11.
-  Fix issue #998: Cannot resize last column with UI
-  Fix typo in OpenView.cpp (#1000)
-  Update Apache tika to 2.1.0 and change the download URL to the URL suggested by JohnF-tfa (https://github.com/WinMerge/winmerge/issues/715#issuecomment-939630493)
-  Fix a problem where the string in the Windows common dialog would not change to the language when switching languages.
-  Fix issue #1004:  Where to report documentation/help errors?
-  Galician translation update (#1005)
-  Add Portuguese.isl (#1017)
-  FolderCompare: Additional Properties (Windows Property System+Hash(MD5, SHA-1, SHA-256)) (#996)
-  Update Hungarian.po (#1023)
-  Fix issue #1007: Comparing broken lnk-files (windows shortcuts) freezes WinMerge
-  Update ChangeLog&ReleaseNotes
-  Bump revision to 2.16.16
-  Update ChangeLog&ReleaseNotes (2)
-  CompareMSExcelFiles.sct: Make the number before the sheet name zero-padded. Submitted by Shirai
-  Update Slovenian translation. Submited by JadranR
-  Update ChangeLog&ReleaseNotes (3)
-  Update German.po (#1027)
-  Update ChangeLog&ReleaseNotes (4)
-  Update TranslationsStatus

### Release 3

Link: https://github.com/WinMerge/winmerge/releases/tag/v2.16.28
- Tag: `v2.16.28`
- Nome: (sem nome)
- Publicada em: 2023-02-14
- Release anterior (cronológica): `v2.16.26`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Revert "Fix issue #1646, #1644: Filtering qualified files (2)"
-  Revert "Fix issue #1646, #1644: Filtering qualified files"
-  Update ChangeLog&ReleaseNotes
-  Bump revision to 2.16.28

### Release 4

Link: https://github.com/WinMerge/winmerge/releases/tag/v2.16.34
- Tag: `v2.16.34`
- Nome: v2.16.34
- Publicada em: 2023-10-27
- Release anterior (cronológica): `v2.16.33`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 51

-  Update jq to version 1.7 (2)
-  Update Korean.isl (#2041)
-  Korean.isl: Change the file encoding from UTF-8 to CP-949
-  MergeDoc.cpp: Change it to get the Prediffer plugin without depending on CDirDoc.
-  Introduce IDirDoc interface
-  refactor
-  Small code changes for CMDIChildWnd handling (#2043)
-  Update winimerge to 1.0.41
-  Fix issue #2045: WinMerge Crashed for Comparing Clipboard Texts
-  Fix sf.net ticket #2163: Save As: default directory should be file's original directory (2)
-  refactor
-  Fix issue #2046: Folder compare omits unique folders from results if they contain any files and/or subfolders
-  Modify the "Line Filters" dialog. (#2047)
-  refactor
-  Update
-  Improve line filters and substitution filters (#2032) (2)
-  Improve line filters and substitution filters (#2032) (3)
-  Improve line filters and substitution filters (#2032) (4)
-  Fix typo
-  Update ignore_comments.cpp
-  Add "(F4)" to the description of the toolbar icon "Difference in the Current Line". refs #2050
-  Add "(F4)" to the description of the toolbar icon "Difference in the Current Line". refs #2050 (2)
-  Update French.po (#2055)
-  Update Korean.po (#2057)
-  Allow NUL and \\.\NUL in paths specified as command line arguments (#2056)
-  Improve line filters and substitution filters (#2032) (5)
-  Update Testing/Data/Compare/Dir*/ignore_comments.cpp
-  Add excel.xlsx, excel.xlsm
-  Update Korean.isl (#2059)
-  Update Korean.isl (#2060)
-  Korean.isl: Change the file encoding from UTF-8 to CP-949
-  Update French.po 16.30 => 16.32 (#2058)
-  DiffWrapper.cpp: Remove unnecessary #include
-  Update French.po
-  Update French.po
-  Move the parser source files in editlib.vcxitems to editlibparsers.vcxitems.
-  Fix build error on VS2017
-  FolderCompare.vcxproj: Remove MFC dependencies
-  Add file*_nolasteol.txt
-  Fix a crash problem when the Diff algorithm is set to something other than default and one file does not have an EOL of the last line and the other file has an EOL of the last line.
- ... e mais 11 commits

### Release 5

Link: https://github.com/WinMerge/winmerge/releases/tag/Merge7z2409.0
- Tag: `Merge7z2409.0`
- Nome: Merge7z2409.0
- Publicada em: 2024-12-05
- Release anterior (cronológica): `v2.16.45.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 7

-  Update Korean.isl (#2558)
-  Update Korean.isl (#2559)
-  Korean.isl: Change the file encoding from UTF-8 to CP-949
-  Fix issue #2562: Looks like the View Tab Bar "folder icon" is getting a green check-mark before the folder compare has even completed.
-  Remove unnecessary #includes
-  Fix issue #2566: WinMerge 2.16.44.0 : CompareMSWordFiles.sct Plugin : Forced Enabled Confirm Conversions Pop-Up
-  Update POCO C++ libraries to 1.14.0
