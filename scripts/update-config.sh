#!/bin/bash
# Config update helper for S1 Display
# Helps merge new config options while preserving existing settings

set -e

echo "S1 Display - Config Update Helper"
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

CURRENT_CONFIG="/opt/s1-display/config.yaml"
NEW_CONFIG="config.yaml"

if [ ! -f "$CURRENT_CONFIG" ]; then
    echo "No existing config found at $CURRENT_CONFIG"
    echo "Installing new config..."
    cp "$NEW_CONFIG" "$CURRENT_CONFIG"
    echo "✓ Config installed"
    exit 0
fi

echo "Current config: $CURRENT_CONFIG"
echo "New template:   $NEW_CONFIG"
echo

# Show what's different
echo "=== Differences (- current, + new template) ==="
echo
diff -u "$CURRENT_CONFIG" "$NEW_CONFIG" || true
echo
echo "================================================"
echo

# Offer options
echo "What would you like to do?"
echo
echo "1) Keep current config (no changes)"
echo "2) Backup current and use new template (lose custom settings)"
echo "3) Manual merge - add new option to current config"
echo "4) Show current config"
echo "5) Show new template"
echo
read -p "Enter choice [1-5] (default: 1): " choice
choice=${choice:-1}

if [ "$choice" = "1" ]; then
    echo "✓ No changes made to config"
    echo
    echo "To add new options manually:"
    echo "  sudo nano $CURRENT_CONFIG"
    echo
    echo "New options you may want to add:"
    echo "  time:"
    echo "    show_am_pm: true  # Show AM/PM for 12h format"

elif [ "$choice" = "2" ]; then
    BACKUP="$CURRENT_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Creating backup at: $BACKUP"
    cp "$CURRENT_CONFIG" "$BACKUP"
    cp "$NEW_CONFIG" "$CURRENT_CONFIG"
    echo "✓ Config updated (old config backed up)"
    echo
    echo "Your old settings are in: $BACKUP"
    echo "Review and copy any custom settings you want to keep"

elif [ "$choice" = "3" ]; then
    echo
    echo "Manual merge helper"
    echo "==================="
    echo
    echo "Recent additions to config.yaml:"
    echo
    echo "1. AM/PM support (added: $(date +%Y-%m-%d))"
    echo "   Add to 'time' section:"
    echo "     show_am_pm: true  # Show AM/PM for 12h format"
    echo
    read -p "Add 'show_am_pm' option to time widget? (Y/n): " add_am_pm
    add_am_pm=${add_am_pm:-Y}

    if [[ "$add_am_pm" =~ ^[Yy]$ ]]; then
        # Check if already exists
        if grep -q "show_am_pm:" "$CURRENT_CONFIG"; then
            echo "  Already exists in config"
        else
            # Create backup
            BACKUP="$CURRENT_CONFIG.backup.$(date +%Y%m%d_%H%M%S)"
            cp "$CURRENT_CONFIG" "$BACKUP"

            # Try to add after format line in time section
            if grep -q "^time:" "$CURRENT_CONFIG"; then
                # Use sed to add the line after "format:"
                sed -i '/^time:/,/^[a-z]/ {
                    /format:/ a\
  show_am_pm: true  # Show AM/PM for 12h format (only applies when format is 12h)
                }' "$CURRENT_CONFIG"
                echo "✓ Added show_am_pm to time section"
                echo "  Backup saved: $BACKUP"
            else
                echo "⚠ Could not find 'time:' section"
                echo "  Please add manually:"
                echo "    time:"
                echo "      show_am_pm: true"
            fi
        fi
    fi

    echo
    echo "✓ Manual merge complete"
    echo
    echo "Review the updated config:"
    echo "  sudo nano $CURRENT_CONFIG"

elif [ "$choice" = "4" ]; then
    echo
    echo "=== Current Config ==="
    cat "$CURRENT_CONFIG"
    echo "======================"

elif [ "$choice" = "5" ]; then
    echo
    echo "=== New Template ==="
    cat "$NEW_CONFIG"
    echo "===================="

else
    echo "Invalid choice"
    exit 1
fi

echo
echo "After updating config, restart the service:"
echo "  sudo systemctl restart s1-dashboard.service"
