# Deploy do Lab04 no Streamlit Community Cloud

Esta pasta existe só para o deploy. Para rodar localmente, não use esta pasta: `uv run lab04`.

- `streamlit_app.py`: executa o [`../app.py`](../app.py) como script principal.
- `requirements.txt`: **gerado** do `uv.lock`, que continua sendo a fonte das versões. O Cloud usa este
  arquivo porque ele está na mesma pasta do main file. Não edite à mão; se o `uv.lock` mudar, regenere
  (o teste `tests/test_deploy.py` falha se os dois divergirem):

  ```bash
  # na raiz do Lab04 (onde está o pyproject.toml)
  uv export --frozen --format requirements.txt --no-dev --no-hashes --no-emit-project --no-header \
    > deploy/requirements.txt
  ```

## Atenção: sem espaço no caminho

O instalador do Cloud faz `cd` para a pasta do app sem aspas e falha com espaço no caminho
(`cd: too many arguments`, seguido de `No pyproject.toml found`). No repositório da disciplina o
caminho passa por `Enunciado 4/`, então **o deploy não funciona a partir dele**. Faça o deploy de um
repositório em que o conteúdo do Lab04 esteja na raiz.

**Configuração no Cloud:** branch `main`, main file path `deploy/streamlit_app.py`,
Python 3.12 (em *Advanced settings*), app público (*Share → "This app is public and searchable"*),
subdomínio `lab-experimentacao-medicao-lab04` (igual a `DASHBOARD_URL` em `src/config.py`).
