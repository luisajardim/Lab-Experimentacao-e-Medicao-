# risingwavelabs/risingwave

Repositório: https://github.com/risingwavelabs/risingwave

## Metadados

- Linguagem: Rust

## Releases sorteadas

### Release 1

Link: https://github.com/risingwavelabs/risingwave/releases/tag/v0.1.1
- Tag: `v0.1.1`
- Nome: v0.1.1
- Publicada em: 2022-02-25
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/risingwavelabs/risingwave/releases/tag/v1.9.1
- Tag: `v1.9.1`
- Nome: v1.9.1
- Publicada em: 2024-06-06
- Release anterior (cronológica): `v1.9.1-rc.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 19

-  fix(ci): backwards compat test for 1.9 should use etcd (#16820) (#16975)
-  feat(ci): introduce slow e2e test step (#16953) (#16978)
-  chore(ci): increase timeout for slow e2e tests (#16980) (#16982)
-  feat(frontend): redact sql option in log (#16993)
-  fix: Mixing arrangement backfill and no shuffle backfill can lead to scale failure part 2 (#16983) (#16995)
-  fix(storage): cherrypick fix compactor task parallelism race (#17000)
-  fix(log-store): write truncate offset when consuming persistented data (#17005) (#17008)
-  fix(object store): do not call abort when streaming upload finish error and fix azure workload identity (#16961) (#16997)
-  fix: cherry-pick rebuild log store iter when exists for a timeout (#17009) (#17055)
-  chore(catalog): avoid rw_catalog in pg_tables (#16915) (#17058)
-  feat(sink): support view dependency in the sink into table (#17043) (#17060)
-  fix(connector): don't log config/props that may contain sensitive info (#17086)
-  cherry-pick feat(source): parse avro map into jsonb (#16948) (#17114)
-  feat(telemetry): impl report to scarf (#17046) (#17120)
-  fix(optimizer): fix functional index selection (#17039) (#17042)
-  feat(build): add rustup to the release image (#17100) (#17126)
-  cherry-pick fix: pulsar error during recovery (#17112) (#17129)
-  chore: update version to 1.9.1
-  fix(build): install rustup on ubuntu 22.04 (#17133)

### Release 3

Link: https://github.com/risingwavelabs/risingwave/releases/tag/v2.2.4
- Tag: `v2.2.4`
- Nome: v2.2.4
- Publicada em: 2025-03-25
- Release anterior (cronológica): `v2.0.7`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  ci: add cherry-pick 2.0 (#18074)
-  fix(stream): fix functional dependencies for row merge (#18072)
-  chore: update Cargo package version to 2.1.0-alpha (#18075)
-  feat: support constructor `MAP {..}` and index operator `m[k]` for map (#18066)
-  chore: fix RustRover macro expansion (#18077)
-  chore: remind labeling new features or improvements as experiemental if needed (#18084)
-  feat(frontend): bind default value for `approx_percentile` relative_error (#18082)
-  refactor: reduce periodical logs (#18080)
-  test(frontend): test two phase approx percentile with group key is banned (#18085)
-  feat: Optimize the performance of scaling in the SQL backend. (#16722)
-  refactor(meta): only retry on connection error when registering worker node (#18061)
-  fix(schedule): Restrict parallelism that exceed the virtual node limit during automatic scaling. (#18006)
-  feat(frontend): support single phase approx percentile in batch (#18083)
-  feat(license): add limit for total cpu cores in the cluster (#18022)
-  fix(parser): fix unparse of include columns (#18098)
-  fix(meta): adapt time travel for partial checkpoint (#18093)
-  feat: support more map functions (#18073)
-  feat(iceberg): bump iceberg-rust to v0.3.0 (#18088)
-  feat(test): switch meta to sql backend in simluate test (#15612)
-  feat(connector): add support for path-style access in Iceberg sink connector (#17747)
-  fix: udf error ui (#18118)
-  fix(connector): file source do not panic when credential is wrong (#17935)
-  fix(sink): fix sink in to Cassandra failed when using column name containing upper case letter  (#17493)
-  fix: remove overly strict assertion during stream pause/resume (#18131)
-  feat(cdc): auto schema change for mysql cdc (#17876)
-  fix(meta): fix cpu core limit check query (#18122)
-  fix: overwrite splite assignment for config change (#18128)
-  refactor(grafana): provide finer grain filter for object store op (#18004)
-  feat(ci): add `fast-docker-build-arm` workflow (#18124)
-  fix: flaky udf e2e error ui test (#18132)
-  ci: fix log size limit failure by increasing limit (#18117)
-  refactor(expr): show candicates when function not found (#18078)
-  perf(stream): set `noop_update_hint` when jsonb access exists (#18065)
-  chore: patch cargo `patch-production` profile (#18139)
-  fix(ci): fix bad indent of `cassandra sink test` (#18150)
-  feat: support custom kafka group id prefix (#18115)
-  refactor(meta): only bail out on server-side error when registering worker node (#18127)
-  fix: check split assignment before pushing mutation (#18134)
-  fix(meta): fix time travel metadata for partial checkpoint (#18160)
-  fix(meta): correctly persist license key system param in SQL backend (#18163)
- ... e mais 210 commits

### Release 4

Link: https://github.com/risingwavelabs/risingwave/releases/tag/v2.3.3
- Tag: `v2.3.3`
- Nome: v2.3.3
- Publicada em: 2025-06-05
- Release anterior (cronológica): `v2.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 118

