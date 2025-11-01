#!/bin/bash
# Quick fix for S1 Display permissions

echo "AceMagic S1 Display - Permission Fix"
echo "===================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Installing udev rules..."
cp 99-s1-display.rules /etc/udev/rules.d/

echo "Reloading udev rules..."
udevadm control --reload-rules
udevadm trigger

echo
echo "✓ Permissions fixed!"
echo
echo "Now unplug and replug your S1 device (or reboot)"
echo "Then run: python3 diagnose.py"
echo
