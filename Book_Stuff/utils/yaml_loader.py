from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent

NOVEL_YAML = BASE_DIR / "novels.yaml"

with open(
    NOVEL_YAML,
    "r",
    encoding="utf-8"
) as f:

    NOVEL_CONFIG = yaml.safe_load(f)
