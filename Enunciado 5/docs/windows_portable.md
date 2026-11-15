# Ambiente portátil no Windows (`scripts/windows_portable.ps1`)

Coleta no Windows **sem instalar nada no sistema**: Node, npm, pnpm, Yarn Classic, Bun, uv e o
Python do uv ficam numa pasta só, todos os caches apontam para ela, e as variáveis valem só na
janela do PowerShell aberta pelo script. No fim, `-Clean` apaga a pasta e nada sobra
(conferido: nada em `%APPDATA%`, `%LOCALAPPDATA%` nem `~\.bun`).

Também padroniza as versões nas 3 máquinas, o que reduz uma ameaça à validade interna.

| Ferramenta | Versão | Observação |
|---|---|---|
| Node.js | 24.22.3 (LTS) | zip oficial, SHA-256 conferido |
| npm | o que vem com o Node (11.x) | é o que um dev tem na prática |
| pnpm | 12.21.0 | `npm -g` dentro da pasta |
| Yarn Classic | 1.22.22 | `npm -g` dentro da pasta |
| Yarn Berry | 4.18.1 | **não** é instalado aqui: vem do release em `projects/*/lockfiles/yarn-berry-*/` (T03) |
| Bun | 1.4.4 | zip oficial, SHA-256 conferido |
| uv | 0.13.8 | zip oficial, SHA-256 conferido; baixa o Python 3.12 para dentro da pasta |

## Uso

Escolha uma pasta **curta**, num disco NTFS comum (não Dev Drive), com uns 20 GB livres. Exemplo `F:\lab05`.

```powershell
# 1. Abre uma janela pronta (baixa tudo na 1ª vez, ~2 GB depois do uv sync).
#    -Repo copia o Enunciado 5 para F:\lab05\repo (pode ser o caminho \\wsl.localhost\... do WSL
#    ou um clone do Windows). Não apaga dados já coletados em repo\.
powershell -NoExit -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root F:\lab05 -Repo .

# 2. Na janela aberta (já em F:\lab05\repo):
uv sync
uv run lab05 registry up
uv run lab05 registry warm
uv run lab05 collect --machine <nome> --dry-run
uv run lab05 collect --machine <nome> [--pilot | --reps N]
uv run lab05 registry down

# 3. Leve data\raw\<nome>\ de volta para o repositório (no WSL: cp -r /mnt/f/lab05/repo/data/raw/<nome> data/raw/)
#    e commite de lá. Depois:
powershell -ExecutionPolicy Bypass -File scripts\windows_portable.ps1 -Root F:\lab05 -Clean
```

`-Run "<comando>"` executa um comando no ambiente e sai (ex.: `-Run "uv run pytest -q"`).
O `LAB05_WORKDIR` fica em `<Root>\work` automaticamente.

## Cuidados

- Não rode as ferramentas do Windows sobre `\\wsl.localhost\...` nem as do WSL sobre `/mnt/c|f/...`:
  a ponte entre os sistemas é lenta e estragaria as medições. Por isso o script **copia** o repositório.
- `-Clean` só apaga uma pasta criada pelo script (procura o marcador `.lab05-portable`) e nunca a raiz de um disco.
- Conferido no Windows 11 (F:\lab05): `uv run pytest` (60 passam; 1 pulado porque symlink exige
  privilégio), Verdaccio sobe e desce, `collect --dry-run` ok, `-Clean` remove tudo.
