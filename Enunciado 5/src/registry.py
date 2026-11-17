"""Registry npm local (Verdaccio) que faz cache dos pacotes para a coleta.

Isola o efeito do gerenciador da velocidade da internet de cada máquina e evita martelar o
registry público: cada pacote é baixado de lá uma única vez e depois servido do storage local.

- `registry_env(manager, registry)`: variáveis de ambiente que apontam um gerenciador para o
  registry escolhido, sem tocar na configuração global do usuário (contrato com a T04, #99).
- `up()` / `down()` / `health()`: sobe, derruba e checa o Verdaccio em segundo plano.
- `warm(project_dirs)`: pré-aquece o cache com as dependências dos projetos-carga (T03, #98).

Uso: `uv run lab05 registry {up,down,status,warm}` (ou `uv run python -m registry ...`).
Documentação: `docs/registry.md`.

Issues: #97 (T02).
"""

from __future__ import annotations

import argparse
import contextlib
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import psutil
import requests

from config import MANAGERS, PROJECTS, PROJECTS_DIR, REGISTRIES, ROOT

REGISTRY_DIR = ROOT / "registry"
CONFIG_PATH = REGISTRY_DIR / "config.yaml"
STORAGE_DIR = REGISTRY_DIR / "storage"
PID_PATH = REGISTRY_DIR / "verdaccio.pid"
LOG_PATH = REGISTRY_DIR / "verdaccio.log"

PORT = 4873
LOCAL_URL = f"http://localhost:{PORT}/"
PUBLIC_URL = "https://registry.npmjs.org/"
VERDACCIO_VERSION = "7.1.0"

HEALTH_TIMEOUT_S = 2.0
STARTUP_TIMEOUT_S = 120.0


def registry_url(registry: str = "local") -> str:
    """URL do registry (`local` = Verdaccio, `public` = registry.npmjs.org)."""
    if registry not in REGISTRIES:
        raise ValueError(f"registry inválido: {registry!r} (use {REGISTRIES})")
    return LOCAL_URL if registry == "local" else PUBLIC_URL


def registry_env(manager: str, registry: str = "local") -> dict[str, str]:
    """Variáveis de ambiente que fazem `manager` usar o registry escolhido.

    Só variáveis de ambiente: nada é escrito em `.npmrc`/`.yarnrc` globais do usuário.
    O chamador mescla o resultado em `os.environ` ao rodar o comando de instalação.
    """
    if manager not in MANAGERS:
        raise ValueError(f"gerenciador inválido: {manager!r} (use {tuple(MANAGERS)})")
    url = registry_url(registry)
    # O npm lê npm_config_*; o pnpm 11+ IGNORA npm_config_* e só lê pnpm_config_* (o piloto de
    # 17/11 caiu nisso: o pnpm foi ao registry público); o Bun lê BUN_CONFIG_REGISTRY (e respeita
    # npm_config_registry); o Yarn Classic lê YARN_REGISTRY e npm_config_registry.
    env = {"npm_config_registry": url}
    if manager == "pnpm":
        env["pnpm_config_registry"] = url
    elif manager == "bun":
        env["BUN_CONFIG_REGISTRY"] = url
    elif manager == "yarn-classic":
        env["YARN_REGISTRY"] = url
    elif manager in ("yarn-berry-nm", "yarn-berry-pnp"):
        # Yarn Berry ignora npm_config_*: usa YARN_NPM_REGISTRY_SERVER e recusa http sem whitelist.
        env["YARN_NPM_REGISTRY_SERVER"] = url.rstrip("/")
        if registry == "local":
            env["YARN_UNSAFE_HTTP_WHITELIST"] = "localhost"
    return env


def health(timeout: float = HEALTH_TIMEOUT_S) -> bool:
    """True se o Verdaccio responde em `/-/ping`."""
    try:
        return requests.get(f"{LOCAL_URL}-/ping", timeout=timeout).ok
    except requests.RequestException:
        return False


def _read_pid() -> int | None:
    try:
        return int(PID_PATH.read_text().strip())
    except (FileNotFoundError, ValueError):
        return None


def _npx() -> str:
    exe = shutil.which("npx.cmd" if os.name == "nt" else "npx") or shutil.which("npx")
    if not exe:
        raise RuntimeError("npx não encontrado: instale o Node.js (ver docs/protocolo.md)")
    return exe


def _detach_kwargs() -> dict:
    if os.name == "nt":
        flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        return {"creationflags": flags}
    return {"start_new_session": True}


