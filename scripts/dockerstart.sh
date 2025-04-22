#!/bin/bash

# Get the project root from this script's location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Starting txtai-assistant in Docker..."

# Create necessary directories
mkdir -p "$PROJECT_ROOT/logs"
mkdir -p "$PROJECT_ROOT/data"

# Install Python dependencies (no venv)
pip install --upgrade pip
pip install -r "$PROJECT_ROOT/server/requirements.txt"

# Use .env.template if .env is missing
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "No .env file found — copying from template."
    cp "$PROJECT_ROOT/.env.template" "$PROJECT_ROOT/.env"
fi

# Launch the app
cd "$PROJECT_ROOT/server"
python main.py