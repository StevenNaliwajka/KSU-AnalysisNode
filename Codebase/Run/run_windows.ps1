# run_windows.ps1

# Exit on error
$ErrorActionPreference = "Stop"

# Get project root (2 levels above this script)
$PROJECT_ROOT = Resolve-Path "$PSScriptRoot\..\.."

$VENV_PATH = "$PROJECT_ROOT\.venv"

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
    Write-Host "[ Available Operations ]"
    Write-Host "  1. Run analysis dashboard"
    Write-Host "  2. Run SDR Analysis UI"
    Write-Host "  3. Extract Phase Shift from IQ Files"
    Write-Host ""
    Write-Host "  4. Exit"
    Write-Host "============================"

    $choice = Read-Host "Select an option [1-4]"

    switch ($choice) {
        "1" {
            python "$PROJECT_ROOT\Codebase\Run\run_dashboard.py"
        }
        "2" {
            python -m SDRAnalysis.main
        }
        "3" {
            python "$PROJECT_ROOT\Codebase\SDRAnalysis\iq_phase_extractor.py"
        }
        "4" {
            Write-Host "Exiting."
            break
        }
        Default {
            Write-Host "Invalid option. Please choose 1, 2, 3, or 4."
        }
    }
}
