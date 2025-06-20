# Exit on error
$ErrorActionPreference = "Stop"

# Define root directory (where this script lives)
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_PATH = "$PROJECT_ROOT\.venv"
$RUN_DIR = "$PROJECT_ROOT\Codebase\Run"

# Verify virtual environment exists
if (-Not (Test-Path "$VENV_PATH\Scripts\Activate.ps1")) {
    Write-Error "Virtual environment not found at $VENV_PATH. Run setup_windows.ps1 first."
    exit 1
}

# Activate virtual environment
& "$VENV_PATH\Scripts\Activate.ps1"

# Set PYTHONPATH to include Codebase
$env:PYTHONPATH = "$PROJECT_ROOT\Codebase;$env:PYTHONPATH"

# Menu loop
while ($true) {
    Write-Host ""
    Write-Host "=== TVWS Research Tool ==="
    Write-Host "1. Get data (pull from remote)"
    Write-Host "2. Run analysis dashboard"
    Write-Host "3. Train a new ML model"
    Write-Host "4. Predict using a trained model"
    Write-Host "5. Clean/preprocess data"
    Write-Host "6. Evaluate model on a dataset"
    Write-Host "7. Export visualizations"
    Write-Host "8. Manage saved models"
    Write-Host "9. Exit"
    Write-Host "=============================="

    $choice = Read-Host "Select an option [1-9]"

    switch ($choice) {
        "1" { python "$RUN_DIR\get_data_from_remote.py" }
        "2" { python "$RUN_DIR\run_dashboard.py" }
        "3" { python "$RUN_DIR\train_ml_model.py" }
        "4" { python "$RUN_DIR\predict_with_trained_model.py" }
        "5" { python "$RUN_DIR\clean_data.py" }
        "6" { python "$RUN_DIR\evaluate_model_on_dataset.py" }
        "7" { python "$RUN_DIR\export_visualization.py" }
        "8" { python "$RUN_DIR\manage_saved_models.py" }
        "9" {
            Write-Host "Exiting."
            break
        }
        Default {
            Write-Host "Invalid option. Please choose between 1–9."
        }
    }
}
