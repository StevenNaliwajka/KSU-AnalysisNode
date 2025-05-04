#!/bin/bash

# Exit on error
set -e

# Define root directory (modify if not run from the script's root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Analysis folder path (modify if necessary)
ANALYSIS_FOLDER="$PROJECT_ROOT/Codebase/Analysis"

# Python script to run
TARGET_SCRIPT="$ANALYSIS_FOLDER/tvws_vs_moisture.py"

# Activate the virtual environment (you may need to modify this path)
VENV_PATH="$PROJECT_ROOT/venv"
source "$VENV_PATH/bin/activate"

# Run the Python script
python "$TARGET_SCRIPT"
