#!/bin/bash
# Installation script for S1 Time Display

set -e

echo "AceMagic S1 Time Display - Installation Script"
echo "==============================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip libhidapi-hidraw0 libhidapi-libusb0

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages

# Create installation directory
echo "Creating installation directory..."
mkdir -p /opt/s1-display

# Copy files
echo "Copying files..."
cp s1_display.py /opt/s1-display/
cp time_display.py /opt/s1-display/
chmod +x /opt/s1-display/time_display.py

# Install systemd service
echo "Installing systemd service..."
cp s1-time-display.service /etc/systemd/system/
systemctl daemon-reload

# Enable and start service
echo "Enabling and starting service..."
systemctl enable s1-time-display.service
systemctl start s1-time-display.service

echo
echo "Installation complete!"
echo
echo "Service status:"
systemctl status s1-time-display.service --no-pager
echo
echo "Useful commands:"
echo "  View logs:       sudo journalctl -u s1-time-display.service -f"
echo "  Stop service:    sudo systemctl stop s1-time-display.service"
echo "  Start service:   sudo systemctl start s1-time-display.service"
echo "  Restart service: sudo systemctl restart s1-time-display.service"
echo "  Disable service: sudo systemctl disable s1-time-display.service"
