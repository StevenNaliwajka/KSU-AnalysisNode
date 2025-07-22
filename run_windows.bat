@echo off
REM Entry point batch script to launch PowerShell run menu

REM Get the directory where this .bat file is located (project root)
SET SCRIPT_DIR=%~dp0

REM Full path to the PowerShell script inside Codebase\Setup
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Setup\run_windows.ps1

REM Launch PowerShell with -NoExit to keep the window open for errors/output
powershell -NoExit -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

REM Optional: Pause at the end in case NoExit is ignored
pause
