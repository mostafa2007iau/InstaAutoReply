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

# 5. Create systemd service file
echo "Creating systemd service file..."
PROJECT_DIR=$(pwd)
USER=$(whoami)

sudo tee /etc/systemd/system/instaautoreply.service > /dev/null <<EOF
[Unit]
Description=InstaAutoReply Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8008
Restart=always
RestartSec=10
Environment="PATH=$PROJECT_DIR/venv/bin"

[Install]
WantedBy=multi-user.target
EOF

# 6. Reload systemd, enable and start the service
echo "Enabling and starting instaautoreply service..."
sudo systemctl daemon-reload
sudo systemctl enable instaautoreply.service
sudo systemctl start instaautoreply.service

echo "--- Installation Complete ---"
echo "Service status:"
sudo systemctl status instaautoreply.service --no-pager
echo ""
echo "The service is now running and will start automatically on boot."
echo "To check service status: sudo systemctl status instaautoreply.service"
echo "To view logs: sudo journalctl -u instaautoreply.service -f"
