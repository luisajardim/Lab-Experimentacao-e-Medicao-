"""Ponto de entrada do dashboard do Lab04 no Streamlit Community Cloud.

O instalador do Cloud faz `cd` para a pasta do app sem aspas e falha com o espaço em
`Enunciado 4` ("cd: too many arguments"). Esta pasta, sem espaço, só executa o
`Enunciado 4/app.py` como se ele fosse o script principal. Localmente, use `uv run lab04`.

Issue: #93.
"""

import runpy
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "Enunciado 4" / "app.py"

runpy.run_path(str(APP), run_name="__main__")
