@echo off
REM Launch PowerShell menu for TVWS Research Tool

SET SCRIPT_DIR=%~dp0
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Run\run_windows.ps1

echo [INFO] Running: %PS_SCRIPT%
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

pause
