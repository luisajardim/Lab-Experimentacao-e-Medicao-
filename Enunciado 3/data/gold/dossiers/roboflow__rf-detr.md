# roboflow/rf-detr

Repositório: https://github.com/roboflow/rf-detr

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/roboflow/rf-detr/releases/tag/1.4.1
- Tag: `1.4.1`
- Nome: RF-DETR 1.4.1
- Publicada em: 2026-01-30
- Release anterior (cronológica): `1.4.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 21

-  fix: Adjust class count in `train_from_config` for Roboflow datasets (#588)
-  make the release action trigger with post tags (#589)
-  bump version from `1.4.0` to `1.4.0.post0`
-  Merge pull request #590 from roboflow/develop
-  Fix license link badges in installation section (#591)
-  update YOLO dataset format support (#74)
-  chore: exclude python 3.9 from `pyproject.toml` (#594)
-  Hotfix: pin `transformers` dependency to version range >4.0.0, <5.0.0 (#599)
-  chore(pre-commit): ⬆ pre_commit autoupdate (#598)
-  Chore GH Actions workflows to use `release` event & asset uploads (#575)
-  [BUG][CLI] Fix error in cli script (#246)
-  Modified misleading num_classes Warnings (#261)
-  enh: add custom print-freq argument (#603)
-  add type annotations to cli (#604)
-  ENH: add type annotations to platform module (#605)
-  Add F1 score assertions and clarify IoU threshold in `test_intermediate_scenario` (#596)
-  Simplify PR conflict labeler workflow (#613)
-  add missing warnings module import
-  update checkpoint tables with license column (#614)
-  bump version to `1.4.1`
-  Reorder `Upload assets to GitHub Release` step in workflow

### Release 2

Link: https://github.com/roboflow/rf-detr/releases/tag/1.6.4
- Tag: `1.6.4`
- Nome: v1.6.4: custom pretrain_weights
- Publicada em: 2026-04-10
- Release anterior (cronológica): `1.6.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 14

