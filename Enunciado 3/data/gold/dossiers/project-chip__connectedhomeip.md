# project-chip/connectedhomeip

Repositório: https://github.com/project-chip/connectedhomeip

## Metadados

- Linguagem: C++

## Releases sorteadas

### Release 1

Link: https://github.com/project-chip/connectedhomeip/releases/tag/test_event_2_2012_04_21
- Tag: `test_event_2_2012_04_21`
- Nome: Updated rollup branch for test event 2
- Publicada em: 2021-04-21
- Release anterior (cronológica): `test_event_2_2012_04_19`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 32

-  [zcl] Log string attributes when parsing ZCL responses (#6126)
-  Replace the EndPoint::PrepareIO() functions with stored state (#6109)
-  [im] Update codegen for #6019 (#6119)
-  Fix CheckExchangeMessages crashes when malicious packet is sent (#6120)
-  Add presubmit checks for RPCs (#6056)
-  Optimize memory usage by refactoring ExchangeContext (#5942)
-  [M5Stack] Add a Screen to control the Door Lock Cluster (#6113)
-  ESP32: Advertisement stop error for slow advertisement timeout (#6129)
-  Change default setup pin code from 12345678 to 20202021 (#6133)
-  CHIPSetupPayloadParserTests fails (#6140)
-  chip-device-ctrl: add ability to configure reporting (subscribe) (#6138)
-  Build failure on some platforms because of an unused variable and some conversion issues (#6154)
-  [zcl] Enable optional Basic Cluster attributes for controller apps (#6135)
-  Use Network Provisioning for both chip-tool and ChipTool iOS (#5990)
-  ZAP generation fails after #6135 for src/controller and src/darwin (#6161)
-  iOS ChipTool does not compile: No visible @interface for 'NSData' declares the selector 'dataUsingEncoding:' (#6162)
-  Build error when compiling with define BIGENDIAN_CPU set (#6143) (#6158)
-  chip_bypass_rendezvous=true does not work anymore after #6065 (#6160)
-  Revert "Fix CheckExchangeMessages crashes when malicious packet is sent (#6120)" (#6164)
-  [ble] update Service Data UUID (#6163)
-  uint64_t support in emberAfFillExternalBuffer (#6100)
-  Implement Operational Credentials Cluster for initial Fabric support (#6096)
-  [cirque] Add cirque test for Python device controller (#5851)
-  Use spec defined max application message size (#6174)
-  Adding Darwin focused CI. Resolves: #506 (#6168)
-  Add IM AttributePahParams CommandPathParams CommandPathParams (#6149)
-  [ble/rendezvous] Decouple BLE transport from Rendezvous (#5337)
-  [python] Update document of python device controller (#6197)
-  Use endpoint 0 instead of 1 in iOS ChipTool for Network Provisioning, Echo and Bindings (#6165)
-  Crash in -[BleConnection start] (#6169)
-  [im] Add command obj to all cluster callbacks (#5994)
-  [cc13x2x7_26x2x7] Fix BLE Provisioning issues for TE#2 (#6152)

### Release 2

Link: https://github.com/project-chip/connectedhomeip/releases/tag/v1.0.0
- Tag: `v1.0.0`
- Nome: V1.0.0 Release
- Publicada em: 2022-09-30
- Release anterior (cronológica): `test_event_4_2021_07_06`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Update TV app to use the new IM changes (#7906)
-  fix condition for setting ble name (#8114)
-  Remove PeerConnectionState::mTransport (#8109)
-  Use {{chip_server_responses}} instead of multiple #ifs for iterating over the command responses (#8059)
-  Revert "Adding request-commissioning CHIPTool command (#7729)" (#8095)
-  Move APP/gen/callback.h to src/app/common/gen/ (#8065)
-  Added Command Line Tool to Generate Attestation Certificates (#7981)
-  Use gdbus for openthread (#7913)
-  [hotfix] Fix regression / crash caused by #7873 (#8054)
-  Split up src/platform/BUILD.gn (#8099)
-  add ESP32C3 CI (#7942)
-  Implement TLV in CASE Sigma Protocol (#7952)
-  Fix crash when receiving a message that wants an ack on a closed exchange that's still alive. (#8068)
-  Fix compile error, due to merge conflict (#8127)
-  Remove dead code (#8108)
-  Fix python compile. (#8135)
-  SRP publish not triggered on renewal of entry (#8118)
-  [TE4] Enable Lighting Devices types cluster and attributes (#7934)
-  Update build timeouts from 15/20 minutes to 25/30 minutes. (#8140)
-  Fix mbedtls version in .gitmodules (#8142)
-  Make chip-echo-requester run on a single event loop (#8100)
-  CSR support in crypto HSM (#7897)
-  Don't wait for CASE connection if resolve fails in chip-device-ctrl (#8161)
-  Darwin BLE: fix length check in advertisement data (#8112)
-  Remove unused or redundant helpers from src/app/zap-templates/templates/app/helper.js (#8141)
-  [im] Add helper for mapping ember error code to im protocol code (#8131)
-  Log string attribute value into CHIPClientCallbacks.cpp (#8134)
-  [TV App] Enable missing attributes  (#8120)
-  Mbed: Add 'cortex-debug' vscode extension to devcontainer.json (#8122)
-  Clean up temporary error code macros added in PR#7916 (#8119)
-  Add CHIP_Crypto_HMAC implementation (#8144)
-  Minor clean-ups in src/crypto (#8182)
-  Fix bloat check workflow concurrency (#8189)
-  [util] Introduce `to_underlying` for casting enum classes to underlying values. (#8125)
-  [ChipTool] Add pairing qrcode/manualcode option (#8168)
-  Improve PlatformManager documentation. (#8181)
-  [nrfconnect] Minor shell improvements (#8156)
-  Add test for sending a command to an unsupported endpoint (#8073)
-  Enable ECDH derive secret with HW accelerated crypto engine (#8155)
-  Zap add accessors helpers for attributes (#7183)
- ... e mais 210 commits

### Release 3

Link: https://github.com/project-chip/connectedhomeip/releases/tag/v1.0.0.2
- Tag: `v1.0.0.2`
- Nome: v1.0.0.2 Bug Fix Release
- Publicada em: 2023-01-03
- Release anterior (cronológica): `V1.0.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  Update ZAP to tip. (#24141)
-  Remove the MfgSpecificPing command from Darwin API. (#24139)
-  Update ZAP to tip. (#24160)
-  basic_information: change the name of emberAfBasicInformationClusterServerInitCallback (#24162)
-  Go back to using the storage key 1.0 used for group fabric info. (#24163)

### Release 4

Link: https://github.com/project-chip/connectedhomeip/releases/tag/v1.4.2.0
- Tag: `v1.4.2.0`
- Nome: v1.4.2.0 Release
- Publicada em: 2025-06-27
- Release anterior (cronológica): `v1.4.0.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 250

-  Add TC_CCTRL_2_1, TC_CCTRL_2_2, TC_CCTRL_2_3 to CI (#35886)
-  Documentation: Fix defaults on build_python.sh (#35901)
-  Add provisional General Commissioning Cluster TCUpdateDeadline attribute (#35903)
-  Make use of DataModel::Provider device type resolution in the access control (#35862)
-  Add missing feature map bit (#35915)
-  When logging work items in MTRDevice_Concrete, include names, not just ids. (#35920)
-  Fix Matter.framework path descriptions to be more readable. (#35921)
-  Fix formatting of unknown IDs in MTRClusterNames bits. (#35922)
-  Fix some error messages when XPC exceptions happen. (#35923)
-  tv-casting-app fix load stale binding endpoints from un-needed fabrics (#35907)
-  Re-enerated using updated alchemy which recognizes Cameras domain (#35895)
-  Update Darwin availability annotations for new camera bits. (#35925)
-  [Fabric-Sync] Fix compile warnings (#35927)
-  Use ScheduleLambda() instead of PlatformMgr().ScheduleWork to excute command (#35926)
-  Enable MRP in WiFi-PAF commissioning (#35500)
-  [Linux] Matter Linux Water Leak Detector Example (#35392)
-  [HotFix] Missing declaration in provisional water-leak-detector-app.m… (#35938)
-  WebRTC requestor cluster (#35910)
-  Move some Matter.framework server APIs used only with concrete controllers to the concrete controller class. (#35943)
-  Remove PASE verifier computation overrides from MTRDeviceController_Concrete. (#35945)
-  Add a size-display script for binaries. (#35942)
-  Fix handling of controllerNodeID on non-concrete controllers. (#35946)
-  Clean up asyncGetCommissionerOnMatterQueue on MTRDeviceController. (#35947)
-  Fix efr32 test_driver build and make sure the linkerfile matches the target board (#35952)
-  One more decouple from ember from src/app and ensure we can compile without `ember-compatibility-functions.cpp` (#35919)
-  [Fabric-Bridge] Replace ScheduleWork with ScheduleLambda (#35949)
-  [ICD] Make optional spec checks mandatory with the launch of LongIdleTime ICDs (#35956)
-  [java]fix errorcode in GetConnectedDeviceCallbackForTestJni (#35958)
-  Fix android batch command test (#35954)
-  Make function argument a reference, to avoid passing in struct data around (#35950)
-  Remove a test-only method from base MTRDeviceController. (#35944)
-  Fix attribute-table logs to not log strings as %p. (#35941)
-  Documentation: getting started - changing examples (#35929)
-  Add missing feature map bit (#35915) (#35961)
-  Fix --int-arg, --bool-arg, etc options parsing (#35249)
-  Add TC_BRBINFO_4_1 to CI (#35940)
-  [darwin-framework-tool] Automatically check for leaks on shutdown if enable_leak_checking is true (#35936)
-  DM XMLs: Remove a couple of clusters/DTs not in 0.9 (#35937)
-  Add restyled workflow (#35967)
-  Fix mis-quote in pullapprove (#35968)
- ... e mais 210 commits

### Release 5

Link: https://github.com/project-chip/connectedhomeip/releases/tag/v1.5.1.0
- Tag: `v1.5.1.0`
- Nome: v1.5.1.0 Release
- Publicada em: 2026-04-13
- Release anterior (cronológica): `v1.5.0.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 51

-  [WebRTC] Align test scripts with test plan trickle ICE update (#41990) (#42226)
-  [1.5 CI cherrypicks] - fix up CI runs for 1.5 (#42263)
-  [Backport v1.5]: Enable TCP support for ESP platform (#42281)
-  Integrate NXP MCU missing changes in v1.5-branch (#42289)
-  esp32: fix ICD configuration options (#42339) (#42385)
-  esp32: fix issues for network commissioning test cases of incorrect ssid or password (#42320) (#42386)
-  [v1.5 Backport] Integrate NXP MCU missing changes in v1.5-branch (#42450)
-  [1.5-branch] Cherry-pick the latest Server Cluster Interface changes for WebRTC Requester Cluster (#42572)
-  [1.5-branch] Migrate WebRTC Provider Cluster to Server Cluster Interface (#42571)
-  gitmodules: exclude unnecessary submodule cloning for esp32 (#42007) (#42651)
-  TestSystemCommands: Improve application startup detection to prevent sending a SIGTERM before signal handler is setup (#41688) (#42720)
-  [1.5-branch] Migrate TLS Client Management Cluster to code-driven (#42395) (#42662)
-  [1.5-branch] Cherry-pick Migrate TLS Certificate Management Cluster to code-driven (#42455) (#42740)
-  [Cherry Pick] cherry pick ACE_2_4 test and device reboot functionality onto 1.5.1 (#42684)
-  [1.5-branch] Cherry-pick Rename TlsCertificateManagementCluster to TLSCertificateManagementCluster (#42731) (#42747)
-  [AVSUM] Handle spec updates to Pan and Tilt Min and Max Ranges (#42114) (#42766)
-  Cherry-pick revision conformance (#42757)
-  Cherry-picks: PRs supporting provisional CDs (with correct base branch this time) (#42761)
-  Fix CMAF clip duration calculation and recorded file cleanup (#41699) (#42768)
-  Fix Camera app crash on multiple start and stop sessions. (#42442) (#42769)
-  Cherry Pick -> [Chime] XML and Zap Regen for Chime Cluster updates per spec. (#42671) (#42773)
-  [AVSUM] Initial PR for conversion to Code Driven - Rename of cluster and associated classes (#42279) (#42776)
-  Cherry-pick to 1.5: PRs supporting pairing hint TCR (#42784)
-  [v1.5-branch CP] TC-SC-3.5: Fix Bug in Test Script, accepting DUT Commissioner without ICAC in its chain (#42775)
-  Cherry-pick to 1.5: 1.5.1 DM files (#42780)
-  [Cherry Pick] Camera AVSM changes for Code Driven Migration to 1.5.1 (#42767)
-  Cherry-pick(#42273): Check for self-conflict on TLS ep update (#42765)
-  [Push AV] Fix issue in Motion Zone based clip recording (#42417) (#42770)
-  Cherry pick -> [AVSUM] Migrate to use of the DefaultServerCluster (code driven( (#42… (#42787)
-  [Push AV] Refactor clip recorder with status enums and error handling (#42681) (#42771)
-  Cherry pick -> [Chime] PRs to convert Chime to Code Driven and new functionality (#42785)
-  Disable kotlin static code analysis (#41933) (#42803)
-  Cherry-pick(#42599, #42713, #42741): [Camera SDK 1.5.1] Push AV XML update and SDK updates (#42772)
-  Cherry-pick(#42367, #42368, #42370): [Push AV 1.5.1] Update upload sequence of the record clip files (#42860)
-  [1.5-branch] Cherry pick [WebRTC] Support multiple streams during WebRTC session establishment (#42827) (#42859)
-  [CherryPick] Add CameraAVSM test scripts for test cases in CameraAVSM Testplan PR 5640 (#42832) (#42857)
-  [1.5-branch] Cherry-pick Fix camera app crashes on unexpected SDPs  (#42923)
-  [1.5-branch] Fix failed fabric removal due to TLS enpoint's fabric index lookup failure (#42951)
-  [1.5-branch] Cherry-pick Parse and set ICE servers to PeerConnection (#42955) (#42999)
-  [Ameba] Cherry-pick fix for WiFi connection and server initialization (#43019)
- ... e mais 11 commits
