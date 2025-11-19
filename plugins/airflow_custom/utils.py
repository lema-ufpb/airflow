from os import path
import yaml
from typing import Dict
from pathlib import Path

_config_cache = {}


def load_config(base_path: str, filename: str = "parameters.yml") -> Dict[str, dict]:
    """
    Load configuration from a config.yml file relative to the base_path.

    Procura o config/parameters.yml:
    1. Em config/parameters.yml (relativo ao base_path)
    2. No mesmo diretório de base_path
    3. Se não existir, um nível acima

    Adiciona o campo 'data_dir' ao config['vars'] com o caminho absoluto para a pasta /data.

    Faz cache por base_path para evitar múltiplas leituras.
    """
    if base_path in _config_cache:
        return _config_cache[base_path]

    config_path = path.join(path.dirname(base_path), "config", filename)

    if not path.exists(config_path):
        config_path = path.join(path.dirname(base_path), filename)

    if not path.exists(config_path):
        config_path = path.join(path.dirname(
            path.dirname(base_path)), filename)

    if not path.exists(config_path):
        raise FileNotFoundError(
            f"File not found: {filename} searched in {path.dirname(base_path)}")

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}

        data.setdefault("vars", {})

        data_dir = path.abspath(
            path.join(path.dirname(base_path), "data"))
        data["vars"]["data_dir"] = data_dir

        clean_data = {str(k): v for k, v in data.items()}

        _config_cache[base_path] = clean_data

        return clean_data

    except yaml.YAMLError as e:
        raise Exception(
            f"YAML parse error in config file at {config_path}: {e}") from e


def version(base_path: str) -> str:
    """Update DAG version based on git ci commit."""
    release_file = path.join(path.dirname(base_path), ".release")
    try:
        with open(release_file, "r") as f:
            version = f.readline()
    except Exception:
        version = "dev"

    return f'{version}'


def create_doc(base_path: str) -> str:
    """ Create documentation for DAGs """
    try:
        doc = Path(path.dirname(base_path),
                   "docs/main.md").read_text(encoding="utf8")
        return doc
    except FileNotFoundError:
        raise FileNotFoundError(f"Documentation file not found: {base_path}")
