# Deploy do Lab04 no Streamlit Community Cloud

O código do dashboard está em [`Enunciado 4/`](../Enunciado%204/). Esta pasta existe só para o deploy:
o instalador do Streamlit Cloud faz `cd` para a pasta do app sem aspas e falha com o espaço em
`Enunciado 4` (`cd: too many arguments`), então o Cloud aponta para cá.

- `streamlit_app.py`: executa o `Enunciado 4/app.py` como script principal.
- `requirements.txt`: **gerado** do `Enunciado 4/uv.lock`, que continua sendo a fonte das versões. Não edite à mão;
  se o `uv.lock` mudar, regenere (o teste `tests/test_deploy.py` falha se os dois divergirem):

  ```bash
  cd "Enunciado 4"
  uv export --frozen --format requirements.txt --no-dev --no-hashes --no-emit-project --no-header \
    > ../lab04_deploy/requirements.txt
  ```

**Configuração no Cloud:** repositório `luisajardim/Lab-Experimentacao-e-Medicao-`, branch `main`,
main file path `lab04_deploy/streamlit_app.py`, Python 3.12, app público.

Para rodar localmente, não use esta pasta: `cd "Enunciado 4" && uv run lab04`.
