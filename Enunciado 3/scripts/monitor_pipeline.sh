#!/usr/bin/env bash
# Monitor read-only do pipeline DORA. Uso:
#   scripts/monitor_pipeline.sh collect
#   scripts/monitor_pipeline.sh all 15
# Novos estágios recebem o monitor genérico automaticamente; para uma métrica
# específica, basta adicionar uma função probe_<nome-do-estagio> abaixo.

set -euo pipefail

STAGE="${1:-all}"
INTERVAL="${2:-0}"
CONFIG="${CONFIG:-config.toml}"
PYTHON_BIN="${PIPELINE_PYTHON:-python3}"
[[ -x .venv/bin/python ]] && PYTHON_BIN=".venv/bin/python"

if [[ ! -f "$CONFIG" ]]; then
  printf 'Config não encontrado: %s\n' "$CONFIG" >&2
  exit 2
fi

stage_choices() {
  "$PYTHON_BIN" -m pipeline --help \
    | sed -n 's/.*--stage {\([^}]*\)}.*/\1/p' \
    | tr ',' '\n' \
    | awk '!seen[$0]++'
}

paths() {
  python3 - "$CONFIG" <<'PY'
import sys
import tomllib
from pathlib import Path

config_path = Path(sys.argv[1]).resolve()
with config_path.open("rb") as file:
    config = tomllib.load(file)
base = config_path.parent
for key, value in config["paths"].items():
    print(f"{key}={base / value}")
print(f"final_sample_size={config['filters'].get('final_sample_size', '')}")
PY
}

probe_collect() {
  python3 - "$CONFIG" <<'PY'
import csv
import sys
import tomllib
from pathlib import Path

config_path = Path(sys.argv[1]).resolve()
with config_path.open("rb") as file:
    config = tomllib.load(file)
base, paths = config_path.parent, config["paths"]
manifest_path = base / paths.get("candidate_manifest_csv", paths["candidates_csv"])
gold_dir = base / paths["gold_dir"]
with manifest_path.open(encoding="utf-8-sig", newline="") as file:
    manifest = {row["full_name"] for row in csv.DictReader(file) if row.get("full_name")}
gold = {
    f"{path.parent.name}/{path.stem}"
    for path in gold_dir.rglob("*.json")
    if path.parent != gold_dir
}
done = len(manifest & gold)
total = len(manifest)
print(f"manifesto: {total} | JSONs presentes: {done} | faltam: {total - done} | progresso: {done / total:.1%}" if total else "manifesto vazio")
PY
}

probe_collect_commits() {
  python3 - "$CONFIG" <<'PY'
import csv
import json
import sys
import tomllib
from pathlib import Path

config_path = Path(sys.argv[1]).resolve()
with config_path.open("rb") as file:
    config = tomllib.load(file)
base, paths = config_path.parent, config["paths"]
template = base / paths["gold_dir"] / "labels_template.csv"
gold_dir = base / paths["gold_dir"]
if not template.exists():
    print("template gold ausente")
    raise SystemExit
rows = list(csv.DictReader(template.open(encoding="utf-8-sig", newline="")))
expected = completed = 0
for row in rows:
    owner, repo = row["full_name"].split("/", 1)
    source = gold_dir / owner / f"{repo}.json"
    if not source.exists():
        continue
    data = json.loads(source.read_text(encoding="utf-8"))
    commits = {entry.get("release"): entry for entry in data.get("commits_between", [])}
    for index in range(1, 6):
        url = row.get(f"release_url_{index}", "")
        if not url:
            continue
        expected += 1
        tag = url.rsplit("/tag/", 1)[-1]
        if tag in commits:
            completed += 1
print(f"compares das releases gold: {completed}/{expected} ({completed / expected:.1%})" if expected else "nenhuma release gold")
PY
}

probe_metrics() {
  python3 - "$CONFIG" <<'PY'
import csv
import sys
import tomllib
from pathlib import Path

config_path = Path(sys.argv[1]).resolve()
with config_path.open("rb") as file:
    config = tomllib.load(file)
metrics = config_path.parent / config["paths"]["datasets_dir"] / "metrics.csv"
target = config["filters"].get("final_sample_size", "?")
if not metrics.exists():
    print(f"metrics.csv ainda não gerado | alvo: {target}")
else:
    with metrics.open(encoding="utf-8-sig", newline="") as file:
        count = sum(1 for _ in csv.DictReader(file))
    print(f"métricas: {count}/{target} repositórios")
PY
}

probe_report() {
  python3 - "$CONFIG" <<'PY'
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

config_path = Path(sys.argv[1]).resolve()
with config_path.open("rb") as file:
    config = tomllib.load(file)
reports = config_path.parent / config["paths"]["reports_dir"]
files = sorted(path for path in reports.glob("*") if path.is_file())
if not files:
    print("nenhum relatório gerado")
for path in files:
    age = datetime.now(timezone.utc).timestamp() - path.stat().st_mtime
    print(f"{path.name}: {age / 60:.1f} min desde atualização")
PY
}

probe_generic() {
  local stage="$1"
  local started
  started="$(pgrep -fc "python.*pipeline.*--stage[ =]${stage}" || true)"
  printf '%s: %s processo(s) detectado(s); use uma função probe_%s para detalhes.\n' "$stage" "$started" "${stage//-/_}"
}

render() {
  clear 2>/dev/null || true
  printf 'Monitor DORA — %s\n%s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')" "$(printf '%0.s-' {1..72})"
  local stages
  if [[ "$STAGE" == "all" ]]; then
    stages="$(stage_choices)"
  else
    stages="$STAGE"
  fi
  while IFS= read -r stage; do
    [[ -z "$stage" ]] && continue
    printf '[%s] ' "$stage"
    local function="probe_${stage//-/_}"
    if declare -F "$function" >/dev/null; then
      "$function"
    else
      probe_generic "$stage"
    fi
  done <<< "$stages"
}

while :; do
  render
  [[ "$INTERVAL" -gt 0 ]] || break
  sleep "$INTERVAL"
done
