# run_windows.ps1

# Exit on error
$ErrorActionPreference = "Stop"

# Define root directory (where this script lives)
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_PATH = "$PROJECT_ROOT\venv"
$DASHBOARD_PATH = "$PROJECT_ROOT\Codebase\dashboard.py"

# Verify virtual environment exists
if (-Not (Test-Path "$VENV_PATH\Scripts\Activate.ps1")) {
    Write-Error "Virtual environment not found at $VENV_PATH. Run setup_windows.ps1 first."
    exit 1
}

# Activate virtual environment
& "$VENV_PATH\Scripts\Activate.ps1"

# Set PYTHONPATH to include Codebase
$env:PYTHONPATH = "$PROJECT_ROOT\Codebase;$env:PYTHONPATH"

# Run the dashboard
python "$DASHBOARD_PATH"
