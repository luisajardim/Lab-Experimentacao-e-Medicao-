"""Runner de instalação: uma linha de `runs.csv` por instalação medida.

Para cada célula (projeto × cenário × gerenciador) de uma máquina (bloco), o runner:

1. monta um diretório de trabalho limpo com o projeto-carga e os arquivos do tratamento
   (`projects/<projeto>/lockfiles/<gerenciador>/`, ver `projects/README.md`);
2. prepara o cenário (`config.SCENARIOS`): cache vazio ou cheio, lockfile, `node_modules`;
3. roda a instalação medida (`metrics.run_measured`): tempo, CPU e pico de RAM;
4. mede o disco do projeto e do cache (hard links contados uma vez) e o nº de arquivos;
5. roda o `build` (instalação válida?) e grava a linha no CSV (append, com retomada).

A ordem das células é aleatorizada por repetição, com semente derivada da máquina. Falhas
não interrompem a coleta: ficam registradas em `exit_code` e `build_ok`.

Uso: `uv run lab05 collect --machine bernardo --pilot` (ou `uv run python -m runner ...`).
Detalhes e decisões em `docs/runner.md`.

Issues: #99 (T04).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import uuid
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

import config
import metrics
from config import (
    DATA_RAW,
    DEFAULT_REGISTRY,
    MANAGERS,
    NODE_EXPECTED_VERSION,
    PROJECTS,
    PROJECTS_DIR,
    REGISTRIES,
    RUNS_FILENAME,
    SCENARIOS,
    SEED,
)
from schema import COLUMN_NAMES, read_runs, validate

DEFAULT_REPS = 10            # coleta completa: o N definitivo sai da T09 (#104)
PILOT_REPS = 5
PILOT_SCENARIOS = ("cold", "warm-cache")
DEFAULT_WARMUP = 2
DEFAULT_TIMEOUT_S = 900.0
BUILD_TIMEOUT_S = 600.0

LOCKFILE_NAMES = frozenset({"package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml",
                            "bun.lock", "bun.lockb", "yarn.lock"})
# O que a instalação cria dentro do projeto (é o que entra em `disk_mb` e `n_files`).
INSTALL_ARTIFACTS = ("node_modules", ".pnp.cjs", ".pnp.loader.mjs", ".pnp.data.json",
                     ".yarn/unplugged", ".yarn/cache", ".yarn/install-state.gz",
                     ".yarn/__virtual__")
# Pastas do projeto-carga que nunca são copiadas para o diretório de trabalho.
COPY_IGNORE = ("lockfiles", "node_modules", ".pnp.*", "dist", ".next", ".turbo")

RESUME_KEY = ("machine", "project", "scenario", "manager", "rep", "registry", "warmup")


# ---------------------------------------------------------------- comandos por tratamento


@dataclass(frozen=True)
class ManagerSpec:
    """Como chamar um gerenciador. `program` é o nome do executável (resolvido com
    `shutil.which`, que acha `npm.cmd` etc. no Windows) ou uma lista já pronta (testes)."""

    program: str | tuple[str, ...]
    install_cold: tuple[str, ...]
    install_frozen: tuple[str, ...]
    install_reinstall: tuple[str, ...]
    build: tuple[str, ...] = ("run", "build")
    version: tuple[str, ...] = ("--version",)

    def argv(self) -> list[str]:
        if isinstance(self.program, tuple):
            return list(self.program)
        path = shutil.which(self.program)
        if path is None:
            raise FileNotFoundError(f"executável não encontrado no PATH: {self.program}")
        return [path]

    def install_args(self, scenario: str) -> list[str]:
        if scenario == "cold":
            return list(self.install_cold)
        if scenario == "reinstall":
            return list(self.install_reinstall)
        return list(self.install_frozen)


_NPM_FLAGS = ("--no-audit", "--no-fund")
_YARN_CLASSIC = ManagerSpec("yarn", ("install",), ("install", "--frozen-lockfile"),
                            ("install", "--frozen-lockfile"))
_YARN_BERRY = ManagerSpec("yarn", ("install",), ("install", "--immutable"),
                          ("install", "--immutable"))

COMMANDS: dict[str, ManagerSpec] = {
    "npm": ManagerSpec("npm", ("install", *_NPM_FLAGS), ("ci", *_NPM_FLAGS),
                       ("install", *_NPM_FLAGS)),
    "pnpm": ManagerSpec("pnpm", ("install",), ("install", "--frozen-lockfile"),
                        ("install", "--frozen-lockfile")),
    "bun": ManagerSpec("bun", ("install",), ("install", "--frozen-lockfile"),
                       ("install", "--frozen-lockfile")),
    "yarn-classic": _YARN_CLASSIC,
    "yarn-berry-nm": _YARN_BERRY,
    "yarn-berry-pnp": _YARN_BERRY,
}


def cache_env(manager: str, cache_dir: Path) -> dict[str, str]:
    """Variáveis que mandam o gerenciador usar um cache dedicado (sem tocar na config global).

    O cache fica no mesmo disco do diretório de trabalho: o pnpm e o Yarn só usam hard links
    quando o store/cache e o projeto estão no mesmo volume.
    """
    c = str(cache_dir)
    env = {"LAB05_CACHE_DIR": c}
    if manager == "npm":
        env["npm_config_cache"] = c
    elif manager == "pnpm":
        env["npm_config_store_dir"] = str(cache_dir / "store")
        env["npm_config_cache_dir"] = str(cache_dir / "cache")
        env["npm_config_state_dir"] = str(cache_dir / "state")
    elif manager == "bun":
        env["BUN_INSTALL_CACHE_DIR"] = c
    elif manager == "yarn-classic":
        env["YARN_CACHE_FOLDER"] = c
    elif manager in ("yarn-berry-nm", "yarn-berry-pnp"):
        env["YARN_ENABLE_GLOBAL_CACHE"] = "true"
        env["YARN_GLOBAL_FOLDER"] = c
        env["YARN_CACHE_FOLDER"] = str(cache_dir / "cache")
        env["YARN_ENABLE_TELEMETRY"] = "0"
    return env


def _registry_env(manager: str, registry: str) -> dict[str, str]:
    import registry as registry_mod  # T02 (#97); import tardio para os testes trocarem

    return registry_mod.registry_env(manager, registry)


def build_env(manager: str, registry: str, cache_dir: Path, phase: str) -> dict[str, str]:
    env = dict(os.environ)
    # Variáveis herdadas que mudariam o comportamento das ferramentas entre máquinas.
    for key in ("CI", "NODE_ENV", "npm_config_production", "YARN_ENABLE_IMMUTABLE_INSTALLS"):
        env.pop(key, None)
    env.update({
        "NO_UPDATE_NOTIFIER": "1",
        "npm_config_update_notifier": "false",
        "LAB05_PHASE": phase,   # prep | measure | build | version (aparece nos logs)
    })
    env.update(cache_env(manager, cache_dir))
    env.update(_registry_env(manager, registry))
    return env


# ---------------------------------------------------------------- sequência


def machine_seed(machine: str, seed: int = SEED) -> int:
    """Semente estável por máquina (sha256 do nome; `hash()` muda a cada processo)."""
    digest = hashlib.sha256(machine.encode("utf-8")).digest()
    return seed + int.from_bytes(digest[:4], "big")


def build_sequence(machine: str, projects: Iterable[str], scenarios: Iterable[str],
                   managers: Iterable[str], reps: int, warmup: int = DEFAULT_WARMUP,
                   seed: int = SEED) -> list[dict]:
    """Aquecimento (células sorteadas, `rep = 0`) + uma permutação das células por repetição."""
    cells = [(p, s, m) for p in projects for s in scenarios for m in managers]
    if not cells:
        return []
    rng = np.random.default_rng(machine_seed(machine, seed))
    seq = []
    picks = rng.choice(len(cells), size=min(warmup, len(cells)), replace=False) if warmup else []
    for i in picks:
        seq.append((cells[int(i)], 0, True))
    for rep in range(1, reps + 1):
        for i in rng.permutation(len(cells)):
            seq.append((cells[int(i)], rep, False))
    return [{"project": p, "scenario": s, "manager": m, "rep": rep, "warmup": w, "order": k}
            for k, ((p, s, m), rep, w) in enumerate(seq, start=1)]


# ---------------------------------------------------------------- uma instalação


@dataclass
class Collector:
    """Estado de uma coleta numa máquina. Os testes injetam `commands` e `projects_dir`."""

    machine: str
    registry: str = DEFAULT_REGISTRY
    projects_dir: Path = PROJECTS_DIR
    workdir: Path = field(default_factory=config.workdir)
    commands: dict[str, ManagerSpec] = field(default_factory=lambda: dict(COMMANDS))
    timeout_s: float = DEFAULT_TIMEOUT_S
    build_timeout_s: float = BUILD_TIMEOUT_S
    log: Callable[[str], None] = print
    _versions: dict[str, str] = field(default_factory=dict)
    _node_version: str | None = None

    # -- caminhos
    def project_dir(self, project: str, manager: str) -> Path:
        return self.workdir / "run" / f"{project}--{manager}"

    def cache_dir(self, manager: str) -> Path:
        return self.workdir / "cache" / manager

    def log_path(self, run_id: str) -> Path:
        path = self.workdir / "logs" / self.machine / f"{run_id}.log"
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    # -- montagem do diretório de trabalho
    def treatment_files(self, project: str, manager: str) -> Path:
        return self.projects_dir / project / "lockfiles" / manager

    def fresh_project(self, project: str, manager: str, with_lockfile: bool) -> Path:
        src = self.projects_dir / project
        if not (src / "package.json").exists():
            raise FileNotFoundError(f"projeto-carga sem package.json: {src}")
        dst = self.project_dir(project, manager)
        metrics.rmtree_robust(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*COPY_IGNORE))
        treatment = self.treatment_files(project, manager)
        if treatment.is_dir():
            for item in treatment.iterdir():
                if item.name in LOCKFILE_NAMES and not with_lockfile:
                    continue
                target = dst / item.name
                if item.is_dir():
                    shutil.copytree(item, target, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, target)
        return dst

    def remove_artifacts(self, project_dir: Path) -> None:
        for rel in INSTALL_ARTIFACTS:
            metrics.rmtree_robust(project_dir / rel)

    # -- comandos
    def _run_plain(self, cmd: list[str], cwd: Path, env: dict, timeout: float) -> tuple[int, str]:
        try:
            r = subprocess.run(cmd, cwd=str(cwd), env=env, capture_output=True, text=True,
                               timeout=timeout, stdin=subprocess.DEVNULL)
            return r.returncode, (r.stdout or r.stderr).strip()
        except subprocess.TimeoutExpired:
            return metrics.TIMEOUT_EXIT_CODE, ""

    def manager_version(self, manager: str, cwd: Path) -> str:
        if manager not in self._versions:
            spec = self.commands[manager]
            env = build_env(manager, self.registry, self.cache_dir(manager), "version")
            code, out = self._run_plain(spec.argv() + list(spec.version), cwd, env, 60)
            lines = out.splitlines()
            self._versions[manager] = lines[-1].strip().lstrip("v") if code == 0 and lines else ""
        return self._versions[manager]

    def node_version(self) -> str:
        if self._node_version is None:
            node = shutil.which("node")
            out = ""
            if node:
                try:
                    out = subprocess.run([node, "--version"], capture_output=True, text=True,
                                         timeout=30).stdout.strip()
                except (OSError, subprocess.TimeoutExpired):
                    out = ""
            self._node_version = out.lstrip("v")
        return self._node_version

    # -- a instalação medida
    def run_one(self, project: str, scenario: str, manager: str, rep: int, order: int,
                warmup: bool) -> dict:
        sc = SCENARIOS[scenario]
        spec = self.commands[manager]
        cache = self.cache_dir(manager)
        run_id = str(uuid.uuid4())
        log_path = self.log_path(run_id)

        # 1-2. Diretório limpo + cenário. Cache sempre reconstruído do zero, para conter só
        # os pacotes deste projeto (senão cache_mb mistura projetos).
        workdir = self.fresh_project(project, manager, with_lockfile=sc["lockfile"])
        metrics.rmtree_robust(cache)
        cache.mkdir(parents=True, exist_ok=True)
        if sc["cache"]:
            prep_env = build_env(manager, self.registry, cache, "prep")
            prep = metrics.run_measured(spec.argv() + spec.install_args("ci"), workdir, prep_env,
                                        self.timeout_s, log_path)
            if prep.exit_code != 0:
                self.log(f"  [aviso] instalação preparatória falhou ({prep.exit_code})")
            if not sc["node_modules"]:
                self.remove_artifacts(workdir)

        # 3. Instalação medida.
        env = build_env(manager, self.registry, cache, "measure")
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
        m = metrics.run_measured(spec.argv() + spec.install_args(scenario), workdir, env,
                                 self.timeout_s, log_path)

        # 4. Disco: artefatos do projeto; cache sem os inodes já contados no projeto.
        proj = metrics.tree_usage([workdir / rel for rel in INSTALL_ARTIFACTS])
        cache_usage = metrics.tree_usage(cache, exclude_inodes=proj.inodes)

        # 5. Build (instalação válida?).
        build_ok = False
        if m.exit_code == 0:
            build_env_ = build_env(manager, self.registry, cache, "build")
            b = metrics.run_measured(spec.argv() + list(spec.build), workdir, build_env_,
                                     self.build_timeout_s, log_path)
            build_ok = b.exit_code == 0

        return {
            "machine": self.machine,
            "run_id": run_id,
            "timestamp": timestamp,
            "project": project,
            "scenario": scenario,
            "manager": manager,
            "manager_version": self.manager_version(manager, workdir),
            "node_version": self.node_version(),
            "registry": self.registry,
            "rep": rep,
            "order": order,
            "warmup": warmup,
            "wall_s": round(m.wall_s, 4),
            "cpu_s": round(m.cpu_s, 4),
            "peak_rss_mb": round(m.peak_rss_mb, 2),
            "disk_mb": round(proj.mb, 4),
            "cache_mb": round(cache_usage.mb, 4),
            "n_files": proj.n_files,
            "build_ok": build_ok,
            "exit_code": m.exit_code,
        }


# ---------------------------------------------------------------- coleta


def default_out(machine: str) -> Path:
    return DATA_RAW / machine / RUNS_FILENAME


def done_keys(out: Path) -> set[tuple]:
    if not out.exists() or out.stat().st_size == 0:
        return set()
    df = read_runs(out)
    return {tuple(row) for row in df[list(RESUME_KEY)].itertuples(index=False, name=None)}


def append_row(row: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    df = validate(pd.DataFrame([row], columns=list(COLUMN_NAMES)))
    header = not out.exists() or out.stat().st_size == 0
    with open(out, "a", newline="", encoding="utf-8") as fh:
        df.to_csv(fh, header=header, index=False)
        fh.flush()
        os.fsync(fh.fileno())


def version_matches(found: str, expected: str) -> bool:
    """`found` é a versão `expected` ou uma versão dentro dela (ex.: 1.22.22 em 1.22)."""
    return found == expected or found.startswith(expected + ".")


def check_versions(col: Collector, project: str, managers: Iterable[str]) -> None:
    """Aborta se algum gerenciador (ou o Node) não estiver na versão esperada de `config`.

    Pega máquinas com versões erradas e, principalmente, o Yarn Classic que vira Berry sem
    aviso: o Yarn 1.22 obedece ao `yarnPath` de um `.yarnrc.yml` em QUALQUER pasta acima do
    projeto (ou na home), e aí as linhas sairiam rotuladas como yarn-classic sendo Berry.
    """
    wrong = []
    node = col.node_version()
    if not version_matches(node, NODE_EXPECTED_VERSION):
        wrong.append(f"node: esperado {NODE_EXPECTED_VERSION}.x, encontrado {node or '?'}")
    for manager in managers:
        workdir = col.fresh_project(project, manager, with_lockfile=False)
        found = col.manager_version(manager, workdir)
        expected = MANAGERS[manager]["expected_version"]
        if not version_matches(found, expected):
            wrong.append(f"{manager}: esperado {expected}.x, encontrado {found or '?'}")
        metrics.rmtree_robust(workdir)
    if wrong:
        raise SystemExit(
            "[lab05] versões fora do esperado (config.py): " + "; ".join(wrong) + ". "
            "Use o ambiente de scripts/windows_portable.ps1 e confira se não há um .yarnrc.yml "
            f"numa pasta acima de {col.workdir} ou na sua home.")


def collect(machine: str, *, projects: Iterable[str] = tuple(PROJECTS),
            scenarios: Iterable[str] = tuple(SCENARIOS), managers: Iterable[str] = tuple(MANAGERS),
            reps: int = DEFAULT_REPS, warmup: int = DEFAULT_WARMUP,
            registry: str = DEFAULT_REGISTRY, out: Path | None = None,
            timeout_s: float = DEFAULT_TIMEOUT_S, seed: int = SEED,
            collector: Collector | None = None, log: Callable[[str], None] = print,
            verify_versions: bool = True) -> int:
    """Roda (ou retoma) a coleta de uma máquina. Devolve quantas instalações foram feitas."""
    out = out or default_out(machine)
    managers = tuple(managers)
    col = collector or Collector(machine=machine, registry=registry, timeout_s=timeout_s, log=log)
    missing = []
    for m in managers:
        try:
            col.commands[m].argv()
        except FileNotFoundError:
            missing.append(m)
    if missing:
        raise SystemExit(f"[lab05] gerenciadores não encontrados no PATH: {', '.join(missing)}")
    projects = tuple(projects)
    if verify_versions:
        check_versions(col, projects[0], managers)

    seq = build_sequence(machine, projects, scenarios, managers, reps, warmup, seed)
    done = done_keys(out)
    todo = [c for c in seq if (machine, c["project"], c["scenario"], c["manager"], c["rep"],
                               col.registry, c["warmup"]) not in done]
    log(f"[lab05] {machine}: {len(seq)} instalações na sequência, {len(seq) - len(todo)} já "
        f"gravadas, {len(todo)} a fazer → {out}")
    for i, c in enumerate(todo, start=1):
        label = (f"[{i}/{len(todo)}] #{c['order']} {c['project']} · {c['scenario']} · "
                 f"{c['manager']} · rep {c['rep']}{' (aquecimento)' if c['warmup'] else ''}")
        try:
            row = col.run_one(c["project"], c["scenario"], c["manager"], c["rep"], c["order"],
                              c["warmup"])
        except FileNotFoundError as exc:
            raise SystemExit(f"[lab05] {exc}") from exc
        append_row(row, out)
        status = "ok" if row["exit_code"] == 0 and row["build_ok"] else (
            f"FALHOU (exit {row['exit_code']}, build_ok={row['build_ok']})")
        log(f"{label}: {row['wall_s']:.2f} s, {row['disk_mb']:.1f} MB, {status}")
    return len(todo)


# ---------------------------------------------------------------- CLI


def _csv_list(value: str, allowed: Iterable[str], name: str) -> tuple[str, ...]:
    items = tuple(v.strip() for v in value.split(",") if v.strip())
    bad = [v for v in items if v not in allowed]
    if bad:
        raise argparse.ArgumentTypeError(f"{name} inválido(s): {bad}; use {tuple(allowed)}")
    return items


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="lab05 collect", description=__doc__.splitlines()[0])
    p.add_argument("--machine", required=True, help="nome do bloco (ex.: bernardo, luisa, pedro)")
    p.add_argument("--pilot", action="store_true",
                   help=f"piloto: cenários {', '.join(PILOT_SCENARIOS)} e {PILOT_REPS} repetições")
    p.add_argument("--reps", type=int, default=None,
                   help=f"repetições por célula (padrão {DEFAULT_REPS}; piloto {PILOT_REPS})")
    p.add_argument("--warmup", type=int, default=DEFAULT_WARMUP, help="rodadas de aquecimento")
    p.add_argument("--projects", type=lambda v: _csv_list(v, PROJECTS, "projeto"),
                   default=tuple(PROJECTS))
    p.add_argument("--scenarios", type=lambda v: _csv_list(v, SCENARIOS, "cenário"), default=None)
    p.add_argument("--managers", type=lambda v: _csv_list(v, MANAGERS, "gerenciador"),
                   default=tuple(MANAGERS))
    p.add_argument("--registry", choices=REGISTRIES, default=DEFAULT_REGISTRY)
    p.add_argument("--out", type=Path, default=None, help="CSV de saída (padrão data/raw/<maquina>/)")
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_S,
                   help="timeout por instalação (s)")
    p.add_argument("--dry-run", action="store_true", help="só mostra a sequência")
    p.add_argument("--skip-version-check", action="store_true",
                   help="não confere as versões de config.py (só para depurar; nunca na coleta)")
    args = p.parse_args(argv)
    if args.scenarios is None:
        args.scenarios = PILOT_SCENARIOS if args.pilot else tuple(SCENARIOS)
    if args.reps is None:
        args.reps = PILOT_REPS if args.pilot else DEFAULT_REPS
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.dry_run:
        seq = build_sequence(args.machine, args.projects, args.scenarios, args.managers,
                             args.reps, args.warmup)
        for c in seq[:20]:
            print(f"#{c['order']:>4} rep {c['rep']:>2} {'W' if c['warmup'] else ' '} "
                  f"{c['project']:<12} {c['scenario']:<11} {c['manager']}")
        if len(seq) > 20:
            print(f"... ({len(seq) - 20} a mais)")
        print(f"[lab05] {len(seq)} instalações ({args.warmup} de aquecimento) "
              f"para {args.machine}, registry {args.registry}")
        return 0
    collect(args.machine, projects=args.projects, scenarios=args.scenarios,
            managers=args.managers, reps=args.reps, warmup=args.warmup, registry=args.registry,
            out=args.out, timeout_s=args.timeout, verify_versions=not args.skip_version_check)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
