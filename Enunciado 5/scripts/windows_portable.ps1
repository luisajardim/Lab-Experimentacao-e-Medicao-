<#
.SYNOPSIS
    Ambiente portátil do Lab05 no Windows: Node, npm, pnpm, Yarn, Bun e uv numa pasta só,
    sem instalar nada no sistema (nada em Program Files, %APPDATA% ou no registro).

.DESCRIPTION
    Baixa as versões fixadas (com conferência de SHA-256) para <Root>\tools, aponta todos os
    caches para <Root>\caches, define as variáveis só no processo atual e, opcionalmente,
    copia o Enunciado 5 para <Root>\repo. A coleta usa <Root>\work como LAB05_WORKDIR.
    Para desfazer tudo: -Clean (apaga <Root> inteiro).

    Issues: #102 (T07, protocolo de coleta), #100 (T05, piloto).

.PARAMETER Root
    Pasta raiz do ambiente (caminho curto, num disco NTFS comum), ex.: F:\lab05.
.PARAMETER Repo
    Pasta do Enunciado 5 a copiar para <Root>\repo (ex.: o caminho \\wsl.localhost\... do WSL).
    Não apaga o que já existe em <Root>\repo (os dados coletados ficam).
.PARAMETER Run
    Comando a executar dentro do ambiente preparado (na pasta do repo) antes de sair.
.PARAMETER Clean
    Derruba o Verdaccio e os processos que rodam de <Root> e apaga <Root>.

