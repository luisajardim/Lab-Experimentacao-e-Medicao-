# cemu-project/Cemu

Repositório: https://github.com/cemu-project/Cemu

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/cemu-project/Cemu/releases/tag/v2.0
- Tag: `v2.0`
- Nome: Cemu 2.0
- Publicada em: 2022-08-22
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/cemu-project/Cemu/releases/tag/v2.1
- Tag: `v2.1`
- Nome: Cemu 2.1
- Publicada em: 2024-08-26
- Release anterior (cronológica): `v2.0-95`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  nn_fp: Implement GetMyComment and UpdateCommentAsync (#1173)
-  Update translation files
-  Preparations for 2.1 (#1306)

### Release 3

Link: https://github.com/cemu-project/Cemu/releases/tag/v2.3
- Tag: `v2.3`
- Nome: Cemu 2.3
- Publicada em: 2024-11-01
- Release anterior (cronológica): `v2.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  Vulkan: Add explicit synchronization on frame boundaries (#1290)
-  boss: Fix BOSS not honoring the proxy_server setting (#1344)
-  Various smaller code improvements (#1343)
-  Add support for fmt 11 (#1366)
-  Vulkan: Protect against uniform var ringbuffer overflow (#1378)
-  Linux: Fix crash on invalid command-line arguments
-  input: Add option to make `show screen` button a toggle (#1383)
-  Windows: Save icons to Cemu user data directory (#1390)
-  input: Fix crash when closing add controller dialog before search completes (#1386)
-  Make `MEMPTR<T>` a little more `T*`-like (#1385)
-  nn_nfp: Implement GetNfpReadOnlyInfo and fix deactivate event

### Release 4

Link: https://github.com/cemu-project/Cemu/releases/tag/v2.4
- Tag: `v2.4`
- Nome: Cemu 2.4
- Publicada em: 2024-11-13
- Release anterior (cronológica): `v2.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  macOS: Fix libusb path for bundle (#1403)
-  macOS: Fix absolute path to libusb dylib (#1405)
-  procui: swap `tickDelay` and `priority` args in callbacks (#1408)
-  nsyshid/libusb: correct error message formatting and print error string on open fail (#1407)
-  nsyshid: Add support for emulated Dimensions Toypad (#1371)
-  FST: Refactoring to fix a read bug + verify all reads
-  erreula: Rework implementation and fix bugs
-  config: Fix receive_untested_updates using the wrong default
-  CI: Remove outdated workflow

### Release 5

Link: https://github.com/cemu-project/Cemu/releases/tag/v2.6
- Tag: `v2.6`
- Nome: Cemu 2.6
- Publicada em: 2025-02-06
- Release anterior (cronológica): `v2.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 22

-  UI: Correctly handle unicode paths during save export
-  Debugger: Added right click context menu to disasm view + small fixes
-  Vulkan: Use cache for sampler objects
-  Play bootSound.btsnd while shaders/pipelines are compiling (#1047)
-  Fix building against Boost 1.87.0 (#1455)
-  build: Add ALLOW_PORTABLE flag (#1464)
-  debug: Fix shader dumping (#1466)
-  Use one CPU emulation thread for --force-interpreter (#1467)
-  Update build instructions for fedora and add troubleshooting step for alternative architectures (#1468)
-  Vulkan: Added R5_G6_B5_UNORM to supported readback formats (#1430)
-  Latte: Implement better index caching (#1443)
-  nsyshid: Make Libusb the Windows backend (#1471)
-  Update precompiled.h
-  nsyshid: Initialise interface index as 0 (#1473)
-  Fix building against fmt 11.1.0 (#1474)
-  Revert "Fix building against fmt 11.1.0 (#1474)"
-  fix building with fmt11 and GCC
-  CI: Update action version
-  Vulkan: Improve post-shutdown cleanup and minor improvements (#1401)
-  coreinit: Time to tick conversion is unsigned
-  coreinit: Clean up time functions
-  BUILD.md: Provide more info about build configuration flags (#1486)
