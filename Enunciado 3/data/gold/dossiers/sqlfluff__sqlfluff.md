# sqlfluff/sqlfluff

Repositório: https://github.com/sqlfluff/sqlfluff

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/sqlfluff/sqlfluff/releases/tag/1.4.0
- Tag: `1.4.0`
- Nome: [1.4.0] - 2022-10-31
- Publicada em: 2022-10-31
- Release anterior (cronológica): `1.3.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 60

-  Update github badge and add docker badge (#3884)
-  Reflow centralisation 1: Scope + Respace (#3824)
-  MySQL: Implement (key_part, ...) in index definitions (#3887)
-  Snowflake: Create network policy ip lists (#3888)
-  Bring L008 into reflow work (#3908)
-  Reflow centralisation 2: Rebreak (operators & commas) (#3847)
-  fix(redshift): Allow keywords in qualified references (#3905)
-  provide custom DeprecatedOption (#3904)
-  Fix typos (#3901)
-  fix(test): Return ParseExample namedtuple in get_parse_fixtures (#3911)
-  feat: Handle postgres ranges (#3903)
-  [issue_3897] fix issue with empty enum for postgres (#3910)
-  feat: Output to stderr using click (#3902)
-  Postgres Revoke fix (#3912)
-  `DATABRICKS`: Add Support for Delta Live Tables (DLT) Syntax (#3899)
-  [issue_3794] allow to use 'usage' as identifier for postgres (#3914)
-  Map old configs to new configs (#3915)
-  [issue_3687] sparksql: added * EXCEPT for SELECT clause (#3922)
-  SQLite: Add support for table-level CHECK constraint (#3923)
-  T-SQL: Allow specifying join hints (#3921)
-  SparkSQL: Fixed bug with `QUALIFY` usage without `WHERE` clause (applies also for Databricks dialect) (#3930)
-  MySQL: Fix create trigger (#3928)
-  T-SQL: Fix indendentation of OUTER APPLY (#3932)
-  Break apart reflow classes and extract methods (#3919)
-  Add INSERT INTO <> DEFAULT VALUES to ANSI SQL and T-SQL (#3934)
-  Refactor Lexer: Split apart elements_to_segments and refine placement of meta segments. (#3925)
-  Fix crash in L042 on "UNION" or other "set" queries (#3931)
-  Hive: Add support for LATERAL VIEW clause (#3935)
-  T-SQL: Allow to parse SYNONYM statements (#3941)
-  MySQL: Support optional "IF NOT EXISTS" with CREATE TRIGGER (#3943)
-  Load the full dbt manifest (#3926)
-  Add templated block uuids (#3936)
-  Adding missing KeywordSegments for different file types in Athena dialect (#3898)
-  Consolidate comma style configs (#3945)
-  Enable dumping of performance information to csv. (#3937)
-  T-SQL: Allow arbitrary expressions in PARTITION BY clause (#3939)
-  Postgres: ALTER PROCEDURE (#3949)
-  fixed typos in docstrings and comments (#3953)
-  TSQL: Add support for UPDATE STATISTICS option FULLSCAN (#3950)
-  MySQL: Support REPLACE statement (#3964)
- ... e mais 20 commits

### Release 2

Link: https://github.com/sqlfluff/sqlfluff/releases/tag/2.0.6
- Tag: `2.0.6`
- Nome: [2.0.6] - 2023-04-19
- Publicada em: 2023-04-20
- Release anterior (cronológica): `2.0.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 23

