@echo off
REM Orpheus Collage Tools - Windows Launcher
REM This batch file runs the Python script on Windows

setlocal

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%collage_tools.py"

REM Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Check if Python 3 is available
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python3
    ) else (
        echo ❌ Python 3 is required but not found!
        echo Please install Python 3 from https://python.org
        pause
        exit /b 1
    )
)

REM Run the Python script with all arguments
"%PYTHON_CMD%" "%PYTHON_SCRIPT%" %*

endlocal
