# mudler/LocalAGI

Repositório: https://github.com/mudler/LocalAGI

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/mudler/LocalAGI/releases/tag/v2.1.0
- Tag: `v2.1.0`
- Nome: v2.1.0
- Publicada em: 2025-06-02
- Release anterior (cronológica): `v2.0.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 105

-  chore(deps): Update dependencies (#42)
-  chore: update telegram
-  chore(deps): bump docker/metadata-action (#43)
-  docs: update README.md (#48)
-  chore(deps): bump github.com/sashabaranov/go-openai from 1.19.4 to 1.38.1 (#47)
-  Update README.md
-  chore(ui): Switch to text-based Bun lock file to allow diffing (#50)
-  fix: correct image name, switch to sd-1.5-ggml as default (#51)
-  chore(deps-dev): bump globals from 15.15.0 to 16.0.0 in /webui/react-ui (#45)
-  fix(githubreader): do not use pointers (#53)
-  fix(github*): pass by correctly owner and repository (#54)
-  feat(ui): Structured observability/status view (#40)
-  feat(browseragent): add browser agent runner action (#55)
-  chore(deps): bump github.com/sashabaranov/go-openai (#63)
-  chore(deps): bump github.com/metoro-io/mcp-golang from 0.9.0 to 0.11.0 (#64)
-  chore(deps-dev): bump react-router-dom in /webui/react-ui (#65)
-  chore(deps-dev): bump eslint-plugin-react-hooks in /webui/react-ui (#67)
-  feat: add history metadata of agent browser (#71)
-  chore: default to gemma-3-12b-it-qat (#60)
-  chore(deps-dev): bump vite from 6.3.1 to 6.3.2 in /webui/react-ui (#69)
-  feat: allow the agent to perform things concurrently (#74)
-  chore: better defaults for parallel jobs (#76)
-  fix: Handle state on agent restart and update observables (#75)
-  feat: local MCP server support (#61)
-  Update README.md (#80)
-  chore(deps): bump actions/checkout from 2 to 4 (#44)
-  feat(browseragent): post screenshot on slack (#81)
-  fix(discord): automatically add 'Bot' prefix to token if missing (#83)
-  fix(docker): Add mcpbox server to extended compose files (#84)
-  chore(mcpbox): use dind (#85)
-  chore(mcpbox): use ubuntu:24.04 as base (#86)
-  feat(ui): Action playground config and parameter forms
-  fix(ci): add DEBIAN_FRONTEND
-  chore(mcpbox): add wget and curl
-  feat(ui): Add summary details of each observable
-  Update README with videos
-  chore(defaults): Enable reasoning by default (#89)
-  feat: add deep research action (#91)
-  fix: set default timeout
-  feat: specify timeout (#97)
- ... e mais 65 commits

### Release 2

Link: https://github.com/mudler/LocalAGI/releases/tag/v2.2.0
- Tag: `v2.2.0`
- Nome: v2.2.0
- Publicada em: 2025-06-30
- Release anterior (cronológica): `v2.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 25

-  feat: improve parameter generation by forcing reasoning (#193)
-  feat: do not use JSON extraction for reasoning (#194)
-  chore(deps): bump github.com/bwmarrin/discordgo from 0.28.1 to 0.29.0 (#197)
-  chore(deps-dev): bump eslint from 9.27.0 to 9.28.0 in /webui/react-ui (#198)
-  chore(deps): bump github.com/JohannesKaufmann/html-to-markdown/v2 from 2.3.2 to 2.3.3 (#199)
-  chore(deps-dev): bump @eslint/js from 9.27.0 to 9.28.0 in /webui/react-ui (#200)
-  chore(deps-dev): bump @types/react from 19.1.4 to 19.1.6 in /webui/react-ui (#201)
-  chore(deps): bump github.com/slack-go/slack from 0.16.0 to 0.17.1 (#202)
-  chore(deps): bump golang.org/x/crypto from 0.38.0 to 0.39.0 (#203)
-  chore(deps-dev): bump react-router-dom from 7.6.1 to 7.6.2 in /webui/react-ui (#204)
-  fix(api): Use RawMessage for nested polymorphic JSON in OpenAI request input (#207)
-  chore(deps-dev): bump @types/react-dom from 19.1.5 to 19.1.6 in /webui/react-ui (#205)
-  chore(deps): bump github.com/sashabaranov/go-openai from 1.40.0 to 1.40.1 (#196)
-  chore(deps-dev): bump @vitejs/plugin-react from 4.5.0 to 4.5.1 in /webui/react-ui (#206)
-  fix: use correct env key in panic (#215)
-  Fix/catch nil panic (#216)
-  chore(deps-dev): bump @vitejs/plugin-react from 4.5.2 to 4.6.0 in /webui/react-ui (#217)
-  fix(multimodal): fix multimodal input in telegram and slack (#219)
-  feat(api): Handle tool calls in responses API
-  chore(deps-dev): bump @types/react from 19.1.6 to 19.1.8 in /webui/react-ui (#213)
-  chore(deps-dev): bump eslint from 9.28.0 to 9.29.0 in /webui/react-ui (#211)
-  Update README with docs on how to create custom actions
-  Add final remarks
-  Update LocalAI images
-  feat(mutlimodal): do parse all images shared in the conversation (#221)

### Release 3

Link: https://github.com/mudler/LocalAGI/releases/tag/v2.2.1
- Tag: `v2.2.1`
- Nome: v2.3.0
- Publicada em: 2025-07-23
- Release anterior (cronológica): `v2.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  chore(deps): bump github.com/sashabaranov/go-openai from 1.40.1 to 1.40.3 (#225)
-  chore(deps-dev): bump eslint from 9.29.0 to 9.30.0 in /webui/react-ui (#228)
-  chore(deps-dev): bump vite from 6.3.5 to 7.0.0 in /webui/react-ui (#226)
-  Add docker compose for amd gpu (#230)
-  chore: Add web search test
-  fix(observability): Show tool calls as the completion of jobs
-  fix(docker): Update model and backend directories (#232)
-  chore(deps-dev): bump @eslint/js from 9.28.0 to 9.30.0 in /webui/react-ui (#227)
-  chore(deps-dev): bump react-router-dom from 7.6.2 to 7.6.3 in /webui/react-ui (#224)
-  chore(deps): bump github.com/slack-go/slack from 0.17.1 to 0.17.2 (#222)
-  chore(deps): bump github.com/slack-go/slack from 0.17.2 to 0.17.3 (#237)
-  chore(deps-dev): bump globals from 16.2.0 to 16.3.0 in /webui/react-ui (#236)
-  chore(deps-dev): bump eslint from 9.30.0 to 9.30.1 in /webui/react-ui (#233)
-  fix(api): Validate input function call result message (#239)
-  chore(deps-dev): bump vite from 7.0.0 to 7.0.2 in /webui/react-ui (#234)
-  chore(deps): bump golang.org/x/crypto from 0.39.0 to 0.40.0 (#244)
-  fix(telegram): correctly process group chat messages

### Release 4

Link: https://github.com/mudler/LocalAGI/releases/tag/v2.4.0
- Tag: `v2.4.0`
- Nome: v2.4.0
- Publicada em: 2025-08-07
- Release anterior (cronológica): `v2.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 5

Link: https://github.com/mudler/LocalAGI/releases/tag/v2.9.0
- Tag: `v2.9.0`
- Nome: v2.9.0
- Publicada em: 2026-05-08
- Release anterior (cronológica): `v2.8.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_
