"""Gerenciador de pacotes falso para testar o runner sem rede (T04, #99).

Uso: `python fake_pm.py [--fail] <args do gerenciador>`.

- `--version`: imprime 9.9.9.
- `run build`: sai com 0 se existe `node_modules` (ou `.pnp.cjs`), senão 1.
- qualquer outro comando é uma "instalação": dorme um pouco, enche o cache (`LAB05_CACHE_DIR`)
  se estiver vazio, recria `node_modules` com hard links para os arquivos do cache + 1 arquivo
  próprio, e escreve um lockfile se não houver. Com `--fail`, sai com 3 sem instalar.

Se `FAKE_LOG` estiver definido, cada chamada grava uma linha JSON com o estado encontrado
(fase, cache cheio?, `node_modules` existe?, lockfile existe?).
"""

import json
import os
import shutil
import sys
import time
from pathlib import Path

N_FILES = int(os.environ.get("FAKE_FILES", "8"))
FILE_SIZE = int(os.environ.get("FAKE_FILE_SIZE", str(64 * 1024)))
LOCKFILES = ("package-lock.json", "pnpm-lock.yaml", "bun.lock", "yarn.lock")


def log_state(args: list[str], cache: Path) -> None:
    path = os.environ.get("FAKE_LOG")
    if not path:
        return
    state = {
        "args": args,
        "phase": os.environ.get("LAB05_PHASE", ""),
        "cache_had_files": cache.is_dir() and any(cache.iterdir()),
        "node_modules": Path("node_modules").exists(),
        "lockfile": any(Path(n).exists() for n in LOCKFILES),
    }
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(state) + "\n")


def main() -> int:
    args = sys.argv[1:]
    fail = "--fail" in args
    args = [a for a in args if a != "--fail"]
    cache = Path(os.environ.get("LAB05_CACHE_DIR", ".fake-cache"))
    if args[:1] == ["--version"]:
        print("9.9.9")
        return 0
    log_state(args, cache)
    if args[:2] == ["run", "build"]:
        return 0 if Path("node_modules").exists() or Path(".pnp.cjs").exists() else 1
    time.sleep(0.05)
    if fail:
        print("falha simulada", file=sys.stderr)
        return 3
    cache.mkdir(parents=True, exist_ok=True)
    if not any(cache.iterdir()):
        for i in range(N_FILES):
            (cache / f"pkg{i}.tgz").write_bytes(b"x" * FILE_SIZE)
    shutil.rmtree("node_modules", ignore_errors=True)
    nm = Path("node_modules")
    nm.mkdir()
    for f in sorted(cache.iterdir()):
        os.link(f, nm / f.name)
    (nm / "own.txt").write_bytes(b"y" * FILE_SIZE)
    if not any(Path(n).exists() for n in LOCKFILES):
        Path("package-lock.json").write_text('{"fake": true}\n', encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
