@echo off
REM Launch PowerShell menu for TVWS Research Tool

<<<<<<< HEAD
REM Get the directory where this .bat file is located (project root)
=======
>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda
SET SCRIPT_DIR=%~dp0
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Run\run_windows.ps1

<<<<<<< HEAD
REM Full path to the PowerShell script inside Codebase\Setup
SET PS_SCRIPT=%SCRIPT_DIR%Codebase\Setup\run_windows.ps1

REM Launch PowerShell with -NoExit to keep the window open for errors/output
powershell -NoExit -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

REM Optional: Pause at the end in case NoExit is ignored
=======
echo [INFO] Running: %PS_SCRIPT%
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"

>>>>>>> b21a4621b521d932bccd7393b4c6e562e73a3bda
pause
