# Exit on error
$ErrorActionPreference = "Stop"

# Debug: Show starting point
Write-Host "`n[DEBUG] Starting run_windows.ps1"

# Define project root (2 levels up from this script)
$PROJECT_ROOT = Resolve-Path "$PSScriptRoot\..\.."
$VENV_PATH = "$PROJECT_ROOT\.venv"

# Debug: Show resolved paths
Write-Host "[DEBUG] Project root: $PROJECT_ROOT"
Write-Host "[DEBUG] Virtual environment path: $VENV_PATH"

# Activate virtual environment with error handling
try {
    & "$VENV_PATH\Scripts\Activate.ps1"
    Write-Host "[DEBUG] Virtual environment activated."
} catch {
    Write-Host "[ERROR] Failed to activate virtual environment:"
    Write-Host $_.Exception.Message
    pause
    exit 1
}

# Set PYTHONPATH
$env:PYTHONPATH = "$PROJECT_ROOT\Codebase;$env:PYTHONPATH"
Write-Host "[DEBUG] PYTHONPATH set to: $env:PYTHONPATH"

# Menu loop
while ($true) {
    Write-Host ""
    Write-Host "=== TVWS Research Tool ==="
    Write-Host ""
    Write-Host "[ Data Operations ]"
    Write-Host "  1. Get data (pull from remote)"
    Write-Host "  2. Clean/preprocess data"
    Write-Host "  3. Split Train/Test CSVs"
    Write-Host ""
    Write-Host "[ General Analysis ]"
    Write-Host "  4. Run analysis dashboard"
    Write-Host ""
    Write-Host "[ Machine Learning ]"
    Write-Host "  5. Train a new ML model"
    Write-Host "  6. Predict using a trained model"
    Write-Host "  7. Manage saved models"
    Write-Host "  8. Find best soil header for training"
    Write-Host "  9. Export visualizations"
    Write-Host ""
    Write-Host "  10. Exit"
    Write-Host "============================"

    $choice = Read-Host "Select an option [1-10]"

    switch ($choice) {
        "1" { python "$PROJECT_ROOT\Codebase\Run\get_data_from_remote.py" }
        "2" { python "$PROJECT_ROOT\Codebase\Run\clean_data.py" }
        "3" {
            $ratio = Read-Host "Enter train ratio (e.g., 0.8 for 80% train)"
            python "$PROJECT_ROOT\Codebase\Run\split_csv_data.py" --train_ratio $ratio
        }
        "4" { python "$PROJECT_ROOT\Codebase\Run\run_dashboard.py" }
        "5" { python "$PROJECT_ROOT\Codebase\Run\train_ml_model.py" }
        "6" { python "$PROJECT_ROOT\Codebase\Run\predict_with_trained_model.py" }
        "7" { python "$PROJECT_ROOT\Codebase\Run\manage_saved_models.py" }
        "8" { python "$PROJECT_ROOT\Codebase\Run\find_best_soil_header.py" }
        "9" { python "$PROJECT_ROOT\Codebase\Run\export_visualization.py" }
        "10" {
            Write-Host "`nExiting."
            pause
            exit
        }
        default {
            Write-Host "[ERROR] Invalid option. Please choose a number between 1 and 10."
        }
    }

    Write-Host "`n[INFO] Operation complete. Returning to menu..."
}
