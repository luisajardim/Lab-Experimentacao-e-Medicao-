# clojure/clojurescript

Repositório: https://github.com/clojure/clojurescript

## Metadados

- Linguagem: Clojure

## Releases sorteadas

### Release 1

Link: https://github.com/clojure/clojurescript/releases/tag/r3030
- Tag: `r3030`
- Nome: 0.0-3030
- Publicada em: 2015-03-07
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/clojure/clojurescript/releases/tag/r1.8.34
- Tag: `r1.8.34`
- Nome: 1.8.34
- Publicada em: 2016-03-18
- Release anterior (cronológica): `r1.7.228`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 50

-  CLJS-1546: cljs.core/run! does not always return nil
-  CLJS-1547: Wrong output encoding when compile with goog.LOCALE
-  Update Maven dependency information
-  CLJS-620: Warnings are generated when using a macro in argument position
-  CLJS-1318: Fix typo in documentation of `specify`
-  CLJS-1542: Self-host: cljs/compile-str not handling errors properly
-  CLJS-1557: Make special-symbol? return true for catch and finally
-  CLJS-1488: cljs.repl/source Cannot read source of cljs functions that use #js reader
-  CLJS-1552: doc for & should match fn
-  CLJS-1551: Self-host: assert-args dormant in macros
-  CLJS-1550: Enhance docstring for extend-type wrt type-sym
-  CLJS-1541: Self-host: Cannot require 'cljs.js using cljs.jar
-  CLJS-1565: Self-host: whitespace optimization is broken
-  CLJS-970: generate assert message when compiling
-  CLJS-1555: make-array macro missing 2 arg arity
-  CLJS-1411: make-array signature differs from clojure
-  bump to Clojure 1.8
-  1.8 revision
-  CLJS-744: ISequential types should implement JS indexOf, lastIndexOf
-  less cryptic error if :main doesn't correspond to any file
-  move apply declare
-  CLJS-1571: Make special-symbol? true for 'var
-  CLJS-1567: make-array macro missing > 2 arg arity
-  CLJS-1492: Warn when using :optimisations instead of :optimizations
-  CLJS-1569: IndexedSeq doesn't implement IWithMeta / IMeta
-  bump tools reader and Google Closure Compiler dependencies
-  cleanup charset handling, improve error message
-  revert to previous Closure Compiler for now
-  fix typo in project.clj
-  enable direct linking when building
-  add direct linking to project.clj
-  CLJS-1580: Self-host: goog.provide offsets source-maps
-  CLJS-1579: cljs.source-map/invert-reverse-map discards gcol
-  CLJS-1578: Corrupted Analysis Files Break Compilation
-  CLJS-1568: LazyTransformer doesn't implement IMeta
-  CLJS-1570: :parallel-build causes invalid truth check in cljs.reader/read-number
-  CLJS-1573: Self-host: Invalid UTF escaping in cljs-in-cljs
-  CLJS-1521: Self-host: Macro namespaces cannot be aliased
-  CLJS-1584: Self-host: core/str error with condp
-  CLJS-1564: Self-host: cached macro *loaded* update
- ... e mais 10 commits

### Release 3

Link: https://github.com/clojure/clojurescript/releases/tag/r1.8.40
- Tag: `r1.8.40`
- Nome: 1.8.40
- Publicada em: 2016-03-28
- Release anterior (cronológica): `r1.8.34`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  Updates for 1.8.34
-  add missing known compiler options
-  CLJS-1592: Self-host: Robustness for core tests
-  :warning-handlers missing from known compiler options
-  CLJS-1603: Only warn for misspelled comp/REPL opts
-  CLJS-1605: Add all repl* options to known-repl-options

### Release 4

Link: https://github.com/clojure/clojurescript/releases/tag/r1.8.51
- Tag: `r1.8.51`
- Nome: 1.8.51
- Publicada em: 2016-04-25
- Release anterior (cronológica): `r1.8.40`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  1.8.40
-  Avoid corrupted compiler env in ana/parse-ns
-  bump tools.reader to 1.0.0-beta1
-  CLJS-1617: Evaluation order of arguments to 'list' is right-to-left
-  CLJS-1624: Avoid the use of JSC_HOME for tests
-  CLJS-1621: Foreign libs modules of different type doesn't compile together
-  CLJS-1626: cljs.test for bootstrap
-  CLJS-1612: Resolve ns aliases in syntax quote
-  CLJS-1595: Update Closure Compiler
-  CLJS-1632: Typos, c/e, and consistency of docs/params
-  CLJS-1588: Self-host: satisfies? on defrecord instance

### Release 5

Link: https://github.com/clojure/clojurescript/releases/tag/r1.9.671
- Tag: `r1.9.671`
- Nome: 1.9.671
- Publicada em: 2017-06-30
- Release anterior (cronológica): `r1.9.660`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  fix :fn-invoke-direct edgecase around keywords
-  just emit call if for some reason we haven't already optimized
-  resolve returns improperly constructed Var
-  need to elide :c.a/analyzed in c.a/analyze-wrap-meta
-  CLJS-2136: Clarify IFind contract to avoid double-lookups
-  remove integer validation in PV -find
-  fix Subvec IFind, add tests
-  Subvec should not delegate -find, additional tests
-  CLJS-2137: Missing INext on some sequences
-  CLJS-2139: Undeclared var regression in fn bodies
-  1.9.671
