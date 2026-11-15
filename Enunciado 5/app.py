"""Dashboard do Lab05 (Streamlit) — esqueleto provisório da T01 (#96).

A versão com as 4 abas (Todos × npm, Yarn × Yarn, Adoção × desempenho, Impacto) é a
T10 (#105). Por enquanto mostra só um resumo dos dados no schema de `runs.csv`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import streamlit as st  # noqa: E402

from config import PROJECTS_URL, REPO_URL  # noqa: E402
from schema import load_runs  # noqa: E402

st.set_page_config(page_title="Lab05 — Gerenciadores de pacotes", layout="wide")
st.title("Lab05 — npm × pnpm × Yarn × Bun")
st.caption(f"[Repositório]({REPO_URL}) · [Kanban]({PROJECTS_URL})")

df = load_runs()
if df.empty:
    df = load_runs(include_synthetic=True)
    st.warning("Ainda não há coleta real: exibindo o **CSV sintético** (números inventados).")

st.info("Dashboard em construção: as abas chegam na T10 (#105).")
st.metric("Instalações medidas", len(df))
st.dataframe(
    df.groupby(["manager", "scenario"])["wall_s"].median().unstack().round(2),
    width="stretch",
)
