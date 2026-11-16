"""Specs da máquina (bloco) e checagem do checklist de coleta.

Grava `data/raw/<maquina>/specs.json` com o que caracteriza um bloco do experimento: CPU,
núcleos, RAM, disco da pasta de trabalho, versão do Windows, do Node e dos 6 gerenciadores.
Sem isso, uma diferença entre máquinas não tem como ser explicada na análise.

Também confere, da forma que dá para automatizar, os itens do checklist de `docs/protocolo.md`
(tomada, perfil de energia, Defender, espaço em disco, versões esperadas) e **avisa** sobre o
que estiver fora. Ele não corrige nada e não falha a coleta: quem decide é quem está coletando.

Tudo o que depende do sistema é "melhor esforço": se um comando não existir, demorar ou falhar,
o campo vira `null` e a coleta continua. Nenhuma informação pessoal é lida.

Uso: `uv run lab05 specs --machine <nome>` (ou `uv run python -m specs --machine <nome>`).
Protocolo: `docs/protocolo.md`.

Issues: #102 (T07).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import psutil

import config
from config import (
    DATA_RAW,
    MANAGERS,
    NODE_EXPECTED_VERSION,
    PROJECTS,
    PROJECTS_DIR,
    SPECS_FILENAME,
)

SCHEMA_VERSION = 1
GB = 1024 ** 3
CMD_TIMEOUT_S = 60.0

IS_WINDOWS = os.name == "nt"

# Espaço livre mínimo recomendado na pasta de trabalho. A coleta refaz o cache a cada
# instalação, e o pior caso (next-app) passa de 350 MB só de `node_modules` + cache; a folga
# cobre os logs, o storage do Verdaccio e o arquivo temporário do antivírus.
MIN_FREE_GB = 20.0


# ---------------------------------------------------------------- utilidades


def _run(cmd: list[str], timeout: float = CMD_TIMEOUT_S) -> str | None:
    """Roda um comando e devolve a saída limpa, ou `None` se não der (melhor esforço)."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                              stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    out = (proc.stdout or "").strip()
    return out or None


def _powershell(script: str, timeout: float = CMD_TIMEOUT_S) -> str | None:
    """Roda um trecho de PowerShell (só no Windows). `None` fora do Windows ou em erro."""
    if not IS_WINDOWS:
        return None
    exe = shutil.which("powershell") or shutil.which("pwsh")
    if exe is None:
        return None
    return _run([exe, "-NoProfile", "-NonInteractive", "-Command", script], timeout)


_VERSION_RE = re.compile(r"\d+(?:\.\d+)*(?:[-+][0-9A-Za-z.]+)?")


def _parse_version(out: str | None) -> str | None:
    """Primeiro número de versão da saída de um `--version`.

    Alguns programas respondem só `1.22.22`, outros uma linha inteira
    (`uv 0.13.8 (3d97a6aad 2026-11-12 x86_64-pc-windows-msvc)`).
    """
    if not out:
        return None
    match = _VERSION_RE.search(out.splitlines()[-1].strip().lstrip("v"))
    return match.group(0) if match else None


def _version_of(program: str, args: tuple[str, ...] = ("--version",)) -> str | None:
    """Versão de um executável do PATH."""
    path = shutil.which(program)
    if path is None:
        return None
    return _parse_version(_run([path, *args]))


# ---------------------------------------------------------------- blocos do specs.json


def os_info() -> dict:
    """Sistema operacional. No Windows, acrescenta a edição e o build exato."""
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "arch": platform.machine(),
    }
    if IS_WINDOWS:
        out = _powershell(
            "$i = Get-CimInstance Win32_OperatingSystem; "
            "[Console]::Out.Write(\"$($i.Caption)|$($i.Version)|$($i.BuildNumber)\")"
        )
        if out and out.count("|") == 2:
            caption, version, build = out.split("|")
            info["edition"] = caption.strip() or None
            info["build"] = build.strip() or None
            info["version"] = version.strip() or info["version"]
    return info


def cpu_info() -> dict:
    """Modelo, núcleos físicos e lógicos e frequência máxima."""
    freq = None
    try:
        measured = psutil.cpu_freq()
        freq = round(measured.max or measured.current, 0) if measured else None
    except (OSError, NotImplementedError, AttributeError):
        freq = None
    model = platform.processor() or None
    if IS_WINDOWS:
        out = _powershell(
            "[Console]::Out.Write((Get-CimInstance Win32_Processor | "
            "Select-Object -First 1 -ExpandProperty Name))"
        )
        model = (out or model or "").strip() or None
    return {
        "model": model,
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "max_freq_mhz": freq,
    }


