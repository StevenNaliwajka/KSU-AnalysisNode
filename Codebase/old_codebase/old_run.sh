#!/bin/bash

# Exit on error
set -e

# Define root directory (where run.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Analysis folder path
ANALYSIS_FOLDER="$PROJECT_ROOT/Codebase/Analysis"

# Python script to run
TARGET_SCRIPT="$ANALYSIS_FOLDER/tvws_vs_moisture.py"

# Activate the virtual environment
VENV_PATH="$PROJECT_ROOT/venv"
source "$VENV_PATH/bin/activate"

# Add Codebase to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# Run the Python script
python "$TARGET_SCRIPT"
