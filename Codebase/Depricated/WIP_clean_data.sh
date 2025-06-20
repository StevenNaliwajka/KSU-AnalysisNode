#!/bin/bash

# Exit on error
set -e

# Get project root (directory of this script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEBASE_DIR="$PROJECT_ROOT/Codebase"
VENV_PATH="$PROJECT_ROOT/venv"
TARGET_SCRIPT="$CODEBASE_DIR/DataManager/data_cleaner.py"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Add project root to PYTHONPATH so Codebase/ imports work
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Run the data cleaner script
python "$TARGET_SCRIPT"
