# gitbucket/gitbucket

Repositório: https://github.com/gitbucket/gitbucket

## Metadados

- Linguagem: Scala

## Releases sorteadas

### Release 1

Link: https://github.com/gitbucket/gitbucket/releases/tag/1.7
- Tag: `1.7`
- Nome: (sem nome)
- Publicada em: 2013-10-25
- Release anterior (cronológica): `1.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 125

-  (refs #33)Match committer by mail address.
-  Merge branch 'master' into #33_match-by-email
-  (refs #33)Use RequestCache instead of AccountService directly.
-  allow users to build a war on Linux
-  Update README.md
-  GitBucket 1.6 released.
-  Update README.md
-  (refs #106)Skip migration if the current version is illegal.
-  (refs #106)Don't use DbStarter because GitBucket does not use tcp server and it also create connection for each transaction.
-  Merge branch 'master' of https://github.com/takezoe/gitbucket
-  Add org.h2.Driver.load().
-  (refs #108)Add ZIP download button to the repository viewer tab.
-  (refs #38)Add reverting wiki from history.
-  Fix commit message for Wiki editing.
-  Clone Wiki working repository if it does not exist before reverting.
-  (refs #109)Change link color for absent Wiki pages.
-  Add testcase example.
-  Fix bug dot not skip migration when first init
-  Merge pull request #110 from tanacasino/fix/migration-skip
-  (refs #73)Add Wiki conflict detection and some fix.
-  Add FileUtil#getContentType().
-  (refs #84)Add jquery.elastic and apply to issue and comment textarea.
-  Add testcase.
-  Add testcase for Pagination.
-  Did a lot of design-optimizations
-  Fix for pull request #119 to take some part of design fix.
-  Fix typo when assigning issues
-  Merge pull request #122 from lucas-clemente/patch-1
-  (refs #116)Add --host option to bind Jetty connector to the specified hostname.
-  Merge branch 'buildXML' of https://github.com/ssogabe/gitbucket
-  Add testcase for AvatarImageProvider.
-  (refs #121)Optimize push performance for a lot of commit.
-  Fix branch name.
-  (refs #121)Configure maxIdleTime and soLingerTime.
-  (refs #121)Create WebHookPayload only when web hook has been registered.
-  Remove debug code.
-  (refs #120)URL encode branch name except '/'.
-  Add padding around repository readme content
-  Add full name to account and use it to create commits (#125)
-  Merge pull request #126 from robinst/readme-padding
- ... e mais 85 commits

### Release 2

Link: https://github.com/gitbucket/gitbucket/releases/tag/2.7
- Tag: `2.7`
- Nome: (sem nome)
- Publicada em: 2014-12-29
- Release anterior (cronológica): `2.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 20

