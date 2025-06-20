@echo off
REM Entry point batch script to launch PowerShell run menu

REM Get the directory where this .bat file is located
SET SCRIPT_DIR=%~dp0

REM Full path to the PowerShell script
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Setup\run_windows.ps1

REM Call the PowerShell script
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
