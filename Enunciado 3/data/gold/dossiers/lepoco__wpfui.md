# lepoco/wpfui

Repositório: https://github.com/lepoco/wpfui

## Metadados

- Linguagem: C#

## Releases sorteadas

### Release 1

Link: https://github.com/lepoco/wpfui/releases/tag/3.0.2
- Tag: `3.0.2`
- Nome: 3.0.2
- Publicada em: 2024-07-26
- Release anterior (cronológica): `3.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 32

-  Fix ListView to be compatible when ListView.View is a GridView
-  Bump github/codeql-action from 1 to 3
-  Bump actions/checkout from 2 to 4
-  Merge remote-tracking branch 'upstream/development' into fix/gridview-compatibility
-  Change ViewState's type from a string to an enum of two states: Default and GridView
-  Implement the GridView feature by binding directly to the View property.
-  Extract DefaultTextBoxScrollViewerStyle to it's own ResourceDictionary
-  Avoid overflow in text input components
-  Simplify PassiveScrollViewer usage by adding properties to style
-  Fix TitleBarButton Foreground error when change theme
-  Merge pull request #1005 from seasonyuu/development
-  Merge branch 'development' into TextInputOverflow
-  Merge pull request #998 from lepoco/dependabot/github_actions/development/actions/checkout-4
-  Merge branch 'development' into dependabot/github_actions/development/github/codeql-action-3
-  Merge pull request #997 from lepoco/dependabot/github_actions/development/github/codeql-action-3
-  Merge branch 'development' into TextInputOverflow
-  Improve lineargradient border for TextBox in Light/Dark theme (also effects PasswordBox and NumberBox)
-  Merge branch 'development' into fix/gridview-compatibility
-  Merge pull request #1006 from koal44/enhancement/textbox-border
-  Merge pull request #999 from tmijail/TextInputOverflow
-  Merge branch 'development' into fix/gridview-compatibility
-  Merge branch 'fix/gridview-compatibility' of https://github.com/koal44/wpfui into fix/gridview-compatibility
-  Re-implement custom ui:ListView class and remove the ListViewViewStateConverter
-  Addd documentation and tool to the VS tools manifest
-  Merge pull request #979 from koal44/fix/gridview-compatibility
-  Update release
-  Bump version
-  Merge branch 'main' into development
-  Update labeler.yml
-  Merge branch 'development' of https://github.com/lepoco/wpfui into development
-  Update labeler.yml
-  Merge pull request #1008 from lepoco/development

### Release 2

Link: https://github.com/lepoco/wpfui/releases/tag/3.0.5
- Tag: `3.0.5`
- Nome: 3.0.5
- Publicada em: 2024-07-26
- Release anterior (cronológica): `3.0.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 44

