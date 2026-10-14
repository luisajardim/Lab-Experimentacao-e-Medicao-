# Future-House/paper-qa

Repositório: https://github.com/Future-House/paper-qa

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/Future-House/paper-qa/releases/tag/v3.0.0.dev3
- Tag: `v3.0.0.dev3`
- Nome: v3.0.0.dev3
- Publicada em: 2023-06-14
- Release anterior (cronológica): `v3.0.0.dev2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  Update README.md
-  Added memory to query (#140)

### Release 2

Link: https://github.com/Future-House/paper-qa/releases/tag/v3.13.4
- Tag: `v3.13.4`
- Nome: v3.13.4
- Publicada em: 2023-12-05
- Release anterior (cronológica): `v3.13.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  More score parsing improvements (#218)

### Release 3

Link: https://github.com/Future-House/paper-qa/releases/tag/v5.0.4
- Tag: `v5.0.4`
- Nome: v5.0.4
- Publicada em: 2024-09-17
- Release anterior (cronológica): `v5.0.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  `DocMetadataClient` can now take instantiated providers and processors (#414)
-  Promoting agent factories to `Settings` (#407)
-  Add section for `pytest-recording` plugin in `CONTRIBUTING.md`
-  Add stub_data_dir fixture to retraction test (#420)
-  `pytest-recording` docs in `CONTRIBUTING.md` (#410)
-  Fixing `test_crossref_journalquality_fields_filtering` incorrect cassette set up (#423)
-  Broken title search ut (#411)
-  Update pre-commit-ci/lite-action action to v1.0.3 (#422)
-  Pinning min `pymupdf` version (#424)
-  Preventing `Environment`s from sharing one `Docs` (#425)
-  Dropped `PyCryptodome` and `build` dependencies (#426)

### Release 4

Link: https://github.com/Future-House/paper-qa/releases/tag/v5.5.0
- Tag: `v5.5.0`
- Nome: v5.5.0
- Publicada em: 2024-11-20
- Release anterior (cronológica): `v5.3.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 40

-  Renamed to PQASession type (#653)
-  Lock file maintenance
-  Ability to zero-shot `gen_answer` (#658)
-  Lock file maintenance
-  Moving to `uv` dependency groups (#660)
-  Lock file maintenance
-  Convert citation to formatted_citation usage where necessary (#666)
-  Catch edge case where externalIds field is None (#668)
-  Made o1 temperature issue a warning, instead of valueerror (#669)
-  Added train and eval splits' questions and DOIs (#662)
-  `fake` agent allowing timeouts or exceptions, (#672)
-  Optional `AnswerSetting.max_answer_attempts` to allow a new unsure branch (#673)
-  Made it so you do not die on invalid tool (#670)
-  Allowing latest `pydantic-settings` and regenerated cassettes (#674)
-  Empty tool calls leading to `done` condition (#671)
-  Changed it to be debug for source quality (#675)
-  Deprecation cycle for `AgentSettings.should_pre_search` (#679)
-  Moved agent prompts to `prompts.py` (#681)
-  Refactor to remove `skip_system` from `LLMModel.run_prompt` (#680)
-  Resolving `evidence_detailed_citations` and `Answer` deprecations (#682)
-  Fixed agent prompt names and contents after #681 mess up (#683)
-  Removed `tool_names` validation for `gen_answer` being present (#685)
-  Fixing `test_evaluation` logic bugs (#686)
-  Removed `GenerateAnswer.FAILED_TO_ANSWER` as its unnecessary (#691)
-  Allowing serialized `Settings` in `get_settings` (#688)
-  Fixed LDP runner's `TRUNCATED` not calling `gen_answer`, and documented `AgentStatus` (#690)
-  Removed `gen_answer`'s dead argument `question` (#689)
-  Making sure we copy distractors (#694)
-  Created `complete` tool to allow unsure answers (#684)
-  Added missing `test_from_question` cassette (#696)
-  Moved `fake` agent to LLM propose `complete` tool (#695)
-  Default to ordered tool calls (#697)
-  Lock file maintenance (#699)
-  Refactored `TestGradablePaperQAEnvironment` for DRY code (#702)
-  Fixing `PaperQAEnvironment.reset` respecting `mmr_lambda` and `text_hashes` (#703)
-  Removed `"cannot answer"` literals and added `reset` tool (#698)
-  Update all non-major dependencies (#705)
-  Fixing `LitQAEvaluation` bugs: incorrect reward indices, not using LLM's native knowledge (#708)
-  Adding filters to paper-qa Docs (#707)
-  Fixed mutably defaulted `NumpyVectorStore.texts` (#711)

### Release 5

Link: https://github.com/Future-House/paper-qa/releases/tag/v5.14.0
- Tag: `v5.14.0`
- Nome: v5.14.0
- Publicada em: 2025-02-22
- Release anterior (cronológica): `v5.13.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  Propagates llmclient changes to pqa (#839)
