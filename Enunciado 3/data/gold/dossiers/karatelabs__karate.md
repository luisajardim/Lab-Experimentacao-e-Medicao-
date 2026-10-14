# karatelabs/karate

Repositório: https://github.com/karatelabs/karate

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/karatelabs/karate/releases/tag/v0.2.2
- Tag: `v0.2.2`
- Nome: (sem nome)
- Publicada em: 2017-03-02
- Release anterior (cronológica): `v0.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  now can combine embedded expressions referring to '$' in rhs of match expressions - which closes #19
-  fixed typo in archetype sample package name, actually revamped whole example as well which fixes #22
-  improved regex matching of script eval, which fixes #21
-  release v0.2.2

### Release 2

Link: https://github.com/karatelabs/karate/releases/tag/v0.6.1
- Tag: `v0.6.1`
- Nome: (sem nome)
- Publicada em: 2017-10-08
- Release anterior (cronológica): `v0.6.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 56

-  bump version for dev
-  realized what the subtle race condition was
-  minor cleanup refactoring and doc edits
-  refactoring, avoid code duplication
-  refactoring cucumber runner
-  refactor cleanup of karate cucumber wrapping
-  breaking change for java api to call feature
-  improved error reporting for call failures
-  added vs code plugin details to doc which fixes #186
-  added readme for spring rest-docs
-  minor add to doc for form-field example
-  doc improvements and added headers example
-  implemented scenario tags access in script which fixes #191
-  enhanced tag introspection for #191
-  print takes comma delimited args which fixes #190
-  minor refactoring of json set
-  implemented append to json arrays which fixes #189
-  improving doc for re-usable features + auth
-  ssl validation bypass which fixes #193
-  edit typo
-  added missing optimization in new tag resolution routine
-  fixed the nashorn null pointer exception based on the answers at https://stackoverflow.com/questions/25332640/getenginebynamenashorn-returns-null
-  Merge pull request #197 from cnrani/karate-fix-local
-  minor doc change
-  Merge branch 'master' into develop
-  cleanup of pull request #197 which fixes #196
-  stop variable state dump which fixes #198
-  added fix for java.lang.NoClassDefFoundError: jdk/nashorn/api/scripting/NashornScriptEngineFactory when running on TEP(linux based)
-  Merge branch 'master' of https://github.com/cnrani/karate into cnrani-master
-  Merge branch 'cnrani-master' into develop
-  added feature count print to parallel stats
-  not contains implemented for strings which fixes #201
-  updated doc to reflect code changes
-  implemented match not equals which was quite tricky
-  minor doc edit for heading hyperlink
-  improved error messages for typos which fixes #180
-  re-factored cross field expressions, introduced 'self parent' concept
-  refactoring reporters, introducing native html report wip
-  Added support for plugging in filters based on tags
-  Merge pull request #204 from sunilsishtla/develop
- ... e mais 16 commits

### Release 3

Link: https://github.com/karatelabs/karate/releases/tag/v0.9.0
- Tag: `v0.9.0`
- Nome: (sem nome)
- Publicada em: 2018-12-02
- Release anterior (cronológica): `v0.8.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  improved logging doc
-  fix for gatling report missing last scenario http request #460
-  bump dev version to point one
-  improve readme for standalone jar awareness
-  Merge branch 'master' into develop
-  adding issue template
-  Update ISSUE_TEMPLATE.md
-  Merge branch 'master' into develop
-  Issue-464: proper handling of abort and slight improvement in KarateJunitFormatter
-  Merge pull request #466 from vmchukky/Issue-464
-  code doc edit after pr #466 thx @vmchukky
-  adding important updates to doc
-  Merge branch 'master' into develop
-  karate ui was broken with logging change ref #469
-  fix for ui mode file in current working dir
-  Merge remote-tracking branch 'upstream/master' into develop
-  Merge remote-tracking branch 'upstream/develop' into develop
-  Issue-425: fix NPE while importing postman collection with item array
-  implemented being able to select tag when calling feature ref #471
-  Merge pull request #473 from vmchukky/Issue-425
-  adding example of using Nil for gatling pause-times, doc edits
-  added some fun examples for finding index of match in arrays
-  minor doc edits
-  bump version to 0.9.0 for cucumber exit branch
-  removing karate-testng, karate-restdocs and karate-web
-  removing references to testng in the doc
-  cukexit - the cucumber exit :P in full swing
-  defensive coding to ensure well-formed report json / xml output ref #475
-  adding unit test for #475
-  Merge branch 'develop' into cukexit
-  wip start of json reporter
-  cukexit wip json report
-  configure report had no effect #478
-  Merge branch 'develop' into cukexit
-  Issue-479: karate-ui enhanced to create-new/edit-existing/save-modified features
-  Merge pull request #480 from vmchukky/Issue-479
-  Merge branch 'develop' into cukexit
-  cukexit wip step execution reporting
-  cukexit wip cucumber json report replacement mostly done
-  cukexit wip coming along well #444
- ... e mais 210 commits

### Release 4

Link: https://github.com/karatelabs/karate/releases/tag/v2.0.6
- Tag: `v2.0.6`
- Nome: v2.0.6
- Publicada em: 2026-04-29
- Release anterior (cronológica): `v2.0.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 106

