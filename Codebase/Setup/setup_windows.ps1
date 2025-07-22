# setup_windows.ps1

# Get the directory this script lives in
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two directories up to the project root
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."
$env:PROJECT_ROOT = $PROJECT_ROOT

# Ensure Data folder exists at root
$DATA_DIR = Join-Path $PROJECT_ROOT "Data"
if (-Not (Test-Path $DATA_DIR)) {
    Write-Output "[INFO] Creating missing Data directory at $DATA_DIR"
    New-Item -ItemType Directory -Path $DATA_DIR | Out-Null
} else {
    Write-Output "[INFO] Data directory already exists at $DATA_DIR"
}

# Check for Python
Write-Output "`n[INFO] Checking for Python..."
$python = Get-Command py -ErrorAction SilentlyContinue
if (-Not $python) {
    Write-Error "Python is not installed. Please install it from https://www.python.org/downloads/windows/"
    exit 1
}
Write-Output "[INFO] Python is available."

# Call setup_venv.ps1 from same directory as this script
$SETUP_VENV_SCRIPT = Join-Path $SCRIPT_DIR "setup_venv.ps1"
if (-Not (Test-Path $SETUP_VENV_SCRIPT)) {
    Write-Error "Missing setup_venv.ps1 at $SETUP_VENV_SCRIPT"
    exit 1
}

# Use .venv path two levels up
$VENV_PATH = Join-Path $PROJECT_ROOT ".venv"

Write-Output "`n[INFO] Running setup_venv.ps1..."
& "$SETUP_VENV_SCRIPT" -venv "$VENV_PATH"

Write-Output "`n[INFO] Setup complete."
Write-Output "[INFO] Configure your files in /Config/*"
Write-Output "[INFO] To run the program:"
Write-Output "    $VENV_PATH\Scripts\activate"
Write-Output "    python run.py"
