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
    Write-Host ""
    Write-Host "[ Data Operations ]"
    Write-Host "  1. Get data (pull from remote)"
    Write-Host "  2. Clean/preprocess data"
    Write-Host ""
    Write-Host "[ General Analysis ]"
    Write-Host "  3. Run analysis dashboard"
    Write-Host ""
    Write-Host "[ Machine Learning ]"
    Write-Host "  4. Train a new ML model"
    Write-Host "  5. Predict using a trained model"
    Write-Host "  6. Manage saved models"
    Write-Host "  7. Export visualizations"
    Write-Host ""
    Write-Host "  8. Exit"
    Write-Host "=============================="

    $choice = Read-Host "Select an option [1-8]"

    switch ($choice) {
        "1" { python "$RUN_DIR\get_data_from_remote.py" }
        "2" { python "$RUN_DIR\clean_data.py" }
        "3" { python "$RUN_DIR\run_dashboard.py" }
        "4" { python "$RUN_DIR\train_ml_model.py" }
        "5" { python "$RUN_DIR\predict_with_trained_model.py" }
        "6" { python "$RUN_DIR\manage_saved_models.py" }
        "7" { python "$RUN_DIR\export_visualization.py" }
        "8" {
            Write-Host "Exiting."
            break
        }
        Default {
            Write-Host "Invalid option. Please choose between 1–8."
        }
    }
}
