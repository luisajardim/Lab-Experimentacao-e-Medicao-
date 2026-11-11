"""Ponto de entrada do dashboard do Lab04 no Streamlit Community Cloud.

Executa o `app.py` da pasta acima (a raiz do Lab04) como se ele fosse o script
principal, com o `requirements.txt` desta pasta. Localmente, use `uv run lab04`.

O instalador do Cloud faz `cd` para a pasta do app sem aspas, então o caminho até
aqui não pode ter espaço: no repositório da disciplina ele passa por `Enunciado 4`.
Faça o deploy de um repositório em que o conteúdo do Lab04 esteja na raiz
(main file path `deploy/streamlit_app.py`).

Issue: #93.
"""

import runpy
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"

runpy.run_path(str(APP), run_name="__main__")
