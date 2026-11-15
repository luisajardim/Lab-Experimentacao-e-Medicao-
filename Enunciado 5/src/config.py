"""Configuração central do Lab05.

Constantes compartilhadas por todos os módulos: semente fixa, caminhos, os 6 tratamentos
(gerenciadores de pacotes, com o npm como controle), os 4 cenários de instalação, os 3
projetos-carga, as versões esperadas e a paleta fixa (uma cor por gerenciador).

Issues: #96 (T01).
"""

import os
from pathlib import Path

SEED = 42

ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = ROOT / ".env"


def load_env(path: Path = ENV_FILE) -> dict[str, str]:
    """Carrega `KEY=VALOR` do `.env` (sem dependência externa) em `os.environ`.

    Variáveis já definidas no terminal têm prioridade sobre o arquivo. Linhas vazias e
    comentários (`#`) são ignorados; aspas em volta do valor são removidas. Devolve o que foi lido.
    """
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.removeprefix("export ").partition("=")
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key] = value
        os.environ.setdefault(key, value)
    return values


load_env()

# Pasta de trabalho da coleta (projetos copiados, caches isolados, logs). Precisa ficar no
# mesmo disco físico do cache, e NUNCA num tmpfs (o /tmp do WSL fica na RAM). Padrão: `.work/`
# dentro do Enunciado 5 (ignorada pelo git); no Windows, prefira um caminho curto no `.env`
# (ex.: F:\lab05\work) por causa do limite de 260 caracteres dos caminhos.
WORKDIR_ENV = "LAB05_WORKDIR"


def workdir() -> Path:
    """Pasta de trabalho da coleta: `LAB05_WORKDIR` (terminal ou `.env`) ou `ROOT/.work`."""
    value = os.environ.get(WORKDIR_ENV, "").strip()
    return Path(value).expanduser() if value else ROOT / ".work"
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"                    # data/raw/<maquina>/runs.csv + specs.json
DATA_SYNTHETIC = DATA_RAW / "synthetic"    # CSV sintético (T01) para desenvolver antes da coleta
DATA_PROCESSED = DATA / "processed"        # dataset final validado (T13)
DATA_DOWNLOADS = DATA / "npm_downloads"    # séries da API de downloads do npm (T15)
PROJECTS_DIR = ROOT / "projects"           # projetos-carga (T03)
DOCS = ROOT / "docs"

RUNS_FILENAME = "runs.csv"
SPECS_FILENAME = "specs.json"

# Tratamentos: id -> metadados. O npm é o controle (`CONTROL`).
# `family` agrupa as variantes do Yarn (aba Yarn × Yarn). `expected_version` é o prefixo da
# versão a usar; a versão exata instalada é registrada em cada linha do CSV
# (`manager_version`) e fixada no protocolo de coleta (T07, #102).
MANAGERS = {
    "npm": {"label": "npm", "family": "npm", "expected_version": "11"},
    "pnpm": {"label": "pnpm", "family": "pnpm", "expected_version": "10"},
    "bun": {"label": "Bun", "family": "bun", "expected_version": "1"},
    "yarn-classic": {"label": "Yarn Classic", "family": "yarn", "expected_version": "1.22"},
    "yarn-berry-nm": {"label": "Yarn Berry (node-modules)", "family": "yarn",
                      "expected_version": "4"},
    "yarn-berry-pnp": {"label": "Yarn Berry (PnP)", "family": "yarn", "expected_version": "4"},
}
CONTROL = "npm"
YARN_VARIANTS = tuple(m for m, meta in MANAGERS.items() if meta["family"] == "yarn")

# Cenários de instalação (esquema da página de benchmarks do pnpm).
# Cada cenário diz o que existe ANTES da instalação medida.
SCENARIOS = {
    "cold": {"label": "A frio", "lockfile": False, "cache": False, "node_modules": False},
    "ci": {"label": "CI (lockfile, sem cache)", "lockfile": True, "cache": False,
           "node_modules": False},
    "warm-cache": {"label": "Cache quente", "lockfile": True, "cache": True,
                   "node_modules": False},
    "reinstall": {"label": "Reinstalação", "lockfile": True, "cache": True,
                  "node_modules": True},
}

# Projetos-carga (criados na T03, #98, a partir dos templates oficiais).
PROJECTS = {
    "express-api": {"label": "API Express"},
    "react-vite": {"label": "React + Vite"},
    "next-app": {"label": "Next.js"},
}

NODE_EXPECTED_VERSION = "24"   # Node.js LTS ativo em nov/2026; versão exata no protocolo (T07)

REGISTRIES = ("local", "public")   # local = Verdaccio (T02); public = checagem da T19
DEFAULT_REGISTRY = "local"

ALPHA = 0.05

# Paleta fixa (ColorBrewer Dark2 + Paired): mesma cor por gerenciador em todas as abas.
PALETTE = {
    "npm": "#7F8C8D",            # cinza: o controle
    "pnpm": "#D95F02",
    "bun": "#E7298A",
    "yarn-classic": "#A6CEE3",   # família Yarn em tons de azul
    "yarn-berry-nm": "#1F78B4",
    "yarn-berry-pnp": "#08306B",
}

REPO_URL = "https://github.com/luisajardim/Lab-Experimentacao-e-Medicao-"
PROJECTS_URL = "https://github.com/users/luisajardim/projects/2"
DASHBOARD_URL = ""   # preenchido no deploy (T11, #106)