-  Prevent icons in MenuItems from being tabstops
-  Merge pull request #1055 from Difegue/patch-1
-  Fix incorrectly refactored High Contrast theme dictionary selection
-  Merge branch 'development' into patch-2
-  Merge pull request #1063 from Difegue/patch-2
-  Fixed the markup extension for the SymbolIcon and FontIcon class not working at all.
-  Rewrite of the arc class. Added SweepDirection as property, viewbox to easier scale the arc aswell as a new startpoint at 12am and refactoring of the code.
-  Fixed the PenLineCap property.
-  Added back doc and removed regions.
-  Merge pull request #1067 from m0lDaViA/development
-  Well, it can be null
-  Format code
-  Update themes.md
-  Merge branch 'development' into patch-1
-  Update UiApplication.cs
-  Update UiApplication.cs
-  Merge pull request #1080 from jonmotos/patch-1
-  Update UiApplication.cs
-  Merge pull request #1082 from ricaun/patch-2
-  [TYPO] link to 404 (#1102)
-  Fix warnings (#1104)
-  fix non-legacy backdrop when switching themes (#1094)
-  fix: possible null reference exceptions in PasswordBox (#1091)
-  fix: TextBox, NumberBox, PasswordBox  Placeholder Not Working Properly. (#1109)
-  fix:  PlaceholderText may not display promptly under certain circumstances (#1115)
-  Update themes.md (#1114)
-  Update window titlebar color (#1122)
-  fix: possible multiple invocations of the INavigationAware interface methods. (#1116)
-  Update `INotifyCollectionChanged` events in `MenuItems` and `FooterMenuItems` of the `NavigationView` (#1098)
-  Format code
-  Update themes.md (#1124)
-  Revert changes that make it impossible to use {ui:SymbolIcon} as the Value of a Setter (#1159)
-  Fix DynamicScrollViewer not responding to touch events (#1154)
-  fix:SnackbarPresenter might throw ObjectDisposedException. (#1138)
-  Fix MessageBox Button Icons (#1164)
-  chore: update RadioButton.xaml (#1135)
-  Workaround for touch input triggering alongside the hwnd hook on titlebar (#1153)
-  fix: setting NotifyIcon.TooltipText at runtime doesn't work (#1132)
-  Doc: supplement the document content. (#1119)
-  Fix: MessageBox does not support WindowStartupLocation (#1130)
- ... e mais 4 commits

### Release 3

Link: https://github.com/lepoco/wpfui/releases/tag/4.0.0
- Tag: `4.0.0`
- Nome: 4.0.0
- Publicada em: 2025-02-01
- Release anterior (cronológica): `3.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 64

-  Move code and add abstractions
-  Update docs
-  Update notices
-  Update analyzers
-  Update sample
-  Add sample for dialog
-  Simplify demo
-  Merge branch 'development' into feature/4.0
-  Test translations
-  Merge branch 'development' into feature/4.0
-  Merge branch 'development' into feature/4.0
-  Merge branch 'development' into feature/4.0
-  Update interfaces
-  Provide default navigation page provider #1134
-  Update MainWindow.xaml.cs
-  Update README.md
-  Merge branch 'development' into feature/4.0
-  Merge branch 'development' into feature/4.0
-  Merge branch 'development' into feature/4.0
-  Merge pull request #1107 from lepoco/feature/4.0
-  Merge branch 'development' of https://github.com/lepoco/wpfui into development
-  Format code
-  Merge pull request #1166 from lepoco/development
-  Update packages
-  Update docfx.json
-  Update docfx.json
-  Merge pull request #1171 from lepoco/development
-  Use flow from main to release, instead of development
-  Merge pull request #1172 from lepoco/bugfix/update-docs
-  Update pipelines for main development (#1173)
-  Set Expander content height to * instead of Auto (#1186)
-  Fix: failing to correctly trigger the methods of the INavigationAware interface. (#1177)
-  Add support for ARM64, update extensions and docs, allow non-Windows builds (#1196)
-  SystemThemeWatcher Documentation content changes (#1200)
-  [getting-started.md] fixed for English grammar and flow (#1210)
-  perf: Exclude the definition of the CanCenterOverWPFOwnerPropertyInfo field in .NET 8 or higher (#1202)
-  Remove accidentally added characters (#1282)
-  Create top-issues-dashboard.yml (#1286)
-  Move issues
-  Add support for .NET 9 (#1287)
- ... e mais 24 commits

### Release 4

Link: https://github.com/lepoco/wpfui/releases/tag/4.2.1
- Tag: `4.2.1`
- Nome: 4.2.1
- Publicada em: 2026-04-23
- Release anterior (cronológica): `4.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 21

-  fix(controls): Add ItemsPanel to ComboBox to enable GroupStyle support (#1645)
-  fix(controls): Fix NullReferenceException in Arc(#1644)
-  feat(app): Add ability to disable automatic apply of system accent color in `UiApplication` (#1643)
-  fix(controls): Update ContentDialog For TitleBar CenterContent (#1642)
-  fix(controls): NavigationViewItemAutomationPeer followup (#1646)
-  fix(controls): Remove AnimationFactorToValueConverter from CheckBox.xaml (#1649)
-  fix(controls): Fix TextBlock issues (#1640)
-  fix: Add null check for Application.Current (#1684)
-  fix(controls): unhook event on closed fluentwindow (#1682)
-  fix: Optimize LINQ call (#1683)
-  fix: Refactor SystemThemeWatcher WndProc to listen to Windows theme changes (#1677)
-  fix(controls): Fix ProgressRing not restarting properly when visibily changes (#1678)
-  fix: Center align DynamicScrollBar Grid elements (#1676)
-  fix(controls): Fix card automation peers (#1675)
-  fix(controls): fixes #1670 - TitleBar throws NRE when Collapsed (#1671)
-  fix(controls): scroll buttons on horizontal ScrollBar for RTL FlowDirection (#1690)
-  fix(controls): DataGrid editing behavior for ComboBox and CheckBox columns
-  fix(controls): Add ViewportSize bindings to ListView ScrollBars
-  fix(controls): NumberBox need validating new value after applying step change value
-  fix(controls): Proper foreground on Button content
-  fix: Bump dependencies, update docs, format code (#1692)

### Release 5

Link: https://github.com/lepoco/wpfui/releases/tag/4.3.0
- Tag: `4.3.0`
- Nome: 4.3.0
- Publicada em: 2026-05-04
- Release anterior (cronológica): `4.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  fix(controls): Add UpdateAutoSuggestBoxSuggestions call on MenuItemCollection change (#1696)
-  fix(tray): support Unicode for NotifyIcon.TooltipText (#1706)
-  feat(controls): Implement `SpinButtonPlacementMode.Compact` for `NumberBox` (#1709)
-  fix(controls): Change order of triggers for Button (#1702)
-  feat: Bump version (#1710)
