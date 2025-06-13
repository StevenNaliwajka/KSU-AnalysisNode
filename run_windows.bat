@echo off
setlocal

:: Define root directory (directory this script lives in)
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "VENV_PATH=%PROJECT_ROOT%\venv"
set "PY_PATH=%VENV_PATH%\Scripts\python.exe"
set "DASHBOARD_PATH=%PROJECT_ROOT%\Codebase\dashboard.py"

:: Check if venv exists
if not exist "%PY_PATH%" (
    echo Virtual environment not found. Run setup_windows.ps1 first.
    pause
    exit /b 1
)

:: Set PYTHONPATH
set PYTHONPATH=%PROJECT_ROOT%\Codebase;%PYTHONPATH%

:: Run dashboard
"%PY_PATH%" "%DASHBOARD_PATH%"

pause
