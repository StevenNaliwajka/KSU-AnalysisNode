#!/bin/bash
# Activate venv and run the updater

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run Python script
python "$SCRIPT_DIR/update_soil_moisture.py"