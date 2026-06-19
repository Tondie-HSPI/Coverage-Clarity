from pathlib import Path
from typing import Any

import yaml


def _load_yaml_file(file_name: str) -> dict[str, Any]:
    base_dir = Path(__file__).resolve().parent
    rules_path = base_dir / file_name
    with rules_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_obligation_rules() -> dict[str, Any]:
    return _load_yaml_file("obligations.yaml")


def load_governance_rules() -> dict[str, Any]:
    return _load_yaml_file("governance.yaml")


def load_endorsement_rules() -> dict[str, Any]:
    return _load_yaml_file("endorsements.yaml")
