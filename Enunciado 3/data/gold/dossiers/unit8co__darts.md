# unit8co/darts

Repositório: https://github.com/unit8co/darts

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/unit8co/darts/releases/tag/0.3.0
- Tag: `0.3.0`
- Nome: Release 0.3.0
- Publicada em: 2020-10-06
- Release anterior (cronológica): `0.2.2`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/unit8co/darts/releases/tag/0.31.0
- Tag: `0.31.0`
- Nome: Darts minor 0.31.0
- Publicada em: 2024-10-13
- Release anterior (cronológica): `0.30.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 35

-  Release 0.30.0
-  Fix/regr model hist fc static covs no target lags (#2426)
-  fix bug in shapexplainer with native multioutput support and explaini… (#2428)
-  Replacing the obsolete applymap with map (#2436)
-  Uses applymap for older versions of pandas (for new ones map is used). (#2443)
-  Replacement of deprecated Series.fillna -> 'method' with ffill() and bfill(). (#2442)
-  Added the IQR Detector (#2441)
-  fix the sample_weights bug (#2445)
-  Update README.md to be more colorblind friendly (#2433)
-  Access a value by position, use iloc. (#2448)
-  Removes warning: "Passing literal json to 'read_json' is deprecated". (#2450)
-  fix: PerformanceWarning - DataFrame is highly fragmented (#2447)
-  Fix Issue 2454 (#2455)
-  rewrite Hyperparameter optimization with Ray Tune (#2459)
-  Improvement/Adds temporal_hidden_size_past and temporal_hidden_size_future hyperparams to TiDEModel (#2416)
-  Convert pd_series1 to float64 type. (#2466)
-  fix resampling with DateOffset (#2479)
-  Use pd_series3 in tests, was always using series2 before (#2474)
-  Allow broadcasting single-sample TimeSeries onto multi-sample TimeSeries (#2476)
-  fix series_reduction docstring (#2486)
-  Fix/RegressionEnsembleModel save and load (#2465)
-  Update 21-TSMixer-examples.ipynb (#2508)
-  Bump jupyterlab from 4.0.11 to 4.2.5 in /requirements (#2515)
-  Fix/bug time series.from group dataframe 2491 (#2512)
-  attempt to fix failing test due to randomness (#2518)
-  Fix/update doc (#2511)
-  Feature add activation to BlockRNN (#2492) (#2504)
-  Fix/bug 2491 revisited (#2520)
-  Fix/bug time series.append and prepend (#2522)
-  fixes bug when plotting multivariate probabilistic series where the c… (#2532)
-  Fix/optimized hfc prob regr (#2534)
-  Feat/metrics quantiles (#2530)
-  Fix the comment of scorers_are_univariate (#2542)
-  fix plkl param prediction with multi_models=False (#2545)
-  Release 0.31.0 (#2561)

### Release 3

Link: https://github.com/unit8co/darts/releases/tag/0.40.0
- Tag: `0.40.0`
- Nome: Darts minor 0.40.0
- Publicada em: 2025-12-23
- Release anterior (cronológica): `0.39.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 10

-  Release 0.39.0
-  Fix/tft explainer index error (#2957)
-  add steps to check storage (#2963)
-  [New Model] Support Chronos-2 small and synthetic variants (#2962)
-  fix PLForecastingModel.configure_torch_metrics() with updated args (#2958)
-  upper cap 'scikit-learn<1.8.0' until catboost updates (#2972)
-  Feat/darts options (#2956)
-  Fix typos in Chronos-2 notebook (#2975)
-  Add Autoregression Compatibility for Optimized Historical Forecasts on SKLearn models (#2921)
-  Release 0.40.0 (#2978)

### Release 4

Link: https://github.com/unit8co/darts/releases/tag/0.42.1
- Tag: `0.42.1`
- Nome: Darts patch 0.42.1
- Publicada em: 2026-03-07
- Release anterior (cronológica): `0.42.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  Release 0.42.1 (#3036)
-  Bump version: 0.42.0 → 0.42.1

### Release 5

Link: https://github.com/unit8co/darts/releases/tag/0.43.0
- Tag: `0.43.0`
- Nome: Darts minor 0.43.0
- Publicada em: 2026-03-23
- Release anterior (cronológica): `0.42.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 4

-  Return axes from TFTExplainer.plot_variable_selection (#3039)
-  Feature: Allow specifying a subset of columns to apply the data transformer on (#3023)
-  update changelog (#3042)
-  Bump version: 0.42.1 → 0.43.0
