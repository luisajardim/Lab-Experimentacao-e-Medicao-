"""Testes da análise de adoção e da aba Adoção × desempenho (T16, #113).

Nada aqui lê os CSVs reais da coleta: as séries são montadas à mão, para os números esperados
serem óbvios na própria asserção.
"""

import numpy as np
import pandas as pd
import pytest

import adoption
import figures
from config import CONTROL, MANAGERS
from npm_downloads import PACKAGES


@pytest.fixture
def daily():
    """Série diária de 2 anos completos, um valor por pacote que facilita a conta.

    `downloads` é constante por pacote, então o total de N dias é `N × valor` e o crescimento
    ano contra ano é exatamente 0 %. São 730 dias de propósito: com menos, a janela do "ano
    anterior" cairia fora da série e o crescimento sairia inflado.
    """
    dias = pd.date_range("2025-01-01", periods=730, freq="D")
    valores = {"npm": 10, "pnpm": 100, "bun": 5, "yarn": 20, "@yarnpkg/cli": 1}
    return pd.DataFrame([
        {"package": p, "day": d, "downloads": v, "tool_era": True}
        for p, v in valores.items() for d in dias
    ])


@pytest.fixture
def weekly():
    semanas = pd.date_range("2025-10-06", periods=10, freq="7D")
    return pd.DataFrame([
        {"package": p, "week_start": w, "downloads": v, "days": 7,
         "complete_week": True, "tool_era": True}
        for p, v in {"npm": 70, "pnpm": 700, "yarn": 140}.items() for w in semanas
    ])


@pytest.fixture
def runs():
    """Coleta mínima mas pareável: 2 projetos × 2 cenários × 6 gerenciadores × 4 repetições.

    O npm leva 10 s em tudo; cada gerenciador tem um tempo fixo, então o speedup de cada célula
    é exato e a média geométrica entre células também.
    """
    tempos = {"npm": 10.0, "pnpm": 5.0, "bun": 2.0, "yarn-classic": 20.0,
              "yarn-berry-nm": 10.0, "yarn-berry-pnp": 4.0}
    rows = []
    for project in ("express-api", "react-vite"):
        for scenario in ("cold", "ci"):
            for manager, wall in tempos.items():
                for rep in range(1, 5):
                    rows.append({
                        "machine": "m1", "run_id": f"{project}{scenario}{manager}{rep}",
                        "timestamp": "2026-11-24T10:00:00-03:00", "project": project,
                        "scenario": scenario, "manager": manager, "manager_version": "1",
                        "node_version": "24", "registry": "local", "rep": rep, "order": rep,
                        "warmup": False, "wall_s": wall, "cpu_s": wall, "peak_rss_mb": 10.0,
                        "disk_mb": 10.0, "cache_mb": 5.0, "n_files": 100, "build_ok": True,
                        "exit_code": 0,
                    })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- contratos de mapeamento


def test_todo_tratamento_tem_um_pacote():
    assert set(adoption.PACKAGE_OF_MANAGER) == set(MANAGERS)


def test_os_dois_linkers_do_berry_compartilham_o_pacote():
    assert (adoption.PACKAGE_OF_MANAGER["yarn-berry-nm"]
            == adoption.PACKAGE_OF_MANAGER["yarn-berry-pnp"] == "@yarnpkg/cli")


def test_cada_pacote_tem_cor_e_rotulo():
    for package in PACKAGES:
        assert adoption.PACKAGE_PALETTE[package].startswith("#")
        assert adoption.PACKAGE_LABELS[package]


# ---------------------------------------------------------------- janelas e totais


def test_window_total_soma_exatamente_a_janela(daily):
    total = adoption.window_total(daily, days=7)
    assert total["pnpm"] == 7 * 100
    assert total["npm"] == 7 * 10


def test_window_total_respeita_o_until(daily):
    """Janela que termina antes do fim da série não arrasta dias posteriores."""
    fim = pd.Timestamp("2025-10-07")
    total = adoption.window_total(daily, days=7, until=fim)
    assert total["pnpm"] == 7 * 100


def test_window_total_vazio_quando_nao_ha_serie():
    assert adoption.window_total(pd.DataFrame()).empty


def test_adoption_table_calcula_fatia_e_crescimento(daily):
    table = adoption.adoption_table(daily)
    assert list(table["package"]) == ["pnpm", "yarn", "npm", "bun", "@yarnpkg/cli"]
    pnpm = table.set_index("package").loc["pnpm"]
    assert pnpm["downloads_window"] == 700
    # 100 de 136 downloads diários somados (10+100+5+20+1)
    assert pnpm["share_window"] == pytest.approx(100 / 136)
    assert pnpm["growth_pct"] == pytest.approx(0.0)   # série constante


