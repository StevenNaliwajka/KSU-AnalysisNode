#!/bin/bash

# Exit on error
set -e

# Define root directory (where run_linux.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Virtual environment path
VENV_PATH="$PROJECT_ROOT/.venv"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Add Codebase to PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# Menu loop
while true; do
    echo ""
    echo "=== TVWS Research Tool ==="
    echo ""
    echo "[ Available Operations ]"
    echo "  1. Run analysis dashboard"
    echo "  2. Run SDR Analysis"
    echo ""
    echo "  3. Exit"
    echo "============================"
    read -p "Select an option [1-3]: " choice

    case $choice in
        1)
            python "$PROJECT_ROOT/Codebase/Run/run_dashboard.py"
            ;;
        2)
            python -m SDRAnalysis.main
            ;;
        3)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid option. Please choose 1, 2, or 3."
            ;;
    esac
done
