"""Testes do coletor de specs (T07, #102).

Nada aqui depende da máquina em que roda: subprocess, psutil e platform são simulados, para
a suíte dar o mesmo resultado no Windows do grupo e em qualquer CI.
"""

import json

import pytest

import specs
from config import MANAGERS, NODE_EXPECTED_VERSION


@pytest.fixture
def fake_specs():
    """Um `specs.json` conforme o protocolo, para os testes de aviso partirem do caso bom."""
    tools = {"node": f"{NODE_EXPECTED_VERSION}.22.3", "python": "3.12.16", "uv": "0.13.8"}
    tools.update({m: meta["expected_version"] + ".0" for m, meta in MANAGERS.items()})
    return {
        "schema_version": specs.SCHEMA_VERSION,
        "machine": "teste",
        "timestamp": "2026-11-16T20:00:00-03:00",
        "os": {"system": "Windows", "release": "11", "version": "10.0.26200",
               "arch": "AMD64", "edition": "Microsoft Windows 11 Pro", "build": "26200"},
        "cpu": {"model": "CPU de teste", "physical_cores": 8, "logical_cores": 16,
                "max_freq_mhz": 3200.0},
        "ram": {"total_gb": 16.0, "available_gb": 8.0},
        "disk": {"workdir": "W:\\lab05\\work", "volume": "W:\\", "total_gb": 500.0,
                 "free_gb": 200.0, "fstype": "NTFS", "media_type": "SSD"},
        "tools": tools,
        "checklist": {"on_ac_power": True, "battery_percent": 100.0,
                      "power_plan": "Alto desempenho", "defender_realtime_enabled": True},
        "note": "",
    }


# ---------------------------------------------------------------- parsing de versão


@pytest.mark.parametrize(("saida", "esperado"), [
    ("1.22.22", "1.22.22"),
    ("v24.22.3", "24.22.3"),
    ("uv 0.13.8 (3d97a6aad 2026-11-12 x86_64-pc-windows-msvc)", "0.13.8"),
    ("aviso na primeira linha\n4.18.1", "4.18.1"),
    ("", None),
    (None, None),
    ("sem número nenhum", None),
])
def test_parse_version(saida, esperado):
    assert specs._parse_version(saida) == esperado


# ---------------------------------------------------------------- avisos do protocolo


def test_sem_avisos_quando_tudo_conforme(fake_specs):
    assert specs.warnings(fake_specs) == []


def test_avisa_versao_errada_de_gerenciador(fake_specs):
    fake_specs["tools"]["pnpm"] = "9.0.0"
    avisos = specs.warnings(fake_specs)
    assert any(a.startswith("pnpm:") for a in avisos)


def test_avisa_gerenciador_ausente(fake_specs):
    fake_specs["tools"]["bun"] = None
    assert any("bun:" in a and "nada" in a for a in specs.warnings(fake_specs))


def test_avisa_node_errado(fake_specs):
    fake_specs["tools"]["node"] = "22.17.0"
    assert any(a.startswith("Node:") for a in specs.warnings(fake_specs))


def test_avisa_pouco_espaco_em_disco(fake_specs):
    fake_specs["disk"]["free_gb"] = specs.MIN_FREE_GB - 1
    assert any("disco:" in a for a in specs.warnings(fake_specs))


def test_nao_avisa_disco_quando_desconhecido(fake_specs):
    fake_specs["disk"]["free_gb"] = None
    assert not any("disco:" in a for a in specs.warnings(fake_specs))


def test_avisa_bateria_e_perfil_de_energia(fake_specs):
    fake_specs["checklist"]["on_ac_power"] = False
    fake_specs["checklist"]["power_plan"] = "Economia de energia"
    avisos = specs.warnings(fake_specs)
    assert any("energia:" in a for a in avisos)
    assert any("perfil de energia:" in a for a in avisos)


def test_aceita_perfil_em_ingles(fake_specs):
    fake_specs["checklist"]["power_plan"] = "High performance"
    assert specs.warnings(fake_specs) == []