def test_adoption_table_cresce_quando_a_serie_cresce():
    """Ano atual com o dobro do anterior tem de dar +100 %."""
    dias = pd.date_range("2025-01-01", periods=730, freq="D")
    rows = [{"package": "pnpm", "day": d, "downloads": 1 if i < 365 else 2, "tool_era": True}
            for i, d in enumerate(dias)]
    table = adoption.adoption_table(pd.DataFrame(rows))
    assert table.set_index("package").loc["pnpm", "growth_pct"] == pytest.approx(100.0)


def test_adoption_table_sem_ano_anterior_nao_inventa_crescimento():
    rows = [{"package": "bun", "day": d, "downloads": 5, "tool_era": True}
            for d in pd.date_range("2026-01-01", periods=30, freq="D")]
    table = adoption.adoption_table(pd.DataFrame(rows))
    assert np.isnan(table.set_index("package").loc["bun", "growth_pct"])


def test_adoption_table_vazia_nao_quebra():
    assert adoption.adoption_table(pd.DataFrame()).empty


def test_add_share_soma_um_em_cada_semana(weekly):
    com_share = adoption.add_share(weekly)
    por_semana = com_share.groupby("week_start")["share"].sum()
    assert np.allclose(por_semana, 1.0)


def test_add_share_semana_toda_zerada_nao_vira_nan():
    zeros = pd.DataFrame([{"package": "bun", "week_start": pd.Timestamp("2026-01-05"),
                           "downloads": 0, "days": 7, "complete_week": True, "tool_era": True}])
    assert adoption.add_share(zeros)["share"].iloc[0] == 0.0


# ---------------------------------------------------------------- leitura dos CSVs


def test_load_daily_filtra_a_era_da_ferramenta(tmp_path):
    destino = tmp_path / "downloads_daily.csv"
    destino.write_text(
        "package,day,downloads,tool_era\n"
        "bun,2015-02-27,19,False\n"
        "bun,2023-09-08,100,True\n", encoding="utf-8")
    assert list(adoption.load_daily(destino)["downloads"]) == [100]
    assert len(adoption.load_daily(destino, tool_era_only=False)) == 2


def test_load_weekly_descarta_semana_incompleta(tmp_path):
    destino = tmp_path / "downloads_weekly.csv"
    destino.write_text(
        "package,week_start,downloads,days,complete_week,tool_era\n"
        "npm,2025-12-29,4,4,False,True\n"
        "npm,2026-01-05,7,7,True,True\n", encoding="utf-8")
    assert list(adoption.load_weekly(destino)["downloads"]) == [7]
    assert len(adoption.load_weekly(destino, complete_only=False)) == 2


def test_load_sem_arquivo_devolve_frame_com_as_colunas(tmp_path):
    vazio = adoption.load_daily(tmp_path / "nao-existe.csv")
    assert vazio.empty and "downloads" in vazio.columns


def test_fetched_at_sem_arquivo_e_vazio(tmp_path):
    assert adoption.fetched_at(tmp_path / "nao-existe.csv") == ""


# ---------------------------------------------------------------- desempenho agregado


def test_overall_speedup_usa_media_geometrica(runs):
    out = adoption.overall_speedup(runs).set_index("manager")
    assert CONTROL not in out.index                       # o controle não se compara consigo
    assert out.loc["pnpm", "speedup_geo"] == pytest.approx(2.0)    # 10 s / 5 s
    assert out.loc["bun", "speedup_geo"] == pytest.approx(5.0)
    assert out.loc["yarn-classic", "speedup_geo"] == pytest.approx(0.5)
    assert out.loc["pnpm", "n_cells"] == 4                # 2 projetos × 2 cenários


def test_media_geometrica_nao_e_aritmetica():
    """0,5× e 2,0× têm de dar 1,0×, não 1,25×: é a razão de ser da média geométrica."""
    cells = pd.DataFrame([{"manager": "pnpm", "speedup": 0.5},
                          {"manager": "pnpm", "speedup": 2.0}])
    valores = cells["speedup"]
    assert float(np.exp(np.log(valores).mean())) == pytest.approx(1.0)


def test_overall_speedup_reporta_amplitude_nao_ic(runs):
    """Com speedup idêntico em todas as células, a amplitude colapsa no próprio ponto."""
    out = adoption.overall_speedup(runs).set_index("manager")
    linha = out.loc["bun"]
    assert linha["speedup_min"] == pytest.approx(linha["speedup_max"]) == pytest.approx(5.0)