def up(timeout: float = STARTUP_TIMEOUT_S) -> int | None:
    """Sobe o Verdaccio em segundo plano (idempotente) e espera ficar saudável.

    Devolve o pid do processo iniciado, ou o pid registrado se já estava de pé.
    """
    if health():
        print(f"[lab05] Verdaccio já está de pé em {LOCAL_URL}")
        return _read_pid()
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [_npx(), "--yes", f"verdaccio@{VERDACCIO_VERSION}", "--config", str(CONFIG_PATH),
           "--listen", str(PORT)]
    with open(LOG_PATH, "ab") as log:
        proc = subprocess.Popen(cmd, cwd=REGISTRY_DIR, stdout=log, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, **_detach_kwargs())
    PID_PATH.write_text(str(proc.pid))
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if health():
            print(f"[lab05] Verdaccio {VERDACCIO_VERSION} de pé em {LOCAL_URL} (pid {proc.pid})")
            return proc.pid
        if proc.poll() is not None:
            break
        time.sleep(1)
    down()
    raise RuntimeError(f"Verdaccio não subiu em {timeout:.0f} s; veja {LOG_PATH}")


def down() -> bool:
    """Encerra a árvore de processos do Verdaccio (idempotente). True se havia algo a encerrar."""
    pid = _read_pid()
    PID_PATH.unlink(missing_ok=True)
    if pid is None:
        return False
    try:
        root = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return False
    procs = [*root.children(recursive=True), root]
    for p in procs:
        with contextlib.suppress(psutil.NoSuchProcess):
            p.terminate()
    _, alive = psutil.wait_procs(procs, timeout=10)
    for p in alive:
        with contextlib.suppress(psutil.NoSuchProcess):
            p.kill()
    print("[lab05] Verdaccio encerrado")
    return True


def default_project_dirs() -> list[Path]:
    """Pastas dos projetos-carga que já existem (com package.json)."""
    return [PROJECTS_DIR / p for p in PROJECTS if (PROJECTS_DIR / p / "package.json").exists()]


def _npm() -> str:
    exe = shutil.which("npm.cmd" if os.name == "nt" else "npm") or shutil.which("npm")
    if not exe:
        raise RuntimeError("npm não encontrado: instale o Node.js")
    return exe


def warm(project_dirs: list[Path] | None = None) -> list[Path]:
    """Instala uma vez, via Verdaccio, as dependências de cada projeto (pré-aquece o storage).

    Usa uma cópia temporária do projeto (só package.json e lockfile do npm) e um cache npm
    temporário, para que todo download passe pelo Verdaccio. Devolve os projetos aquecidos.
    """
    dirs = default_project_dirs() if project_dirs is None else list(project_dirs)
    dirs = [d for d in dirs if (Path(d) / "package.json").exists()]
    if not dirs:
        print("[lab05] Nenhum projeto-carga encontrado em projects/ (T03, #98): nada a aquecer.")
        return []
    if not health():
        raise RuntimeError("Verdaccio fora do ar: rode `uv run lab05 registry up` antes.")
    env = {**os.environ, **registry_env("npm", "local")}
    warmed = []
    for project in map(Path, dirs):
        with tempfile.TemporaryDirectory(prefix="lab05-warm-") as tmp:
            work, cache = Path(tmp) / "proj", Path(tmp) / "cache"
            work.mkdir()
            shutil.copy2(project / "package.json", work / "package.json")
            # Lockfile do npm: no layout da T03 fica em lockfiles/npm/ (ver projects/README.md);
            # sem ele o npm resolveria versões diferentes das usadas na coleta.
            for lock in (project / "lockfiles" / "npm" / "package-lock.json",
                         project / "package-lock.json"):
                if lock.exists():
                    shutil.copy2(lock, work / "package-lock.json")
                    break
            print(f"[lab05] Aquecendo o cache com {project.name}...")
            subprocess.run(
                [_npm(), "install", "--ignore-scripts", "--no-audit", "--no-fund",
                 "--cache", str(cache)],
                cwd=work, env=env, check=True)
        warmed.append(project)
    return warmed


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="lab05 registry", description=__doc__.splitlines()[0])
    parser.add_argument("action", choices=["up", "down", "status", "warm"])
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)
    if args.action == "up":
        up()
    elif args.action == "down":
        if not down():
            print("[lab05] Verdaccio não estava rodando (pelo pid registrado)")
    elif args.action == "status":
        ok = health()
        print(f"[lab05] Verdaccio {'de pé' if ok else 'fora do ar'} em {LOCAL_URL}")
    else:
        warm()


if __name__ == "__main__":
    main()
