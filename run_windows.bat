@echo off
REM Launch PowerShell menu for TVWS Research Tool

REM Get the directory where this .bat file is located (project root)
SET SCRIPT_DIR=%~dp0

REM Full path to the PowerShell script inside Codebase\Setup
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Setup\run_windows.ps1

REM Launch PowerShell with -NoExit to keep the window open for errors/output
echo [INFO] Running: %PS_SCRIPT%
powershell -NoExit -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

REM Pause at the end
pause