# apache/seatunnel

Repositório: https://github.com/apache/seatunnel

## Metadados

- Linguagem: Java

## Releases sorteadas

### Release 1

Link: https://github.com/apache/seatunnel/releases/tag/v1.0.0
- Tag: `v1.0.0`
- Nome: v1.0.0
- Publicada em: 2018-01-06
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/apache/seatunnel/releases/tag/v1.2.2
- Tag: `v1.2.2`
- Nome: [Stable]v1.2.2
- Publicada em: 2019-03-05
- Release anterior (cronológica): `v1.2.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  added checkSQLSyntax in sql filter
-  Update docs of 3.md
-  Merge pull request #241 from InterestingLab/rickyhuo.docs.study
-  fix #230
-  fixed class not found erro for Jdbc Input
-  Add fixed json schema
-  Refine comments and doc
-  Merge pull request #247 from huangdeheng/fea.json-schema
-  programatically do createSparkConf() even after this has been done in start-waterdrop.sh for the convience of debug in IDE
-  Merge pull request #245 from InterestingLab/garyelephant.issue.230
-  Merge pull request #224 from InterestingLab/garyelephant.fea.sql-filter

### Release 3

Link: https://github.com/apache/seatunnel/releases/tag/v1.4.2
- Tag: `v1.4.2`
- Nome: [Stable]v1.4.2
- Publicada em: 2019-12-06
- Release anterior (cronológica): `v1.4.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 24

-  Update README.md
-  Merge pull request #387 from InterestingLab/garyelephant.docs.readme
-  Update README.md
-  Merge pull request #388 from InterestingLab/garyelephant.docs.readme
-  Update checkConfig of static input for parameter of table_name
-  Update docs for hive2ck
-  Support jdbc optional option
-  Merge pull request #393 from InterestingLab/rickyhuo.enhance.input
-  Merge pull request #394 from InterestingLab/rickyhuo.enhance.input.jdbc
-  Update 2.md
-  Merge pull request #398 from wangpengpeng/patch-1
-  搜狗奇点系统使用 waterdrop 作为 etl 工具, 帮助建立实时数仓体系
-  Update README.md
-  Update README.md
-  Update README.md
-  Merge pull request #401 from InterestingLab/garyelephant.docs.use_docs
-  Add files via upload
-  Update README.md
-  Update README.md
-  Merge pull request #403 from InterestingLab/garyelephant.docs.readme
-  1) fix type err in FileStream doc
-  Merge pull request #409 from lingo-xp/lingoxp.doc.errfix
-  Bump version 1.4.2
-  Merge pull request #410 from InterestingLab/rickyhuo.release.1.4.2

### Release 4

Link: https://github.com/apache/seatunnel/releases/tag/v1.5.0
- Tag: `v1.5.0`
- Nome: [Stable]v1.5.0
- Publicada em: 2020-06-09
- Release anterior (cronológica): `v1.4.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 28

-  Fix the usage of acceptedClickHouseSchema
-  Update issue templates
-  Merge pull request #474 from InterestingLab/RickyHuo-patch-1
-  Fix #476
-  Merge pull request #475 from InterestingLab/rickyhuo.fixbug.clikchouse.schema
-  Merge pull request #477 from InterestingLab/rickyhuo.enhance.clickhouse.chinese
-  Update issue templates
-  Merge pull request #498 from InterestingLab/garyelephant.issue_template
-  Update issue templates
-  Merge pull request #499 from InterestingLab/garyelephant.issue_template
-  Replace config-1.3.3-SNAPSHOT.jar with waterdrop-config module
-  Remove antlr4 plugins
-  Bump version 1.5.0
-  添加yarn提交队列参数设置
-  添加yarn提交队列参数设置
-  Merge pull request #502 from gegedebenben/master
-  Bump version 1.5.0
-  Merge pull request #501 from InterestingLab/rickyhuo.v1.config
-  Add filter plugins of urldecode and urlencode
-  Update batchProcessing
-  Remove useless code
-  Fix #507
-  Update start-waterdrop-structured-streaming.sh for queue
-  Remove useless code
-  Merge pull request #509 from InterestingLab/rickyhuo.enhance.batch.main
-  Merge pull request #506 from InterestingLab/rickyhuo.fea.urldecode
-  Support spark.driver.extra*
-  Merge pull request #511 from InterestingLab/rickyhuo.enhance.driver

### Release 5

Link: https://github.com/apache/seatunnel/releases/tag/2.3.3
- Tag: `2.3.3`
- Nome: 2.3.3 Release
- Publicada em: 2023-08-22
- Release anterior (cronológica): `2.3.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 153

