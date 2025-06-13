#!/bin/bash

# Exit on error
set -e

# Define root directory (where run.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Virtual environment path
VENV_PATH="$PROJECT_ROOT/venv"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Add Codebase to PYTHONPATH for clean module imports
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# Run the Dash dashboard app from Codebase
python "$PROJECT_ROOT/Codebase/dashboard.py"
