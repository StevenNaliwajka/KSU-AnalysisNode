import json
import os

from ..VENVPathing.get_venv_root import get_venv_root


def load_env_vars():
    """Load environment variables from JSON file."""

    parent_dir = get_venv_root()
    # Construct the full path to the file in the parent directory.
    config_file = os.path.join(parent_dir, "run_env_var.json")

    if not os.path.exists(config_file):
        return

    with open(config_file, "r") as file:
        try:
            env_vars = json.load(file)
            for key, value in env_vars.items():
                os.environ[key] = str(value)
        except json.JSONDecodeError as e:
            print(f"Error loading {config_file}: {e}")