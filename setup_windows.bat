@echo off
setlocal

:: Define root directory (directory this script lives in)
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: Call the PowerShell setup script from its new location
powershell -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1"

pause
