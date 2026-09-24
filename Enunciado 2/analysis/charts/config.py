from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "trials-log.json"
OUTPUT_DIR = BASE_DIR / "analysis" / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"

TREATMENTS = ("SEM_IA", "COM_IA")
TREATMENT_LABELS = {"SEM_IA": "Sem IA", "COM_IA": "Com IA"}
TREATMENT_PALETTE = {"SEM_IA": "#365F91", "COM_IA": "#D97941"}
TIMEBOX_MINUTES = 25

ALIASES = {
    "kata-05-isbn-10-calculator": "kata-05-isbn-10-validator",
    "kata-06-pagination": "kata-06-array-chunking-pagination",
}

QUALITY_METRICS = (
    "loc",
    "cyclomatic_complexity",
    "halstead_volume",
    "halstead_difficulty",
    "halstead_effort",
    "duplication_percentage",
)
QUALITY_LABELS = {
    "loc": "LOC",
    "cyclomatic_complexity": "Complexidade ciclomática",
    "halstead_volume": "Halstead volume",
    "halstead_difficulty": "Halstead difficulty",
    "halstead_effort": "Halstead effort",
    "duplication_percentage": "Duplicação (%)",
}
