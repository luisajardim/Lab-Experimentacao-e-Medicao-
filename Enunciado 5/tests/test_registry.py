"""Testes do registry local (T02, #97). Sem rede: requests, subprocess e psutil são simulados."""

from pathlib import Path

import pytest
import requests

import registry
from config import MANAGERS


@pytest.mark.parametrize("manager", list(MANAGERS))
def test_registry_env_points_every_manager_to_local(manager):
    env = registry.registry_env(manager)
    assert env["npm_config_registry"] == registry.LOCAL_URL
    assert all(isinstance(v, str) for v in env.values())


def test_registry_env_specific_variables():
    assert registry.registry_env("bun")["BUN_CONFIG_REGISTRY"] == registry.LOCAL_URL
    assert registry.registry_env("yarn-classic")["YARN_REGISTRY"] == registry.LOCAL_URL
    for m in ("yarn-berry-nm", "yarn-berry-pnp"):
        env = registry.registry_env(m)
        assert env["YARN_NPM_REGISTRY_SERVER"] == registry.LOCAL_URL.rstrip("/")
        assert env["YARN_UNSAFE_HTTP_WHITELIST"] == "localhost"


def test_registry_env_public_has_no_http_whitelist():
    env = registry.registry_env("yarn-berry-pnp", "public")
    assert env["YARN_NPM_REGISTRY_SERVER"] == registry.PUBLIC_URL.rstrip("/")
    assert "YARN_UNSAFE_HTTP_WHITELIST" not in env
    assert registry.registry_env("npm", "public")["npm_config_registry"] == registry.PUBLIC_URL


@pytest.mark.parametrize("args", [("pip", "local"), ("npm", "mirror")])
def test_registry_env_rejects_invalid(args):
    with pytest.raises(ValueError):
        registry.registry_env(*args)


def test_health_true_false(monkeypatch):
    class Resp:
        ok = True

    monkeypatch.setattr(registry.requests, "get", lambda *a, **k: Resp())
    assert registry.health()

    def boom(*a, **k):
        raise requests.ConnectionError

    monkeypatch.setattr(registry.requests, "get", boom)
    assert not registry.health()


@pytest.fixture
def tmp_registry(monkeypatch, tmp_path):
    monkeypatch.setattr(registry, "REGISTRY_DIR", tmp_path)
    monkeypatch.setattr(registry, "STORAGE_DIR", tmp_path / "storage")
    monkeypatch.setattr(registry, "PID_PATH", tmp_path / "verdaccio.pid")
    monkeypatch.setattr(registry, "LOG_PATH", tmp_path / "verdaccio.log")
    return tmp_path


def test_up_is_idempotent_when_already_healthy(monkeypatch, tmp_registry):
    monkeypatch.setattr(registry, "health", lambda **k: True)
    monkeypatch.setattr(registry.subprocess, "Popen",
                        lambda *a, **k: pytest.fail("não deveria subir outro processo"))
    registry.PID_PATH.write_text("123")
    assert registry.up() == 123


def test_up_starts_process_and_writes_pid(monkeypatch, tmp_registry):
    calls = iter([False, True])
    monkeypatch.setattr(registry, "health", lambda **k: next(calls))
    monkeypatch.setattr(registry, "_npx", lambda: "npx")
    started = {}

    class Proc:
        pid = 4242

        def poll(self):
            return None

    def fake_popen(cmd, **kwargs):
        started["cmd"] = cmd
        return Proc()

    monkeypatch.setattr(registry.subprocess, "Popen", fake_popen)
    assert registry.up(timeout=5) == 4242
    assert registry.PID_PATH.read_text() == "4242"
    assert f"verdaccio@{registry.VERDACCIO_VERSION}" in started["cmd"]
    assert str(registry.PORT) in started["cmd"]


def test_down_without_pid_is_noop(tmp_registry):
    assert registry.down() is False


def test_down_with_stale_pid_removes_file(monkeypatch, tmp_registry):
    registry.PID_PATH.write_text("999999")

    def gone(pid):
        raise registry.psutil.NoSuchProcess(pid)

    monkeypatch.setattr(registry.psutil, "Process", gone)
    assert registry.down() is False
    assert not registry.PID_PATH.exists()


def test_warm_without_projects_is_noop(monkeypatch, tmp_path):
    monkeypatch.setattr(registry, "health", lambda **k: pytest.fail("não deveria checar"))
    assert registry.warm([tmp_path / "nao-existe"]) == []


def test_warm_installs_copy_through_local_registry(monkeypatch, tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    (project / "package.json").write_text('{"name": "x", "version": "1.0.0"}')
    monkeypatch.setattr(registry, "health", lambda **k: True)
    monkeypatch.setattr(registry, "_npm", lambda: "npm")
    seen = {}

    def fake_run(cmd, cwd, env, check):
        seen.update(cmd=cmd, cwd=cwd, registry=env["npm_config_registry"])

    monkeypatch.setattr(registry.subprocess, "run", fake_run)
    assert registry.warm([project]) == [project]
    assert seen["registry"] == registry.LOCAL_URL
    assert seen["cwd"] != project and "--cache" in seen["cmd"]
    assert not (project / "node_modules").exists()


def test_warm_uses_npm_lockfile_from_t03_layout(monkeypatch, tmp_path):
    project = tmp_path / "proj"
    (project / "lockfiles" / "npm").mkdir(parents=True)
    (project / "package.json").write_text('{"name": "x", "version": "1.0.0"}')
    (project / "lockfiles" / "npm" / "package-lock.json").write_text('{"lockfileVersion": 3}')
    monkeypatch.setattr(registry, "health", lambda **k: True)
    monkeypatch.setattr(registry, "_npm", lambda: "npm")
    copied = {}

    def fake_run(cmd, cwd, env, check):
        copied["lock"] = (Path(cwd) / "package-lock.json").read_text()

    monkeypatch.setattr(registry.subprocess, "run", fake_run)
    registry.warm([project])
    assert copied["lock"] == '{"lockfileVersion": 3}'


def test_warm_requires_registry_up(monkeypatch, tmp_path):
    (tmp_path / "package.json").write_text("{}")
    monkeypatch.setattr(registry, "health", lambda **k: False)
    with pytest.raises(RuntimeError, match="fora do ar"):
        registry.warm([tmp_path])


def test_main_status(monkeypatch, capsys):
    monkeypatch.setattr(registry, "health", lambda **k: False)
    registry.main(["status"])
    assert "fora do ar" in capsys.readouterr().out
