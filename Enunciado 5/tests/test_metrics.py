"""Testes das métricas de instalação (T04, #99)."""

import os
import stat
import sys

import pytest

import metrics


def _write(path, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"a" * size)
    return path


def test_tree_usage_counts_hard_links_once(tmp_path):
    a = _write(tmp_path / "d" / "a.bin", 1000)
    os.link(a, tmp_path / "d" / "a_link.bin")
    _write(tmp_path / "d" / "sub" / "b.bin", 500)
    usage = metrics.tree_usage(tmp_path / "d")
    assert usage.bytes == 1500
    assert usage.n_files == 2
    assert len(usage.inodes) == 2


@pytest.mark.skipif(sys.platform == "win32", reason="symlink exige privilégio no Windows")
def test_tree_usage_does_not_follow_symlinks(tmp_path):
    _write(tmp_path / "outside" / "big.bin", 10_000)
    _write(tmp_path / "d" / "small.bin", 10)
    os.symlink(tmp_path / "outside", tmp_path / "d" / "link_dir")
    os.symlink(tmp_path / "outside" / "big.bin", tmp_path / "d" / "link_file")
    usage = metrics.tree_usage(tmp_path / "d")
    assert (usage.bytes, usage.n_files) == (10, 1)


def test_tree_usage_excludes_inodes_and_handles_missing(tmp_path):
    shared = _write(tmp_path / "proj" / "x.bin", 300)
    os.link(shared, tmp_path / "cache_x.bin")
    _write(tmp_path / "cache" / "y.bin", 200)
    os.replace(tmp_path / "cache_x.bin", tmp_path / "cache" / "x.bin")
    proj = metrics.tree_usage([tmp_path / "proj", tmp_path / "nao_existe"])
    cache = metrics.tree_usage(tmp_path / "cache", exclude_inodes=proj.inodes)
    assert proj.bytes == 300
    assert cache.bytes == 200 and cache.n_files == 1
    assert metrics.tree_usage(tmp_path / "nao_existe").bytes == 0


def test_tree_usage_accepts_single_file(tmp_path):
    f = _write(tmp_path / "f.bin", 42)
    assert metrics.tree_usage(f).bytes == 42


def test_rmtree_robust_removes_read_only_files(tmp_path):
    f = _write(tmp_path / "d" / "ro" / "file.txt", 10)
    os.chmod(f, stat.S_IREAD)
    metrics.rmtree_robust(tmp_path / "d")
    assert not (tmp_path / "d").exists()
    metrics.rmtree_robust(tmp_path / "d")   # inexistente: não falha
    single = _write(tmp_path / "single.txt", 1)
    os.chmod(single, stat.S_IREAD)
    metrics.rmtree_robust(single)
    assert not single.exists()


def test_run_measured_reports_time_cpu_and_memory(tmp_path):
    code = (
        "import time\n"
        "buf = bytearray(60 * 1024 * 1024)\n"
        "t = time.perf_counter()\n"
        "while time.perf_counter() - t < 0.4: sum(range(1000))\n"
        "raise SystemExit(5)\n"
    )
    log = tmp_path / "out.log"
    m = metrics.run_measured([sys.executable, "-c", code], tmp_path, dict(os.environ),
                             timeout_s=30, log_path=log)
    assert m.exit_code == 5 and not m.timed_out
    assert m.wall_s >= 0.4
    assert m.cpu_s >= 0.2
    assert m.peak_rss_mb >= 40
    assert log.exists()


def test_run_measured_kills_on_timeout(tmp_path):
    m = metrics.run_measured([sys.executable, "-c", "import time; time.sleep(30)"], tmp_path,
                             dict(os.environ), timeout_s=0.5)
    assert m.timed_out and m.exit_code == metrics.TIMEOUT_EXIT_CODE
    assert m.wall_s < 10
