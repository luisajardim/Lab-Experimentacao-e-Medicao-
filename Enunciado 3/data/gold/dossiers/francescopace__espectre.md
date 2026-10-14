# francescopace/espectre

Repositório: https://github.com/francescopace/espectre

## Metadados

- Linguagem: Python

## Releases sorteadas

### Release 1

Link: https://github.com/francescopace/espectre/releases/tag/1.2.0
- Tag: `1.2.0`
- Nome: v1.2.0 - Simplified Architecture & MVS Segmentation
- Publicada em: 2025-11-16
- Release anterior (cronológica): (nenhuma)

**Release notes**

_(vazio)_

**Commits desde a release anterior**

_(não disponíveis nos JSONs — use o link da release/compare no GitHub)_

### Release 2

Link: https://github.com/francescopace/espectre/releases/tag/1.4.0
- Tag: `1.4.0`
- Nome: v1.4.0 - Major Refactoring - Technical Debt Reduction
- Publicada em: 2025-11-28
- Release anterior (cronológica): `1.3.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 26

-  fix(wavelet): harden wavelet_denoise with overflow protection and calloc
-  Merge pull request #20 from francescopace/fix/issue-15-wavelet-hardening
-  feat: add ESP32 base configuration (WIP)
-  Fix #16 – Migrate ESPectre CLI from Bash to Python
-  feat: Add Wi-Fi Theremin sonification and enable continuous feature extraction
-  Merge pull request #21 from francescopace/feature/theremin
-  Remove references to the C6 having support for 5GHz WiFi
-  requested changes
-  Merge pull request #23 from kylefmohr/remove-5ghz-references
-  add pygments>=2.19.2
-  Merge pull request #26 from mcfd/patch-1
-  docs: add binary sensor and numeric sensor configurations for Home Assistant
-  feat: Micro-ESPectre - Pure Python motion detection for MicroPython
-  refactor: remove unused K_FACTOR parameter
-  feat: Increase traffic generator max rate to 1000 pps (Nyquist-Shannon theorem)
-  refactor: Centralize configuration and validation logic
-  refactor: Add micro-espectre analysis tools and refactor data processing
-  feat: add two-pass variance algorithm and centralize configuration defaults
-  test: improve segmentation tests with stricter thresholds and memory checks
-  refactor: remove CSI raw data extractor from firmware and web UI
-  refactor: consolidate segmentation logic into csi_processor module
-  refactor: move mqtt_publish_task to mqtt_handler module
-  refactor: extract feature calculation into separate module
-  feat: Add WiFi and device info to MQTT info command
-  feat: Add Hampel filter for turbulence in MVS
-  docs: prepare v1.4.0 release documentation

### Release 3

Link: https://github.com/francescopace/espectre/releases/tag/2.2.0
- Tag: `2.2.0`
- Nome: v2.2.0 - Gain Lock, Low-Pass Filter & ML Data Collection
- Publicada em: 2025-12-19
- Release anterior (cronológica): `2.1.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 18

-  feat: filter null subcarriers based on chip type during NBVI calibration
-  feat: (micro-espectre) add ML data collection infrastructure
-  feat: CSI auto-normalization and dynamic null subcarrier detection
-  feat(micro-espectre): add pytest test suite and simplify tools
-  docs: consolidate documentation and disable Hampel filter by default
-  fix(nbvi): signed/unsigned CSI handling and normalization optimization
-  feat: Butterworth low-pass filter, lazy variance, filters disabled by default
-  feat(nbvi): optimize min_spacing and add guard band exclusion
-  docs: improve dashboard compatibility and document name_add_mac_suffix
-  fix: re-publish threshold to HA after API connection is established
-  docs: improve documentation structure and add project email
-  docs: add landing page
-  feat: Add dynamic gauge option for Home Assistant dashboard
-  docs: improve landing page
-  test: increase test coverage for micro-espectre
-  fix: Pause traffic generator during NBVI calibration processing
-  fix: remove non-runtime settings from NVS storage
-  feat: Gain Lock, Baseline Normalization

### Release 4

Link: https://github.com/francescopace/espectre/releases/tag/2.3.0
- Tag: `2.3.0`
- Nome: v2.3.0 - End of Year Edition 🎉
- Publicada em: 2025-12-31
- Release anterior (cronológica): `2.2.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 27

-  chore: trigger GitHub Pages deploy
-  feat: optimize partition table for better memory allocation
-  docs: add ESP32-C3 Super Mini support and update dashboards
-  feat: add support for ESP32 original (WROOM-32D)
-  feat: multi-window validation for optimal subcarrier selection
-  feat: ESPectre the game
-  fix: Improve traffic generator resilience during SPIFFS operations
-  feat: calibration fallback with normalization when NBVI fails
-  feat: detect WiFi channel changes and reset detection buffer
-  docs: improve game page SEO and navigation
-  feat: add external traffic mode support (traffic_generator_rate: 0)
-  fix: update test callback signature to match new csi_processed_callback_t
-  docs: document sensor entity customization options
-  fix: disable SerialStreamer when logger uses hardware UART
-  fix: align NBVI parameters between C++ and Python
-  feat: add ping mode for traffic generator
-  feat: add standalone CSI traffic generator script with HA integration
-  feat: add configurable gain lock mode with auto-skip for strong signals
-  fix: correct Home Assistant command_line switch configuration
-  ci: add Dependabot config and website analytics
-  ci: add workflow and requirements.txt to path triggers
-  deps(ci): bump codecov/codecov-action from 4 to 5 (#54)
-  deps(ci): bump actions/checkout from 4 to 6 (#55)
-  deps(ci): bump actions/setup-python from 5 to 6
-  docs: add community test results
-  fix: correct stream command hint to use ./me collect (micro-espectre)
-  docs: reorganize v2.3.0 changelog

### Release 5

Link: https://github.com/francescopace/espectre/releases/tag/2.7.0
- Tag: `2.7.0`
- Nome: v2.7.0 - ESPectre configuration over BLE and subcarrier normalization
- Publicada em: 2026-03-17
- Release anterior (cronológica): `2.6.0`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 5

-  fix(micro-espectre): update firmware release to rc7 and refresh hashes
-  fix: normalize short and double HT CSI payloads across stacks
-  chore: refresh paired datasets and retrain ml artifacts with seed search
-  feat: replace serial game channel with reusable BLE API
-  fix: align nbvi validation with runtime filters and test datasets
