# xorbitsai/inference

Repositório: https://github.com/xorbitsai/inference

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/xorbitsai/inference/releases/tag/v0.5.2
- Tag: `v0.5.2`
- Nome: v0.5.2
- Publicada em: 2023-09-27
- Release anterior (cronológica): `v0.5.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  ENH: validate model URI on register (#476)
-  ENH: Skip download for embedding models (#499)
-  ENH: set `trust_remote_code` to true (#500)

### Release 2

Link: https://github.com/xorbitsai/inference/releases/tag/v0.10.3
- Tag: `v0.10.3`
- Nome: v0.10.3
- Publicada em: 2024-04-24
- Release anterior (cronológica): `v0.10.2.post1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  BUG: Fix Launching embedding or reranking models from commandline fails due to PEFT  (#1343)
-  FEAT: support llama-3 family (#1332)
-  DOC: Add new models to README (#1346)
-  FEAT: Add Belle-whisper-large-v3-zh (#1351)
-  BUG: Fix extra parameters issue when auto-recovering models (#1348)
-  DOC: Update README, add FastGPT to integrations (#1355)
-  ENH: fix the max length of codeqwen-7B-chat (#1354)
-  BUG: Fix old rerank models use flag rerank issue (#1350)
-  ENH: Clear cache for embedding and rerank (#1360)

### Release 3

Link: https://github.com/xorbitsai/inference/releases/tag/v0.16.2
- Tag: `v0.16.2`
- Nome: v0.16.2
- Publicada em: 2024-11-01
- Release anterior (cronológica): `v0.16.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  DOC: modify NPU doc (#2485)
-  DOC: Add doc for ocr (#2492)
-  BLD: Remove Python 3.8 & Support Python 3.12 (#2503)
-  BUG: fix bge-reranker-v2-minicpm-layerwise rerank issue (#2495)
-  FEAT: add download from openmind_hub (#2504)

### Release 4

Link: https://github.com/xorbitsai/inference/releases/tag/v1.7.0
- Tag: `v1.7.0`
- Nome: v1.7.0
- Publicada em: 2025-06-13
- Release anterior (cronológica): `v1.6.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 24

-  FEAT: support CogView4 image model (#3557)
-  FEAT: [UI] support model_ability filter for image and video models. (#3563)
-  BUG: Fix dependency (#3566)
-  DOC: update links (#3565)
-  FEAT: [UI] auto-switch to active tab when Running Models page loads. (#3568)
-  FEAT: support first-last-frame to video (#3555)
-  FEAT: [UI] add Japanese and Korean language support. (#3574)
-  FEAT: SeACoParaformer model (#3587)
-  BUG: Fix cmdline (#3589)
-  BUG: fix potential hang for sglang (#3597)
-  FEAT: support verbose_json for funasr family audio2text models (#3591)
-  FEAT: support deepseek-r1-0528 Mixed quantization (#3601)
-  ENH: Support pcm response_format (#3606)
-  DOC: Update CosyVoice doc (#3605)
-  FEAT: support engines for embedding models (#2791)
-  FEAT:support MiniCPM4 Series (#3609)
-  BUG: [UI] fixed the mobile language switching bug. (#3608)
-  BUG:  Fix the error when using Qwen function call with Spring AI. (#3614)
-  FEAT: [UI] add model_engine parameter to embedding model. (#3617)
-  FEAT: add kwargs for transripts client API (#3622)
-  BUG: [UI] fix model_engine parameter bug. (#3620)
-  FEAT: support qwen3 embedding (#3615)
-  FEAT: support qwen3-reranker (#3627)
-  DOC: update models (#3628)

### Release 5

Link: https://github.com/xorbitsai/inference/releases/tag/v1.13.0
- Tag: `v1.13.0`
- Nome: v1.13.0
- Publicada em: 2025-11-15
- Release anterior (cronológica): `v1.12.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 16

-  DOC: added new models (#4206)
-  BUG: Deepseek-OCR error in docker (#4208)
-  ENH: IndexTTS2 stream output (#4213)
-  chore: sync models JSON [audio, embedding, image, llm, rerank, video] (#4214)
-  chore: sync models JSON [audio, embedding, image, llm, rerank, video] (#4226)
-  FEAT: [model] Qwen3-VL-MLX support (#4203)
-  DOC: Xinference 1.12.0 installation issues with uv (#4228)
-  BUG: ensure unique tool call IDs using UUID (#4242)
-  BUG: IndexTTS2-offline-deploy (#4202)
-  FEAT: auto batch embedding (#4197)
-  chore: sync models JSON [audio] (#4243)
-  ENH: add embedding benchmark (#4244)
-  BUG: Fix cache model not shown on audio、video and image (#4247)
-  FEAT: update models via Xinference model hub (#4241)
-  DOC: add model update documentation. (#4246)
-  BLD: Fix CI error caused by peft version (#4249)
