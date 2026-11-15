"""Métricas de uma instalação: tempo, CPU, memória, disco e nº de arquivos.

- `run_measured`: roda um comando, mede o tempo de relógio (`perf_counter`) e acompanha a
  árvore de processos com o psutil numa thread de amostragem (pico de RSS somado e CPU).
- `tree_usage`: tamanho de uma pasta sem seguir links, contando cada arquivo **uma vez por
  inode** (`(st_dev, st_ino)`), por causa dos hard links do pnpm e do Yarn.
- `rmtree_robust`: remoção de pastas que aguenta Windows (arquivo somente leitura, caminho
  longo, antivírus segurando o arquivo por alguns instantes).

Limitações (documentadas em `docs/runner.md`): o psutil só vê processos vivos no instante da
amostra, então filhos que vivem menos que o intervalo de amostragem entram no pico de RSS e na
CPU só se forem pegos. No POSIX a CPU é complementada por `getrusage(RUSAGE_CHILDREN)`; no
Windows ela é só a amostrada (subestima um pouco).

Issues: #99 (T04).
"""

from __future__ import annotations

import contextlib
import os
import shutil
import stat
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import psutil

MB = 1024 * 1024
SAMPLE_INTERVAL_S = 0.05
TIMEOUT_EXIT_CODE = 124   # mesma convenção do `timeout` do coreutils

IS_WINDOWS = os.name == "nt"


def _long(path: Path | str) -> str:
    """Caminho estendido no Windows (`\\\\?\\`), para passar do limite de 260 caracteres."""
    p = os.path.abspath(path)
    if IS_WINDOWS and not p.startswith("\\\\?\\"):
        return "\\\\?\\" + p
    return p


# ---------------------------------------------------------------- disco


@dataclass(frozen=True)
class TreeUsage:
    bytes: int
    n_files: int
    inodes: frozenset[tuple[int, int]]

    @property
    def mb(self) -> float:
        return self.bytes / MB


def _is_link(entry: os.DirEntry) -> bool:
    if entry.is_symlink():
        return True
    is_junction = getattr(entry, "is_junction", None)   # Python 3.12+
    return bool(is_junction and is_junction())


def tree_usage(paths, exclude_inodes=frozenset()) -> TreeUsage:
    """Soma o tamanho dos arquivos em `paths` (pastas ou arquivos), sem seguir links.

    Cada arquivo conta uma vez por `(st_dev, st_ino)`, mesmo que apareça várias vezes por hard
    link, e arquivos cujo inode está em `exclude_inodes` não contam. Links simbólicos e
    junctions não são seguidos nem contados. Caminhos inexistentes são ignorados.
    """
    if isinstance(paths, (str, Path)):
        paths = [paths]
    seen: set[tuple[int, int]] = set()
    total = 0
    n_files = 0

    def add(path: str, st: os.stat_result) -> None:
        nonlocal total, n_files
        key = (st.st_dev, st.st_ino)
        if key in seen or key in exclude_inodes:
            return
        seen.add(key)
        total += st.st_size
        n_files += 1

    def file_stat(entry: os.DirEntry) -> os.stat_result:
        # No Windows, DirEntry.stat() devolve st_ino = 0: é preciso o lstat de verdade.
        st = entry.stat(follow_symlinks=False)
        if IS_WINDOWS or st.st_ino == 0:
            st = os.lstat(entry.path)
        return st

    stack: list[str] = []
    for p in paths:
        p = _long(p)
        if os.path.islink(p) or not os.path.lexists(p):
            continue
        if os.path.isdir(p):
            stack.append(p)
        else:
            add(p, os.lstat(p))
    while stack:
        current = stack.pop()
        try:
            it = os.scandir(current)
        except (FileNotFoundError, NotADirectoryError, PermissionError):
            continue
        with it:
            for entry in it:
                try:
                    if _is_link(entry):
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        stack.append(entry.path)
                    elif entry.is_file(follow_symlinks=False):
                        add(entry.path, file_stat(entry))
                except FileNotFoundError:
                    continue
    return TreeUsage(total, n_files, frozenset(seen))


