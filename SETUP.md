# Setup Guide

## Project Structure

```
s1-display-linux-driver/
├── src/                        # All Python source code
│   ├── core/                  # Core display components
│   │   ├── s1_display.py      # USB HID driver
│   │   └── fonts.py           # Bitmap fonts (3x5, 5x7)
│   ├── widgets/               # Widget implementations
│   │   └── widgets.py         # All widget classes
│   ├── dashboard.py           # Advanced dashboard app
│   ├── time_display.py        # Simple clock app
│   ├── diagnose.py            # Connection diagnostic tool
│   └── test_display.py        # Hardware test suite
├── web/                       # Web configuration interface
│   ├── app.py                 # Flask web server
│   ├── templates/
│   │   └── index.html         # Main web interface
│   └── static/
│       ├── css/style.css      # Styling
│       └── js/app.js          # Drag-and-drop logic
├── scripts/                   # Installation and services
│   ├── install.sh             # Main installer
│   ├── fix-permissions.sh     # USB permission fix
│   ├── 99-s1-display.rules    # udev rules
│   ├── s1-dashboard.service   # Dashboard systemd service
│   └── s1-time-display.service # Simple clock service
├── docs/                      # Documentation and examples
│   └── examples.py            # Display style examples
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
└── README.md                  # Main documentation
```

## Quick Setup on Hecate

### 1. Fix Permissions

```bash
cd s1-display-linux-driver
sudo chmod +x scripts/fix-permissions.sh
sudo ./scripts/fix-permissions.sh
# Unplug and replug device or reboot
```

### 2. Install

```bash
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
# Choose option 2: Dashboard + Web Interface (RECOMMENDED)
```

### 3. Access Web Interface

Open browser to: `http://hecate:5000`

Or find IP: `http://$(hostname -I | awk '{print $1}'):5000`

## Web Interface Features

### Drag and Drop Widgets
- **Left Panel**: Available widgets
- **Center**: Display preview (640x340px = 2x scale of 320x170)
- **Right Panel**: Widget properties editor

### Adding Widgets
1. Drag widget from left panel
2. Drop onto display
3. Widget automatically enabled

### Customizing
1. Click widget on display
2. Properties panel shows:
   - Color picker
   - Prefix text
   - Progress bar toggle
   - Other settings

### Server Monitoring
1. Click "Add Server Monitor"
2. Enter details:
   - Name, Host/IP
   - Port (optional for TCP, else uses ping)
   - Check interval
   - Colors for online/offline

### Saving
- **Save Config**: Writes to `/opt/s1-display/config.yaml`
- **Save & Restart**: Saves and restarts dashboard service

## Manual Testing

### Test Dashboard
```bash
cd src
sudo python3 dashboard.py
# Should see widgets on display
```

### Test Web Interface
```bash
cd web
python3 app.py
# Access at http://localhost:5000
```

### Run Diagnostics
```bash
cd src
python3 diagnose.py
# Check USB connection
```

## Service Management

### Dashboard
```bash
sudo systemctl status s1-dashboard.service
sudo journalctl -u s1-dashboard.service -f
sudo systemctl restart s1-dashboard.service
```

### Web Interface
```bash
sudo systemctl status s1-web.service
sudo journalctl -u s1-web.service -f
sudo systemctl restart s1-web.service
```

## Configuration

Edit `/opt/s1-display/config.yaml` or use web interface.

Example:
```yaml
time:
  enabled: true
  format: 24h
  color: [255, 255, 255]

hostname:
  enabled: true
  prefix: "Host: "
  color: [100, 200, 255]

network:
  local_ip:
    enabled: true
  tailscale_ip:
    enabled: true

system:
  cpu_usage:
    enabled: true
    show_bar: true
  memory_usage:
    enabled: true
    show_bar: true

servers:
  - name: "Router"
    host: "192.168.1.1"
    enabled: true
    check_interval: 10
```

## Troubleshooting

### Can't Connect to Web Interface

1. Check service is running:
   ```bash
   sudo systemctl status s1-web.service
   ```

2. Check firewall:
   ```bash
   sudo ufw allow 5000
   ```

3. Try localhost:
   ```bash
   curl http://localhost:5000
   ```

### Permission Errors

```bash
sudo ./scripts/fix-permissions.sh
# Unplug/replug device
```

### Import Errors

The new folder structure uses relative imports. Make sure you're running from the correct directory:
- Dashboard: Run from `src/` or use systemd service
- Web: Run from `web/` or use systemd service

### Device Not Found

```bash
lsusb | grep 04d9:fd01
# Should see the device
```

If not visible, check USB connection and try different port.

## Development

### Adding New Widgets

1. Edit `src/widgets/widgets.py`:
   ```python
   class MyWidget(Widget):
       def get_value(self) -> str:
           return "My Value"
   ```

2. Register in `web/app.py`:
   ```python
   {
       'id': 'my_widget',
       'name': 'My Widget',
       'icon': '🎯',
       'description': 'Description',
       'config_key': 'my_widget'
   }
   ```

3. Update `src/dashboard.py` to create and render widget

### Modifying Web Interface

- **HTML**: `web/templates/index.html`
- **CSS**: `web/static/css/style.css`
- **JavaScript**: `web/static/js/app.js`
- **Backend**: `web/app.py`

## Files Removed

Cleaned up unnecessary files:
- ❌ Multiple markdown files (consolidated to README.md + SETUP.md)
- ❌ Root directory clutter (moved to organized folders)
- ❌ Duplicate examples (kept one in docs/)

## What's New

✅ **Clean folder structure** with logical organization
✅ **Web-based configuration** with drag-and-drop
✅ **Single README.md** for main documentation
✅ **Organized scripts** in dedicated folder
✅ **Separated concerns** (core, widgets, web, scripts)
✅ **Professional layout** ready for GitHub

## Updating After Code Changes

When you modify the code, use the update script:

```bash
sudo ./scripts/update.sh
```

**Options:**
1. **Python code only** - Updates dashboard, widgets, drivers
2. **Web interface only** - Updates HTML, CSS, JS
3. **Everything** - Updates all files
4. **Just restart** - Restarts services without copying files

**Quick update (most common):**
```bash
cd s1-display-linux-driver
sudo ./scripts/update.sh
# Pull from git? y (if updating from repository)
# Choose 1 (Python code only)
# Choose 3 (Restart both services)
```

**Note:** The script will automatically backup your `config.yaml` before pulling from git.

**Manual update:**
```bash
# Copy files
sudo cp -r src/* /opt/s1-display/src/
sudo cp -r web/* /opt/s1-display/web/

# Restart services
sudo systemctl restart s1-dashboard.service
sudo systemctl restart s1-web.service
```

## Next Steps

1. Install on hecate using instructions above
2. Access web interface at `http://hecate:5000`
3. Drag widgets to configure display
4. Save and enjoy!
