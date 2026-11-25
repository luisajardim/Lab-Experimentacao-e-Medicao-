"""Testes do coletor de downloads do npm (T15, #112).

Nada aqui vai à rede: `_get_json` é sempre substituído por um dublê. Os casos cobrem o que a
API faz de verdade e nos morderia em silêncio — ela **corta** janelas maiores que ~550 dias e
responde `{"error": ...}` com HTTP 200.
"""

from datetime import date, timedelta

import pytest

import npm_downloads as nd
from config import MANAGERS

# ---------------------------------------------------------------- blocos da janela


def test_blocos_cobrem_a_janela_sem_sobrepor():
    inicio, fim = date(2015, 1, 10), date(2026, 11, 23)
    pedacos = list(nd.blocks(inicio, fim))
    assert pedacos[0][0] == inicio and pedacos[-1][1] == fim
    for anterior, seguinte in zip(pedacos, pedacos[1:], strict=False):
        assert seguinte[0] == anterior[1] + timedelta(days=1)


def test_nenhum_bloco_passa_do_limite_da_api():
    """Acima de ~550 dias a API corta sem avisar: o bloco tem de ficar abaixo disso."""
    for inicio, fim in nd.blocks(date(2015, 1, 10), date(2026, 11, 23)):
        assert (fim - inicio).days + 1 <= nd.BLOCK_DAYS < 550


def test_janela_de_um_dia_vira_um_bloco():
    assert list(nd.blocks(date(2026, 1, 1), date(2026, 1, 1))) == [
        (date(2026, 1, 1), date(2026, 1, 1))
    ]


# ---------------------------------------------------------------- uma chamada à API


def _fake_api(monkeypatch, resposta):
    chamadas = []

    def fake(url, timeout=None):
        chamadas.append(url)
        return resposta(url) if callable(resposta) else resposta

    monkeypatch.setattr(nd, "_get_json", fake)
    monkeypatch.setattr(nd.time, "sleep", lambda _s: None)
    return chamadas


def test_fetch_block_le_os_dias(monkeypatch):
    _fake_api(monkeypatch, {"downloads": [{"day": "2026-01-01", "downloads": "7"},
                                          {"day": "2026-01-02", "downloads": 9}]})
    assert nd.fetch_block("pnpm", date(2026, 1, 1), date(2026, 1, 2)) == [
        {"day": "2026-01-01", "downloads": 7},
        {"day": "2026-01-02", "downloads": 9},
    ]


def test_fetch_block_codifica_pacote_com_escopo(monkeypatch):
    chamadas = _fake_api(monkeypatch, {"downloads": []})
    nd.fetch_block("@yarnpkg/cli", date(2026, 1, 1), date(2026, 1, 2))
    assert "%40yarnpkg%2Fcli" in chamadas[0]


def test_fetch_block_aceita_pacote_sem_dados(monkeypatch):
    """Pacote que ainda não existia na janela devolve lista vazia, não erro."""
    _fake_api(monkeypatch, {"error": "no stats for this package for this range (0008)"})
    assert nd.fetch_block("bun", date(2015, 1, 10), date(2016, 1, 1)) == []


def test_fetch_block_erro_de_verdade_sobe(monkeypatch):
    _fake_api(monkeypatch, {"error": "end date > start date"})
    with pytest.raises(RuntimeError, match="end date"):
        nd.fetch_block("npm", date(2010, 1, 1), date(2010, 1, 5))


def test_fetch_block_sem_campo_downloads_nao_quebra(monkeypatch):
    _fake_api(monkeypatch, {"start": "2026-01-01", "end": "2026-01-02"})
    assert nd.fetch_block("npm", date(2026, 1, 1), date(2026, 1, 2)) == []


def test_fetch_block_repete_em_erro_temporario(monkeypatch):
    import urllib.error

    tentativas = []

    def fake(url, timeout=None):
        tentativas.append(url)
        if len(tentativas) < 3:
            raise urllib.error.HTTPError(url, 503, "indisponível", {}, None)
        return {"downloads": [{"day": "2026-01-01", "downloads": 1}]}

    monkeypatch.setattr(nd, "_get_json", fake)
    monkeypatch.setattr(nd.time, "sleep", lambda _s: None)
    assert len(nd.fetch_block("npm", date(2026, 1, 1), date(2026, 1, 1))) == 1
    assert len(tentativas) == 3


def test_fetch_block_404_e_pacote_inexistente(monkeypatch):
    import urllib.error

    def fake(url, timeout=None):
        raise urllib.error.HTTPError(url, 404, "não encontrado", {}, None)

    monkeypatch.setattr(nd, "_get_json", fake)
    monkeypatch.setattr(nd.time, "sleep", lambda _s: None)
    assert nd.fetch_block("nao-existe", date(2026, 1, 1), date(2026, 1, 1)) == []


