#!/bin/bash
# Wrapper to activate venv and run dashboard

# Exit on error
set -e

# Define project root (go 2 levels up from this script: Setup → Codebase → Project root)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Virtual environment path
VENV_PATH="$PROJECT_ROOT/.venv"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Add Codebase to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# Run the dashboard
exec python "$PROJECT_ROOT/Codebase/Run/run_dashboard.py"
