#!/bin/bash

# Constants for easy modification
VENV_NAME="mc"
ARGS_FILE="args.json"
REQUIREMENTS_FILE="requirements.txt"
APP_FILE="app.py"

# Create args.json file
echo '{"server_type": "VANILLA", "online_mode": true, "version": "1.20.4", "memory": 1, "cf_page_url": "", "cf_api_key": ""}' > "$ARGS_FILE"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_NAME" ]; then
  python3 -m venv "$VENV_NAME"
fi

# Activate virtual environment
source "$VENV_NAME/bin/activate"

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
  pip install -r "$REQUIREMENTS_FILE"
fi

# Run application
if [ -f "$APP_FILE" ]; then
  python "$APP_FILE"
else
  echo "Error: $APP_FILE not found."
fi