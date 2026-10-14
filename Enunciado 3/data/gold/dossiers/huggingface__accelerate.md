# huggingface/accelerate

Repositório: https://github.com/huggingface/accelerate

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/huggingface/accelerate/releases/tag/v0.11.0
- Tag: `v0.11.0`
- Nome: v0.11.0 Gradient Accumulation and SageMaker Data Parallelism
- Publicada em: 2022-07-18
- Release anterior (cronológica): `v0.10.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 40

-  Offload and modules with unused submodules (#442)
-  Better checks for if a TPU device exists (#456)
-  Right step point (#459)
-  Raise a clear warning if a user tries to modify the AcceleratorState (#458)
-  Handle bfloat16 weights in disk offload (#460)
-  Handle bfloat16 weights in disk offload without adding memory overhead (#460) (#461)
-  Include bf16 support for TPUs and CPUs, and a better check for if a CUDA device supports BF16 (#462)
-  Fix subtle bug in BF16 (#463)
-  Link CI slow runners to the commit (#464)
-  Cleanup CI Warnings (#465)
-  Expose some is_*_available utils in docs (#466)
-  Add docbuilder to quality (#468)
-  Refactor Utility Documentation (#467)
-  Fix when TPU device check is ran (#469)
-  Dev version
-  Some typos and cosmetic fixes (#472)
-  Pin datasets for now (#477)
-  Revert "Pin datasets for now (#477)" (#478)
-  Rm gradient accumulation on TPU (#479)
-  Use datasets 2.2.0 for now (#481)
-  fixing fsdp autowrap functionality (#475)
-  add use_distributed property (#487)
-  Introduce automatic gradient accumulation wrapper + fix a few test issues (#484)
-  update dataloader wrappers to have `total_batch_size` attribute (#493)
-  Fix scheduler in gradient accumulation example (#500)
-  SageMaker DP Support (#494)
-  SageMaker enhancements to allow custom docker image, input channels referring to s3/remote data locations and metrics logging (#504)
-  Fix DispatchDataLoader length when `split_batches=True` (#509)
-  Make gradient accumulation work with dispatched dataloaders (#510)
-  Add gradient accumulation doc (#511)
-  Add benchmarks (#506)
-  Fix a bug when reduce a tensor. (#513)
-  Don't unwrap in save_state() (#489)
-  Add special Parameters modules support (#519)
-  fixing deepspeed multi-node launcher (#514)
-  Fixup all example CI tests and properly fail (#517)
-  Warn user if no trackers are installed (#524)
-  FSDP integration enhancements and fixes (#522)
-  Relese: v0.11.0
-  Fix accelerate tests command (#528)

### Release 2

Link: https://github.com/huggingface/accelerate/releases/tag/v0.13.0
- Tag: `v0.13.0`
- Nome: v0.13.0 Launcher update (multinode and GPU selection) and mutliple bug fixes
- Publicada em: 2022-10-05
- Release anterior (cronológica): `v0.12.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 70

