# flowable/flowable-engine

Repositório: https://github.com/flowable/flowable-engine

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/flowable/flowable-engine/releases/tag/flowable-6.0.0
- Tag: `flowable-6.0.0`
- Nome: Flowable 6.0.0 release
- Publicada em: 2017-02-15
- Release anterior (cronológica): `flowable-6.0.0.RC1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Add support for rescheduling a timer job via the ManagementService.
-  Be confident, be brave, 6.0.0-SNAPSHOT it is
-  CSS uses just 'color' and not 'font color' (#85)
-  Update references in package.html files (#86)
-  Variable was assigned to itself (#90)
-  Remove unnecessary null check (#89)
-  Duplicate condition in if stmt or condition (#87)
-  add more extensions to skipAuthenticationCheck (#91)
-  Remove redundant casts (#92)
-  Merge branch 'timer-reschedule2' of https://github.com/roberthafner/flowable-engine
-  Redundant String.toString() and String.format() calls removed (#93)
-  Logging messages with mismatch placeholders and arguments (#94)
-  Remove redundant placeholder
-  Removed redundant placeholders
-  Removed redundant placeholders
-  Merge branch 'master' of https://github.com/flowable/flowable-engine
-  Added more reschedule convenience methods + test additions
-  Use parameterized log messages instead of string concatenation (#95)
-  Fix security scripting behaviour
-  Fix JavaDoc for recently added rescheduled methods (#98)
-  #96 @Deployment multi-tenant support (#97)
-  Update FlowableProperties to use 'spring.flowable' namespace. (#99)
-  Remove unnecessary semicolon (#100)
-  equals() on Enum constants replaced by an identity comparison (==) (#102)
-  Remove unnecessary "null" check before "equals()" call (#101)
-  Modifiers should be specified in the canonical preferred order (#103)
-  Simplify "if" statement to single assignment or return (#104)
-  Remove unnecessary return statement (#105)
-  Remove method that is identical to its super method (#106)
-  Use "addAll()" instead of manual copy of array contents (#107)
-  Change JUnit class with simpler but equivalent calls (#108)
-  Fix spring async executor issue
-  Merge with master
-  Added interrupting event sub process support to modeler + model display
-  Added event subscription query to RuntimeService
-  Added event subscriptions to REST API + Admin app
-  Apply PR #110 to Flowable 6 master
-  Added timer event support for event subprocess start events
-  Renaming of UI app property filenames
-  fix a never touched if branch
- ... e mais 210 commits

### Release 2

Link: https://github.com/flowable/flowable-engine/releases/tag/flowable-6.0.1
- Tag: `flowable-6.0.1`
- Nome: Flowable 6.0.1 release
- Publicada em: 2017-04-28
- Release anterior (cronológica): `flowable-5.23.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  MyBatis Multi-db vendor support + other simple tweaks
-  First batch of changes from experimental branch
-  Another commit
-  Added extra oneTaskProcess test that doesn't complete the task and thus needs a deployment cleanup.
-  - Added support for parallel gateway (+ simple test)
-  Added simple test for nested parallelism
-  Merge
-  - Refactored scriptTask and receiveTask + simple test
-  Merge
-  Refactored EndExecutionOperation to better handle scoped executions. Added a test with a timer that doesn't fire that didnt work before.
-  Added a test with non-interrupting timer boundary event. This led to again refactorings in the EndExecutionOperation. That seems to be a quite crucial operation in the grand scheme of things.
-  Added test for conditions on sequence flow (w/o exclusive gateway). Passes without any change.
-  Added test with complex non-interrupting behavior. That caused some refactorings to improve the logic.
-  Merge
-  Added use case 'tricky merge'. Not possible on current Activiti version.
-  Minor tweaks: change runtime exception to ActivitiException and expose ProcessDefinitionCacheEntry on utl as public
-  Merge
-  Merge
-  Merge
-  Merge
-  changed to activiti5 package
-  Reformat to 4 spaces
-  Fixing backwards compatibility test projects after mega-merge of Tijs
-  Removing db scripts from activiti5-compatibility module, they are not needed there.
-  Merge branch 'master' into activiti6
-  - Added DebugCommandInvoker to get an overview of the operations (+ added as default to parent test class)
-  Timer, Async + execution listener improvements
-  Merge with branch
-  Fixed merge issue
-  Refactored DebuggingCommandInvoker into a cleaner Configurator, which is more extensible for other use cases
-  WIP for test logging output for core engine execution
-  Merge branch 'activiti6' of https://github.com/Activiti/Activiti into activiti6
-  Further yakshaving: fixing execution tree logging
-  Disabling process execution logger by default. Enable it by uncommenting the test config.
-  Refactor ProcessDefinition cache usage:
-  Adding in support for default sequenceflow (generically)
-  Commenting out this test fixes 400 others. Need to investigate why, obviously.
-  Fixing various tests with simple fixes. Leaving the hard ones for Tijs.
-  Fixing ScriptTaskTest
-  Fixing up business rule task
- ... e mais 210 commits

