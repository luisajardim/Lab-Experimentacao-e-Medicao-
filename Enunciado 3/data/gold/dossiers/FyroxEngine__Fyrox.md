# FyroxEngine/Fyrox

Repositório: https://github.com/FyroxEngine/Fyrox

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/FyroxEngine/Fyrox/releases/tag/0.22
- Tag: `0.22`
- Nome: v0.22
- Publicada em: 2021-08-12
- Release anterior (cronológica): `v0.21`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 89

-  update readme
-  added with_root for FileSelectorBuilder
-  open access to SkyBox::textures
-  update readme
-  ability to change FileBrowser filter, improved filter API
-  ability to change path of a resource
-  re-export walkdir
-  Added a mask_char to TextBox and FormattedText
-  remove invalid bone handles when resolving scene
-  Combined `with_mask_char` and `with_no_mask_char`
-  Merge pull request #139 from VictorKoenders/textbox_mask_char
-  Provide a way to alter control_flow passed in from the event loop
-  Add ControlFlow parameter to all on_tick() example methods
-  Merge pull request #140 from pcbeard/GameStateControlFlow
-  update readme
-  added important comment for `feature` field in Intersection struct
-  split particle_system into separate mods
-  fixed compatibility with old scene format
-  fixed CI
-  added `with_particles` and a set of builder-like methods for `Particle`
-  add ability to change depth func to PipelineState
-  fixed particle systems rendering
-  added `#[visit(option)]`
-  added ability to modify particle "soft" boundary sharpness factor
-  add basic deferred decals
-  normals fix for decals
-  fixed decal's texture resolving
-  refactor gbuffer mod
-  fixed decal normals
-  proper decal's normal map blending
-  ability to set color for decals
-  added decal masking
-  fixed clear of default buffer
-  fixed warning
-  refactor resource management
-  update to hrtf 0.7
-  switch from clipboard to copypasta
-  linux ci fix
-  clean up rg3d-resource, remove outdated backward compat code
-  add `define_new_resource` macro
- ... e mais 49 commits

### Release 2

Link: https://github.com/FyroxEngine/Fyrox/releases/tag/v0.24
- Tag: `v0.24`
- Nome: v0.24
- Publicada em: 2022-01-07
- Release anterior (cronológica): `v0.23`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Initial commit
-  added basic functionality
-  updated readme
-  fixed typo
-  added save/load for scene
-  added world outliner (read only test version)
-  added syncing between world outliner and scene selection
-  build fix
-  added correct world outliner syncing, fixed selection issues, added delete command
-  updated plan
-  added instructions how to load scenes
-  fixed gizmo transform in complex node chain
-  added test file browser (wip)
-  added docking manager
-  updated readme, added screenshot
-  embedded scene preview, partial fix for interaction mode gizmo scale
-  added docking manager resize when window resizes
-  added side bar with interaction modes
-  added position, rotation, scale input fields in node editor
-  updated readme
-  changed font
-  added menu prototype (WIP)
-  added link to rg3d engine
-  continue working on main menu, removed entity panel
-  improved scale interaction mode behavior
-  handled unhandled menu items
-  updated readme
-  started adding show/hide functionality in world outliner
-  added welcome message
-  made CommandStack generic, added Command trait
-  fixed rotation interaction mode
-  started adding asset browser
-  build fix after ui refactoring
-  added sceneitem and assetitem widgets, added visibility toggle in WO
-  started adding asset previewer + rustfmt
-  fixed panic when deleting object, fixed spot light defaults
-  added multi selection (WIP)
-  fixed some warnings
-  added multi selection from world outliner and by ctrl+click
-  fixed selection looping
- ... e mais 210 commits

### Release 3

Link: https://github.com/FyroxEngine/Fyrox/releases/tag/v0.28
- Tag: `v0.28`
- Nome: 0.28
- Publicada em: 2022-12-23
- Release anterior (cronológica): `v0.27`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 240

