@echo off
setlocal enabledelayedexpansion

<<<<<<< HEAD
REM === Determine paths ===
pushd %~dp0
set "PROJECT_ROOT=%CD%"
popd

REM Add Codebase to PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%\Codebase;%PYTHONPATH%"
=======
:: Get path to this .bat file
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: Now go deeper into Codebase\Setup
powershell -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1"
>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda

REM Debug info
echo [INFO] PROJECT_ROOT is %PROJECT_ROOT%
echo [INFO] PYTHONPATH is %PYTHONPATH%

REM Paths to required files
set "SETUP_VENV_PS1=%PROJECT_ROOT%\Codebase\Setup\setup_venv.ps1"
set "SETUP_FILES_PY=%PROJECT_ROOT%\Codebase\Setup\setup_files.py"
set "REQUIREMENTS_TXT=%PROJECT_ROOT%\Codebase\Setup\requirements.txt"
set "VENV_PATH=%PROJECT_ROOT%\.venv"

REM === Check existence ===
if not exist "%SETUP_FILES_PY%" (
    echo [ERROR] Missing: %SETUP_FILES_PY%
    pause
    exit /b 1
)
if not exist "%SETUP_VENV_PS1%" (
    echo [ERROR] Missing: %SETUP_VENV_PS1%
    pause
    exit /b 1
)
if not exist "%REQUIREMENTS_TXT%" (
    echo [ERROR] Missing: %REQUIREMENTS_TXT%
    pause
    exit /b 1
)

REM === Run setup_files.py ===
echo [INFO] Running setup_files.py...
py "%SETUP_FILES_PY%"
if errorlevel 1 (
    echo [ERROR] setup_files.py failed.
    pause
    exit /b 1
)

REM === Setup venv ===
echo [INFO] Setting up virtual environment...
powershell -ExecutionPolicy Bypass -File "%SETUP_VENV_PS1%" -venv "%VENV_PATH%"
if errorlevel 1 (
    echo [ERROR] setup_venv.ps1 failed.
    pause
    exit /b 1
)

REM === Final instructions ===
echo ----------------------------------------------------
echo [INFO] Setup complete.
echo.
echo To activate your environment:
echo     call "%VENV_PATH%\Scripts\activate"
echo Then run:
echo     run_windows.bat
pause
