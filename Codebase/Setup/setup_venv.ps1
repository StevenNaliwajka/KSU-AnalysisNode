# setup_venv.ps1

param (
    [string]$venv = "$PSScriptRoot\..\..\venv"
)

Write-Output "Setting up Python virtual environment..."

# Normalize venv path (do not resolve before creation)
$VENV_PATH = [System.IO.Path]::GetFullPath($venv)
$REQUIREMENTS_FILE = "$PSScriptRoot\requirements.txt"

# Check for Python
$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "Python is not installed. Please install it from https://www.python.org/downloads/windows/"
    exit 1
}

# Create venv if missing
if (-Not (Test-Path "$VENV_PATH")) {
    Write-Output "Creating virtual environment at $VENV_PATH"
    & py -m venv "$VENV_PATH"
} else {
    Write-Output "Virtual environment already exists at $VENV_PATH"
}

# Validate venv python path
$venvPython = Join-Path $VENV_PATH "Scripts\python.exe"
if (-Not (Test-Path $venvPython)) {
    Write-Error "Python not found in virtual environment at $venvPython"
    exit 1
}

# Install requirements
if (Test-Path $REQUIREMENTS_FILE) {
    Write-Output "Installing dependencies from requirements.txt..."
    & "$venvPython" -m pip install --upgrade pip
    & "$venvPython" -m pip install -r "$REQUIREMENTS_FILE"
} else {
    Write-Warning "No requirements.txt found at $REQUIREMENTS_FILE"
}

# Run setup_files.py
$setupFiles = "$PSScriptRoot\setup_files.py"
if (Test-Path $setupFiles) {
    Write-Output "`nRunning setup_files.py..."
    & "$venvPython" "$setupFiles"
} else {
    Write-Warning "setup_files.py not found at $setupFiles"
}
