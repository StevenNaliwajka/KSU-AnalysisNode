# setup_windows.ps1

<<<<<<< HEAD
# Get the directory this script lives in
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two directories up to the project root
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."
$env:PROJECT_ROOT = $PROJECT_ROOT

# Ensure Data folder exists at root
=======
# Get the directory where this script lives
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Go two levels up to project root (from Codebase/Setup/)
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."
$env:PROJECT_ROOT = $PROJECT_ROOT

# Ensure Data directory exists at project root
>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda
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

<<<<<<< HEAD
# Call setup_venv.ps1 from same directory as this script
$SETUP_VENV_SCRIPT = Join-Path $SCRIPT_DIR "setup_venv.ps1"
=======
# Call setup_venv.ps1 from same folder
$SETUP_VENV_SCRIPT = Join-Path $SCRIPT_DIR "setup_venv.ps1"
$VENV_DIR = Join-Path $PROJECT_ROOT ".venv"

>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda
if (-Not (Test-Path $SETUP_VENV_SCRIPT)) {
    Write-Error "Missing setup_venv.ps1 at $SETUP_VENV_SCRIPT"
    exit 1
}

# Use .venv path two levels up
$VENV_PATH = Join-Path $PROJECT_ROOT ".venv"

Write-Output "`n[INFO] Running setup_venv.ps1..."
<<<<<<< HEAD
& "$SETUP_VENV_SCRIPT" -venv "$VENV_PATH"
=======
& "$SETUP_VENV_SCRIPT" -venv "$VENV_DIR"

# Call setup_files.py from the same folder
$SETUP_FILES_SCRIPT = Join-Path $SCRIPT_DIR "setup_files.py"

if (-Not (Test-Path $SETUP_FILES_SCRIPT)) {
    Write-Error "Missing setup_files.py at $SETUP_FILES_SCRIPT"
    exit 1
}

Write-Output "`n[INFO] Running setup_files.py..."

# Use Python from the virtual environment
$PYTHON_EXE = Join-Path $VENV_DIR "Scripts\python.exe"

# Set working directory to project root to ensure imports like 'Codebase.X' work
Push-Location $PROJECT_ROOT
& "$PYTHON_EXE" "$SCRIPT_DIR\setup_files.py"
Pop-Location

>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda

Write-Output "`n[INFO] Setup complete."
Write-Output "[INFO] Configure your files in /Config/*"
Write-Output "[INFO] To run the program:"
<<<<<<< HEAD
Write-Output "    $VENV_PATH\Scripts\activate"
=======
Write-Output "    $VENV_DIR\Scripts\activate"
>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda
Write-Output "    python run.py"
