# d99kris/nchat

Repositório: https://github.com/d99kris/nchat

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/d99kris/nchat/releases/tag/v2.40
- Tag: `v2.40`
- Nome: v2.40
- Publicada em: 2022-03-26
- Release anterior (cronológica): `v2.26`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/d99kris/nchat/releases/tag/v3.60
- Tag: `v3.60`
- Nome: v3.60
- Publicada em: 2023-06-25
- Release anterior (cronológica): `v3.39`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 3

Link: https://github.com/d99kris/nchat/releases/tag/v4.86
- Tag: `v4.86`
- Nome: v4.86
- Publicada em: 2024-06-04
- Release anterior (cronológica): `v4.50`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 4

Link: https://github.com/d99kris/nchat/releases/tag/v5.15.26
- Tag: `v5.15.26`
- Nome: v5.15.26
- Publicada em: 2026-05-16
- Release anterior (cronológica): `v5.14.44`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 26

-  fixes #502 - improved mime type detection
-  fix cmake warning
-  skip installing themes and update themes doc
-  add ayu-dark and gruvbox-dark-hard themes (#507)
-  fix make.sh install to skip sudo if already root user (#508)
-  update whatsmeow to 20260325 from tulir/whatsmeow@dbc4f26
-  update signalmeow to 20260324 from mautrix/signal@73a8a77
-  whatsapp robustness fixes
-  signal robustness fixes
-  add protocol suffix in desktop notification name
-  add protocol/profile level directory locking
-  fix whatsapp sending audio messages
-  remove non-critical warning log
-  fix telegram local reflecting removal of own reaction when being the last reaction
-  update tdlib to 1.8.63 from tdlib/td@f06b0ba
-  update whatsmeow to 20260416 from tulir/whatsmeow@3ff20cd
-  update signalmeow to 20260416 from mautrix/signal@1f45d1a
-  fix signal abi mismatch after libsignal ref bump
-  github ci: bump actions/checkout and actions/cache to v5
-  fixes #516 - improve view once handling
-  add support for message edited indicator
-  improve handling of custom message deletion (message_delete modes 2 and 3)
-  fixes #519 - add support for pinned message indicator and jump to pinned message (telegram and whatsapp)
-  fixes #520 - add support for pin/unpin of selected message (telegram)
-  restrict custom message_delete to whatsapp and signal
-  add support for passing custom dev cmake args

### Release 5

Link: https://github.com/d99kris/nchat/releases/tag/v5.18.20
- Tag: `v5.18.20`
- Nome: v5.18.20
- Publicada em: 2026-08-15
- Release anterior (cronológica): `v5.17.26`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 22

-  remove musl whatsapp/signal warnings for official patched-go builds
-  update doc
-  support user-writable install prefix in make.sh
-  update license doc
-  fixes #551 - strip double-width padding for wide chars irrespective of emoji setting
-  update doc with arch nchat-bin install instructions (#563)
-  fixes #560 - add support for receiving whatsapp video note messages
-  fixes #315 - support re-downloading whatsapp/signal attachments after profile tmp dir cleared
-  fixes #320 - auto-retry failed attachment downloads
-  update tdlib to 1.8.66 from tdlib/td@a9966eb
-  update whatsmeow to 20260718 from tulir/whatsmeow@fac667d
-  update signalmeow to 20260716 from mautrix/signal@4bbfe7e
-  add scheduled workflow to delete actions artifacts after one day
-  fixes #556 - match accented and mixed-case characters in contact, chat and message search
-  fixes #522 - show chat history for whatsapp unarchived chats without restart
-  add build check for common go dependency mismatch between whatsapp and signal
-  update whatsmeow to 20260730 from tulir/whatsmeow@662ad1d
-  update signalmeow to 20260723 from mautrix/signal@6e57bf3
-  add script to verify combined whatsapp and signal go build on dependency mismatch
-  relax common go dependency check to compare base versions only
-  add configurable ctrl and meta key prefixes for help bar (#572)
-  update signalmeow to 20260807 from mautrix/signal@8c7333a