-  prepare for next development iteration [no ci]
-  Restore element.parent, add element.closest(selector)
-  Replace element.parent with closest(selector) + matches(selector)
-  Bump org.apache.httpcomponents.client5:httpclient5 from 5.6 to 5.6.1
-  Bump org.thymeleaf:thymeleaf from 3.1.4.RELEASE to 3.1.5.RELEASE
-  Support array-loop argument in karate.call() / karate.callonce()
-  Surface beforeScenario / afterScenario hooks in HTML reports
-  Merge pull request #2807 from karatelabs/dependabot/maven/org.apache.httpcomponents.client5-httpclient5-5.6.1
-  Merge pull request #2808 from karatelabs/dependabot/maven/org.thymeleaf-thymeleaf-3.1.5.RELEASE
-  Optional chaining (?.) + nullish coalescing — spec compliance
-  TEST262.md — refresh roadmap after the optional-chaining session
-  Iteration-layer unification + un-skip Symbol.iterator
-  TEST262.md — compact and refactor for LLM-friendly reading [no ci]
-  BigInt + numeric separators — ES2020/2021 spec compliance
-  Prototype extensibility, function-decl hoisting, generic Array methods
-  TEST262.md — refresh Open gaps note on harness-helper dependencies
-  Map + Set + String.prototype.matchAll + per-Engine prototype isolation
-  Date polish — spec MakeDay/MakeTime + Invalid Date + cross-cutting prototype/toString fixes
-  TEST262.md — promote function-identity trio to top action item [no ci]
-  Function-object identity trio — isConstructable + Function global + minimal Reflect + JsBuiltinMethod
-  TEST262.md — re-rank priorities by core-engine confidence + harness leverage [no ci]
-  Class/super skip-list expansion + bitwise compound assignments
-  void unary operator + binary/octal numeric literals
-  Descriptor infra — defineProperty accessors + isExtensible/seal/freeze
-  TEST262.md — add scaffolding pointers to Tier 2 attribute-enforcement plan [no ci]
-  Per-property attribute enforcement + propertyHelper/compareArray un-skip
-  Built-in intrinsic attribute attribution + tombstone-on-delete + Math wrap
-  TEST262.md — tighten Tier 2 rollout pointers for fresh-session usability [no ci]
-  IsValidSimpleAssignmentTarget early-error pass
-  Per-Engine reset for built-in constructor singletons
-  Number constructor wrap (JsBuiltinMethod + per-method attrs)
-  Object constructor wrap (JsBuiltinMethod + per-method attrs)
-  Array + String constructor wraps (JsBuiltinMethod + per-method attrs)
-  Function / BigInt / Map / Set / Date constructor wraps
-  TEST262.md — record constructor-singleton wrap sweep [no ci]
-  Array.prototype wrap + Prototype tombstones / getOwnAttrs
-  TEST262.md — record Array.prototype wrap [no ci]
-  Number + String prototype wraps
-  Lift _methodCache to Prototype + add method() helper + Date wrap
-  Constructor wraps — use name + method() helper
- ... e mais 66 commits

### Release 5

Link: https://github.com/karatelabs/karate/releases/tag/v2.0.9
- Tag: `v2.0.9`
- Nome: v2.0.9
- Publicada em: 2026-05-13
- Release anterior (cronológica): `v2.0.8`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 38

-  prepare for next development iteration [no ci]
-  docs: always comment 'vX.Y.Z released' on closed issues; use [no ci] for release version bump
-  ci: point CVE check at cached NVD data dir; enable maven cache [no ci]
-  docs: trim migration guide to v1->v2 scope; drop What's New preamble and v2.x->v2.x notes [no ci]
-  core: route set RHS through evalKarateExpression for v1 parity (refs #2813)
-  markup: K7 devTrace + K8 ka:data-mirror
-  Build(deps): Bump github/codeql-action from 4.35.3 to 4.35.4 (#2836)
-  Build(deps): Bump netty.version from 4.2.12.Final to 4.2.13.Final (#2834)
-  Build(deps-dev): Bump org.owasp:dependency-check-maven (#2835)
-  core: JS function → Java functional-interface coercion + JsLazy split (refs #2837)
-  markup: K3 ka:island + friendly _._ error + dev-mode 500 body
-  markup: tests for th:with object spread (...obj) syntax
-  markup: K16/K17/K18/K21/K22 — strict scope refs + new accessors
-  markup+js: th:attr SyntaxError hint, th:each strict, in operator
-  markup: minor hardening — type-tagged hints, dispatch validation,
-  http: CsrfProtection.createTemplateToken returns null when no token is available
-  http: send HX-Redirect for context.redirect on htmx-originated requests
-  markup: proactively reject th:fragment="name(params)" at template load
-  markup: KaFragmentProcessor — attribute-level th:fragment validation
-  markup+http: per-render context.set + per-request context.setGlobal/getGlobal
-  test resources: drop internal planning-code shorthand from comments
-  gherkin: warn on v1 @parallel tag at parse time + migration docs (refs #2838)
-  docs: structural updates — DESIGN module-map fix, capabilities additions, @timeout TODO
-  core+http: propagate KarateConfig to HTTP client on call inheritance (refs #2839)
-  driver: honor stop:false flag — skip quit + bypass pool
-  test: manual smoke for driver stop:false (W3C chromedriver path)
-  cucumber-json: flatten called sub-feature steps into parent steps[]
-  core: evaluate scenario names with bare ${...} placeholders
-  reports: expose passedRate on SUITE_EXIT.summary and FEATURE_EXIT (refs #2832)
-  core+reports: surface karate.callSingle + config-time output in reports (refs #2840)
-  core: split at `..` before `[` in match jsonpath expressions (refs #2841)
-  core+js: restore String.prototype.substr and karate.set(map) bulk form (refs #2842)
-  core+tests: trim test-log noise and drop orphan jflex plugin
-  js+test262: abrupt-completion sweep + RegExp.escape + lexer \v/\x (+51 PASS)
-  js+core: phase-0 prep for json-smart removal in karate-js
-  js: drop json-smart in karate-js, ship own strict JsonParser
-  core+tests: set suite end time before firing SUITE_EXIT (refs #2843)
-  release 2.0.9 [no ci]