-  Enable contrib init file and RPM's spec file to run on RHEL 6/CentOS 6 as non root user.
-  (refs #9) Comments for commit and diff
-  Merge pull request #564 from mrkm4ntr/coment-for-diff
-  (refs #564)Change the attached files directory to /commens from /issues
-  (refs #564)Fix for repository renaming
-  (refs #567)Fix condition of repository search for issues.
-  Add SSH clone url option when enabled SSH access
-  (refs #577)Remove all HTML tags in Markdown
-  (refs #578)Clean original and parent repository information when it's deleted
-  (refs #578)Add migration for repositories which have removed parent or origin repository.
-  add enableTaskList to post params for _preview
-  Merge pull request #579 from banjun/fix-editor-preview-NoSuchElementException-enableTaskList
-  Fix a few issues detected by static analysis
-  Merge pull request #580 from HairyFotr/patch-lint
-  Merge pull request #561 from torutk/rpm_nonroot
-  Fix bug on showing inline comments in Pull Request.
-  Merge pull request #581 from mrkm4ntr/fix-comment-in-pr
-  Merge pull request #556 from michaeljayt/add-ssh-clone-url
-  Fix for #581. Column name and CSS is changed.
-  Update README.md for 2.7 release

### Release 3

Link: https://github.com/gitbucket/gitbucket/releases/tag/3.10
- Tag: `3.10`
- Nome: (sem nome)
- Publicada em: 2015-12-29
- Release anterior (cronológica): `3.9`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 89

-  Moving to Bootstrap3
-  Add bootstrap-theme-github
-  Merge branch 'master' into css_bootstrap3
-  Fix header styles
-  Fix sidebar style
-  Adjust styles for Bootstrap3
-  Fix global header style
-  Fix styles
-  Fix branch list styles
-  Fix styles
-  Fix issue styles
-  Fix pull request creation form style
-  Fix commit list style
-  Fix diff styles
-  Fix styles of issues and pull requests
-  Fix fork button
-  Merge branch 'master' of https://github.com/takezoe/gitbucket into css_bootstrap3
-  Merge branch 'css_bootstrap3' of https://github.com/takezoe/gitbucket into css_bootstrap3
-  Fix styles
-  Merge branch 'master' into css_bootstrap3
-  Fix styles
-  Fix styles of the repository creation page and more
-  Fix styles of system administration page
-  Merge branch 'master' into css_bootstrap3
-  Fix styles of account and group creation page
-  Fix styles of plugins page
-  Fix sidebar style
-  Fix styles of repository setting pages
-  Fix ZeroClipboard button
-  Fix borderd table style
-  Fix issue search box
-  Fix typo
-  Use customized Bootstrap3 theme
-  Fix tables and some pages
-  Fix styles
-  Use Bootstrap panels instead of GitBucket original styles
-  Fix label editing form
-  Fix table vertical border
-  Fix milestone creation / editing form
-  Remove unused bootstrap files
- ... e mais 49 commits

### Release 4

Link: https://github.com/gitbucket/gitbucket/releases/tag/4.30.0
- Tag: `4.30.0`
- Nome: 4.30.0
- Publicada em: 2018-12-15
- Release anterior (cronológica): `4.29.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 122

-  Upgraded mariadb-java-client: 2.2.6 -> 2.3.0
-  Upgraded postgresql jdbc: 42.2.4 -> 42.2.5
-  apache-sshd: 1.6.0 -> 1.7.0
-  tika-core: 1.17 -> 1.19
-  commons-compress: 1.15 -> 1.18
-  httpclient: 4.5.4 -> 4.5.6
-  Merge pull request #2155 from uli-heller/mariadb-jdbc-230
-  Merge pull request #2158 from uli-heller/tika-1.19
-  Merge pull request #2159 from uli-heller/commons-compress-118
-  Merge pull request #2160 from uli-heller/httpclient-456
-  Merge branch 'master' into postgresql-jdbc-4225
-  Merge pull request #2156 from uli-heller/postgresql-jdbc-4225
-  Merge branch 'master' into apache-sshd-170
-  Merge pull request #2157 from uli-heller/apache-sshd-170
-  Upgraded apache-sshd: 1.7.0 -> 2.1.0
-  Fixes for apache-sshd-2.1.0: Package name for Command and CommandFactory
-  Fixes for apache-sshd-2.1.0: use java.nio.file.Path instead of java.io.File
-  Fixes for apache-sshd-2.1.0: Fixed package for 'UnknownCommand' - closes #2161
-  Split ApiController
-  add 404 for post/put/delete/patch. see #1445
-  fix comments
-  Add removeUser method for move responsibility of calling hooks
-  Move management of directories and calling hooks from Controller to Service
-  Move locks from Controller to Service and other changes.
-  Merge pull request #2163 from kounoike/pr-refactor-apicontroller
-  Merge pull request #2162 from uli-heller/apache-sshd-210
-  Move some methods to Service from Controller.
-  fix test
-  remove unused argument(baseUrl)
-  Move webhook call to service
-  Merge remote-tracking branch 'upstream/master' into pr-call-hook-moveto-service
-  fix test's inheritances
-  fix visibility for test
-  Update version to 4.30.0-SNAPSHOT
-  Add suspendAccount method
-  add missing ApiXXControllerBase
-  scalafmt
-  tika: Upgraded to 1.19.1
-  jgit: Upgraded to 5.1.2
-  Merge pull request #2166 from uli-heller/tika-1191
- ... e mais 82 commits

### Release 5

Link: https://github.com/gitbucket/gitbucket/releases/tag/4.35.1
- Tag: `4.35.1`
- Nome: (sem nome)
- Publicada em: 2020-12-28
- Release anterior (cronológica): `4.35.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  Show commit status at commits tab of pull request (#2606)
-  Bump to sbt 1.4.6, Scala 2.13.3, and Scalatra 2.7.1 (#2609)
-  Fix WEB_HOOK table migration issue in 4.35.0 (#2610)
-  Call webhook when pull request is merged (#2611)
-  Resurrect ActivityComponent for binary compatibility in 4.35.1 (#2612)
-  Release 4.35.1