-  working screenshots
-  update dependencies
-  fixed `Operation failed! Reason: Modify { value: dyn Reflect }` error
-  fixed editing properties of 2d collider shader
-  fixed editing of properties for joint2d
-  fix `color_grading_lut` property inspector
-  fixed panic when editing cascades properties of directional light
-  prevent panicking when there's invalid bone handle
-  hide `data` field from inspector for Surface
-  fixed terrain layer deletion from inspector
-  0.27.1
-  mark every key down message as modified in text box widget
-  direct access to Popup widget fields
-  fixed inability to close "orphaned" context menus
-  fixed clippy warnings
-  fixed incorrect rendering of luminance and luminance_alpha textures
-  check GL_ARB_texture_swizzle before use texture swizzle
-  added `invert drag` option for camera settings in the editor
-  added camera movement speed parameter in editor settings
-  provide access to button fields
-  ability to set `selected` flag to `Decorator` widget on build stage
-  more hotkeys for the editor
-  highlight selected interaction mode button
-  ability to add, remove, set items for `MenuItem` widget
-  add list of recent scenes to `File` menu in the editor
-  reload settings when reconfiguring the editor
-  fixed clippy warnings + rustfmt
-  use reflection instead of hand-written commands for absm editor
-  use universal command for parameters collection in absm editor
-  keep tooltips hidden
-  handle rest of panels in `View` menu
-  `Frustum::center`
-  fixed cascaded shadow maps
-  fixed script changing via reflection 
-  Update cargo audit CI
-  Merge pull request #343 from martin-t/audit
-  Merge pull request #323 from thomas992/patch-1
-  fixed script property editor
-  Merge remote-tracking branch 'origin/master'
-  smooth cascaded shadow maps for directional lights
- ... e mais 200 commits

### Release 4

Link: https://github.com/FyroxEngine/Fyrox/releases/tag/v0.30
- Tag: `v0.30`
- Nome: v0.30
- Publicada em: 2023-06-10
- Release anterior (cronológica): `v0.29`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  improved `Graph::find_x` methods
-  `Graph::find_map/find_up_map/find_up_by_name`
-  event passing for scripts
-  more data for absm ActiveStateChanged event
-  configurable size for light pictograms
-  fixed doc tests
-  improved script event api + added routing methods
-  rename script events to script messages
-  script message dispatcher
-  restrict script message payload on `Send` + more impls
-  fixed incorrect script message delivery in case of targeted mode
-  Add a missing reference to the script template
-  Merge pull request #420 from z80maniac/template-script-fix
-  bump version
-  reset user force and torque of rigid bodies
-  refactored scene node life time management
-  fixed message dispatching
-  fixed off-screen ui rendering compatibility with hdr pipeline
-  compound conditions for absm transitions
-  added missing property editor
-  fixed incorrect activation of transition/states during preview mode absm
-  improved color gradient api
-  simplified `color_over_lifetime` field in particle systems
-  property editor for ColorGradient
-  ability to add/remove/change color of color gradient points
-  performance stats
-  fixed potential panic
-  fixed `ParticleSystem::clear_particles`
-  ability to "rewind" particle systems in particle system control panel
-  fixed preview mode for particle systems
-  determinism for particle systems 
-  added missing property editor
-  ability to rewind particle systems to a particular time
-  reset prng state when rewinding particle systems
-  ability to rewind particle systems to a specific time in the editor
-  sync preview checkbox in particle system control panel
-  refactored `Reflect` trait to use closures (wip)
-  continue refactoring
-  refactored handle mapping to new reflection api
-  fixed tests
- ... e mais 210 commits

### Release 5

Link: https://github.com/FyroxEngine/Fyrox/releases/tag/v0.33
- Tag: `v0.33`
- Nome: v0.33
- Publicada em: 2024-01-25
- Release anterior (cronológica): `v0.32`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  updated comments
-  reimplemented A* algorithm
-  Improved readablility
-  Added benchmark for assorted complete grid sizes
-  added test for partial paths
-  added benchmark for when A* is forced to move backwards
-  fixed spelling and added optimization
-  Standardized new benchmarks
-  Created resource io system
-  Changed resource_io visibility and added convience getter
-  Added directory walking and resource is_dir and is_file checking for fbx material search
-  Added send requirement for walking iterator, No-op directory walking on wasm and android
-  Moved use for std::future::ready into the conditional block
-  Use no-op for default walk_directory impl
-  Added directory reading to ResourceIo
-  Added allow(unused) for path to is_dir
-  Added default usages of FsResourceIo for editor
-  Added seperate types for wasm to allow !Send
-  Removed unused import
-  Moved use for walkdir into conditional block
-  Removed wasm specific logic for FileReader as Send is required
-  Updated sound examples to use FsResourceIo
-  Use FsResourceIo for sound tests to fix test errors
-  Small doc corrections
-  Merge pull request #549 from jacobtread/master
-  impl `Visit` for usize/isize
-  added `Reflect`, `Debug`, `Visit` impls for ui widgets
-  `WidgetConstructorContainer`
-  widget container
-  use widget container in the pool
-  impl `Reflect + Debug + Visit` for `UserInterface`
-  fixed scene loading in derived mode
-  save joints binding local frames
-  description for lods
-  Translating the touch event and emitting it to the UI. Need to create WidgetMessages
-  Created widget message variants
-  Added touch event handling to buttons
-  build fix for rustc <1.72
-  bump patch
-  Merge remote-tracking branch 'origin/patch'
- ... e mais 210 commits