# ---------------------------------------------------------------- série e cache


def test_fetch_series_junta_os_blocos_em_ordem(monkeypatch):
    def resposta(url):
        inicio = url.rsplit("/", 2)[-2].split(":")[0]
        return {"downloads": [{"day": inicio, "downloads": 5}]}

    _fake_api(monkeypatch, resposta)
    rows = nd.fetch_series("pnpm", date(2015, 1, 10), date(2020, 1, 1), verbose=False)
    assert [r["day"] for r in rows] == sorted(r["day"] for r in rows)
    assert all(r["package"] == "pnpm" for r in rows)
    assert all(set(r) == set(nd.DAILY_COLUMNS) for r in rows)


def test_write_e_read_daily_dao_a_volta(tmp_path):
    rows = [nd.row("npm", "2026-01-01", 10)]
    destino = nd.write_csv(tmp_path / "d" / "downloads_daily.csv", nd.DAILY_COLUMNS, rows)
    assert nd.read_daily(destino) == rows


def test_read_daily_sem_arquivo_e_vazio(tmp_path):
    assert nd.read_daily(tmp_path / "nao-existe.csv") == []


def test_last_day_por_pacote():
    rows = [{"package": "npm", "day": "2026-01-02", "downloads": 1},
            {"package": "npm", "day": "2026-01-05", "downloads": 1},
            {"package": "pnpm", "day": "2026-01-09", "downloads": 1}]
    assert nd.last_day(rows, "npm") == date(2026, 1, 5)
    assert nd.last_day(rows, "bun") is None


def test_merge_a_coleta_nova_vence():
    cached = [nd.row("npm", "2026-01-01", 1)]
    fresh = [nd.row("npm", "2026-01-01", 42), nd.row("npm", "2026-01-02", 7)]
    assert nd.merge(cached, fresh) == fresh


def test_collect_so_busca_o_que_falta(monkeypatch, tmp_path):
    """O cache é a verdade: pacote em dia não gera requisição."""
    destino = tmp_path / "downloads_daily.csv"
    ontem = date(2026, 11, 23)
    nd.write_csv(destino, nd.DAILY_COLUMNS,
                 [nd.row(p, ontem.isoformat(), 1) for p in nd.PACKAGES])

    pedidos = []

    def fake_series(package, start, end, sleep_s=None, verbose=True, on_block=None):
        pedidos.append((package, start, end))
        return []

    monkeypatch.setattr(nd, "fetch_series", fake_series)
    nd.collect(until=ontem, path=destino, verbose=False)
    assert pedidos == []


def test_collect_pede_do_dia_seguinte_ao_cache(monkeypatch, tmp_path):
    destino = tmp_path / "downloads_daily.csv"
    nd.write_csv(destino, nd.DAILY_COLUMNS, [nd.row("npm", "2026-11-20", 1)])

    pedidos = []
    monkeypatch.setattr(nd, "fetch_series",
                        lambda package, start, end, sleep_s=None, verbose=True, on_block=None:
                        pedidos.append((package, start, end)) or [])
    nd.collect(until=date(2026, 11, 23), path=destino, verbose=False)
    assert ("npm", date(2026, 11, 21), date(2026, 11, 23)) in pedidos
    assert ("bun", nd.DATA_START, date(2026, 11, 23)) in pedidos


def test_collect_refresh_ignora_o_cache(monkeypatch, tmp_path):
    destino = tmp_path / "downloads_daily.csv"
    nd.write_csv(destino, nd.DAILY_COLUMNS, [nd.row("npm", "2026-11-20", 1)])

    pedidos = []
    monkeypatch.setattr(nd, "fetch_series",
                        lambda package, start, end, sleep_s=None, verbose=True, on_block=None:
                        pedidos.append(start) or [])
    rows = nd.collect(until=date(2026, 11, 23), refresh=True, path=destino, verbose=False)
    assert pedidos == [nd.DATA_START] * len(nd.PACKAGES)
    assert rows == []   # com --refresh o cache antigo não volta para o CSV


def test_collect_salva_o_progresso_a_cada_bloco(monkeypatch, tmp_path):
    """Checkpoint: um 429 insistente no 2º pacote não joga fora o que o 1º já trouxe."""
    destino = tmp_path / "downloads_daily.csv"

    def fake_series(package, start, end, sleep_s=None, verbose=True, on_block=None):
        if package == "npm":
            on_block([nd.row("npm", "2026-11-23", 11)])
            return []
        raise RuntimeError("HTTP Error 429")

    monkeypatch.setattr(nd, "fetch_series", fake_series)
    with pytest.raises(RuntimeError, match="429"):
        nd.collect(until=date(2026, 11, 23), path=destino, verbose=False)

    assert nd.read_daily(destino) == [nd.row("npm", "2026-11-23", 11)]