# ---------------------------------------------------------------- remoção


def _make_writable_and_retry(func, path, _exc) -> None:
    with contextlib.suppress(OSError):
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
    func(path)


def rmtree_robust(path: Path | str, retries: int = 5, delay_s: float = 0.2) -> None:
    """Apaga uma pasta (ou arquivo) sem seguir links, tolerando os problemas do Windows."""
    target = _long(path)
    if not os.path.lexists(target):
        return
    if os.path.islink(target):
        os.unlink(target)
        return
    if os.path.isfile(target):
        os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
        os.unlink(target)
        return
    for attempt in range(retries):
        try:
            shutil.rmtree(target, onexc=_make_writable_and_retry)
            return
        except FileNotFoundError:
            return
        except PermissionError:
            if attempt == retries - 1:
                raise
            time.sleep(delay_s * (attempt + 1))   # antivírus/indexador segurando o arquivo


# ---------------------------------------------------------------- processos


class ProcessMonitor:
    """Amostra a árvore de processos de `pid`: pico de RSS somado e CPU acumulada."""

    def __init__(self, pid: int, interval_s: float = SAMPLE_INTERVAL_S):
        self.pid = pid
        self.interval_s = interval_s
        self.peak_rss = 0
        self._cpu: dict[tuple[int, float], float] = {}
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    @property
    def cpu_s(self) -> float:
        return sum(self._cpu.values())

    def sample(self) -> None:
        try:
            root = psutil.Process(self.pid)
            procs = [root, *root.children(recursive=True)]
        except psutil.Error:
            return
        rss = 0
        for proc in procs:
            try:
                with proc.oneshot():
                    rss += proc.memory_info().rss
                    t = proc.cpu_times()
                    self._cpu[(proc.pid, proc.create_time())] = t.user + t.system
            except psutil.Error:
                continue
        self.peak_rss = max(self.peak_rss, rss)

    def _loop(self) -> None:
        while not self._stop.is_set():
            self.sample()
            self._stop.wait(self.interval_s)

    def start(self) -> ProcessMonitor:
        self._thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        self._thread.join()


@dataclass(frozen=True)
class Measurement:
    wall_s: float
    cpu_s: float
    peak_rss_mb: float
    exit_code: int
    timed_out: bool


def _children_cpu() -> float:
    if IS_WINDOWS:
        return 0.0
    import resource

    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def kill_tree(pid: int) -> None:
    try:
        root = psutil.Process(pid)
        procs = [*root.children(recursive=True), root]
    except psutil.Error:
        return
    for proc in procs:
        with contextlib.suppress(psutil.Error):
            proc.kill()
    psutil.wait_procs(procs, timeout=10)


def run_measured(cmd: list[str], cwd: Path, env: dict[str, str], timeout_s: float | None = None,
                 log_path: Path | None = None,
                 interval_s: float = SAMPLE_INTERVAL_S) -> Measurement:
    """Roda `cmd` (sem shell) e mede tempo, CPU e pico de memória da árvore de processos.

    A saída vai para `log_path` (ou é descartada), nunca para um pipe: um pipe cheio travaria
    a instalação. Se passar de `timeout_s`, a árvore inteira é morta e o código de saída é
    `TIMEOUT_EXIT_CODE`.
    """
    log = open(log_path, "ab") if log_path else subprocess.DEVNULL   # noqa: SIM115
    try:
        cpu_before = _children_cpu()
        start = time.perf_counter()
        proc = subprocess.Popen(cmd, cwd=str(cwd), env=env, stdout=log, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL)
        monitor = ProcessMonitor(proc.pid, interval_s).start()
        timed_out = False
        try:
            exit_code = proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc.pid)
            proc.wait()
            exit_code = TIMEOUT_EXIT_CODE
        wall = time.perf_counter() - start
        monitor.stop()
        cpu = max(monitor.cpu_s, _children_cpu() - cpu_before)
    finally:
        if log_path:
            log.close()
    return Measurement(wall_s=wall, cpu_s=cpu, peak_rss_mb=monitor.peak_rss / MB,
                       exit_code=exit_code, timed_out=timed_out)
