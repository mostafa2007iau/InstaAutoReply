#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e
echo "--- Starting Automated Installation ---"
# Determine the script's own directory to run commands from the correct context.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if running inside Docker
if [ -f /.dockerenv ] || grep -sq 'docker\|lxc' /proc/1/cgroup 2>/dev/null; then
    echo "Docker environment detected."
    IS_DOCKER=true
else
    echo "Standard Linux environment detected."
    IS_DOCKER=false
fi

if [ "$IS_DOCKER" = true ]; then
    # Docker environment: Install dependencies and prepare for supervisor/exec
    echo "Installing Python dependencies for Docker..."
    pip install -r requirements.txt
    
    echo "--- Docker Installation Complete ---"
    echo "Starting uvicorn service..."
    # Use exec to replace the shell process with uvicorn (for Docker CMD/ENTRYPOINT)
    exec uvicorn main:app --host 0.0.0.0 --port 8008
else
    # Standard Linux environment: Full installation with systemd
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
    
    # 5. Create systemd service
    echo "Creating systemd service..."
    SERVICE_NAME="insta-auto-reply.service"
    SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
    
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Instagram Auto Reply Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR
Environment="PATH=$SCRIPT_DIR/venv/bin"
ExecStart=$SCRIPT_DIR/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8008
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # 6. Reload systemd, enable and start the service
    echo "Enabling and starting systemd service..."
    sudo systemctl daemon-reload
    sudo systemctl enable "$SERVICE_NAME"
    sudo systemctl start "$SERVICE_NAME"
    
    echo "--- Installation Complete ---"
    echo "Project is installed in: $SCRIPT_DIR"
    echo "Service status: sudo systemctl status $SERVICE_NAME"
    echo "To view logs: sudo journalctl -u $SERVICE_NAME -f"
fi
