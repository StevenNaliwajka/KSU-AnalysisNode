#!/bin/bash

# Exit on error
set -e

# Define root directory (where run.sh lives)
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
    echo "[ Data Operations ]"
    echo "  1. Get data (pull from remote)"
    echo "  2. Clean/preprocess data"
    echo "  3. Split Train/Test CSVs"
    echo ""
    echo "[ General Analysis ]"
    echo "  4. Run analysis dashboard"
    echo ""
    echo "[ Machine Learning ]"
    echo "  5. Train a new ML model"
    echo "  6. Predict using a trained model"
    echo "  7. Manage saved models"
    echo "  8. Find best soil header for training"
    echo "  9. Export visualizations"
    echo ""
    echo "  10. Exit"
    echo "============================"
    read -p "Select an option [1-10]: " choice

    case $choice in
        1)
            python "$PROJECT_ROOT/Codebase/Run/get_data_from_remote.py"
            ;;
        2)
            python "$PROJECT_ROOT/Codebase/Run/clean_data.py"
            ;;
        3)
            read -p "Enter train ratio (e.g., 0.8 for 80% train): " ratio
            python "$PROJECT_ROOT/Codebase/Run/split_csv_data.py" --train_ratio "$ratio"
            ;;
        4)
            python "$PROJECT_ROOT/Codebase/Run/run_dashboard.py"
            ;;
        5)
            python "$PROJECT_ROOT/Codebase/Run/train_ml_model.py"
            ;;
        6)
            python "$PROJECT_ROOT/Codebase/Run/predict_with_trained_model.py"
            ;;
        7)
            python "$PROJECT_ROOT/Codebase/Run/manage_saved_models.py"
            ;;
        8)
            python "$PROJECT_ROOT/Codebase/Run/find_best_soil_header.py"
            ;;
        9)
            python "$PROJECT_ROOT/Codebase/Run/export_visualization.py"
            ;;
        10)
            echo "Exiting."
            exit 0
            ;;
        *)
            echo "Invalid option. Please choose a number between 1 and 10."
            ;;
    esac
done
