#!/bin/bash

# Ensure the script stops if there's an error
set -e

cd "$(dirname "$0")"

# Check if Python3 or Python is installed
if command -v python3 &> /dev/null
then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null
then
    PYTHON_CMD="python"
else
    echo "Python is not installed. Please install Python to continue."
    exit 1
fi

# Check if pip3 or pip is installed
if command -v pip3 &> /dev/null
then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null
then
    PIP_CMD="pip"
else
    echo "pip is not installed. Please install pip to continue."
    exit 1
fi

# Check if virtualenv exists; if not, create it
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found, creating one..."
    $PYTHON_CMD -m venv $VENV_DIR
    echo "Virtual environment created."
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

$PIP_CMD install --upgrade pip

# Run the Python script
$PIP_CMD install -r requirements.txt

$PYTHON_CMD ./ui.py


# Deactivate the virtual environment
deactivate
