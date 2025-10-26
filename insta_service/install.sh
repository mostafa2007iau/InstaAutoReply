#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Automated Installation ---"

# 1. Update and upgrade system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Python, venv, and git
echo "Installing Python, venv, and git..."
sudo apt-get install python3 python3-venv git -y

# 3. Create a Python virtual environment
echo "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
else
  echo "Virtual environment 'venv' already exists."
fi

# 4. Activate the virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

echo "--- Installation Complete ---"
echo "To run the service, activate the virtual environment with 'source venv/bin/activate' and then run 'uvicorn main:app --host 0.0.0.0 --port 8008'."
