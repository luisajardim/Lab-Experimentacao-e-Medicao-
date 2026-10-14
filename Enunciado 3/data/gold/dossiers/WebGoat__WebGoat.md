# WebGoat/WebGoat

Repositório: https://github.com/WebGoat/WebGoat

## Metadados

- Linguagem: JavaScript

## Releases sorteadas

### Release 1

Link: https://github.com/WebGoat/WebGoat/releases/tag/7.0.1
- Tag: `7.0.1`
- Nome: The OWASP WebGoat 7.0.1 Release
- Publicada em: 2016-02-01
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/WebGoat/WebGoat/releases/tag/v8.1.0
- Tag: `v8.1.0`
- Nome: (sem nome)
- Publicada em: 2020-05-23
- Release anterior (cronológica): `7.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  First attempt to remove JSP and move to Thymeleaf and update to Spring Boot. The Thymeleaf templates can be loaded as snippets which makes it more easy to move away from ECS and create normal HTML pages for a lesson.
-  Fully working WebGoat after migrating to Spring Boot.
-  Images from solutions are loading again
-  Merging changes from Daniel back into the Spring Boot structure
-  Menu options about version, user info work again.
-  Login and logout works together with context root
-  Updating README and moving webapp dir to old
-  Lessons which load JavaScript etc now works
-  Endpoints provided by lessons now work
-  Made lesson resolution with Thymeleaf dynamic
-  Thymeleaf resolver does not need WebSession anymore
-  Thymeleaf works with AsciiDoc
-  clean up
-  Added Docker support.
-  initial support for separation of content from attack in UI
-  initial support for separation of content from attack in UI
-  Turning off caching in spring boot for dev purposes
-  Merge remote-tracking branch 'upstream/feature/spring-boot' into feature/spring-boot
-  Reading yml file based lesson configuration
-  moving attack form to modal/overlay ... initial cut
-  Merge remote-tracking branch 'upstream/feature/spring-boot' into feature/spring-boot
-  Merge pull request #246 from misfir3/feature/spring-boot
-  for the menu part
-  YML config should override lesson class
-  incremental UI changes
-  changing to 'id' for linking in YmlBasedLesson
-  turning off test in the interim
-  committing for local test purposes unrelated to webgoat
-  reverting local test that was committed
-  commenting out incomplete line
-  Getting the attack verification to work
-  Intermediate result for calling multiple lesson endpoints
-  bumping version on feature branch to reflect plans
-  intial rendering of first page/tab/section of content on load
-  Initial client side pagination
-  additional paging work
-  paging mod, binding actions/callback per form within lesson
-  stubbing custom goat file
-  initial test version of CustomGoat.js ... TBD on if we will keep it
-  temp fix
- ... e mais 210 commits

### Release 3

Link: https://github.com/WebGoat/WebGoat/releases/tag/v8.2.0
- Tag: `v8.2.0`
- Nome: v8.2.0
- Publicada em: 2021-07-26
- Release anterior (cronológica): `v8.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 161