-  v.0.13.0.dev0
-  Fix typo in docs/index.mdx (#610)
-  Fix DeepSpeed CI (#612)
-  Trigger doc build
-  Added GANs example to examples (#619)
-  Fix example (#620)
-  Update README.md (#622)
-  Fully remove `subprocess` from the multi-gpu launcher (#623)
-  M1 mps fixes (#625)
-  Fix multi-node issues and simplify param logic (#627)
-  Integrate Rich into Accelerate (#613)
-  update MPS support docs (#629)
-  minor tracker fixes for complete* examples (#630)
-  Use torchrun for multinode (#631)
-  Put back in place the guard (#634)
-  make init_trackers to launch on main process (#642)
-  remove check for main process for trackers initialization (#643)
-  fix link (#645)
-  Add static_graph arg to DistributedDataParallelKwargs. (#637)
-  Small nits to grad accum docs (#656)
-  Saving hyperparams in yaml file for Tensorboard for #521 (#657)
-  Use debug for loggers (#655)
-  Improve docstrings more (#666)
-  accelerate bibtex (#660)
-  Cache torch_tpu check (#670)
-  Manim animation of big model inference (#671)
-  Fix multi-node issues from launch (#672)
-  Make rich an optional dep (#673)
-  Add aim tracker for accelerate (#649)
-  Specify local network on multinode (#674)
-  Test for min torch version + fix all issues (#638)
-  deepspeed enhancements and fixes (#676)
-  DeepSpeed launcher related changes (#626)
-  adding torchrun elastic params (#680)
-  :bug: fix (#683)
-  Fix skip in dispatch dataloaders (#682)
-  Clean up DispatchDataloader a bit more (#686)
-  rng state sync for FSDP (#688)
-  Fix DataLoader with samplers that are batch samplers (#687)
-  fixing support for Apple Silicon GPU in `notebook_launcher` (#695)
- ... e mais 30 commits

### Release 3

Link: https://github.com/huggingface/accelerate/releases/tag/v0.17.0
- Tag: `v0.17.0`
- Nome: v0.17.0: PyTorch 2.0 support, Process Control Enhancements, TPU pod support and FP8 mixed precision training
- Publicada em: 2023-03-09
- Release anterior (cronológica): `v0.16.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 72

-  v0.17.0.dev0
-  Deepspeed param check (#1015)
-  enabling `mps` device by default and removing related config (#1030)
-  fix: links to gradient synchronization (#1035)
-  do not scale gradient in bf16 mode (#1036)
-  Pass keywords arguments of backward function deeper to DeepSpeed (#1037)
-  Refactor process executors to be in AcceleratorState (#1039)
-  Add daily slack notifier for nightlies (#1042)
-  Make sure direct parameters are properly set on device (#1043)
-  Add `cpu_offload_with_hook` (#1045)
-  Update quality tools to 2023 (#1046)
-  Load tensors directly on device (#1028)
-  Fix cpu_offload_with_hook code snippet (#1047)
-  Introduce TPU Pod launching to `accelerate launch` (#1049)
-  Use create_task (#1052)
-  Fix args by adding in the defaults (#1053)
-  deepspeed `hidden_size` auto value default fixes (#1060)
-  Introduce PartialState (#1055)
-  Flag for deprecation (#1061)
-  Try with this (#1062)
-  Update integrations (#1063)
-  Swap utils over to use PartialState (#1065)
-  update fsdp docs and removing deepspeed version pinning (#1059)
-  Fix/implement process-execution decorators on the Accelerator (#1070)
-  Refactor state and make `PartialState` first class citizen  (#1071)
-  Add error if passed --config_file does not exist (#1074)
-  SageMaker image_uri is now optional (#1077)
-  Allow custom SageMaker Estimator arguments (#1080)
-  Fix tpu_cluster arg (#1081)
-  Update complete_cv_example.py (#1082)
-  Added SageMaker local mode config section (#1084)
-  Fix config (#1090)
-  adds missing "lfs" in pull (#1091)
-  add multi_cpu support to reduce (#1094)
-  Update README.md (#1100)
-  Tracker rewrite and lazy process checker (#1079)
-  Update performance.mdx (#1107)
-  Attempt to unwrap tracker. (#1109)
-  TensorBoardTracker: wrong arg def (#1111)
-  Actually raise if exception (#1124)
- ... e mais 32 commits

### Release 4

Link: https://github.com/huggingface/accelerate/releases/tag/v0.20.0
- Tag: `v0.20.0`
- Nome: v0.20.0: MPS and fp4 support on Big Model Inference, 4-bit QLoRA, Intel GPU, Distributed Inference, and much more!
- Publicada em: 2023-06-07
- Release anterior (cronológica): `v0.19.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 73

-  v0.20.0.dev0
-  Support TPU v4 with new PyTorch/XLA TPU runtime (#1393)
-  Add in a section on papers using Accelerate (#1399)
-  Support TPU v2 and v3 on new PyTorch/XLA TPU runtime (#1385)
-  Adding support for local SGD. (#1378)
-  use existing mlflow experiment if exists (#1403)
-  changes required for DS integration (#1406)
-  fix deepspeed failing tests (#1411)
-  Make mlflow logging dir optional (#1413)
-  Intel GPU support initialization (#1118)
-  Fix bug on ipex for diffusers (#1426)
-  Improve Slack Updater (#1433)
-  Let quality yell at the user if it's a version difference (#1438)
-  Ensure that it gets installed (#1439)
-  [`core`] Introducing `CustomDtype` enum for custom dtypes (#1434)
-  Fix XPU (#1440)
-  Make sure torch compiled model can also be unwrapped (#1437)
-  fixed: ZeroDivisionError: division by zero (#1436)
-  fix potential OOM when resuming with multi-GPU training (#1444)
-  Fixes in infer_auto_device_map (#1441)
-  Raise error when logging improperly (#1446)
-  Fix ci (#1447)
-  Distributed prompting/inference utility (#1410)
-  Add to (#1448)
-  split_between_processes (#1449)
-  [docs] Replace `state.rank` -> `process_index` (#1450)
-  Auto multigpu logic (#1452)
-  Update with cli instructions (#1453)
-  Adds `in_order` argument that defaults to False, to log in order. (#1262)
-  fix error for CPU DDP using trainer api. (#1455)
-  Refactor and simplify xpu device in state (#1456)
-  Document how to use commands with python module instead of argparse (#1457)
-  4-bit QLoRA via bitsandbytes (4-bit base model + LoRA) (#1458)
-  Fix skip first batch being perminant (#1466)
-  update conversion of layers to retain original data type. (#1467)
-  Check for xpu specifically (#1472)
-  update `register_empty_buffer` to match torch args (#1465)
-  Update gradient accumulation docs, and remove redundant example (#1461)
-  Imrpove sagemaker (#1470)
-  Split tensors as part of `split_between_processes` (#1477)
- ... e mais 33 commits

### Release 5

Link: https://github.com/huggingface/accelerate/releases/tag/v0.29.1
- Tag: `v0.29.1`
- Nome: v0.29.1: Patchfix
- Publicada em: 2024-04-05
- Release anterior (cronológica): `v0.29.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 2

-  Fixup
-  Release: v0.29.1