def ram_info() -> dict:
    mem = psutil.virtual_memory()
    return {"total_gb": round(mem.total / GB, 2), "available_gb": round(mem.available / GB, 2)}


def disk_info(workdir: Path) -> dict:
    """Disco da pasta de trabalho da coleta: é ele que importa, não o disco do sistema.

    Mede o volume que **contém** a pasta (ela pode ainda não existir). No Windows, tenta
    descobrir se o volume é SSD ou HDD, porque isso muda completamente o tempo de instalação.
    """
    workdir = Path(workdir)
    probe = workdir
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    info: dict = {"workdir": str(workdir), "volume": str(probe)}
    try:
        usage = psutil.disk_usage(str(probe))
        info["total_gb"] = round(usage.total / GB, 2)
        info["free_gb"] = round(usage.free / GB, 2)
    except OSError:
        info["total_gb"] = info["free_gb"] = None
    info["fstype"] = next(
        (p.fstype for p in psutil.disk_partitions(all=False)
         if str(probe).upper().startswith(p.mountpoint.upper())), None) or None
    info["media_type"] = None
    if IS_WINDOWS:
        out = _powershell(
            "[Console]::Out.Write(((Get-PhysicalDisk | "
            "Select-Object -ExpandProperty MediaType) -join ','))"
        )
        info["media_type"] = (out or "").strip() or None
    return info


def _berry_release(manager: str) -> Path | None:
    """Release versionado do Yarn Berry do tratamento (T03): `.../\\.yarn/releases/*.cjs`."""
    for project in PROJECTS:
        releases = PROJECTS_DIR / project / "lockfiles" / manager / ".yarn" / "releases"
        if releases.is_dir():
            found = sorted(releases.glob("yarn-*.cjs"))
            if found:
                return found[0]
    return None


def tool_versions() -> dict:
    """Versões do Node e dos 6 tratamentos, como estão nesta máquina agora.

    O Yarn Classic e o Berry compartilham o binário `yarn`: a versão do Berry é lida do release
    versionado no projeto (é ele que o `yarnPath` ativa durante a coleta), não do PATH.
    """
    versions: dict[str, str | None] = {
        "node": _version_of("node"),
        "python": platform.python_version(),
        "uv": _version_of("uv"),
    }
    for manager in MANAGERS:
        if manager.startswith("yarn-berry"):
            release = _berry_release(manager)
            node = shutil.which("node")
            found = None
            if release is not None and node is not None:
                found = _parse_version(_run([node, str(release), "--version"]))
                found = found or _parse_version(release.stem)
            versions[manager] = found
        elif manager == "yarn-classic":
            versions[manager] = _version_of("yarn")
        else:
            versions[manager] = _version_of(manager)
    return versions


def checklist() -> dict:
    """O que dá para conferir sozinho do checklist de `docs/protocolo.md`.

    Cada item é `True`, `False` ou `None` (não deu para saber). O que não dá para automatizar
    — apps fechados, Windows Update pausado, temperatura inicial — fica para quem coleta,
    e entra no `specs.json` pela opção `--note`.
    """
    items: dict[str, bool | str | None] = {
        "on_ac_power": None,
        "battery_percent": None,
        "power_plan": None,
        "defender_realtime_enabled": None,
    }
    try:
        battery = psutil.sensors_battery()
    except (OSError, NotImplementedError, AttributeError):
        battery = None
    if battery is not None:
        items["on_ac_power"] = bool(battery.power_plugged)
        items["battery_percent"] = round(battery.percent, 1)
    else:
        items["on_ac_power"] = True   # desktop sem bateria: sempre na tomada

    plan = _powershell(
        "$m = (powercfg /getactivescheme) -join ' '; "
        "if ($m -match '\\((.+)\\)') { [Console]::Out.Write($Matches[1]) }"
    )
    items["power_plan"] = (plan or "").strip() or None

    defender = _powershell(
        "try { [Console]::Out.Write((Get-MpComputerStatus -ErrorAction Stop)"
        ".RealTimeProtectionEnabled) } catch { }"
    )
    if defender:
        items["defender_realtime_enabled"] = defender.strip().lower() == "true"
    return items


# ---------------------------------------------------------------- coleta e avisos


