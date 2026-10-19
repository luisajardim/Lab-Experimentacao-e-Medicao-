# jsx-eslint/eslint-plugin-react

Repositório: https://github.com/jsx-eslint/eslint-plugin-react

## Metadados

- Linguagem: JavaScript

## Releases sorteadas

### Release 1

Link: https://github.com/jsx-eslint/eslint-plugin-react/releases/tag/v5.1.1
- Tag: `v5.1.1`
- Nome: (sem nome)
- Publicada em: 2016-05-09
- Release anterior (cronológica): `v5.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  Fix require-render-return crash (fixes #589)
-  Update CHANGELOG and bump version

### Release 2

Link: https://github.com/jsx-eslint/eslint-plugin-react/releases/tag/v6.2.1
- Tag: `v6.2.1`
- Nome: (sem nome)
- Publicada em: 2016-09-12
- Release anterior (cronológica): `v6.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 11

-  [Docs] `prefer-stateless-function`: fix docs for `ignorePureComponents` option.
-  Fix readme link (#794)
-  Add examples of correctly specified propTypes
-  Merge pull request #813 from AndiDog/patch-1
-  Fix typo in no-unused-prop-types.md (#815)
-  Fix false positive in no-unused-prop-types (fixes #801)
-  Fix jsx-no-target-blank to target only anchor elements
-  Use ESLint markVariableAsUsed method instead of our (now useless) custom one (fixes #799)
-  Fix no-target-blank to be case insensitive
-  Update dependencies
-  Update CHANGELOG and bump version

### Release 3

Link: https://github.com/jsx-eslint/eslint-plugin-react/releases/tag/v7.7.0
- Tag: `v7.7.0`
- Nome: v7.7.0
- Publicada em: 2018-02-20
- Release anterior (cronológica): `v7.6.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 29

-  Exclude references to this.state in setState callback
-  Fix typo in comment
-  [New] `forbid-foreign-prop-types`: Add `allowInPropTypes` option
-  [Docs] add `jsx-child-element-spacing`
-  Merge pull request #1610 from pfhayes/setstate
-  [Fix] `no-danger-with-children`: prevent infinite loop
-  test(sort-prop-types) Add failing test for when `sortShapeProp` is true and shape not object literal
-  fix(sort-prop-types): Fix sortShapeProp when shape is not an object literal
-  Merge pull request #1669 from justinanastos/fix/sort-prop-types-shape-no-properties-1668
-  [Fix] `jsx-child-element-spacing`: fix error location
-  Fix an issue with the documentation for 'jsx-child-element-spacing'
-  Created test
-  Fixed bug
-  Added more tests
-  Added more valid tests
-  Added more tests
-  Merge pull request #1675 from yuri-sakharov/fix/react-no-unused-prop-types
-  Test
-  Added test & working
-  [docs] add missing rule to readme
-  Rearranged tests to be at the bottom of componentWillReceiveProps tests. Added a default parser test.
-  [Tests] clean up some formatting
-  Merge pull request #1690 from mindspacepdx/am-should-component-update
-  [Tests] Added tests for jsx-curly-spacing that deal with comments in children.
-  [Tests] number comments to more easily locate failures
-  [Fix] jsx-curly-spacing problem in new tests, fixes #1414
-  [New] Add `jsx-max-depth`
-  [Dev Deps] update `babel-eslint`, `eslint`, `istanbul`, `mocha`
-  Update CHANGELOG and bump version

### Release 4

Link: https://github.com/jsx-eslint/eslint-plugin-react/releases/tag/v7.32.2
- Tag: `v7.32.2`
- Nome: v7.32.2
- Publicada em: 2023-01-29
- Release anterior (cronológica): `v7.32.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 6

-  [Fix] configs: restore `parserOptions` in legacy configs
-  [Tests] avoid a deprecation warning
-  [Fix] `jsx-no-constructed-context-values`, `jsx-no-useless-fragment`: add a rule schema
-  [Fix] `no-unknown-property`: add `fill` for `<marker>`
-  [Tests] `button-has-type`: add passing test
-  Update CHANGELOG and bump version

### Release 5

Link: https://github.com/jsx-eslint/eslint-plugin-react/releases/tag/v7.35.0
- Tag: `v7.35.0`
- Nome: v7.35.0
- Publicada em: 2024-07-20
- Release anterior (cronológica): `v7.34.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 21

-  [New] export flat configs from plugin root and fix flat config crash
-  [New] add `jsx-props-no-spread-multi`
-  [Tests] remove duplicate tests
-  [Tests] `hook-use-state`: test suggestions with `messageId` instead of `desc`
-  [Tests] test rules with ESLint v9
-  add `tests/helpers/getRuleDefiner.js`
-  [New] support eslint v9
-  [Fix] `no-invalid-html-attribute`: substitute placeholders in suggestion messages
-  [actions] Don't install with `--legacy-peer-deps` in pretest check
-  [New] support eslint v9
-  [New] `forbid-component-props`: add `propNamePattern` to allow / disallow prop name patterns
-  [New] `jsx-handler-names`: support ignoring component names
-  [Refactor] `variableUtil`: Avoid creating a single flat variable scope for each lookup
-  [New] version settings: Allow react defaultVersion to be configurable
-  [New] `jsx-closing-tag-location`: add `line-aligned` option
-  [New] `no-danger`: add `customComponentNames` option
-  [Dev Deps] update `@babel/core`, `@babel/eslint-parser`
-  [meta] no point in supporting eslint 9.0 - 9.6 initially
-  [Fix] `sort-prop-types`: single line type ending without semicolon
-  [Fix] `require-default-props`: report when required props have default value
-  Update CHANGELOG and bump version
