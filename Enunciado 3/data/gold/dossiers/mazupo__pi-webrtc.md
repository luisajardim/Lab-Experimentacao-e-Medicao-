# mazupo/pi-webrtc

Repositório: https://github.com/mazupo/pi-webrtc

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/mazupo/pi-webrtc/releases/tag/v1.0.6-rc.2
- Tag: `v1.0.6-rc.2`
- Nome: v1.0.6-rc.2
- Publicada em: 2025-03-21
- Release anterior (cronológica): `v1.0.6-rc.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  feat: enable libcamera selection in addition to v4l2
-  chore: set libcamera:0 as default and refine setup instructions
-  chore: update download link to v1.0.6-rc.1
-  fix: correct description error for V4L2 device
-  perf: write image to virtual camera via os writer
-  feat: add YOLO virtual camera streaming to V4L2 loopback
-  refactor: rename codec folder to codecs and mv v4l2 codecs to it
-  Merge pull request #252 from TzuHuanTai/refactor/move-v4l2-codecs-to-codecs-folder
-  fix: check the stun url
-  feat: run multi-signaling service simutaniously
-  fix: version label

### Release 2

Link: https://github.com/mazupo/pi-webrtc/releases/tag/v1.1.0
- Tag: `v1.1.0`
- Nome: v1.1.0
- Publicada em: 2025-05-15
- Release anterior (cronológica): `v1.0.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 3

Link: https://github.com/mazupo/pi-webrtc/releases/tag/v1.3.2
- Tag: `v1.3.2`
- Nome: v1.3.2
- Publicada em: 2026-04-11
- Release anterior (cronológica): `v1.3.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  refactor: remove redundant link libs
-  fix: atomic callback handling for thread safety
-  refactor: video processing components to use configuration structs
-  chore: upgrade to clang 20 and protobuf v31.1
-  refactor: update WebRTC API usage from `rtc::` to `webrtc::` namespace and adopt modular peer connection factory
-  chore: upgrade libwebrtc to m146

### Release 4

Link: https://github.com/mazupo/pi-webrtc/releases/tag/v3.0.0
- Tag: `v3.0.0`
- Nome: v3.0.0
- Publicada em: 2026-09-03
- Release anterior (cronológica): `v2.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/mazupo/pi-webrtc/releases/tag/v3.0.1
- Tag: `v3.0.1`
- Nome: v3.0.1
- Publicada em: 2026-09-16
- Release anterior (cronológica): `v3.0.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 19

-  chore: update links and references to the new repository
-  chore: update api urls
-  chore: add gamepad usage docs and example script
-  chore: update links to new domain
-  fix: convert v4l2 camera frames with libyuv on jetson
-  feat: add a jetson nvdec decoder for compressed v4l2 cameras
-  fix: warn failed v4l2 control in logs and skip inapplicable ones
-  fix: clear the encode callback on v4l2 h264 encoder release
-  fix: incorrect AV1 encoder modes declared on jetson
-  fix: set transceiver to sendonly
-  fix: make whep endpoint work with browser players
-  fix: stop whep peers from renegotiating on their own
-  refactor: rename http-port to whep-port
-  docs: simplify signaling and advanced guides
-  feat: route whep streams by camera alias
-  fix: keep audio transceivers sendrecv
-  fix: attach audio capturer to the audio device module
-  ci: rename build workflows by target platform
-  ci: publish private builds to sponsor repos