def collect(machine: str, workdir: Path | None = None, note: str = "") -> dict:
    """Monta o dicionário que vai para `specs.json`."""
    workdir = Path(workdir) if workdir else config.workdir()
    return {
        "schema_version": SCHEMA_VERSION,
        "machine": machine,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "os": os_info(),
        "cpu": cpu_info(),
        "ram": ram_info(),
        "disk": disk_info(workdir),
        "tools": tool_versions(),
        "checklist": checklist(),
        "note": note,
    }


def _matches(found: str | None, expected: str) -> bool:
    return bool(found) and (found == expected or found.startswith(expected + "."))


def warnings(specs: dict) -> list[str]:
    """Avisos sobre o que está fora do protocolo. Lista vazia = tudo certo."""
    out: list[str] = []
    tools = specs.get("tools", {})

    node = tools.get("node")
    if not _matches(node, NODE_EXPECTED_VERSION):
        out.append(f"Node: esperado {NODE_EXPECTED_VERSION}.x, encontrado {node or 'nada'}")
    for manager, meta in MANAGERS.items():
        found = tools.get(manager)
        if not _matches(found, meta["expected_version"]):
            out.append(f"{manager}: esperado {meta['expected_version']}.x, "
                       f"encontrado {found or 'nada'}")

    disk = specs.get("disk", {})
    free = disk.get("free_gb")
    if free is not None and free < MIN_FREE_GB:
        out.append(f"disco: {free:.1f} GB livres em {disk.get('volume')}, "
                   f"abaixo dos {MIN_FREE_GB:.0f} GB recomendados")

    check = specs.get("checklist", {})
    if check.get("on_ac_power") is False:
        out.append("energia: a máquina está na bateria; ligue na tomada antes de coletar")
    plan = check.get("power_plan")
    if plan and "alto desempenho" not in plan.lower() and "high performance" not in plan.lower():
        out.append(f"perfil de energia: '{plan}' (o protocolo pede Alto desempenho)")
    if check.get("defender_realtime_enabled") is False:
        out.append("Defender: proteção em tempo real desligada; o protocolo a mantém LIGADA "
                   "(no padrão) em todas as máquinas")
    return out


def default_out(machine: str) -> Path:
    return DATA_RAW / machine / SPECS_FILENAME


def write(specs: dict, out: Path | None = None) -> Path:
    """Grava o `specs.json` (sobrescreve) e devolve o caminho."""
    path = out or default_out(specs["machine"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(specs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def summary(specs: dict) -> str:
    """Resumo de uma olhada, para conferir na hora da coleta."""
    cpu, ram, disk, tools = specs["cpu"], specs["ram"], specs["disk"], specs["tools"]
    lines = [
        f"  máquina   {specs['machine']}",
        f"  SO        {specs['os'].get('edition') or specs['os']['system']} "
        f"{specs['os'].get('build') or specs['os']['release']}",
        f"  CPU       {cpu['model']} ({cpu['physical_cores']} núcleos físicos, "
        f"{cpu['logical_cores']} lógicos)",
        f"  RAM       {ram['total_gb']} GB",
        f"  disco     {disk.get('free_gb')} GB livres de {disk.get('total_gb')} GB "
        f"em {disk.get('volume')} ({disk.get('fstype') or '?'}"
        f"{', ' + disk['media_type'] if disk.get('media_type') else ''})",
        f"  trabalho  {disk.get('workdir')}",
        "  versões   " + ", ".join(f"{k} {v or '?'}" for k, v in tools.items()),
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- CLI


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="lab05 specs", description=__doc__.splitlines()[0])
    p.add_argument("--machine", required=True,
                   help="nome do bloco (o mesmo usado em `collect --machine`)")
    p.add_argument("--out", type=Path, default=None,
                   help="arquivo de saída (padrão: data/raw/<maquina>/specs.json)")
    p.add_argument("--note", default="",
                   help="observação manual (temperatura inicial, apps abertos, o que mudou)")
    p.add_argument("--print", dest="print_only", action="store_true",
                   help="só mostra o JSON, sem gravar")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    specs = collect(args.machine, note=args.note)
    if args.print_only:
        print(json.dumps(specs, indent=2, ensure_ascii=False))
    else:
        path = write(specs, args.out)
        print(f"[lab05] specs de {args.machine} gravadas em {path}")
    print(summary(specs))
    problems = warnings(specs)
    if problems:
        print("[lab05] fora do protocolo (docs/protocolo.md):")
        for item in problems:
            print(f"  - {item}")
    else:
        print("[lab05] checklist automático: tudo conforme o protocolo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
