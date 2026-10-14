# LibreHardwareMonitor/LibreHardwareMonitor

Repositório: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor

## Metadados

- Linguagem: C#

## Releases sorteadas

### Release 1

Link: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/tag/v0.8.6
- Tag: `v0.8.6`
- Nome: (sem nome)
- Publicada em: 2020-11-20
- Release anterior (cronológica): `v0.8.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 12

-  Update Nct677X.cs (#314)
-  Convert ContextMenu -> ContextMenuStrip, MenuItem -> ToolStripItem, MainMenu -> MenuStrip. (#317)
-  Bugfix: Application crash when network interface is changed (#318)
-  Add missing clamp around pump speed index (#320)
-  Fix error check. (#324)
-  Fixes: Fan speed reporting and control for IT8655E sensors. (#327)
-  Add support for AMD Ryzen 5000 processors (#328)
-  SubHardware in the sample code (#332)
-  Framework version in Readme (#331)
-  Add Processor Cache to SMBios (#333)
-  0.8.6
-  Update main.yml

### Release 2

Link: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/tag/v0.9.2
- Tag: `v0.9.2`
- Nome: v0.9.2
- Publicada em: 2023-03-22
- Release anterior (cronológica): `v0.9.1`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 76

-  0.9.1
-  Remove .NET 5.0 condition
-  Unify package references (#816)
-  Fix Gigabyte Z690 AORUS PRO sensor names. Add EC_Temp sensors. Add voltages. (#817)
-  Update README.md
-  Add Noise Sensors support (#814)
-  Add NZXT GRID+ V3 support (#812)
-  Check if ADL_Adapter_ID_Get exists (#827)
-  Update README.md
-  Cancel Context Menu if was panning (#829)
-  Drop .NET Standard (#839)
-  Bump System.Management from 5.0.0 to 6.0.0 (#840)
-  Update README.md
-  Fix some code analysis issues (#841)
-  Use file-scoped namespaces (#842)
-  Fixing-ITE-IT8628E to show up to 6 fans instead of 4 (#850)
-  Add support for HX1500i (#865)
-  Do not modify enumerated tree when plot is shown. (#853)
-  Revert "Drop .NET Standard (#839)"
-  Thread affinity
-  Bump System.IO.Ports from 6.0.0 to 7.0.0 in /LibreHardwareMonitor
-  Bump System.Management from 6.0.0 to 7.0.0 in /LibreHardwareMonitor
-  Update SMBios.cs (#877)
-  Merge pull request #873 from LibreHardwareMonitor/dependabot/nuget/LibreHardwareMonitor/System.IO.Ports-7.0.0
-  Merge pull request #875 from LibreHardwareMonitor/dependabot/nuget/LibreHardwareMonitor/System.Management-7.0.0
-  Add preliminary support for Nuvoton NCT6799D (#846)
-  Windows storage spaces (#871)
-  Add update interval (#882)
-  Added support for Asus Z790 Max Hero (#894)
-  Added preliminary support for Nuvoton NCT6686D chip #2 (#897)
-  Ring0 and InpOut cleanup (#898)
-  Use Central Package Management for NuGet 6.2+ (#879)
-  Revert "Use Central Package Management for NuGet 6.2+ (#879)"
-  Add view menu item to clear the plot (#900)
-  Bump Newtonsoft.Json from 13.0.1 to 13.0.2 in /LibreHardwareMonitor (#908)
-  Fixes #907
-  Fixes #911
-  Add support for .NET 7 (#878)
-  add nvidia gpu memory used as percentage (#912)
-  Revert "Revert "Use Central Package Management for NuGet 6.2+ (#879)"" (#902)
- ... e mais 36 commits

### Release 3

Link: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/tag/v0.9.4
- Tag: `v0.9.4`
- Nome: v0.9.4
- Publicada em: 2024-11-24
- Release anterior (cronológica): `v0.9.3`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 104

-  Add limited support for “ASUS ROG STRIX X670E-E GAMING WIFI” (#1235)
-  add TtempWaterIn and TempWaterOut for rog maximus z790 formula (#1238)
-  Intel Gen 14 Meteor Lake (#1253)
-  Add Support for ASUS Proart X670E Creator WiFi (#1259)
-  Added Gigabyte Z690 AORUS MASTER (#1258)
-  Added GIGABYTE B560I AORUS PRO AX (#1274)
-  Bump action versions (#1279)
-  Add Humidity Sensors support (#1281)
-  Bugfix: Crash when access to nvml api is unavailable (#1252)
-  fix heap corruption caused by incorrect pointer size in calls to Ftd2xx.dll (#1302)
-  add B650M_AORUS_PRO_AX (#1301)
-  Add ADL pmlog support, fix metrics on newer gpus (#1308)
-  Fix memory size calculation with extended size (#1315)
-  Add 16th voltage input for NCT67xxD chips (#1318)
-  Refactor ADL sensors update (#1317)
-  Bump TaskScheduler from 2.10.1 to 2.11.0 in /LibreHardwareMonitor
-  Avoid multiple initializations of AmdGpu (#1324)
-  Merge pull request #1327 from LibreHardwareMonitor/dependabot/nuget/LibreHardwareMonitor/TaskScheduler-2.11.0
-  Add memory info for Amd GPUs (#1326)
-  Add shared memory free/total for Intel iGPU (#1328)
-  Fix ADL PMLog sensor, ignore invalid values (#1329)
-  Fix AMD Overdrive, update ADL methods to ADL2 variants (#1332)
-  Add basic T-Sensor support (#1347)
-  Add MSR_PLATFORM_ENERGY_COUNTER 0x64D (#1357)
-  Add Support for Asrock H61M-DGS (#1354)
-  Fix missing view for IT8792E and allow fan control for IT8792E on some Gigabyte AMD boards (#1313)
-  ASUS B150M-C_D3, B150M-C (#1225)
-  Update SuperIOHardware.cs
-  Add support for ASUS TUF Gaming X570-Plus (Wi-Fi) (#1362)
-  Add Gigabyte 970A-DS3P (and FX rev 2.1 model) support (#1363)
-  Add support for ASRock Z690 Extreme/Steel Legend (and their WiFi 6e variants) (#1343)
-  Add proper definition support for all Gigabyte B450 models (#1367)
-  Use more descriptive names for VTT, CPU SA/VCCSA, VBat (#1364)
-  GpuIntelIntegrated initial power value should be read from MSR_PP1_ENERGY_STATUS, not from MSR_RAPL_POWER_UNIT (#1366)
-  Add EC support for Z490 ROG MAXIMUS XII HERO (WI-FI) (#1351)
-  Update EmbeddedController.cs
-  LPC/EC: fix signess of the sensor readings (#1382)
-  Update EC registers for Z790 (#1381)
-  Nct677x esio mutex (#1254)
-  Add proper definition support for all Gigabyte B550 models (#1360)
- ... e mais 64 commits

### Release 4

Link: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/tag/v0.9.5
- Tag: `v0.9.5`
- Nome: v0.9.5
- Publicada em: 2026-01-07
- Release anterior (cronológica): `v0.9.4`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 242

-  Added support for ASUS ProArt B760-CREATOR D4 (Nuvoton NCT6798D)
-  Update pull requests.yml
-  Update master.yml
-  Merge tag 'v0.9.4'
-  Gigabyte X670 Aorus Elite AX support
-  Gigabyte X670 Aorus Elite AX support
-  Bump System.Management from 9.0.0 to 9.0.1 in /LibreHardwareMonitor
-  Bump System.IO.Ports from 9.0.0 to 9.0.1 in /LibreHardwareMonitor
-  Merge pull request #1599 from LibreHardwareMonitor/dependabot/nuget/LibreHardwareMonitor/System.Management-9.0.1
-  Merge pull request #1600 from LibreHardwareMonitor/dependabot/nuget/LibreHardwareMonitor/System.IO.Ports-9.0.1
-  Add support for ASUS ROG Crosshair X870E Hero motherboard (#1581)
-  Sensor Statistic NaN Fix (#1549)
-  SAPPHIRERAPIDS support added (#1555)
-  Gigabyte X79 UD3 - Fan control support and missing fan added  (#1558)
-  Add support for ASUS PRIME X870-P (Nuvoton NCT6701D) (#1565)
-  IT87 voltage registers update (#1567)
-  Proart x870e creator wifi (#1547)
-  Add Support For ASUS ROG STRIX X870E-E GAMING WIFI Fan Sensors And Control (#1523)
-  Fix B650M_AORUS_PRO_AX AVCC3 voltage (#1606)
-  Tidy Asus ProArt X870E CREATOR WIFI misconfigurations (#1616)
-  added support for Intel ElkhartLake (#1625)
-  Ryzen 9000 Core Frequency Bugfix (#1548)
-  More precise system utilization (#1562)
-  Intel Ultra 9 200 Series ArrowLake Added (#1630)
-  NCT610XD bugfix register and temperature read (#1631)
-  Bump Microsoft.NETFramework.ReferenceAssemblies and TaskScheduler (#1651)
-  Add Support for Gigabyte X870E Aorus Xtreme AI Top Motherboard (#1647)
-  Bump System.IO.Ports and Microsoft.NETFramework.ReferenceAssemblies (#1641)
-  Bump System.IO.Ports and Microsoft.NETFramework.ReferenceAssemblies (#1639)
-  Bump Microsoft.NETFramework.ReferenceAssemblies and System.Management (#1640)
-  Merge remote-tracking branch 'upstream/master'
-  Bump System.IO.Ports and Microsoft.NETFramework.ReferenceAssemblies (#1667)
-  Bump System.Management and Microsoft.NETFramework.ReferenceAssemblies (#1665)
-  Added motherboard Gigabyte B650 Gaming X AX (#1673)
-  add support for kraken elite 2024 (#1662)
-  Bump System.IO.Ports and Microsoft.NETFramework.ReferenceAssemblies (#1691)
-  Bump System.Management and Microsoft.NETFramework.ReferenceAssemblies (#1692)
-  Update LibreHardwareMonitor.csproj
-  Add initial support for MSI X870 and Z890 Motherboards (NCT6687D) (#1621)
-  Removed forced update interval for storage devices (#1698) (#1699)
- ... e mais 202 commits

### Release 5

Link: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases/tag/v0.9.6
- Tag: `v0.9.6`
- Nome: v0.9.6
- Publicada em: 2026-02-14
- Release anterior (cronológica): `v0.9.5`

**Release notes**

_(vazio)_

**Commits desde a release anterior**

Total: 39

-  Update DiskInfoToolkit. (#2141)
-  Add missing controls (#2157)
-  Feature/arctic fan controller (#2152)
-  Bump System.IO.Ports from 10.0.1 to 10.0.2 (#2158)
-  Bump System.Management from 10.0.1 to 10.0.2 (#2160)
-  Bump System.Threading.AccessControl from 10.0.1 to 10.0.2 (#2161)
-  Bump System.Text.Json from 10.0.1 to 10.0.2 (#2163)
-  Bump System.Resources.Extensions from 10.0.1 to 10.0.2 (#2162)
-  Update System.Resources.Extensions to version 10.0.2
-  Update Identification.cs (#2164)
-  Added query parameters to the /metrics endpoint (#2151)
-  Bump Microsoft.Windows.CsWin32 from 0.3.264 to 0.3.269 (#2165)
-  Save expanded state also for: (#2173)
-  Update PawnIO modules to 2.2 (#2174)
-  Add core voltage for NVIDIA GPU. (#2175)
-  Add sensors for Astral GPUs (#2168)
-  Add support for Thermal Grizzly WireView Pro 2. (#2171)
-  Add fan 7 for MSI MEG Z790 GODLIKE MAX (#2185)
-  Add thermal sensor 1 back for NVMe (#2186)
-  Add Pump Fan 2 for MSI MEG Z790 GODLIKE MAX + handle 0 RPM / unplugged fan (#2187)
-  Fix ASUS Z170 EC temperature read returning zero values (#2153)
-  Add support for MSI PRO B850M-A Project Zero (#2190)
-  Add detection for MSI MAG B850 Tomahawk Wifi. (#2191)
-  TG WireView Pro 2: Changes for firmware update (#2193)
-  Add JAF Fan for Godlike Max & fix Pump Fan 2 (#2194)
-  Add support for MSI MAG B850 Tomahawk Wifi (non-max) using NCT6687DR Controller (#2199)
-  Add MSI controller for AIOs. (#2207)
-  Slight refactor for ARCTIC Fan Controller (#2205)
-  Bump System.Text.Json from 10.0.2 to 10.0.3 (#2214)
-  Bump System.Threading.AccessControl from 10.0.2 to 10.0.3 (#2212)
-  Bump System.IO.Ports from 10.0.2 to 10.0.3 (#2209)
-  Bump System.Resources.Extensions from 10.0.2 to 10.0.3 (#2213)
-  Upgrade package versions in csproj file
-  Fix for new PawnIO release. (#2222)
-  Foundational support for all MSI B840/B850, X870(E), and Z890 Motherboards (#2216)
-  Updates for TG WVP2 (#2215)
-  fix: skip integrated GPU in IGCL enumeration to prevent duplicate hardware entries (#2217)
-  Add IGCL telemetry sensors (temperature, clock, voltage) for Intel integrated GPUs (#2218)
-  Bump version from 0.9.5 to 0.9.6
