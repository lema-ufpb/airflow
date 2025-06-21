from os import path
import yaml
from functools import wraps
from secrets import token_bytes
from datetime import datetime, timedelta
from airflow_custom.telegram import telegram_success_alert, telegram_error_alert
from airflow.models.param import Param  # type: ignore

_config_cache = None


def load_config() -> dict:
    """Load configuration from config.yml file."""
    config_path = path.join(path.dirname(__file__), "config.yml")
    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
            data["vars"]["data_dir"] = path.join(
                path.dirname(path.dirname(__file__)), "data")
            return data
    except (FileNotFoundError, yaml.YAMLError) as e:
        raise Exception(f"Error loading configuration: {e}") from e


def parse_config(task_func):
    """ Decorator to inject configuration into task functions."""
    @wraps(task_func)
    def wrapper(**kwargs):
        global _config_cache
        if _config_cache is None:
            _config_cache = load_config()
        return task_func(config=_config_cache,  **kwargs)
    return wrapper


def dag_version() -> str:
    """Update DAG version based on git ci commit."""
    release_file = path.join(path.dirname(__file__), "../.release")
    try:
        with open(release_file, "r") as f:
            version = f.readline()
    except Exception:
        version = token_bytes(3).hex()
    return f'v{version} {datetime.now().strftime("%Y-%m-%d %H:%M")}'


def get_dag_args(default_args=None, params=None):
    """Get DAG arguments from configuration, allowing overrides/extensions for default_args and params."""
    config = load_config()

    base_default_args = {
        "owner": config["args"]["owner"],
        "retries": 0,
        "retry_delay": timedelta(minutes=1),
        "email_on_failure": False,
        "depends_on_past": False,
        "dagrun_timeout": timedelta(minutes=config["args"]["timeout"]),
        "on_failure_callback": telegram_error_alert,
        "on_success_callback": telegram_success_alert,
    }

    base_params = {
        "example": Param(
            "default value",
            type="string",
            description="A parameter with a default value"
        )
    }

    if default_args:
        base_default_args.update(default_args)

    if params:
        base_params.update(params)

    return {
        "dag_id": config["args"]["id"],
        "start_date": datetime(datetime.now().year, 1, 1),
        "schedule": config["args"]["schedule"],
        "description": config["args"]["description"],
        "tags": config["args"]["tags"] + [dag_version()],
        "default_args": base_default_args,
        "catchup": False,
        "params": base_params,
    }