-  Remove dep status
-  Cleanup readme
-  Update README.MD
-  Fix Docker link
-  Remove Github pages, too many things to keep in sync.
-  Docker command without -d option to show output int console
-  Update README.MD
-  Only push to 1 Docker repo
-  JWT_refresh.adoc: Fix spelling issues
-  PasswordReset_plan.adoc: Spelling fixes
-  PasswordReset_SecurityQuestions.adoc: Typo fix.
-  PasswordReset_host_header.adoc: Typo fixes
-  Delete unused PasswordReset_password_reset_link.adoc
-  SecurePasswordsAssignment: Fix output formatting
-  InsecureLogin_intro.adoc: Typo fix
-  XXE_plan.adoc: Typo fixes
-  XXE_intro.adoc: Typo fixes
-  XXE_changing_content_type.adoc: Typo fixes
-  IDOR_intro.adoc: Fix 404
-  Function ac intro: Spelling and grammar update
-  Function AC Lesson 1: Spelling and grammar fixes.
-  Function AC User: Spelling and grammar fixes.
-  XSS Quiz: Fix 404
-  Dinis Cruz Blog
-  HTML Tampering mitigation: Typo fixes
-  adjustments for arbitrary user support (openshift guideline) (#830)
-  Correcting incorrect information (#835)
-  Update 1proxysetupsteps.adoc (#854)
-  Small fixes june 2020 (#857)
-  first step
-  first step
-  improving lesson due to issue #845
-  lesson pages updated based on comments for #834 and #836 (#864)
-  chore: update CIA grammar and content
-  Link to the original lesson for the goal
-  Blind XXE lesson blocks including the file in the comment directly
-  fix failing test (order)
-  #839: fix the SQL statement as this one does not express that the `orderBy` clause input is user input
-  #841: Clarify the lesson based on the comments
-  #846: add extra test to verify whether the solution is solved for the original user as well
- ... e mais 121 commits

### Release 4

Link: https://github.com/WebGoat/WebGoat/releases/tag/v2023.5
- Tag: `v2023.5`
- Nome: v2023.5
- Publicada em: 2023-11-23
- Release anterior (cronológica): `v2023.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 96

-  chore: release version 2023.4
-  ci: add distribution in snapshot job
-  chore: back to snapshot version after release
-  docs: add documentation we start using Conventional Commits.
-  ci: add maven and docker to dependabot configuration
-  chore: format markdown file
-  refactor: update challenge code
-  Bump actions/cache from 3.2.5 to 3.2.6
-  chore: bump jose4j from 0.7.6 to 0.9.3 (#1431)
-  chore: bump jsoup from 1.14.3 to 1.15.4 (#1430)
-  chore: bump maven-surefire-plugin from 3.0.0-M5 to 3.0.0-M9 (#1429)
-  chore: bump commons-compress from 1.21 to 1.22 (#1428)
-  chore: bump eclipse-temurin from 17-jre-focal to 19-jre-focal (#1427)
-  chore: bump spotless-maven-plugin from 2.29.0 to 2.33.0 (#1426)
-  Add coverage profile
-  fix: challenge 7 (#1433)
-  chore: bump commons-text from 1.9 to 1.10.0
-  chore: bump maven-enforcer-plugin from 3.0.0 to 3.2.1
-  chore: bump webdrivermanager from 4.3.1 to 5.3.2
-  chore: bump commons-io from 2.6 to 2.11.0
-  Restrict SSRF Regexes
-  chore: bump asm from 9.1 to 9.5 (#1460)
-  chore: bump actions/cache from 3.2.6 to 3.3.1 (#1453)
-  chore: bump jruby from 9.3.6.0 to 9.4.2.0 (#1454)
-  chore: bump bootstrap from 3.3.7 to 5.2.3 (#1441)
-  chore: bump guava from 30.1-jre to 31.1-jre (#1448)
-  Fix typo of HijackSession_content0.adoc
-  chore: bump jacoco-maven-plugin from 0.8.8 to 0.8.10
-  chore: bump jsoup from 1.15.4 to 1.16.1 (#1484)
-  chore: bump maven-checkstyle-plugin from 3.1.2 to 3.2.1 (#1472)
-  chore: bump maven-enforcer-plugin from 3.2.1 to 3.3.0 (#1468)
-  chore: bump cglib-nodep from 2.2 to 3.3.0 (#1470)
-  chore: bump zxcvbn from 1.5.2 to 1.7.0 (#1471)
-  feat: upgrade to Spring Boot version 3 (#1477)
-  bug: fix Java image inside Docker file
-  chore: bump spring-boot-starter-parent from 3.0.5 to 3.1.0 (#1497)
-  chore: bump maven-checkstyle-plugin from 3.2.1 to 3.3.0 (#1496)
-  chore: bump maven-surefire-plugin from 3.0.0-M9 to 3.1.0 (#1499)
-  fix: robotframework fails due to updated dependencies (#1508)
-  chore: bump docker/build-push-action from 4.0.0 to 4.1.0 (#1501)
- ... e mais 56 commits

### Release 5

Link: https://github.com/WebGoat/WebGoat/releases/tag/v2026.4
- Tag: `v2026.4`
- Nome: v2026.4
- Publicada em: 2026-09-17
- Release anterior (cronológica): `v2026.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  chore: back to snapshot after v2026.3 (#2530)
-  fix sending mail internally inside docker (#2539)
