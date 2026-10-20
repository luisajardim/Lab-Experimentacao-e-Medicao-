# pterodactyl/panel

Repositório: https://github.com/pterodactyl/panel

## Metadados

- Linguagem: PHP

## Releases sorteadas

### Release 1

Link: https://github.com/pterodactyl/panel/releases/tag/v0.7.0
- Tag: `v0.7.0`
- Nome: v0.7.0 (Derelict Dermodactylus)
- Publicada em: 2018-02-17
- Release anterior (cronológica): `v0.7.0-rc.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 546

-  Begin implementation of new request validation, closes #470
-  Push initial implementations of new repository structure
-  Push updates, removes repositories, begins moving functionality to services.
-  Update admin location routes and controller to use service
-  Use valid version... :crab:
-  Push more tests for location services, setup travis CI integration
-  TravisCI Fixes
-  Update composer lock, update travis to skip post-install scripts for composer
-  Try to fix Travis CI failures
-  Add more location tests, more travis CI fix attempts
-  Include code coverage
-  Cleanup user and location controllers.
-  Push more changes to DBHost service.
-  Apply fixes from StyleCI (#501)
-  More service structure testing and configuration
-  Add ApiKey service, cleanup old API key methods
-  Merge branch 'develop' into feature/PTDL-472
-  Apply fixes from StyleCI (#519)
-  Merge branch 'develop' into feature/PTDL-472
-  Addition of repository to ease testing and maintainability
-  Update location and databasehost services to use repositories
-  Fix terminal scrolling and terminalNotify
-  Add Rust service
-  Add Rust to seeder & rename class to appropriate name
-  Fix StyleCI complaints
-  Merge pull request #534 from ET-Bent/patch-1
-  Most inputs now remember their old values on a failed creation
-  Redirect user to node allocation view after creation, closes #535
-  Merge pull request #540 from OrangeJuiced/develop
-  Update last of existing services to use repositories, includes unit tests
-  Merge branch 'develop' into feature/PTDL-472
-  don't try to apply columns in the relations field...
-  Service refactor to improve organization
-  Add migrations to handle cascade deletions for servers and users
-  Add CS:GO to Source Service Option (#538)
-  Specify ubuntu version & add string validation
-  Created a GMOD Service Option (#542)
-  Update CHANGELOG.md
-  Added a Forge Service Option
-  Remove pesky space
- ... e mais 506 commits

### Release 2

Link: https://github.com/pterodactyl/panel/releases/tag/v0.7.15
- Tag: `v0.7.15`
- Nome: v0.7.15 (Derelict Dermodactylus)
- Publicada em: 2019-08-03
- Release anterior (cronológica): `v0.7.14`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 29

-  Check the boolean itself, not the value.
-  Fix for mass delete error.
-  update php-cs-fixer version
-  update insurgency steam app id (closes #1602)
-  update teamspeak egg (closes #1628)
-  Merge pull request #1652 from pterodactyl/arc-some-fixes
-  Added Disk to overview (issue:1547) (#1569)
-  Reference parent section instead of directly adding scripts to fix issue #1591 (#1598)
-  Merge pull request #1600 from halfpetal/hotfix/1549-wrong-field-ticked
-  Merge pull request #1615 from MatthewSH/hotfix/1614-mass-delete
-  update paper install script
-  fix paper image
-  Merge pull request #1659 from parkervcp/update/paper
-  Updated gmod egg
-  Merge pull request #1664 from pterodactyl/gmod-fix
-  remove paper query port again
-  Merge pull request #1665 from parkervcp/update/paper-again
-  Update CHANGELOG.md
-  Fix database host modification not properly showing SQL errors
-  Fix two-factor token creation for iOS devices, closes #1624
-  Add support for filtering servers in client list-all endpoint
-  Fix Server model to use correct relationship when returning subusers, closes #1589
-  Fix allocations requiring an alias when generated via API.
-  Default to OOM killer being disabled, add back configuration option per-server
-  Fix bulk power when spanning multiple nodes, closes #1526
-  Support special characters in database password, closes #1508
-  Add LOCK permission
-  LOCK TABLES not LOCK
-  Bump for 0.7.15 :100:

### Release 3

Link: https://github.com/pterodactyl/panel/releases/tag/v1.1.1
- Tag: `v1.1.1`
- Nome: v1.1.1 Byedon 🇺🇸
- Publicada em: 2020-11-09
- Release anterior (cronológica): `v1.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Fix allocation permission
-  Fix server state not being updated correctly when adding/removing allocation; closes #2680
-  Update CopyOnClick.tsx
-  Update CopyOnClick.tsx

### Release 4

Link: https://github.com/pterodactyl/panel/releases/tag/v1.6.5
- Tag: `v1.6.5`
- Nome: (sem nome)
- Publicada em: 2021-11-04
- Release anterior (cronológica): `v1.6.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 8

-  Don't force enable-query (#3700)
-  expose uptime to client resources API endpoint (#3705)
-  Update docker-compose.example.yml (#3707)
-  change display format of the container uptime (#3706)
-  fix: use POST for admin logout route (#3710)
-  Fix session management on client API requests; closes #3727
-  Remove tests
-  Fix broken session management for application api

### Release 5

Link: https://github.com/pterodactyl/panel/releases/tag/v1.11.8
- Tag: `v1.11.8`
- Nome: v1.11.8
- Publicada em: 2024-10-24
- Release anterior (cronológica): `v1.11.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 1

-  fix!: use `POST` instead of `DELETE` when disabling 2FA
