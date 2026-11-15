"""Configuração central do Lab05.

Constantes compartilhadas por todos os módulos: semente fixa, caminhos, os 6 tratamentos
(gerenciadores de pacotes, com o npm como controle), os 4 cenários de instalação, os 3
projetos-carga, as versões esperadas e a paleta fixa (uma cor por gerenciador).

Issues: #96 (T01).
"""

from pathlib import Path

SEED = 42

ROOT = Path(__file__).resolve().parents[1]
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
