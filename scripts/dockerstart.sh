#!/bin/bash

# Go to the server directory
cd "$(dirname "$0")/../server"

# Install Python dependencies globally in the container
pip install --upgrade pip
pip install -r requirements.txt

# Use a fallback .env if one isn't provided
if [ ! -f "../.env" ]; then
    echo "WARNING: .env not found, using template."
    cp ../.env.template ../.env
fi

# Start the app
python main.py