-  Add `class_name` to `predict()` detections data to clarify 0-indexed class IDs (#914)
-  chore(pre-commit): ⬆ pre_commit autoupdate (#926)
-  Fix missing Optional type hint in config.py (#795)
-  fix: enable multi-GPU DDP training in Jupyter notebooks (#928)
-  fix: preserve fine-tuned checkpoints when MD5 mismatches on existing file (#935)
-  Fix: resolution kwarg silently ignored in RFDETR.train() (#933)
-  refactor: add missing explicit (non-dynamic) imports silence linter errors (#719)
-  Fix `torch.export.export` compatibility in transformer decoder (#936)
-  fix: pad training dataset to prevent partial grad-accum windows (#937)
-  Add regression test for fine-tuned checkpoint returning OOB class IDs (#938)
-  fix: wire DatasetGridSaver into training — save_dataset_grids was silently a no-op (#946)
-  Fix segmentation multi-GPU DDP crash: find_unused_parameters + fused AdamW precision gate (#947)
-  fix: reconcile cherry-picked training regressions
-  releasing `1.6.4`

### Release 3

Link: https://github.com/roboflow/rf-detr/releases/tag/1.7.1
- Tag: `1.7.1`
- Nome: v1.7.1: Stability (BF16 train & ckpt loading)
- Publicada em: 2026-05-28
- Release anterior (cronológica): `1.7.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 9

-  rolling to the future `1.8.0.dev`
-  Add NumPy 2.x `np.complex_` compatibility shim in package init (#1064)
-  Handle starter checkpoints in `RFDETR.from_checkpoint` when `pretrain_weights` is unset-like (#1065)
-  test(tflite): mask ai_edge_litert in the interpreter mock fixture (#1069)
-  tests: add regression and integrity checks for benchmark download helpers (#1075)
-  fix(segm): keep grad_input fp32 in bf16-mixed AMP backward (#1076)
-  test(datasets): add output-size regression tests (#1077)
-  fix(training): make `_use_fused_optimizer` doctest HW-deterministic (#1081)
-  releasing `1.7.1`

### Release 4

Link: https://github.com/roboflow/rf-detr/releases/tag/1.9.1
- Tag: `1.9.1`
- Nome: v1.9.1: Faster Inference & Export, Correct Export Resize
- Publicada em: 2026-08-04
- Release anterior (cronológica): `1.9.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 17

-  fix(config): `keypoint_flip_pairs` accepts None (#1248)
-  docs(export): fix ONNX Runtime example missing decode step (#1251)
-  fix: slight correction needed for "uv sync" to work (#1253)
-  fix(docs): correct keypoint Params (126.4 → 40.7) and add Params to keypoint benchmarks (#1258)
-  docs(llms): add keypoint coverage to llms.txt and llms-full.txt (#1260)
-  perf: 2.5x faster ExecuTorch XNNPACK inference (#1262)
-  fix(augment): accept a scalar or a pair for Kornia range params (#1255)
-  perf(inference): skip upsampling masks the caller's threshold discards (#1265)
-  fix(deps): gate onnx and executorch extras to interpreters with wheels (#1267)
-  perf(postprocess): pick selected rows without materialising repeated index tensors (#1268)
-  fix(export): match predict()'s antialias=False resize in ONNX/TFLite inference, benchmark and INT8 calibration (#1269)
-  chore(pre-commit): ⬆ pre_commit autoupdate (#1274)
-  refactor: enable mypy strict checking for rfdetr.variants (#1270)
-  refactor: enable mypy strict checking for rfdetr.assets.model_weights (#1273)
-  ci(deps): harden optional dependency resolution
-  test(predict): cover threshold forwarding
-  releasing `1.9.1`

### Release 5

Link: https://github.com/roboflow/rf-detr/releases/tag/1.9.2
- Tag: `1.9.2`
- Nome: v1.9.2: Fixed Roboflow COCO & perf. optim
- Publicada em: 2026-08-11
- Release anterior (cronológica): `1.9.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 23

-  perf(eval): count labels on host in matching (#1276)
-  perf(transformer): avoid materialising repeated top-k gather indices in two-stage selection (#1278)
-  fix(detr): use the resolution-override config when building evaluate()'s datamodule (#1280)
-  perf(matcher): copy only the diagonal cost blocks to CPU before assignment (#1281)
-  perf(postprocess): skip redundant CUDA presence checks in keypoint decode (#1282)
-  fix: guard `ModelContext.reinitialize_detection_head` against cleared weights (#1283)
-  refactor: enable mypy strict checking for rfdetr.datasets.yolo (#1288)
-  fix(eval): log EMA validation metrics under `eval_ema_only` when the base metric is empty (#1289)
-  refactor: enable mypy strict checking for rfdetr.detr (#1299)
-  refine(repro): enable deterministic algorithms (#1307)
-  fix(datasets): retry corrupt COCO zip downloads (#1306)
-  perf(matcher): compute detection-only cost matrix padded to max(T_i), not sum(T_i) (#1297)
-  fix(weights): don't warn about the deterministic `_kp_active_mask` buffer as a missing weight (#1302)
-  fix(weights): only warn about the legacy query fallback when it actually truncates (#1301)
-  refactor: enable mypy strict checking for rfdetr.datasets.save_grids (#1304)
-  fix(coco): drop unannotated grouping categories (#1303)
-  fix(inference): normalise the index-less cuda device before the deferred-move guard compares it (#1311)
-  perf(matcher): vectorize the compact-path safety gate's box/label sweeps (#1312)
-  perf(inference): pin CPU image tensors before the CUDA transfer in predict() (#1313)
-  fix(training): leave completed Rich epoch bars in terminal history without corrupting them (#1316)
-  fix(training): restore callback state when resuming from `BestModelCallback`'s checkpoints (#1318)
-  fix(training): remove stale mypy type: ignore in module_data.py
-  releasing `1.9.2`