.EXAMPLE
    # Abre uma sessão pronta para coletar (as variáveis valem só nessa janela):
    powershell -NoExit -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root F:\lab05 -Repo .
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root F:\lab05 -Run "uv run pytest -q"
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root F:\lab05 -Clean
#>
param(
    [Parameter(Mandatory = $true)][string]$Root,
    [string]$Repo = "",
    [string]$Run = "",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"   # o Invoke-WebRequest fica muito lento com a barra
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Versões fixadas (o que um dev instala hoje). O npm é o que vem com o Node LTS.
# O Yarn Berry não entra aqui: vem do release versionado em projects/*/lockfiles/yarn-berry-*/.
$Versions = [ordered]@{
    Node        = "24.22.3"
    Uv          = "0.13.8"
    Bun         = "1.4.4"
    Pnpm        = "12.21.0"
    YarnClassic = "1.22.22"
}

$Root = [IO.Path]::GetFullPath($Root)
$Marker = Join-Path $Root ".lab05-portable"
$Tools = Join-Path $Root "tools"
$Caches = Join-Path $Root "caches"
$Work = Join-Path $Root "work"
$RepoDst = Join-Path $Root "repo"
$Downloads = Join-Path $Root "downloads"

function Write-Step([string]$Message) { Write-Host "[lab05] $Message" -ForegroundColor Cyan }

function Assert-SafeRoot {
    $driveRoot = [IO.Path]::GetPathRoot($Root)
    if ($Root.TrimEnd("\") -eq $driveRoot.TrimEnd("\")) {
        throw "Root não pode ser a raiz de um disco: $Root"
    }
}

function Stop-RootProcesses {
    Get-Process -ErrorAction SilentlyContinue |
        Where-Object { $_.Path -and $_.Path.StartsWith($Root, [StringComparison]::OrdinalIgnoreCase) } |
        ForEach-Object {
            Write-Step "Encerrando $($_.ProcessName) (pid $($_.Id))"
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
}

if ($Clean) {
    Assert-SafeRoot
    if (-not (Test-Path $Root)) { Write-Step "Nada a apagar: $Root não existe."; exit 0 }
    if (-not (Test-Path $Marker)) {
        throw "$Root não foi criado por este script (falta $Marker); por segurança, não apago."
    }
    Stop-RootProcesses
    Set-Location ([IO.Path]::GetPathRoot($Root))   # não dá para apagar a pasta em que se está
    Write-Step "Apagando $Root ..."
    # rd com o prefixo \\?\ aguenta caminhos longos de node_modules.
    cmd /c "rd /s /q `"\\?\$Root`""
    if (Test-Path $Root) { throw "Não consegui apagar tudo em $Root (algum arquivo em uso?)." }
    Write-Step "Pronto: ambiente removido."
    exit 0
}

Assert-SafeRoot
foreach ($dir in @($Root, $Tools, $Caches, $Work, $Downloads)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}
# Sai de qualquer pasta UNC (ex.: \\wsl.localhost\...): o cmd.exe dos atalhos .cmd não aceita.
Set-Location $Root
if (-not (Test-Path $Marker)) {
    Set-Content -Path $Marker -Value "Ambiente portátil do Lab05 (scripts/windows_portable.ps1). Apague com -Clean."
}

function Get-Download([string]$Url, [string]$Name) {
    $dest = Join-Path $Downloads $Name
    if (-not (Test-Path $dest)) {
        Write-Step "Baixando $Url"
        Invoke-WebRequest -Uri $Url -OutFile "$dest.part" -UseBasicParsing
        Move-Item -Force "$dest.part" $dest
    }
    return $dest
}

function Assert-Sha256([string]$File, [string]$SumsText, [string]$Name) {
    $line = ($SumsText -split "`n") | Where-Object { $_ -match "^\s*([0-9a-fA-F]{64})\s+\*?$([regex]::Escape($Name))\s*$" } |
        Select-Object -First 1
    if (-not $line) { throw "SHA-256 de $Name não encontrado na lista oficial." }
    $expected = ($line.Trim() -split "\s+")[0].ToLower()
    $actual = (Get-FileHash -Algorithm SHA256 -Path $File).Hash.ToLower()
    if ($expected -ne $actual) {
        Remove-Item -Force $File
        throw "SHA-256 não confere para $Name (esperado $expected, obtido $actual)."
    }
}

function Get-Text([string]$Url) {
    $content = (Invoke-WebRequest -Uri $Url -UseBasicParsing).Content
    # O GitHub serve os .sha256 como binário: no PowerShell 5.1 isso chega como byte[].
    if ($content -is [byte[]]) { $content = [Text.Encoding]::UTF8.GetString($content) }
    return [string]$content
}

function Expand-To([string]$Zip, [string]$Dest) {
    $tmp = Join-Path $Downloads ("x-" + [IO.Path]::GetFileNameWithoutExtension($Zip))
    if (Test-Path $tmp) { Remove-Item -Recurse -Force $tmp }
    Expand-Archive -Path $Zip -DestinationPath $tmp -Force
    return $tmp
}

# ---- Node.js (traz o npm) ------------------------------------------------------------
$nodeDir = Join-Path $Tools "node"
if (-not (Test-Path (Join-Path $nodeDir "node.exe"))) {
    $name = "node-v$($Versions.Node)-win-x64.zip"
    $base = "https://nodejs.org/dist/v$($Versions.Node)"
    $zip = Get-Download "$base/$name" $name
    Assert-Sha256 $zip (Get-Text "$base/SHASUMS256.txt") $name
    $tmp = Expand-To $zip $nodeDir
    Move-Item (Join-Path $tmp "node-v$($Versions.Node)-win-x64") $nodeDir
    Remove-Item -Recurse -Force $tmp
}

# ---- uv (instala o Python 3.12 dentro de caches\) ------------------------------------
$uvDir = Join-Path $Tools "uv"
if (-not (Test-Path (Join-Path $uvDir "uv.exe"))) {
    $name = "uv-x86_64-pc-windows-msvc.zip"
    $url = "https://github.com/astral-sh/uv/releases/download/$($Versions.Uv)/$name"
    $zip = Get-Download $url $name
    Assert-Sha256 $zip (Get-Text "$url.sha256") $name
    $tmp = Expand-To $zip $uvDir
    New-Item -ItemType Directory -Force -Path $uvDir | Out-Null
    Get-ChildItem -Path $tmp -Recurse -Filter "*.exe" | Move-Item -Destination $uvDir -Force
    Remove-Item -Recurse -Force $tmp
}

# ---- Bun ----------------------------------------------------------------------------
$bunDir = Join-Path $Tools "bun"
if (-not (Test-Path (Join-Path $bunDir "bun.exe"))) {
    $name = "bun-windows-x64.zip"
    $base = "https://github.com/oven-sh/bun/releases/download/bun-v$($Versions.Bun)"
    $zip = Get-Download "$base/$name" $name
    Assert-Sha256 $zip (Get-Text "$base/SHASUMS256.txt") $name
    $tmp = Expand-To $zip $bunDir
    New-Item -ItemType Directory -Force -Path $bunDir | Out-Null
    Get-ChildItem -Path $tmp -Recurse -Filter "bun.exe" | Move-Item -Destination $bunDir -Force
    Remove-Item -Recurse -Force $tmp
}

# ---- Variáveis só deste processo: tudo dentro de $Root ------------------------------
$npmGlobal = Join-Path $Tools "npm-global"
$env:Path = (@($nodeDir, $npmGlobal, $uvDir, $bunDir) -join ";") + ";" + $env:Path
$env:npm_config_prefix = $npmGlobal                       # npm -g instala aqui
$env:npm_config_cache = Join-Path $Caches "npm"
$env:npm_config_update_notifier = "false"
$env:npm_config_fund = "false"
$env:UV_CACHE_DIR = Join-Path $Caches "uv"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $Caches "python"
$env:UV_TOOL_DIR = Join-Path $Caches "uv-tools"
$env:UV_PYTHON_PREFERENCE = "only-managed"                 # ignora Pythons do sistema
$env:BUN_INSTALL = $bunDir
$env:BUN_INSTALL_CACHE_DIR = Join-Path $Caches "bun"       # o runner sobrescreve por instalação
$env:YARN_CACHE_FOLDER = Join-Path $Caches "yarn"          # idem
$env:LAB05_WORKDIR = $Work

# ---- pnpm e Yarn Classic via npm global (dentro de tools\npm-global) -----------------
$needPnpm = -not (Test-Path (Join-Path $npmGlobal "pnpm.cmd"))
$needYarn = -not (Test-Path (Join-Path $npmGlobal "yarn.cmd"))
if ($needPnpm -or $needYarn) {
    Write-Step "Instalando pnpm $($Versions.Pnpm) e Yarn $($Versions.YarnClassic) em $npmGlobal"
    & npm.cmd install --global --no-audit "pnpm@$($Versions.Pnpm)" "yarn@$($Versions.YarnClassic)"
    if ($LASTEXITCODE -ne 0) { throw "npm install -g falhou ($LASTEXITCODE)." }
}

# ---- Cópia do Enunciado 5 (sem apagar dados já coletados em repo\) --------------------
if ($Repo) {
    $src = [IO.Path]::GetFullPath($Repo)
    Write-Step "Copiando $src -> $RepoDst"
    robocopy $src $RepoDst /E /XD .venv .work node_modules __pycache__ .pytest_cache .ruff_cache storage `
        /XF verdaccio.log verdaccio.pid /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy falhou ($LASTEXITCODE)." }
    $global:LASTEXITCODE = 0
}

# ---- Resumo ------------------------------------------------------------------------
function Get-Ver([string]$Exe, [string]$Arg = "--version") {
    $ErrorActionPreference = "Continue"
    try { return ((& $Exe $Arg 2>$null) | Select-Object -First 1).ToString().Trim() } catch { return "?" }
}
Write-Step "Ambiente pronto em $Root (variáveis valem só nesta janela)"
Write-Host ("  node {0} | npm {1} | pnpm {2} | yarn {3} | bun {4} | {5}" -f `
    (Get-Ver node), (Get-Ver npm.cmd), (Get-Ver pnpm.cmd), (Get-Ver yarn.cmd), (Get-Ver bun), (Get-Ver uv))
Write-Host "  LAB05_WORKDIR = $Work"

if (Test-Path (Join-Path $RepoDst "pyproject.toml")) {
    Set-Location $RepoDst
    Write-Host "  repo: $RepoDst"
    Write-Host "  próximos passos: uv sync -> uv run lab05 registry up -> uv run lab05 registry warm ->"
    Write-Host "                   uv run lab05 collect --machine <nome> --dry-run -> collect -> registry down"
}

if ($Run) {
    Write-Step "Executando: $Run"
    Invoke-Expression $Run
    exit $LASTEXITCODE
}
