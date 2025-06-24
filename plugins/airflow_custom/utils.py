import logging
from os import path
import yaml
from secrets import token_bytes
from datetime import datetime
from typing import Dict
from pathlib import Path

log = logging.getLogger(__name__)
_config_cache = {}


ANSI_STYLES = {
    "bold": "\033[1m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "bold_red": "\033[1m\033[31m",
    "bold_green": "\033[1m\033[32m",
    "bold_yellow": "\033[1m\033[33m",
    "bold_blue": "\033[1m\033[34m",
}

RESET = "\033[0m"


def log_message(message, style="bold_green"):
    """Log a message with a specific ANSI style."""
    style_code = ANSI_STYLES.get(style, "")
    log.info(f"{style_code}{message}{RESET}")


def log_error(message):
    """Log an error message with a specific ANSI style."""
    style_code = ANSI_STYLES.get("bold_red", "")
    log.error(f"❌ {style_code}{message}{RESET}")


def log_warning(message):
    """Log a warning message with a specific ANSI style."""
    style_code = ANSI_STYLES.get("bold_yellow", "")
    log.warning(f"⚠️ {style_code}{message}{RESET}")


def log_info(message):
    """Log an info message with a specific ANSI style."""
    style_code = ANSI_STYLES.get("bold_green", "")
    log.info(f"✅ {style_code}{message}{RESET}")


def load_config(base_path: str) -> Dict[str, dict]:
    """
    Load configuration from a config.yml file relative to the base_path.

    Procura o config.yml:
    1. No mesmo diretório de base_path
    2. Se não existir, um nível acima

    Adiciona o campo 'data_dir' ao config['vars'] com o caminho absoluto para a pasta /data.

    Faz cache por base_path para evitar múltiplas leituras.
    """
    if base_path in _config_cache:
        return _config_cache[base_path]

    config_path = path.join(path.dirname(base_path), "config.yml")

    if not path.exists(config_path):
        config_path = path.join(path.dirname(
            path.dirname(base_path)), "config.yml")

    if not path.exists(config_path):
        raise FileNotFoundError(f"Config file not found near: {base_path}")

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
    release_file = path.join(path.dirname(base_path), "../.release")
    try:
        with open(release_file, "r") as f:
            version = f.readline()
    except Exception:
        version = token_bytes(3).hex()
    return f'v{version} {datetime.now().strftime("%Y-%m-%d %H:%M")}'


def create_doc(base_path: str) -> str:
    """ Create documentation for DAGs """
    try:
        doc = Path(path.dirname(base_path),
                   "docs/main.md").read_text(encoding="utf8")
        return doc
    except FileNotFoundError:
        raise FileNotFoundError(f"Documentation file not found: {base_path}")
