# teamhanko/hanko

Repositório: https://github.com/teamhanko/hanko

## Metadados

- Linguagem: Go

## Releases sorteadas

### Release 1

Link: https://github.com/teamhanko/hanko/releases/tag/backend/v0.10.0
- Tag: `backend/v0.10.0`
- Nome: v0.10: Webhooks, Account Linking, Passkey Names
- Publicada em: 2024-02-16
- Release anterior (cronológica): `backend/v0.9.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 75

-  feat: add support for zh-CN locale in passcode mails
-  chore(deps): bump golang.org/x/crypto from 0.15.0 to 0.16.0 in /backend
-  chore(deps): bump golang.org/x/oauth2 from 0.14.0 to 0.15.0 in /backend
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend
-  feat(i18n): add italian translations
-  Fixed typo (#1238)
-  chore(deps): bump github.com/go-webauthn/webauthn in /backend
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend 
-  chore(deps): bump github.com/nicksnyder/go-i18n/v2 in /backend
-  chore(deps): bump github.com/lestrrat-go/jwx/v2 in /backend
-  chore(deps-dev): bump vite from 4.4.9 to 4.4.12 in /frontend
-  chore(deps): bump github.com/go-webauthn/webauthn in /backend
-  fix: set cookie secure flag
-  chore(deps): bump github.com/google/uuid from 1.4.0 to 1.5.0 in /backend
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend 
-  chore(deps): bump follow-redirects from 1.15.2 to 1.15.4 in /frontend
-  chore(deps): bump follow-redirects from 1.15.1 to 1.15.4 in /docs
-  chore(deps): bump github.com/lestrrat-go/jwx/v2 in /backend
-  chore(deps): bump golang.org/x/oauth2 from 0.15.0 to 0.16.0 in /backend
-  chore(deps): bump golang.org/x/crypto in /quickstart
-  chore(deps): bump github.com/labstack/echo/v4 in /backend
-  chore(deps): bump github.com/go-webauthn/webauthn in /backend
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend
-  feat(webhooks): add webhooks
-  feat(webhooks): add tests and fix review issues
-  fix(webhooks): add event param to testManager
-  fix(webhooks): add removed ID to CreateUserResponse
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend
-  chore(deps): bump github.com/go-playground/validator/v10 in /backend
-  feat(admin api): add user update endpoints
-  fix(admin api): sync with docs spec
-  chore(deps): bump github.com/brianvoe/gofakeit/v6 in /backend
-  chore(deps): bump github.com/google/uuid from 1.5.0 to 1.6.0 in /backend
-  chore(deps): bump github.com/lestrrat-go/jwx/v2 in /quickstart
-  fix(review): fix review findings
-  fix(tests): fix timing issues
-  feat(webhooks): add disable option for time expiration
-  Merge branch 'main' into feat/692-webhooks
-  improve(passkeys): improve passkey naming
- ... e mais 35 commits

### Release 2

Link: https://github.com/teamhanko/hanko/releases/tag/backend/v0.11.0
- Tag: `backend/v0.11.0`
- Nome: v0.11: Sign in with Microsoft, custom email sending
- Publicada em: 2024-04-29
- Release anterior (cronológica): `backend/v0.10.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  docs: add link to discord guide in backend readme
-  feat(thirdparty): add microsoft provider
-  Update LICENSE (#1432)
-  Update README.md (#1433)
-  chore(deps): bump github.com/labstack/echo/v4 in /backend
-  fix: fix saml login for existing users (#1434)
-  [FEAT] disable email delivery (#1419)
-  chore(deps): bump golang.org/x/net from 0.21.0 to 0.23.0 in /quickstart
-  chore(deps): bump github.com/labstack/echo-contrib in /backend
-  fix: don't override error before return (#1447)
-  chore: update versions to v0.11.0

### Release 3

Link: https://github.com/teamhanko/hanko/releases/tag/backend/v1.5.1
- Tag: `backend/v1.5.1`
- Nome: v1.5.1
- Publicada em: 2025-03-31
- Release anterior (cronológica): `backend/v1.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 10

-  chore(deps): bump github.com/sethvargo/go-limiter in /backend
-  chore(deps): bump github.com/ory/dockertest/v3 in /backend
-  chore(deps): bump github.com/go-jose/go-jose/v3 in /backend
-  chore(deps): bump github.com/coreos/go-oidc/v3 in /backend
-  chore(deps): bump github.com/nicksnyder/go-i18n/v2 in /backend
-  chore(deps): bump github.com/go-playground/validator/v10 in /backend
-  chore(deps): bump github.com/tidwall/gjson in /backend
-  fix: migration issues
-  feat: add passkey option to login method chooser (#2100)
-  chore: update versions to 1.5.1 (#2104)

### Release 4

Link: https://github.com/teamhanko/hanko/releases/tag/backend/v2.2.0
- Tag: `backend/v2.2.0`
- Nome: Hanko 2.2: PKCE
- Publicada em: 2025-10-28
- Release anterior (cronológica): `backend/v2.1.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  fix: user verification on passkey creation
-  fix: change module name corresponding to version
-  fix: add missing module name change
-  fix: remove wrong import
-  fix: use correct module path when generating json schema
-  Merge pull request #2257 from teamhanko/fix-module-name
-  fix: export the Claims type (#2268)
-  fix: check for SAML before email existence (#2270)
-  feat: add auth prompt config option (#2260)
-  PKCE OAuth flow (#2266)
-  chore: autogenerate config JSON schema (#2271)
-  chore: increase version numbers (#2274)

### Release 5

Link: https://github.com/teamhanko/hanko/releases/tag/backend/v2.2.1
- Tag: `backend/v2.2.1`
- Nome: Hanko 2.2.1
- Publicada em: 2025-11-13
- Release anterior (cronológica): `backend/v2.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  fix: consistently use persisters with connection (#2276)
-  fix: don't show the divider on login (#2277)
-  fix: unwarranted passcode data in webhooks (#2279)
-  feat: add last used badge (#2283)
-  fix: ensure WebAuthn session data expires time is in UTC (#2287)
-  feat: add flow locking mechanism (#2285)
-  fix: prefilled email and username attribute handling
-  refactor: make setting identifier and its type on login more explicit
-  fix: backend handling of prefilled username and email
-  fix: mode attribute handling
-  docs: fix redis config password schema (#2293)
-  feat: change default thirdparty prompt parameter (#2292)
-  Merge branch 'main' into fix-elements-attribute-handling
-  fix: commit references in comments
-  Merge pull request #2295 from teamhanko/fix-elements-attribute-handling
-  Update README to include 2FA in API features (#2297)
-  chore: increase version numbers (#2298)
