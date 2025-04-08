import yaml
from typing import Any


def load_yaml_config(filepath: str) -> Any:
    """
    Loads a YAML configuration file.

    Args:
        filepath (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    with open(filepath, "r") as file:
        return yaml.safe_load(file)
