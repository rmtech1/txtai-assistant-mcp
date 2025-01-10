#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create necessary directories if they don't exist
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/data"

# Check if virtual environment exists, if not create it
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$PROJECT_ROOT/venv"
fi

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Install/upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r "$PROJECT_ROOT/server/requirements.txt"

# Check if .env file exists, if not create it from template
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "Creating .env file from template..."
    cp "$PROJECT_ROOT/.env.template" "$PROJECT_ROOT/.env"
    echo "Please edit .env file with your configuration"
fi

# Start the server
cd "$PROJECT_ROOT/server"
python main.py
