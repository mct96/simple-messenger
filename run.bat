@echo off
setlocal

REM Ensure the script stops if there's an error
set "errorlevel=1"

REM Change to the directory where this script is located
cd /d %~dp0

REM Check if Python3 or Python is installed
where python3 >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
) else (
    where python >nul 2>nul
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
    ) else (
        echo Python is not installed. Please install Python to continue.
        exit /b 1
    )
)

REM Check if pip3 or pip is installed
where pip3 >nul 2>nul
if not errorlevel 1 (
    set "PIP_CMD=pip3"
) else (
    where pip >nul 2>nul
    if not errorlevel 1 (
        set "PIP_CMD=pip"
    ) else (
        echo pip is not installed. Please install pip to continue.
        exit /b 1
    )
)

REM Check if virtualenv exists; if not, create it
set "VENV_DIR=venv"

if not exist "%VENV_DIR%" (
    echo Virtual environment not found, creating one...
    %PYTHON_CMD% -m venv %VENV_DIR%
    echo Virtual environment created.
)

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM Upgrade pip
%PIP_CMD% install --upgrade pip

REM Install required Python packages
%PIP_CMD% install -r requirements.txt

REM Run the Python script
%PYTHON_CMD% ui.py

REM Deactivate the virtual environment
call deactivate

endlocal
