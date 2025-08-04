@echo off
setlocal enabledelayedexpansion
echo Starting setup...
echo (Debug mode enabled — window will stay open)
pause

:: === Resolve project root (batch file directory) ===
set "SCRIPT_PATH=%~f0"
for %%i in ("%SCRIPT_PATH%") do set "PROJECT_ROOT=%%~dpi"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "LOG_FILE=%PROJECT_ROOT%\setup_windows_errors.log"

echo === Setup Errors (if any) at %date% %time% === > "%LOG_FILE%"

:: Debug info
echo [DEBUG] SCRIPT_PATH: %SCRIPT_PATH%
echo [DEBUG] PROJECT_ROOT resolved to: %PROJECT_ROOT%
echo [DEBUG] Looking for setup_windows.ps1 at: %PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1
if not exist "%PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1" (
    echo [FATAL] setup_windows.ps1 not found at %PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1
    pause
    exit /b 1
)
pause

:: Run PowerShell script
echo [INFO] Running setup_windows.ps1...
"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command ^
    "& { try { & '%PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1' -Verbose } catch { Write-Host '--- PowerShell Error ---'; Write-Host $_.Exception.Message; Write-Host $_.ScriptStackTrace; pause; exit 1 } ; pause }"
set "PS_ERROR=%ERRORLEVEL%"
echo [DEBUG] PowerShell exited with code %PS_ERROR%
if %PS_ERROR% NEQ 0 (
    echo [FATAL] PowerShell script failed (exit code %PS_ERROR%). See %LOG_FILE%
    pause
    exit /b %PS_ERROR%
)
pause

:: === Final instructions ===
echo ----------------------------------------------------
echo [INFO] Setup complete.
echo.
echo To activate your environment:
echo     call "%PROJECT_ROOT%\.venv\Scripts\activate"
echo Then run:
echo     run_windows.bat

pause