def test_overall_speedup_vazio_sem_coleta():
    assert adoption.overall_speedup(pd.DataFrame()).empty


# ---------------------------------------------------------------- cruzamento


def test_adoption_vs_performance_deixa_o_controle_fora(runs, daily):
    points = adoption.adoption_vs_performance(runs, daily)
    assert CONTROL not in set(points["manager"])
    assert set(points["manager"]) == set(MANAGERS) - {CONTROL}


def test_adoption_vs_performance_marca_pacote_compartilhado(runs, daily):
    points = adoption.adoption_vs_performance(runs, daily).set_index("manager")
    assert points.loc["yarn-berry-nm", "shared_package"]
    assert points.loc["yarn-berry-pnp", "shared_package"]
    assert not points.loc["pnpm", "shared_package"]
    # os dois linkers caem no mesmo x, por compartilharem o pacote
    assert (points.loc["yarn-berry-nm", "downloads_year"]
            == points.loc["yarn-berry-pnp", "downloads_year"])


def test_adoption_vs_performance_usa_o_pacote_certo(runs, daily):
    points = adoption.adoption_vs_performance(runs, daily).set_index("manager")
    assert points.loc["yarn-classic", "package"] == "yarn"
    assert points.loc["pnpm", "downloads_year"] == 365 * 100


def test_adoption_vs_performance_sem_dados(runs):
    assert adoption.adoption_vs_performance(runs, pd.DataFrame()).empty
    assert adoption.adoption_vs_performance(pd.DataFrame(), pd.DataFrame()).empty


# ---------------------------------------------------------------- figuras


def test_fig_series_tem_uma_linha_por_pacote(weekly):
    fig = figures.fig_adoption_series(weekly)
    assert len(fig.data) == 3
    assert fig.layout.yaxis.type == "log"


def test_fig_series_aceita_escala_linear(weekly):
    assert figures.fig_adoption_series(weekly, log_y=False).layout.yaxis.type == "linear"


def test_fig_share_empilha_em_percentual(weekly):
    fig = figures.fig_adoption_share(weekly)
    assert all(trace.stackgroup == "one" for trace in fig.data)
    assert tuple(fig.layout.yaxis.range) == (0, 100)


def test_fig_growth_ordena_e_ignora_sem_crescimento(daily):
    table = adoption.adoption_table(daily)
    table.loc[table["package"] == "bun", "growth_pct"] = np.nan
    fig = figures.fig_adoption_growth(table)
    valores = list(fig.data[0].x)
    assert valores == sorted(valores)
    assert "Bun" not in list(fig.data[0].y)


def test_fig_vs_speedup_nao_tem_linha_de_tendencia(runs, daily):
    """5 pontos observacionais não sustentam uma reta; a figura não pode sugerir uma."""
    points = adoption.adoption_vs_performance(runs, daily)
    fig = figures.fig_adoption_vs_speedup(points)
    assert len(fig.data) == 1
    assert fig.data[0].mode == "markers+text"
    assert fig.layout.xaxis.type == "log"


def test_fig_vs_speedup_marca_o_controle_como_referencia(runs, daily):
    points = adoption.adoption_vs_performance(runs, daily)
    fig = figures.fig_adoption_vs_speedup(points)
    linhas = [s for s in fig.layout.shapes if s.type == "line"]
    assert any(s.y0 == s.y1 == 1.0 for s in linhas)
    assert MANAGERS[CONTROL]["label"] not in list(fig.data[0].text)


def test_fig_vs_speedup_distingue_o_pacote_compartilhado(runs, daily):
    points = adoption.adoption_vs_performance(runs, daily)
    fig = figures.fig_adoption_vs_speedup(points)
    simbolos = dict(zip(fig.data[0].text, fig.data[0].marker.symbol, strict=True))
    assert simbolos[MANAGERS["yarn-berry-pnp"]["label"]] == "diamond"
    assert simbolos[MANAGERS["pnpm"]["label"]] == "circle"


def test_fig_vs_speedup_vazio_nao_quebra():
    fig = figures.fig_adoption_vs_speedup(pd.DataFrame())
    assert len(fig.data) == 0


def test_figuras_creditam_a_fonte(weekly, daily):
    table = adoption.adoption_table(daily)
    for fig in (figures.fig_adoption_series(weekly), figures.fig_adoption_share(weekly),
                figures.fig_adoption_growth(table)):
        textos = " ".join(a.text or "" for a in fig.layout.annotations)
        assert "API pública de downloads do npm" in textos
