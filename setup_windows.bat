@echo off
setlocal

:: Get path to this .bat file
set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

:: Now go deeper into Codebase\Setup
powershell -ExecutionPolicy Bypass -File "%PROJECT_ROOT%\Codebase\Setup\setup_windows.ps1"

pause