-  end-of-file > end_of_file (#4753)
-  Fix issue with macros triggering LT01 (#4757)
-  Fix #4745: (max() error in reindent) (#4752)
-  Remove the majority of greedy matchers (#4761)
-  Allow comment match with preceding line (#4758)
-  Fix #4582: Comments after end of line (#4760)
-  Support hive set syntax (#4763)
-  SQLite: Support STRICT (#4766)
-  SQLite: Remove refs to RESPECT and QUALIFY (#4765)
-  SQLite: Fix multiple parse issues in Expression_A_Grammar (#4769)
-  Use the new CollationReferenceSegment everywhere (#4770)
-  Fix #4540: Untaken indents evaluation order. (#4768)
-  Fix #2865 (AL05 exception for Redshift Semi-structured) (#4775)
-  SQLite: Support CreateTrigger (#4767)
-  Snowflake Execute Task with Schema (#4771)
-  Fix #4603 indent after Jinja 'do' directive (#4778)
-  Add a --quiet option for fix (#4764)
-  Fix #2855: (Tech debt: check consistency in TemplatedFile init) (#4776)
-  Fix #3538: (Fix files as we go) (#4777)
-  Fix #4660: Better handling of empty files. (#4780)
-  Inroduce `SAFE` prefix segment (#4773)
-  Snowflake: Support Temporary View (#4789)
-  Prep version 2.0.6 (#4784)

### Release 3

Link: https://github.com/sqlfluff/sqlfluff/releases/tag/2.0.7
- Tag: `2.0.7`
- Nome: [2.0.7] - 2023-04-20
- Publicada em: 2023-04-20
- Release anterior (cronológica): `2.0.6`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  fix: correct macos/osx config file location (#4795)
-  Fix bug with brackets and implicit indents (#4797)
-  Fix regression in implicit indents (#4798)
-  Bump to version 2.0.7 (#4799)

### Release 4

Link: https://github.com/sqlfluff/sqlfluff/releases/tag/3.1.1
- Tag: `3.1.1`
- Nome: [3.1.1] - 2024-08-20
- Publicada em: 2024-08-20
- Release anterior (cronológica): `3.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 49

-  Fix TSQL Post Table Expr intrepreted as function (#6001)
-  Snowflake: fixes drop column if exists parsing rules (#5999)
-  MariaDB: Add mariadb specific syntax for generated columns (#6007)
-  MariaDB: Add support for DELETE/INSERT/REPLACE ... RETURNING (#6008)
-  AM07: Handle set expressions with bracketed selects (#6005)
-  MariaDB: Add support for GROUP BY ... ASC/DESC and GROUP BY ... WITH ROLLUP (#6009)
-  Add additional dateparts from DATEPART() (#6012)
-  Parse API example (#6021)
-  Add support for Clickhouse ORDER BY WITH FILL (#6018)
-  Added GENERATED AS IDENTITY support to DataBricks dialect (#6004)
-  Remove old deps for dbt templater (#6028)
-  Replace types-pkg-resources with types-setuptools (#6039)
-  Snowflake:adds optional IF NOT EXISTS to ADD COLUMN (#6050)
-  Snowflake: fixes parsing for AGGREGATE in CREATE FUNCTION statement (#6049)
-  CV11: Remove rogue print statement (#6047)
-  RF03: Fixed some subquery reference scenarios (#6046)
-  Update the docs on RF03 (#6051)
-  Fix ignored inline rule overrides (#5697) (#6010)
-  fix: redshift dialect, EXTENSION added (#6025)
-  Fix Athena Partitioned By format for iceberg tables (#5399)
-  bq_table_function : Added functionality to parse table functionsin BigQuery (#5480)
-  Fix/snowflake double quotes (#5727)
-  TRINO: support FILTER after WITHIN GROUP agg expression (#6056)
-  ST03: Detect CTE usage in nested `WITH` clauses (#6017)
-  Exclude Macros from a path provided (#6031)
-  Support declare or replace variable statement for Databricks dialect (#6054)
-  MySQL: Added SET TRANSACTION parsing (#5781)
-  Extract path discovery routines from config and linter. (#6057)
-  Run dbt tests in py312 by default (#5861)
-  Copy statement postgres v9 compatibility support (#5181)
-  fix(clickhouse): add support for DateTime64(precision, tz) and Tuples() (#6060)
-  fix(clickhouse): add support for limit by and bracketed format (#6061)
-  ST05: Handle set statement's subsequent queries (#6062)
-  Big docs refactor. (#6052)
-  feat(clickhouse): add support for decimal(x,y), decimal32(x) and match (#6063)
-  pre-commit: Disable progress bar (#6069)
-  LT04: Fix indentation conflict with LT02 (#6068)
-  fix(clickhouse): add support for INTO OUTFILE and supported FORMATs (#6065)
-  fix(clickhouse): add support for rename statement (#6073)
-  Add perma-links for rules (#6066)
- ... e mais 9 commits

### Release 5

Link: https://github.com/sqlfluff/sqlfluff/releases/tag/3.2.3
- Tag: `3.2.3`
- Nome: [3.2.3] - 2024-10-10
- Publicada em: 2024-10-10
- Release anterior (cronológica): `3.2.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 19

-  fix: tsql create function syntax corrections (#6289)
-  Snowflake: support temp UDFs (#6309)
-  Allow expressions in ORDER BY for clickhouse (#6311)
-  Snowflake: Support CTEs and multiple orders of CopyOptions in COPY INTO (#6313)
-  Add groups to the `github-annotation-native` format option. (#6312)
-  Create a "Guides and Howtos" section of the docs. (#6301)
-  Resolve an oscillation bug with LT02 (#6306)
-  Allow double quotes to be escaped by writing twice (#6316)
-  Databricks materialized view (#6319)
-  Snowflake allow double-quoted comments (#6318)
-  Exclude templated casts from CV11 (#6320)
-  Add support for `grant monitor on user ...` in Snowflake dialect (#6322)
-  Postgres: Fix lexing some JSON operators (#6323)
-  Indentation: `UPDATE` and `RETURNING` clauses (#6314)
-  RF05 - fine tuning for snowflake dialect (#6297)
-  Resolve some more edge cases in LT02 (#6324)
-  Trino: Fix rule interactions with lambda functions (#6327)
-  BigQuery: Support Tuple syntax in other locations (#6328)
-  Prep version 3.2.3 (#6329)
