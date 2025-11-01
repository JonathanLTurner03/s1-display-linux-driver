#!/bin/bash
# Installation script for S1 Display Driver

set -e

echo "AceMagic S1 Display Driver - Installation Script"
echo "================================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip libhidapi-hidraw0 libhidapi-libusb0

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages

# Create installation directory
echo "Creating installation directory..."
mkdir -p /opt/s1-display/src/core /opt/s1-display/src/widgets /opt/s1-display/web

# Copy files
echo "Copying files..."
cp -r src/* /opt/s1-display/src/
cp -r web/* /opt/s1-display/web/
cp config.yaml /opt/s1-display/
chmod +x /opt/s1-display/src/time_display.py
chmod +x /opt/s1-display/src/dashboard.py
chmod +x /opt/s1-display/web/app.py

# Install udev rules
echo "Installing udev rules..."
cp scripts/99-s1-display.rules /etc/udev/rules.d/
udevadm control --reload-rules
udevadm trigger

# Install systemd services
echo ""
echo "Which services would you like to install?"
echo "1) Dashboard only"
echo "2) Dashboard + Web Interface (RECOMMENDED)"
echo "3) Simple time display only"
read -p "Enter choice [1-3] (default: 2): " choice
choice=${choice:-2}

if [ "$choice" = "1" ]; then
    cp scripts/s1-dashboard.service /etc/systemd/system/
    SERVICES="s1-dashboard.service"
elif [ "$choice" = "2" ]; then
    cp scripts/s1-dashboard.service /etc/systemd/system/
    # Create web service
    cat > /etc/systemd/system/s1-web.service <<EOF
[Unit]
Description=S1 Display Web Interface
After=network.target s1-dashboard.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/s1-display/web
ExecStart=/usr/bin/python3 app.py
Restart=always
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
EOF
    SERVICES="s1-dashboard.service s1-web.service"
elif [ "$choice" = "3" ]; then
    cp scripts/s1-time-display.service /etc/systemd/system/
    SERVICES="s1-time-display.service"
else
    echo "Invalid choice"
    exit 1
fi

systemctl daemon-reload

# Enable and start services
echo "Enabling and starting services..."
for SERVICE in $SERVICES; do
    systemctl enable $SERVICE
    systemctl start $SERVICE
done

echo
echo "========================================="
echo "Installation complete!"
echo "========================================="
echo

# Show status
for SERVICE in $SERVICES; do
    echo "Status of $SERVICE:"
    systemctl status $SERVICE --no-pager || true
    echo
done

echo "Useful commands:"
for SERVICE in $SERVICES; do
    echo
    echo "  $SERVICE:"
    echo "    View logs:    sudo journalctl -u $SERVICE -f"
    echo "    Restart:      sudo systemctl restart $SERVICE"
    echo "    Stop/Start:   sudo systemctl stop/start $SERVICE"
done

echo
if [[ "$SERVICES" == *"s1-web"* ]]; then
    echo "========================================="
    echo "Web Interface Available!"
    echo "========================================="
    echo
    echo "Access the configuration interface at:"
    echo "  http://$(hostname -I | awk '{print $1}'):5000"
    echo "  or"
    echo "  http://$(hostname):5000"
    echo
    echo "From there you can:"
    echo "  - Drag and drop widgets"
    echo "  - Customize colors and settings"
    echo "  - Add server monitors"
    echo "  - Save and restart from the web interface"
fi

echo
echo "Config file: /opt/s1-display/config.yaml"
echo "Edit and restart service to apply manual changes"