### Release 3

Link: https://github.com/flowable/flowable-engine/releases/tag/flowable-6.1.0
- Tag: `flowable-6.1.0`
- Nome: Flowable 6.1.0 release
- Publicada em: 2017-06-27
- Release anterior (cronológica): `flowable-6.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Initial commit
-  Execution class handling
-  Update en.json
-  Update pt-BR.json
-  Update formfield-edit-popover.html
-  Move to 6.1.0-SNAPSHOT
-  added handsontable
-  Merge branch 'master' of https://github.com/flowable/flowable-engine into dmn-hot
-  Added HTTP Task initial specification
-  Added HTTP Task results specification
-  Merge branch 'master' into flowable-groovy-script-static-engine
-  Some testing
-  Updated HTTP Task specification
-  Added HTTP Task UI model
-  Merge remote-tracking branch 'refs/remotes/flowable/master'
-  Update FormField.java
-  Update editor-directives.js
-  Update formfield-edit-popover.html
-  Update form-element-template.html
-  Update pt-BR.json
-  Update en.json
-  Update es.json
-  hands on table implemenation WIP
-  Update pt-BR.json
-  Update pt-BR.json
-  Update pt-BR.json
-  Update pt-BR.json
-  Moved Retry limit parameter to HTTP Client configuration
-  Removed Retry limit field from converter
-  Updated HTTP Task documentation
-  Update style.css (#369)
-  Update form-builder.html (#368)
-  Decision table editor wip
-  Fixed upload form-field to allow the same field ID to be used in multiple forms and when used as a readOnly field
-  Added ignore exception and renamed fields
-  Added HTTP Task disallow HTTP redirects field
-  Added error handling for Http task specification
-  Added initial implementation of Http task
-  Fix some incorrect comparisons with NaN. (#374)
-  Remove some duplicate HTML element attributes. (#375)
- ... e mais 210 commits

### Release 4

Link: https://github.com/flowable/flowable-engine/releases/tag/flowable-6.4.0
- Tag: `flowable-6.4.0`
- Nome: Flowable 6.4.0 release
- Publicada em: 2018-10-02
- Release anterior (cronológica): `flowable-6.3.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Move to version 6.3.2-SNAPSHOT
-  Update maven-compiler-plugin to version 3.7.0 (#1088)
-  Issue#968 Fix variable order calling formService (#1087)
-  Add more tests for the async history Spring Boot configuration (#1083)
-  Add support for pluggable authentication provider
-  Move spring security classes into a module of their own
-  Use flowable spring security in the rest tests
-  Log warning when non spring authentication is used in the SpringSecurityAuthenticationContext
-  Use correct path mapping for getting historic cmmn resource (#1093)
-  FileOutputStream not closed/released (#1091)
-  Involved groups for processes and tasks (#1092)
-  Merge pull request #1089 from filiphr/pluggable-authentication-provider
-  Make async history executor instance reusable
-  Fix async history session factory initialization
-  Case involved (#1096)
-  fix for or(assignee/owner + involvedGroups) task query (#1094)
-  Remove the usage of FlowableTransactionAutoConfiguration and replace it with FlowableJpaAutoConfiguration
-  Merge pull request #1097 from filiphr/tranasaction-auto-configuration-conditional
-  Async history: add default fallback transformer
-  Identity link event handler (#1098)
-  Update process.js (#1112)
-  Replace "unexisting" with "non-existent" in exception message and javadoc. (#1110)
-  Update ContentItem lastModified timestamp during save (#1102)
-  decision table collection operators (#1113)
-  Issue#1107 Remove call for method to remove embedded references (#1108)
-  added display name to user entity
-  Update to joda-time version 2.10
-  Use displayName in ui common RemoteUser
-  Expose user displayName in REST API
-  Merge pull request #1117 from filiphr/remote-user-display-name
-  Merge pull request #1116 from PascalSchumacher/joda_time_2_10
-  Merge pull request #1118 from filiphr/user-display-name-rest
-  Add missing Deprecated annotation to deprecated components
-  Merge pull request #1119 from filiphr/missing-deprecated-annotation
-  Fix issues with task queries with assignment from task UI
-  Initialize DataObjects when moving state to an unstarted subprocess.
-  Move FlowableForbiddenException to engine-common-api module
-  Replace usages of deprecated method IOUtils#closeQuietly with try-with-resources statements.
-  Merge pull request #1125 from filiphr/extract-forbidden-exception-to-common
-  Merge pull request #1123 from roberthafner/change-state-subprocess-modeled-dataobject
- ... e mais 210 commits

### Release 5

Link: https://github.com/flowable/flowable-engine/releases/tag/flowable-6.5.0
- Tag: `flowable-6.5.0`
- Nome: Flowable 6.5.0 release
- Publicada em: 2020-01-22
- Release anterior (cronológica): `flowable-6.4.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  ProcessInstanceMigration Service and Batch processInstanceMigration validation
-  ProcessInstanceMigrationValidation batch commands and some clean-up
-  ProcessInstanceMigration batch and misc refactoring
-  Serialize JobHandlerConfiguration as Json for ProcessInstanceMigrationJobHandler and ProcessInstanceValidationJobHandler. Added processInstanceId to ProcessInstanceMigrationValidationResult. Methods that validate more than one processInstance now return a list of ProcessInstanceMigrationValidationResult
-  Added ProcessInstanceMigrationService bean to the different Engine configurations
-  BatchProcessInstanceMigration result is now a Json String that contains the children partial results (inProgress) when it applies, can also be used to query the result of specific children
-  Changed migration result from json string to Pojo
-  added Generic ProcessInstanceMigrationResult object
-  revert change on ExecutionEntityImpl
-  Check exception conditions ... batches should not be submitted when there are some root exceptions
-  Split batch table
-  Handle map exceptions
-  Handle map exceptions
-  Handle map exceptions
-  Handle map exceptions
-  Update unit tests to cover mapException
-  Cleanup
-  Explicitly list each import
-  Fix comment
-  Move to version 6.5.0-SNAPSHOT
-  Fix issue with servlet api dependency
-  Correct wildcard import, move static import to the top
-  updated Docker all-in-one build script to latest version
-  History cleanup support
-  Create batch service + add migration batch option
-  Use correct time cycle config
-  Fix jackson databind vulnerability issue
-  Update Commons Codec to version 1.13. (#1862)
-  Update JsonUnit to version 2.8.0. (#1852)
-  Update JUnit to version 5.5.1. (#1851)
-  Document BPMN REST API - Dead letter jobs (#1849)
-  Update Liquibase to version 3.7.0. (#1850)
-  Update MyBatis to version 3.5.2 and MyBatis-Spring to version 2.0.2. (#1845)
-  Merge branch 'master' of https://github.com/Blikingor/flowable-engine
-  Merge branch 'master' of https://github.com/flowable/flowable-engine
-  Some attribute description fixes (#1837)
-  Replace 'RequestMethod.GET' with @GetMapping (#1836)
-  Create batch service: Update BlueprintBasicTest (#1866)
-  Restore "zh_CN" locale version of CDI BPMN documentation (#1864)
-  Replace 'RequestMethod.XXX' with @XXXMapping (#1863)
- ... e mais 210 commits
