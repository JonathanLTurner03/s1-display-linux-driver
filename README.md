# AceMagic S1 Display Driver

Custom display driver for the AceMagic S1's 320×170 TFT display with web-based configuration interface.

## Features

### 🎨 Web Configuration Interface
- **Drag-and-drop** widget builder
- **Live preview** of display layout
- **Visual editor** for colors and settings
- **One-click** save and restart
- Accessible from any device on your network

### 📊 Display Modes
- **Simple Clock** - Large time display
- **Advanced Dashboard** - Customizable widgets with system stats, network info, and server monitoring

### 🔧 Available Widgets
- ⏰ Time (12/24 hour format)
- 📅 Date (customizable format)
- 🖥️ Hostname
- 🌐 Local IP, Tailscale IP, Public IP
- 📊 CPU, Memory, Disk usage (with progress bars)
- 🌡️ System temperature
- 🖧 Server monitoring (ping/TCP check)

## Quick Start

### 1. Installation

```bash
cd s1-display-linux-driver
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

### 2. Access Web Interface

Open your browser and navigate to:
```
http://your-machine-ip:5000
```

For example: `http://192.168.1.100:5000` or `http://hecate:5000`

### 3. Configure Display

1. **Drag widgets** from the left panel to the display preview
2. **Click widgets** to customize colors and settings
3. **Add servers** to monitor using the "Add Server Monitor" button
4. **Save configuration** and restart the service

## Web Interface Usage

### Adding Widgets

1. Drag any widget from the **Available Widgets** panel
2. Drop it onto the **Display Preview**
3. Widget is automatically enabled

### Customizing Widgets

1. Click a widget on the display to select it
2. Use the **Widget Properties** panel on the right to:
   - Change colors
   - Modify prefix text
   - Toggle progress bars
   - Adjust settings

### Server Monitoring

1. Click **"Add Server Monitor"**
2. Enter:
   - Server name
   - Host/IP address
   - Port (optional, for TCP check)
   - Check interval
   - Online/offline colors
3. Click **"Add Server"**

### Saving Changes

- **Save Config** - Saves configuration to disk
- **Save & Restart** - Saves and restarts the dashboard service

## Manual Configuration

Edit `config.yaml` directly if preferred:

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
    prefix: "LAN: "

servers:
  - name: "Router"
    host: "192.168.1.1"
    enabled: true
    check_interval: 10
```

After editing:
```bash
sudo systemctl restart s1-dashboard.service
```

## Project Structure

```
s1-display-linux-driver/
├── src/                    # Python source code
│   ├── core/              # Core display driver
│   │   ├── s1_display.py  # USB HID driver
│   │   └── fonts.py       # Bitmap fonts
│   ├── widgets/           # Widget implementations
│   │   └── widgets.py
│   ├── dashboard.py       # Dashboard application
│   ├── time_display.py    # Simple clock application
│   ├── diagnose.py        # Diagnostic tool
│   └── test_display.py    # Hardware tests
├── web/                   # Web interface
│   ├── app.py            # Flask application
│   ├── templates/        # HTML templates
│   │   └── index.html
│   └── static/           # CSS and JavaScript
│       ├── css/style.css
│       └── js/app.js
├── scripts/              # Installation scripts
│   ├── install.sh
│   ├── fix-permissions.sh
│   ├── 99-s1-display.rules
│   ├── s1-dashboard.service
│   └── s1-time-display.service
├── docs/                 # Documentation
│   └── examples.py
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Service Management

### Dashboard Service

```bash
# View status
sudo systemctl status s1-dashboard.service

# View logs
sudo journalctl -u s1-dashboard.service -f

# Restart
sudo systemctl restart s1-dashboard.service

# Stop/Start
sudo systemctl stop s1-dashboard.service
sudo systemctl start s1-dashboard.service
```

### Web Interface Service

The web interface can be run as a separate service or manually:

```bash
# Run manually
cd web
python3 app.py

# Access at http://localhost:5000
```

## Troubleshooting

### Permission Denied

```bash
sudo ./scripts/fix-permissions.sh
# Then unplug/replug device or reboot
```

### Diagnostic Tool

```bash
cd src
python3 diagnose.py
```

### Check Device

```bash
lsusb | grep 04d9:fd01
```

Should show:
```
Bus XXX Device XXX: ID 04d9:fd01 Holtek Semiconductor, Inc.
```

### Web Interface Not Accessible

1. Check if Flask is running:
   ```bash
   ps aux | grep app.py
   ```

2. Check firewall:
   ```bash
   sudo ufw allow 5000
   ```

3. Verify you're using the correct IP:
   ```bash
   ip addr show
   ```

### Widget Shows "N/A"

- **Tailscale IP**: Tailscale not installed or running
- **Public IP**: No internet connection or curl not installed
- **Temperature**: No temperature sensors available
- **Server**: Host unreachable or incorrect host/port

### Service Won't Start

```bash
# Check logs
sudo journalctl -u s1-dashboard.service -n 50

# Common issues:
# - Missing dependencies: pip3 install -r requirements.txt --break-system-packages
# - Wrong paths: verify files in /opt/s1-display/
# - Device permissions: run fix-permissions.sh
```

## Advanced Usage

### Running Web Interface on Boot

Create systemd service:

```bash
sudo nano /etc/systemd/system/s1-web.service
```

Add:
```ini
[Unit]
Description=S1 Display Web Interface
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/s1-display/web
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable s1-web.service
sudo systemctl start s1-web.service
```

### Custom Widget Development

Add new widgets by editing `src/widgets/widgets.py`:

```python
class CustomWidget(Widget):
    def get_value(self) -> str:
        # Your logic here
        return "Custom Value"
```

Register in `web/app.py`:
```python
{
    'id': 'custom',
    'name': 'Custom Widget',
    'icon': '🎯',
    'description': 'My custom widget',
    'config_key': 'custom'
}
```

## Hardware Requirements

- AceMagic S1 Mini PC with TFT display
- Ubuntu Linux 20.04+ (tested on 22.04 and 24.04)
- USB HID device access (VID: 0x04D9, PID: 0xFD01)

## Software Dependencies

- Python 3.8+
- hidapi
- psutil
- PyYAML
- Flask

Installed automatically via `requirements.txt`.

## Performance

- **CPU Usage**: <1% for dashboard, <0.5% for web interface
- **Memory**: ~50MB for dashboard, ~30MB for web interface
- **Network**: Minimal (only if public_ip widget enabled)
- **Update Frequency**: Configurable (default: 1 second)

## Architecture

### Display Communication
1. USB HID connection (VID:0x04D9, PID:0xFD01)
2. RGB565 framebuffer (320×170 pixels)
3. Heartbeat every second for time sync
4. Full screen redraw via 27 HID packets

### Web Interface
1. Flask web server on port 5000
2. RESTful API for config management
3. Drag-and-drop interface with live preview
4. AJAX updates for status and config changes

### Widget System
1. Base widget class with caching and update intervals
2. Modular widget implementations
3. Auto-layout system for display rendering
4. YAML-based configuration

## Credits

Based on reverse engineering by [tjaworski](https://github.com/tjaworski/AceMagic-S1-LED-TFT-Linux).

## License

Provided as-is for educational and personal use.

## Support

For issues, feature requests, or questions, please check:
1. The troubleshooting section above
2. Run the diagnostic tool: `python3 src/diagnose.py`
3. Check service logs: `sudo journalctl -u s1-dashboard.service -f`