def test_avisa_defender_desligado(fake_specs):
    fake_specs["checklist"]["defender_realtime_enabled"] = False
    assert any("Defender" in a for a in specs.warnings(fake_specs))


def test_nao_avisa_checklist_desconhecido(fake_specs):
    """Item que não deu para ler (`None`) não vira aviso: não sabemos que está errado."""
    fake_specs["checklist"] = dict.fromkeys(fake_specs["checklist"])
    assert specs.warnings(fake_specs) == []


# ---------------------------------------------------------------- gravação e resumo


def test_write_grava_json_valido(fake_specs, tmp_path):
    destino = tmp_path / "bloco" / "specs.json"
    assert specs.write(fake_specs, destino) == destino
    assert json.loads(destino.read_text(encoding="utf-8")) == fake_specs


def test_default_out_usa_a_pasta_do_bloco():
    assert specs.default_out("luisa").parent.name == "luisa"
    assert specs.default_out("luisa").name == "specs.json"


def test_summary_cita_o_essencial(fake_specs):
    texto = specs.summary(fake_specs)
    for trecho in ("teste", "CPU de teste", "16.0", "W:\\lab05\\work", "NTFS"):
        assert trecho in texto


# ---------------------------------------------------------------- coleta (tudo simulado)


def test_collect_tem_todos_os_blocos(monkeypatch, tmp_path):
    monkeypatch.setattr(specs, "os_info", lambda: {"system": "Linux"})
    monkeypatch.setattr(specs, "cpu_info", lambda: {"model": "x"})
    monkeypatch.setattr(specs, "ram_info", lambda: {"total_gb": 1.0})
    monkeypatch.setattr(specs, "disk_info", lambda _w: {"workdir": str(tmp_path)})
    monkeypatch.setattr(specs, "tool_versions", lambda: {"node": "24.0.0"})
    monkeypatch.setattr(specs, "checklist", lambda: {"on_ac_power": True})

    out = specs.collect("teste", workdir=tmp_path, note="sala a 22 graus")

    assert set(out) == {"schema_version", "machine", "timestamp", "os", "cpu", "ram", "disk",
                        "tools", "checklist", "note"}
    assert out["machine"] == "teste" and out["note"] == "sala a 22 graus"
    assert out["schema_version"] == specs.SCHEMA_VERSION


def test_tool_versions_cobre_os_seis_tratamentos(monkeypatch):
    monkeypatch.setattr(specs, "_version_of", lambda *_a, **_k: "9.9.9")
    monkeypatch.setattr(specs, "_berry_release", lambda _m: None)
    versions = specs.tool_versions()
    assert set(MANAGERS) <= set(versions)
    assert versions["yarn-classic"] == "9.9.9"
    assert versions["yarn-berry-nm"] is None   # sem release versionado, não inventa


def test_comandos_que_falham_viram_none(monkeypatch):
    """Máquina sem as ferramentas não quebra a coleta de specs."""
    monkeypatch.setattr(specs.shutil, "which", lambda _p: None)
    assert specs._version_of("pnpm") is None


def test_main_grava_e_devolve_zero(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(specs, "collect", lambda machine, note="": {
        "machine": machine, "note": note, "cpu": {"model": "x", "physical_cores": 1,
                                                  "logical_cores": 2},
        "ram": {"total_gb": 8.0}, "disk": {"free_gb": 100.0, "total_gb": 200.0,
                                           "volume": "C:\\", "workdir": "C:\\w"},
        "os": {"system": "Windows", "release": "11"}, "tools": {"node": "24.0.0"},
        "checklist": {}, "schema_version": 1, "timestamp": "2026-11-16T20:00:00-03:00"})
    destino = tmp_path / "specs.json"
    assert specs.main(["--machine", "teste", "--out", str(destino)]) == 0
    assert destino.exists()
    assert "teste" in capsys.readouterr().out
