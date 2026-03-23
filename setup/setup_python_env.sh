#!/bin/bash

# Exit immediately if any command fails
set -e

echo "Setting up ASHES Python Virtual Environment..."

# Check if ASHESPATH is set (-z checks if the string is empty)
if [[ -z "$ASHESPATH" ]]; then
    echo "FAILURE: ASHESPATH is not set."
    echo "Please run setup_env_vars.sh and then 'source ~/.bashrc' first."
    exit 1
fi

# Define the target environment directory
ENV_DIR="$ASHESPATH/.env"

# Check if the environment already exists
if [[ -d "$ENV_DIR" ]]; then
    echo " -> INFO: Virtual environment already exists at $ENV_DIR."
    echo " -> Skipping creation. (To recreate, delete it using: rm -rf $ENV_DIR)"
else
    echo " -> Creating new Python virtual environment at $ENV_DIR..."
    python3 -m venv "$ENV_DIR"
fi

# Activate the environment (this only activates it for the script's subshell)
echo " -> Activating environment to install/update dependencies..."
source "$ENV_DIR/bin/activate"

# Upgrade pip safely
echo " -> Upgrading pip..."
python3 -m pip install --upgrade pip

# Check if requirements.txt exists before trying to install it
REQ_FILE="$ASHESPATH/setup/requirements.txt"

if [[ -f "$REQ_FILE" ]]; then
    echo " -> Installing dependencies from $REQ_FILE..."
    python3 -m pip install -r "$REQ_FILE"
else
    echo " -> WARNING: $REQ_FILE not found. Skipping dependency installation."
fi

# Deactivate the subshell environment cleanly
deactivate

echo ""
echo "=========================================================="
echo "SUCCESS: Python virtual environment is ready!"
echo "To use it in your current terminal session, run:"
echo ""
echo "    source $ENV_DIR/bin/activate"
echo "=========================================================="