def test_collect_sem_checkpoint_nao_toca_o_csv(tmp_path, monkeypatch):
    destino = tmp_path / "downloads_daily.csv"
    monkeypatch.setattr(nd, "fetch_series",
                        lambda package, start, end, sleep_s=None, verbose=True, on_block=None:
                        on_block([nd.row(package, "2026-11-23", 1)]))
    nd.collect(until=date(2026, 11, 23), path=destino, verbose=False, checkpoint=False)
    assert not destino.exists()


# ---------------------------------------------------------------- limite de requisições


def test_sleep_padrao_respeita_o_limite_de_uma_por_segundo():
    assert nd.SLEEP_S >= 1.0


@pytest.mark.parametrize(("cabecalho", "esperado"), [
    ({"Retry-After": "90"}, 90.0),
    ({"Retry-After": " 7 "}, 7.0),
    ({"Retry-After": "0"}, 1.0),              # nunca menos de 1 s
    ({"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}, None),   # formato de data: ignorado
    ({}, None),
    (None, None),
])
def test_retry_after(cabecalho, esperado):
    import urllib.error

    exc = urllib.error.HTTPError("http://x", 429, "devagar", cabecalho, None)
    assert nd._retry_after(exc) == esperado


def _um_429_depois_ok(monkeypatch, cabecalho):
    """Primeira chamada leva 429 com `cabecalho`, a segunda responde; devolve as esperas feitas."""
    import urllib.error

    esperas, tentativas = [], []

    def fake(url, timeout=None):
        tentativas.append(url)
        if len(tentativas) == 1:
            raise urllib.error.HTTPError(url, 429, "devagar", cabecalho, None)
        return {"downloads": [{"day": "2026-01-01", "downloads": 1}]}

    monkeypatch.setattr(nd, "_get_json", fake)
    monkeypatch.setattr(nd.time, "sleep", esperas.append)
    assert len(nd.fetch_block("npm", date(2026, 1, 1), date(2026, 1, 1))) == 1
    return esperas


def test_retry_after_maior_que_o_backoff_manda(monkeypatch):
    assert _um_429_depois_ok(monkeypatch, {"Retry-After": "600"}) == [600.0]


def test_retry_after_curto_nao_encurta_o_backoff(monkeypatch):
    """A API responde `Retry-After: 0` e, obedecendo a ele, a coleta gastou as 5 tentativas em 4 s."""
    assert _um_429_depois_ok(monkeypatch, {"Retry-After": "0"}) == [nd.BACKOFF_S]


def test_sem_retry_after_usa_o_backoff(monkeypatch):
    assert _um_429_depois_ok(monkeypatch, {}) == [nd.BACKOFF_S]


def test_backoff_cresce_a_cada_tentativa(monkeypatch):
    import urllib.error

    esperas = []

    def fake(url, timeout=None):
        raise urllib.error.HTTPError(url, 429, "devagar", {}, None)

    monkeypatch.setattr(nd, "_get_json", fake)
    monkeypatch.setattr(nd.time, "sleep", esperas.append)
    with pytest.raises(urllib.error.HTTPError):
        nd.fetch_block("npm", date(2026, 1, 1), date(2026, 1, 1))
    assert esperas == [nd.BACKOFF_S * i for i in range(1, nd.MAX_TRIES)]


# ---------------------------------------------------------------- derivados


def test_weekly_soma_por_semana_iso_e_marca_bordas():
    # 2026-01-01 é quinta: a primeira semana (segunda 2025-12-29) fica com 4 dias.
    rows = [nd.row("npm", (date(2026, 1, 1) + timedelta(days=i)).isoformat(), 1)
            for i in range(11)]
    semanas = nd.weekly(rows)
    assert [(s["week_start"], s["downloads"], s["complete_week"]) for s in semanas] == [
        ("2025-12-29", 4, False),
        ("2026-01-05", 7, True),
    ]
    assert all(set(s) == set(nd.WEEKLY_COLUMNS) for s in semanas)


def test_meta_tem_uma_linha_por_pacote_com_a_data_da_coleta():
    rows = [nd.row("npm", "2026-01-01", 3), nd.row("npm", "2026-01-02", 4)]
    linhas = nd.meta(rows, "2026-11-24T19:00:00-03:00")
    assert [m["package"] for m in linhas] == list(nd.PACKAGES)
    npm = next(m for m in linhas if m["package"] == "npm")
    assert (npm["first_day"], npm["last_day"], npm["days"], npm["total_downloads"]) == (
        "2026-01-01", "2026-01-02", 2, 7)
    assert all(m["fetched_at"] == "2026-11-24T19:00:00-03:00" for m in linhas)
    sem_dados = next(m for m in linhas if m["package"] == "bun")
    assert sem_dados["days"] == 0 and sem_dados["first_day"] == ""


def test_meta_cobre_as_colunas_declaradas():
    linhas = nd.meta([], "2026-11-24T19:00:00-03:00")
    assert set(linhas[0]) == set(nd.META_COLUMNS)


def test_gaps_acha_dia_faltando():
    rows = [nd.row("npm", "2026-01-01", 1), nd.row("npm", "2026-01-03", 1)]
    assert nd.gaps(rows) == {"npm": 1}


def test_gaps_vazio_quando_a_serie_e_continua():
    rows = [nd.row("npm", (date(2026, 1, 1) + timedelta(days=i)).isoformat(), 1)
            for i in range(5)]
    assert nd.gaps(rows) == {}


# ---------------------------------------------------------------- era da ferramenta


@pytest.mark.parametrize(("package", "dia", "esperado"), [
    ("bun", "2015-02-27", False),    # nome ocupado por outro pacote desde 2013
    ("bun", "2023-09-07", False),    # véspera do Bun 1.0.0
    ("bun", "2023-09-08", True),
    ("pnpm", "2016-01-31", False),
    ("pnpm", "2016-02-01", True),
    ("yarn", "2016-10-10", False),   # lançamento público do Yarn
    ("yarn", "2016-10-11", True),
    ("@yarnpkg/cli", "2019-09-05", True),
    ("npm", "2015-01-10", True),     # o pacote já era o npm antes dos dados começarem
])
def test_tool_era(package, dia, esperado):
    assert nd.tool_era(package, dia) is esperado


def test_row_marca_a_era():
    assert nd.row("bun", "2015-02-27", 19) == {
        "package": "bun", "day": "2015-02-27", "downloads": 19, "tool_era": False}


def test_read_daily_recalcula_a_era(tmp_path):
    """CSV antigo com a marca errada não contamina: `tool_era` sai sempre de `PACKAGES`."""
    destino = tmp_path / "downloads_daily.csv"
    nd.write_csv(destino, nd.DAILY_COLUMNS,
                 [{"package": "bun", "day": "2015-02-27", "downloads": 19, "tool_era": True}])
    assert nd.read_daily(destino)[0]["tool_era"] is False


def test_meta_separa_a_era_do_total_bruto():
    rows = [nd.row("bun", "2015-02-27", 19), nd.row("bun", "2023-09-08", 100)]
    linha = next(m for m in nd.meta(rows, "x") if m["package"] == "bun")
    assert (linha["total_downloads"], linha["tool_era_downloads"]) == (119, 100)
    assert (linha["days"], linha["tool_era_days"]) == (2, 1)
    assert linha["tool_from"] == "2023-09-08"


def test_toda_data_de_era_cai_dentro_de_uma_janela_plausivel():
    """Guarda-corpo: uma data de `tool_from` depois do fim dos dados zeraria a série em silêncio."""
    for info in nd.PACKAGES.values():
        assert date(2012, 1, 1) <= info["tool_from"] <= date(2026, 1, 1)


# ---------------------------------------------------------------- contratos e CLI


def test_pacotes_apontam_para_tratamentos_que_existem():
    """Se um id de tratamento mudar em `config.MANAGERS`, este teste cai junto."""
    for info in nd.PACKAGES.values():
        assert set(info["treatments"]) <= set(MANAGERS)


def test_todo_tratamento_tem_algum_pacote():
    cobertos = {t for info in nd.PACKAGES.values() for t in info["treatments"]}
    assert cobertos == set(MANAGERS)


def test_cada_pacote_declara_a_ressalva_de_construto():
    assert all(info["caveat"].strip() for info in nd.PACKAGES.values())


def test_main_recusa_sleep_abaixo_de_um_segundo():
    with pytest.raises(SystemExit):
        nd.main(["--sleep", "0.1"])


def test_main_grava_os_tres_csvs(monkeypatch, tmp_path):
    monkeypatch.setattr(nd, "DAILY_CSV", tmp_path / "downloads_daily.csv")
    monkeypatch.setattr(nd, "WEEKLY_CSV", tmp_path / "downloads_weekly.csv")
    monkeypatch.setattr(nd, "META_CSV", tmp_path / "downloads_meta.csv")
    monkeypatch.setattr(nd, "collect", lambda **_k: [nd.row("npm", "2026-01-01", 5)])

    assert nd.main(["--quiet"]) == 0
    for nome in ("downloads_daily.csv", "downloads_weekly.csv", "downloads_meta.csv"):
        assert (tmp_path / nome).exists()


def test_main_sem_dados_devolve_erro(monkeypatch):
    monkeypatch.setattr(nd, "collect", lambda **_k: [])
    assert nd.main(["--quiet"]) == 1
