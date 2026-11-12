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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app.py"
SRC = ROOT / "src"


def _forget_project_modules() -> None:
    """Remove de `sys.modules` os módulos do Lab04 (`src/`) já importados.

    O Streamlit só recarrega módulos da pasta do main file (`deploy/`). Sem isto, depois de
    um push o Cloud roda o `app.py` novo com os módulos de `src/` da versão anterior ainda
    em memória (ex.: `AttributeError` em `figures.fig_real_scatter`).
    """
    for name, module in list(sys.modules.items()):
        file = getattr(module, "__file__", None)
        if file and Path(file).resolve().is_relative_to(SRC):
            del sys.modules[name]


_forget_project_modules()
runpy.run_path(str(APP), run_name="__main__")
