#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Automated Installation ---"

# Determine the script's own directory to run commands from the correct context.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 1. Update and upgrade system packages (optional, can be commented out if not needed)
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Python, venv, and git
echo "Installing Python, venv, and git..."
sudo apt-get install python3 python3-venv git -y

# 3. Create a Python virtual environment in the project directory
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
else
  echo "Virtual environment 'venv' already exists."
fi

# 4. Activate the virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
# Note: 'source' must be used in the shell, but for the script, we can call pip directly.
./venv/bin/pip install -r requirements.txt

echo "--- Installation Complete ---"
echo "Project is installed in: $SCRIPT_DIR"
echo "To run the service, navigate to the directory, activate the virtual environment with 'source venv/bin/activate', and then run 'uvicorn main:app --host 0.0.0.0 --port 8008'."
