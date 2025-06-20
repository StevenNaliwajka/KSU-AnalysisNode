#!/bin/bash

# Exit on error
set -e

# Define root directory (where run.sh lives)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Virtual environment path
VENV_PATH="$PROJECT_ROOT/.venv"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Add Codebase to PYTHONPATH for clean module imports
export PYTHONPATH="$PROJECT_ROOT/Codebase:$PYTHONPATH"

# Menu loop
while true; do
    echo ""
    echo "=== TVWS Research Tool ==="
    echo "1. Get data (pull from remote)"
    echo "2. Run analysis dashboard"
    echo "3. Train a new ML model"
    echo "4. Predict using a trained model"
    echo "5. Clean/preprocess data"
    echo "6. Export visualizations"
    echo "7. Manage saved models"
    echo "8. Exit"
    echo "=============================="
    read -p "Select an option [1-9]: " choice

    case $choice in
        1)
            python "$PROJECT_ROOT/Codebase/Run/get_data_from_remote.py"
            ;;
        2)
            python "$PROJECT_ROOT/Codebase/Run/run_dashboard.py"
            ;;
        3)
            python "$PROJECT_ROOT/Codebase/Run/train_ml_model.py"
            ;;
        4)
            python "$PROJECT_ROOT/Codebase/Run/predict_with_trained_model.py"
            ;;
        5)
            python "$PROJECT_ROOT/Codebase/Run/clean_data.py"
            ;;
        6)
            python "$PROJECT_ROOT/Codebase/Run/export_visualization.py"
            ;;
        7)
            python "$PROJECT_ROOT/Codebase/Run/manage_saved_models.py"
            ;;
        8)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid option. Please choose between 1-9."
            ;;
    esac
done
