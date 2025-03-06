import json
import os

from ..VENVPathing.get_venv_root import get_venv_root


def parse_packages():
    parent_dir = get_venv_root()
    # Construct the full path to the file in the parent directory.
    config_file = os.path.join(parent_dir, "packages.json")
    print(config_file)

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error reading {config_file}: {e}")
        return {}

if __name__ == "__main__":
    parse_packages()