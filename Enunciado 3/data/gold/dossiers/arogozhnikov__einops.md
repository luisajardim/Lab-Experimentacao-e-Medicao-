# arogozhnikov/einops

Repositório: https://github.com/arogozhnikov/einops

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/arogozhnikov/einops/releases/tag/v0.1
- Tag: `v0.1`
- Nome: Initial release (v0.1)
- Publicada em: 2018-11-01
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/arogozhnikov/einops/releases/tag/v0.3.2
- Tag: `v0.3.2`
- Nome: Einops v0.3.2: updated documentation and tutorials, keras -> tf.keras
- Publicada em: 2021-08-31
- Release anterior (cronológica): `v0.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 64

-  docs
-  deploy docs
-  dont modify docs/README
-  arogozhnikov repo
-  add typehints to improve docs
-  fix reduce docs
-  add >>> to docs
-  remove >>> for outputs
-  remove >>> for outputs
-  Merge pull request #75 from cgarciae/master
-  replace replication of readme with soft link
-  more friendly format for code docstrings + added empty line to fix docstrings
-  add link to documentation
-  Merge pull request #76 from arogozhnikov/docs-improvements
-  add separate link to documentation
-  Merge pull request #77 from arogozhnikov/docs-improvements
-  fix #78
-  Merge pull request #79 from arogozhnikov/improve-tutorial
-  css adjustments for tutorials
-  multiple adjustments to tutorials
-  Merge pull request #81 from arogozhnikov/improve-tutorial
-  Change websote with documentation
-  spelling corrections
-  Merge pull request #87 from GarrettMooney/docs/spellcheck
-  Add issue templates
-  Delete extensions--introducing-new-operation---addition-to-notion.md
-  Update extensions--introducing-new-operation---improve-notion.md
-  update first tutorial
-  fix spacing before list
-  more efficient recipe application
-  minimal changes to second part of tutorial
-  Merge remote-tracking branch 'origin/master' into improve-tutorial
-  fix, return result in layers
-  Merge pull request #103 from arogozhnikov/improve-tutorial
-  Fix typo in tutorial
-  Improve documentation for repeat
-  Merge pull request #104 from ollema/patch-1
-  do not use --pre (pre-release versions) of packages during tests
-  Merge pull request #106 from arogozhnikov/use_stable_versions_in_tests
-  Add 'repeat' to __all__
- ... e mais 24 commits

### Release 3

Link: https://github.com/arogozhnikov/einops/releases/tag/v0.5.0
- Tag: `v0.5.0`
- Nome: Einops v0.5.0: einsum + support of flax and oneflow.
- Publicada em: 2022-10-03
- Release anterior (cronológica): `v0.4.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 85

-  add oneflow backend
-  modify author
-  fix test error
-  fix
-  refine
-  adjustments in test mechanics to allow linux-only test for oneflow
-  Merge pull request #181 from arogozhnikov/add_oneflow_backend
-  Update README.md
-  add concept of einstein-style indexing
-  address #189
-  Merge pull request #196 from arogozhnikov/fix-wrong-message
-  Add link to ICLR video about einops
-  Add einsum for np, torch, tf, jax backends
-  Add function that converts to einsum pattern
-  Add function that calls einsum for some tensors
-  Include missing string import for einsum
-  Include einsum in main library
-  Refactor test_einsum
-  Add tests for functional einsum
-  Create docstring for einsum
-  Clean up doctest for einsum
-  Allow duplicates in ParsedExpression for einsum
-  Add tests for repeated indices in einsum
-  Clean up einops.einsum docstrings
-  Improve readability of einsum implementation
-  add classifier for pypi
-  Implement einsum for additional backends
-  Include einsum tests for additional backends
-  Expand einsum documentation
-  Fix einsum docstring example
-  Test values passed through einsum
-  Include helpful error message if -> missing
-  Remove unused class in einsum test
-  Include many more einsum tests
-  Remove unnecessary strip() in einsum
-  Error for singleton axes
-  Include symbolic backends in einsum test
-  Attempt inclusion of mxnet backend for einsum
-  Remove mxnet einsum as non-functional
-  Reduce indentation of einsum tests
- ... e mais 45 commits

### Release 4

Link: https://github.com/arogozhnikov/einops/releases/tag/v0.6.0
- Tag: `v0.6.0`
- Nome: V0.6.0: pack and unpack
- Publicada em: 2022-11-09
- Release anterior (cronológica): `v0.5.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 55

-  minimal typehints in tests
-  type hinting in backends
-  type hints + minor changes
-  optimize reductions in torch where possible
-  type hinting for einmix
-  add type casts to layers' implementations to suppress mypy warnings
-  type hints for layers
-  einsum: fix type hints, fix mypy warnigns, more hinting
-  fox type hints
-  add testing as one of hatch scripts
-  addressing mypy comments
-  use dunders in overloads as positional-only for python 3.7 and earlier
-  Update example to match description
-  Merge pull request #217 from EPronovost/fix-example
-  Merge pull request #221 from arogozhnikov/type-hinting
-  minor formatting things
-  replace stringy type hint with Any
-  check in demo for pack and unpack
-  minor
-  add readme to docs_src to stop confusing people
-  undo adding readme because of conflicts with mkdocs's 'strict mode'
-  make einsum's docstring compatible with strict mode in mkdocs
-  manually add css for codehilite
-  minor
-  minor (formatting, wording)
-  add concat operation to all backends
-  bump version to pre, allow top-level import
-  add an implementation of packing
-  add tests for packing operations
-  skip some tests for mxnet
-  resolve pytorch deprecation warning for assert_allclose
-  add suppression of warnings for local debugging on mac
-  minor changes in notebook, move to documentation folder
-  add note about part 4 of tutorial in readme
-  Merge pull request #222 from arogozhnikov/packing
-  deabbreviate PS as packed shapes everywhere
-  minor
-  add softlink to notebook-4 to documentation
-  remove deprecated requirements
-  change to an actual version of python
- ... e mais 15 commits

### Release 5

Link: https://github.com/arogozhnikov/einops/releases/tag/v0.7.0
- Tag: `v0.7.0`
- Nome: V0.7.0: torch.compile, preserve axis identity, array api
- Publicada em: 2023-10-01
- Release anterior (cronológica): `v0.7.0rc2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 14

-  Update README.md
-  fix #279, update description
-  use oneflow from pypi for tests
-  Merge pull request #281 from arogozhnikov/dev
-  add support for any/all, see #278
-  re-implement bit_count for old pythons (python3.8 in particular)
-  exclude chainer from tests for any/all
-  do not run most tests on any/all, as chainer does not support those
-  maintenance: cache pip dependencies
-  Merge pull request #283 from arogozhnikov/pipcache
-  maintenance: update versions of github actions
-  Merge pull request #285 from arogozhnikov/update_actions
-  set version to 0.7.0
-  Merge remote-tracking branch 'origin/master'
