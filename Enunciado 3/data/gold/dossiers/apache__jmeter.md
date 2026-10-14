# apache/jmeter

Repositório: https://github.com/apache/jmeter

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/apache/jmeter/releases/tag/rel/v5.6
- Tag: `rel/v5.6`
- Nome: v5.6
- Publicada em: 2023-06-24
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/apache/jmeter/releases/tag/rel/v5.4.2
- Tag: `rel/v5.4.2`
- Nome: v5.4.2: Update log4j2 to 2.16.0 to fix CVE-2021-44228
- Publicada em: 2023-06-24
- Release anterior (cronológica): `rel/v5.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Update log4j2 to 2.16.0 to fix CVE-2021-44228: Apache Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints
-  prepare new version 5.4.2
-  prepare new version 5.4.2: change version number
-  prepare new version 5.4.2: Add Matt Sicker's b4c70893b62babe8 key for org.apache.logging.log4j

### Release 3

Link: https://github.com/apache/jmeter/releases/tag/rel/v5.4.3
- Tag: `rel/v5.4.3`
- Nome: v5.4.3: Update log4j to 2.17.0 (fix CVE-2021-45105)
- Publicada em: 2023-06-24
- Release anterior (cronológica): `rel/v5.4.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 3

-  Update log4j to 2.17.0 (fix CVE-2021-45105)
-  prepare new version 5.4.3
-  prepare new version 5.4.3, update changes pages

### Release 4

Link: https://github.com/apache/jmeter/releases/tag/rel/v5.6.1
- Tag: `rel/v5.6.1`
- Nome: v5.6.1
- Publicada em: 2023-07-10
- Release anterior (cronológica): `rel/v5.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Update JMeter screen preview (#575)
-  5.3 is not a minor bugfix
-  Update screenshot
-  Add the 5.3 release
-  docs: clarify how to configure InfluxDB v1 and InfluxDB v2 (#592)
-  Update neo4j-java-driver from 1.7.5 to 4.0.1 (#594)
-  Prepare next development round
-  More precise error message, when no datasource value can be found in JDBC sampler
-  Log exeptions reported via JMeterUtils#reportToUser even when in GUI mode
-  Fix tests to check for changed error messages
-  Correct javadoc and a bit of spacepolice
-  Get rid of warnings in unit test
-  Re-use methods in unit tests
-  Extract functionality to get methods into private method
-  Remove deprecated sudo setting.
-  Spacepolice
-  Correct xml markup
-  Bug 64448 - User Defined Variable Duplication in Right Click Context
-  Bug 64499 - Exiting JMeter when "jmeterengine.stopfail.system.exit=true"
-  Show how to setup rotating logs
-  Fix documentation: sampleresult.timestamp.start is false by default
-  Updated Darklaf to 2.2.1 (from 2.1.1)
-  Better parse curl commands with backslash at line endings and support PUT method with data arguments
-  Try to use neutral words
-  Use neutral wording
-  Revert to darklaf 2.1.1 as 2.2.x break Guis that use GroupLayout
-  Updated commons-collections to 4.4 (from 3.2.2)
-  Allow build failurs on s390x on travis.
-  Use same wording as the docs for mongodb
-  Add option to create a diff
-  darklaf update was reverted (plus one typo correction)
-  No space in front of a colon
-  Markup changes
-  Fix ProxyControl timer that prevents correct shutdown
-  Upgrade darklaf to fix bug 64510, 64543
-  Duplicate entry in changelog
-  Bug 64547 - Report/Dashboard: Ensure graphs Response codes per second is
-  Use StringUtils#defaultIfBlank instead of simulating it
-  Ensure all buttons added to the toolbar behave/look consistently. (#599)
-  Updates with latest bug fixes and mention Weisj
- ... e mais 210 commits

### Release 5

Link: https://github.com/apache/jmeter/releases/tag/rel/v5.6.3
- Tag: `rel/v5.6.3`
- Nome: v5.6.3
- Publicada em: 2024-01-09
- Release anterior (cronológica): `rel/v5.6.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 157

-  Add the 5.6.2 release
-  Fix computation of min in Summary report
-  Add space before stopping_test_host
-  Add references to boms in the generated pom.xml files
-  Fix link to bug database
-  Resolve checkstyle cache miss
-  Fixed Chinese translation errors in multiple languages
-  fix(deps): update dependency org.neo4j.driver:neo4j-java-driver to v4.4.12
-  fix(deps): update dependency org.jetbrains.kotlinx:kotlinx-coroutines-bom to v1.7.3
-  fix(deps): update dependency org.eclipse.jgit:org.eclipse.jgit to v5.13.2.202306221912-r
-  fix(deps): update dependency org.codehaus.groovy:groovy-bom to v3.0.19
-  chore: add checksum for jgit-5.13.2.202306221912
-  fix(deps): update com.miglayout to v11
-  chore: group JMH updates in Renovate
-  chore: group jmespath updates in Renovate
-  Revert "fix(deps): update com.miglayout to v11"
-  chore: miglayout 11.0+ requires Java 11, so we can't upgrade yet
-  chore: set Java LTS release for build script compilation
-  chore: add explicit dependency from kaptGenerateStubsKotlin on versionClass
-  chore: bump oracle-actions/setup-java to v1.3.2
-  chore: use Java 17 for building the build scripts
-  chore: remove dependency on jetbrains.kotlin.jvm.gradle.plugin in build-logic-commons
-  fix(deps): update kotlin monorepo to v1.9.21
-  chore: use toolchains for kotlin-dsl for Gradle 9 compatibility
-  chore: increase test coverage for Java 21 by testing more distributions
-  fix(deps): update dependency org.mongodb:mongo-java-driver to v2.14.3
-  chore(deps): update release-drafter/release-drafter digest to 09c613e
-  chore: add Java 22 (ignored) version to the build matrix
-  fix(deps): update dependency jacoco to v0.8.11
-  fix(deps): update dependency com.github.tomakehurst:wiremock-jre8 to v2.35.1
-  fix(deps): update dependency net.bytebuddy:byte-buddy to v1.14.10
-  fix(deps): update dependency me.champeau.jmh:me.champeau.jmh.gradle.plugin to v0.7.2
-  fix(deps): update dependency checkstyle to v10.12.5
-  chore(deps): update Gradle to v8.4
-  chore: use proper Gradle release checksum
-  style: fix extra whitespace in src/core/build.gradle.kts
-  chore(deps): update plugin org.gradle.toolchains.foojay-resolver-convention to v0.7.0
-  fix(deps): update org.apache.activemq to v5.16.7
-  fix(deps): update dependency org.ow2.asm:asm to v9.6
-  fix(deps): update dependency org.jsoup:jsoup to v1.16.2
- ... e mais 117 commits
