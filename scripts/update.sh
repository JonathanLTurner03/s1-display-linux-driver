#!/bin/bash
# Update script for S1 Display Driver
# Run this after making code changes to update the installed version

set -e

echo "S1 Display Driver - Update Script"
echo "=================================="
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

echo "Updating from: $PROJECT_ROOT"
echo

# Ask what to update
echo "What would you like to update?"
echo "1) Python code only (dashboard, widgets, etc.)"
echo "2) Web interface only (HTML, CSS, JS)"
echo "3) Everything (code + web + config)"
echo "4) Just restart services (no file copy)"
read -p "Enter choice [1-4] (default: 1): " choice
choice=${choice:-1}

if [ "$choice" = "1" ]; then
    echo "Updating Python code..."
    cp -r src/* /opt/s1-display/src/
    echo "✓ Python code updated"

elif [ "$choice" = "2" ]; then
    echo "Updating web interface..."
    cp -r web/* /opt/s1-display/web/
    echo "✓ Web interface updated"

elif [ "$choice" = "3" ]; then
    echo "Updating everything..."
    cp -r src/* /opt/s1-display/src/
    cp -r web/* /opt/s1-display/web/
    cp config.yaml /opt/s1-display/ 2>/dev/null || echo "Skipping config.yaml (edit manually if needed)"
    echo "✓ All files updated"

elif [ "$choice" = "4" ]; then
    echo "Skipping file copy..."
else
    echo "Invalid choice"
    exit 1
fi

echo

# Ask about restarting services
echo "Restart services?"
echo "1) Dashboard only"
echo "2) Web interface only"
echo "3) Both services"
echo "4) Skip restart"
read -p "Enter choice [1-4] (default: 3): " restart_choice
restart_choice=${restart_choice:-3}

if [ "$restart_choice" = "1" ]; then
    echo "Restarting dashboard service..."
    systemctl restart s1-dashboard.service
    echo "✓ Dashboard restarted"
    sleep 2
    systemctl status s1-dashboard.service --no-pager | head -10

elif [ "$restart_choice" = "2" ]; then
    echo "Restarting web interface service..."
    systemctl restart s1-web.service 2>/dev/null || echo "Web service not found"
    echo "✓ Web interface restarted"
    sleep 2
    systemctl status s1-web.service --no-pager | head -10 2>/dev/null || true

elif [ "$restart_choice" = "3" ]; then
    echo "Restarting both services..."
    systemctl restart s1-dashboard.service
    echo "✓ Dashboard restarted"
    systemctl restart s1-web.service 2>/dev/null && echo "✓ Web interface restarted" || echo "⚠ Web service not installed"
    sleep 2
    echo
    echo "Dashboard status:"
    systemctl status s1-dashboard.service --no-pager | head -10
    echo
    if systemctl is-active --quiet s1-web.service 2>/dev/null; then
        echo "Web interface status:"
        systemctl status s1-web.service --no-pager | head -10
    fi

elif [ "$restart_choice" = "4" ]; then
    echo "Skipping service restart"
    echo "Services will use old code until restarted"
fi

echo
echo "=================================="
echo "Update complete!"
echo "=================================="
echo
echo "View logs:"
echo "  Dashboard:      sudo journalctl -u s1-dashboard.service -f"
echo "  Web interface:  sudo journalctl -u s1-web.service -f"
