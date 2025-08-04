# === Debug: Script Entry ===
Write-Host "[DEBUG] setup_windows.ps1 started running" -ForegroundColor Yellow

# === Logging Setup (Errors Only) ===
$logDir = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Definition) "..\.."
if (-Not (Test-Path $logDir)) {
    Write-Host "[DEBUG] Log directory does not exist. Creating: $logDir" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}
$LOG_FILE = Join-Path $logDir "setup_windows_errors.log"

Function LogError {
    param ([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $formatted = "[$timestamp] [ERROR] $Message"
    Add-Content -Path $LOG_FILE -Value $formatted
    Write-Host $formatted -ForegroundColor Red
}

# Start fresh error log
"=== Setup Errors (if any) at $(Get-Date) ===" | Out-File -FilePath $LOG_FILE

# Get the directory where this script lives
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJECT_ROOT = Resolve-Path "$SCRIPT_DIR\..\.."
$env:PROJECT_ROOT = $PROJECT_ROOT
Write-Host "[INFO] Project root is $PROJECT_ROOT"

# Ensure Data directory exists at project root
$DATA_DIR = Join-Path $PROJECT_ROOT "Data"
if (-Not (Test-Path $DATA_DIR)) {
    Write-Host "[INFO] Creating missing Data directory at $DATA_DIR"
    New-Item -ItemType Directory -Path $DATA_DIR | Out-Null
} else {
    Write-Host "[INFO] Data directory already exists at $DATA_DIR"
}

# Check for Python
Write-Host "`n[INFO] Checking for Python..."
$python = Get-Command py -ErrorAction SilentlyContinue
if (-Not $python) {
    LogError "Python is not installed. Please install it from https://www.python.org/downloads/windows/"
    exit 1
}
Write-Host "[INFO] Python is available."

# Call setup_venv.ps1
$SETUP_VENV_SCRIPT = Join-Path $SCRIPT_DIR "setup_venv.ps1"
$VENV_DIR = Join-Path $PROJECT_ROOT ".venv"

if (-Not (Test-Path $SETUP_VENV_SCRIPT)) {
    LogError "Missing setup_venv.ps1 at $SETUP_VENV_SCRIPT"
    exit 1
}

Write-Host "`n[INFO] Running setup_venv.ps1..."
try {
    & "$SETUP_VENV_SCRIPT" -venv "$VENV_DIR" -ErrorAction Stop
} catch {
    LogError "setup_venv.ps1 failed: $($_.Exception.Message)"
    exit 1
}

# Call setup_files.py
$SETUP_FILES_SCRIPT = Join-Path $SCRIPT_DIR "setup_files.py"
if (-Not (Test-Path $SETUP_FILES_SCRIPT)) {
    LogError "Missing setup_files.py at $SETUP_FILES_SCRIPT"
    exit 1
}

Write-Host "`n[INFO] Running setup_files.py..."
$PYTHON_EXE = Join-Path $VENV_DIR "Scripts\python.exe"
Push-Location $PROJECT_ROOT
try {
    & "$PYTHON_EXE" "$SETUP_FILES_SCRIPT" 2>&1 | Out-String | ForEach-Object {
        if ($_ -match "Traceback|Error|Exception|failed") {
            LogError "$_"
        }
    }
} catch {
    LogError "setup_files.py failed: $($_.Exception.Message)"
    exit 1
}
Pop-Location

Write-Host "`n[INFO] Setup complete."
Write-Host "[INFO] Configure your files in /Config/*"
Write-Host "[INFO] To run the program:"
Write-Host "    $VENV_DIR\Scripts\activate"
Write-Host "    python run.py"