-  [Improve][Connector-V2][Jdbc-Source] Support for Decimal types as splict keys  (#4634)
-  [Bug][connector-v2][doris] add streamload Content-type for doris URLdecode error (#4880)
-  [Chore] Change repository name from incubator-seatunnel to seatunnel  (#4868)
-  [Improve][connector-V2-Neo4j]Supports neo4j sink batch write and update docs (#4841)
-  [Hotfix][connector-v2][e2e] Fix maven scope (#4901)
-  quick-start-seatunnel-engine.md (#4943)
-  fix error (#4888)
-  [Hotfix][Connector-V2][ClickhouseFile] Fix ClickhouseFile write file failed when field value is null (#4937)
-  [Improve][Zeta] Add an interface for batch retrieval of JobMetrics (#4576)
-  [Improve] Documentation and partial word optimization. (#4936)
-  [Doc][Connector-V2] StarRocks `nodeUrls` property name fix (#4951)
-  [Feature][E2E][FtpFile] add ftp file e2e test case (#4647)
-  [Hotfix][Connector-V2][StarRocks] Fix code style (#4966)
-  [Hotfix][Connector-v2][HbaseSink]Fix default timestamp (#4958)
-  [Doc]Change the transform website url (#4954)
-  [Docs][Connector-V2][Http]Reconstruct the Http connector document (#4962)
-  [Feature][connector-v2][mongodb] mongodb support cdc sink (#4833)
-  [Bug] [zeta][starter]fix bug (#4983) (#4984)
-  fix redis nodes format error. (#4981)
-  [Improve][CDC]Remove  driver for cdc connector (#4952)
-  [Hotfix][Connector-V2][Mongodb] Fix document error content and remove redundant code (#4982)
-  [Improve][Connector-V2][OSS-Jindo] Optimize jindo oss connector (#4964)
-  [bugfix] Upgrade the key log output level(#4993)
-  [Feature][Zeta] Configuration files support user variable replacement (#4969)
-  [Feature][Transform-V2][SQL] Support 'select *' and 'like' clause for SQL Transform plugin (#4991)
-  [Improve][CDC]change driver scope to provider (#5002)
-  [Hotfix][Connector-V2][Hive] Support user-defined hive-site.xml (#4965)
-  [Improve][Connector-v2][Mongodb]Optimize reading logic (#5001)
-  [Feature][Connector-V2][Clickhouse] clickhouse writes with checkpoints (#4999)
-  [Hotfix][Connector-V2][Mongodb] Compatible with historical parameters (#4997)
-  Split updated modules integration test for part 4 (#5028)
-  [Hotfix] Fix the CI Job name error (#5032)
-  [Feature][CDC] Support disable/enable exactly once for INITIAL (#4921)
-  [bugfix][zeta] Fixed multi-table job data loss and latency issues (#149) (#5031)
-  [Hotfix][CDC] Fix jdbc connection leak for mysql (#5037)
-  [Bugfix][zeta] Fix cdc connection does not close (#4922)
-  Fix XA Transaction bug (#5020)
-  Set Up with Kubernetes, dockerfile document error in constructing docker image (#5022)
-  [Improve][Connector-v2][Mongodb]sink support transaction update/writing (#5034)
-  fix:the HdfsStorage can not delete checkpoint file #5046 (#5054)
- ... e mais 113 commits