-  cherry-pick feat(udf): introduce async and batched JavaScript UDF (#20403) to 2.3 (#20702)
-  fix(ci): fix rustup 1.28.0 breaking change (#20718) (#20723)
-  fix(optimizer): fix predicate pushdown for asof join (#20711) (#20719)
-  fix(ci): fix rust toolchain (#20728) (#20729)
-  fix(storage): fix compactor meta cache config (#20737) (#20741)
-  fix(stoarge): fix in-mem state store seal epoch panic on singleton vnode (#20665) (#20747)
-  fix(iceberg): revert iceberg engine paid feature (#20750) (#20758)
-  refactor: replace hardcoded buffer size with config (#20738) (#20754)
-  fix(source): debezium avro schema evolution (#20699) (#20762)
-  feat: Add support for resource group in database creation (#20751) (#20775)
-  feat: Implement batch-based updates in offline scaling (#20749) (#20776)
-  feat(iceberg): support creating namespace and namespace exists for iceberg catalog (#20759) (#20782)
-  fix(iceberg): reject iceberg on gcs with catalog rather than rest and storage (#20781) (#20784)
-  fix(meta): background ddl wait collect first barrier (#20783) (#20803)
-  feat(iceberg): support list namespaces and tables for jni catalog (#20669) (#20806)
-  fix(meta): allow subset of databases enter running after global recovery (#20792) (#20862)
-  refactor(compaction): optimize level_insert_ssts (#20824) (#20877)
-  refactor(compaction): optimize stale compaction task validation (#20863) (#20884)
-  feat: cherry-pick database isolation fixes in #20827 #20734 #20872 #20879 to release-2.3 (#20869)
-  refactor(connector): correctly log java exceptions (#20840) (#20867)
-  cherry-pick feat: add UdfConfig to enable/disable embedded UDF for different language (#20893) to branch release-2.3 (#20902)
-  feat: introduce `rw_resource_groups` view  (#20920) (#20936)
-  fix(sqlparser): `Display` of `WITH VERSION COLUMN` (#20823) (#20873)
-  feat(storage): separate shared buffer compact SSTs of state table with and without old values (#20939) (#20944)
-  chore: cherry-pick #20891 #20896 #20918 #20937 #20756 #20727 to release-2.3 (#20932)
-  fix(subscription):fix loss of subscription data due to reboot (#20959) (#20964)
-  fix(frontend): `encode protobuf` shall pass options without `legacy_source::ProtobufSchema` (#20949) (#20977)
-  fix(meta): fix late collect resp on failed database in recovery (#20988) (#20997)
-  refactor(config): make rpc client option configurable (#20993) (#21003)
-  fix(meta): change mysql charset to utf8mb4 (#20981) (#21013)
-  feat(sink): support es sink partial update  (#20048) (#20996)
-  fix(udf, 2.3): fix udf test for single-node and standalone binary test (#20986)
-  feat(iceberg): bump iceberg rust for release 2.3 and support s3 tables (#21040)
-  cherry-pick fix(source): modify the logic of gzip compressed file source (#20236) to branch release-2.3 (#21052)
-  fix: fix the self-reference issue in the sink into table creation (#21103) (#21108)
-  chore: update version v2.3.0-rc.1 (#21117)
-  refactor(meta): exclude table change log from time travel metadata (#20948) (#21105)
-  feat: bump foyer with fast recovery (#21114)
-  fix: fix foyer panics, cherry pick #21145 (#21173)
-  chore: Optimize `fragment_ids` retrieval in `scale.rs` by using `select_only()` to boost performance. (#21182) (#21188)
- ... e mais 78 commits

### Release 5

Link: https://github.com/risingwavelabs/risingwave/releases/tag/v2.8.1
- Tag: `v2.8.1`
- Nome: v2.8.1 deprecated
- Publicada em: 2026-04-05
- Release anterior (cronológica): `v2.7.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  test(cdc): migrate mongodb-cdc tests to inline style with all data types (#23753)
-  fix: change placeholder of username in ldap filter config (#23782)
-  feat(vector): support stream vector index lookup (#23288)
-  refactor: improve cluster kill-and-recovery tests with precise recovery tracking (#23728)
-  feat(iceberg): support s3 and glue iam role arn (#23775)
-  chore(deps): Bump mach2 from 0.5.0 to 0.6.0 (#23784)
-  feat(streaming): add functionality to override config when building actors (#23735)
-  chore(ci): add maven cache for `build-other.sh` step (#23781)
-  feat(metrics): add relation busy rate to dashboard (#23730)
-  chore: rename iceberg common fields to better names. (#23790)
-  feat(iceberg): support assume role for s3 and glue catalog together with enable_config_load  (#23788)
-  feat(iceberg): change iceberg list interval sec to 10 sec (#23791)
-  fix(iceberg): rebuild stream when errors occur for iceberg list executor (#23793)
-  chore: replace `number_prefix` with `unit-prefix` (#23801)
-  feat(mysql-cdc): monitor the progress of binlog offsets in the upstream and downstream processes (#23692)
-  fix(iceberg): fix iceberg engine with compaction extra config (#23809)
-  refactor(meta): refine inflight info ownership and avoid unnecessary clone (#23754)
-  fix(iceberg): fix batch iceberg list executor (#23811)
-  fix(dashboard): fix some foyer metrics name followed by OpenMetrics (#23818)
-  feat: add periodic refresh table jobs & refactor ProgressTracker (#23737)
-  fix(iceberg): fix batch iceberg list executor (#23824)
-  fix: support AdaptiveParallelismStrategy as string format in config (#23817)
-  chore: add back grafana json (#23831)
-  chore(iceberg): better logging if mis-config `enable_config_load` on Cloud (#23822)
-  feat: migrate `JoinEncodingType` from session config to per-job config override (#23768)
-  fix(ci): use larger runner with more disk space for workflows that build RW (#23842)
-  fix(streaming): fix locality backfill state -- write upstream chunk to the state (#23838)
-  fix: update Minio client initialization to use keyword arguments (#23836)
-  fix(ci):  bump and pin versions of mdbook and related tools (#23840)
-  fix(ci): update connector node integration test pipeline to java 17 & 21 (#23854)
-  feat(meta): include view definition in diagnostic report (#23853)
-  fix: Supports config checks within compaction group scheduling. (#23841)
-  feat: implement watermark derivation for AsOf joins (#23803)
-  fix(sink): use downstream pk to compact when stream key is its subset (#23859)
-  perf(expr): support writer-style #[function] for array type (#23767)
-  feat: add last_success_time tracking to refresh jobs (#23834)
-  fix(streaming): deduplicate locality backfill ordering edge casued by share sub-plan (#23869)
-  fix(optimizer): fix gap fill column pruning (#23867)
-  fix(test): delay mongodb-cdc test insertion (#23866)
-  fix(iceberg): add snapshot id to iceberg scan (#23882)
- ... e mais 210 commits
