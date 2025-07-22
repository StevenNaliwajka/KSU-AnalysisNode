param (
    [string]$venv = ""
)

Write-Output "`n[INFO] Setting up Python virtual environment..."

# Resolve script directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two directories up to project root
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."

# Ensure Data directory exists at root
$DATA_DIR = Join-Path $PROJECT_ROOT "Data"
if (-Not (Test-Path $DATA_DIR)) {
    Write-Output "[INFO] Creating missing Data directory at $DATA_DIR"
    New-Item -ItemType Directory -Path $DATA_DIR | Out-Null
} else {
    Write-Output "[INFO] Data directory already exists at $DATA_DIR"
}

# Determine virtual environment path
if ($venv) {
    $VENV_DIR = $venv
    Write-Output "[INFO] Using custom virtual environment path: $VENV_DIR"
} else {
    $VENV_DIR = Join-Path $PROJECT_ROOT ".venv"
    Write-Output "[INFO] Using default virtual environment path: $VENV_DIR"
}

$REQUIREMENTS_FILE = Join-Path $SCRIPT_DIR "requirements.txt"

# Check for Python
$python = Get-Command py -ErrorAction SilentlyContinue
if (-Not $python) {
    Write-Error "Python is not installed or 'py' command not found. Please install Python first."
    exit 1
}

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "$VENV_DIR")) {
    Write-Output "[INFO] Creating virtual environment at: $VENV_DIR"
    & py -m venv "$VENV_DIR"
} else {
    Write-Output "[INFO] Virtual environment already exists at: $VENV_DIR"
}

# Verify activation script
$activateScript = "$VENV_DIR\Scripts\Activate.ps1"
if (-Not (Test-Path $activateScript)) {
    Write-Error "Activation script not found at $activateScript. Venv creation may have failed."
    exit 1
}

# Install dependencies
if (Test-Path $REQUIREMENTS_FILE) {
    Write-Output "[INFO] Installing dependencies from requirements.txt..."
    & "$VENV_DIR\Scripts\python.exe" -m pip install --upgrade pip
    & "$VENV_DIR\Scripts\python.exe" -m pip install -r "$REQUIREMENTS_FILE"
    Write-Output "[INFO] Dependencies installed."
} else {
    Write-Output "[INFO] No requirements.txt found at: $REQUIREMENTS_FILE"
}
