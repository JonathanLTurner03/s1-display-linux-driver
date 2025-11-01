# AceMagic S1 Time Display for Ubuntu Linux

A custom display driver that shows the current time on the AceMagic S1's 320x170 TFT display in horizontal (landscape) configuration.

## Features

- Large, easy-to-read digital clock display
- Horizontal (landscape) orientation optimized for the S1 display
- 24-hour time format
- Updates every minute
- Runs as a systemd service for automatic startup
- Black background with white text for minimal power consumption

## Hardware Requirements

- AceMagic S1 Mini PC with TFT display
- Ubuntu Linux (tested on Ubuntu 20.04+)
- USB HID access to the display device (VID: 0x04D9, PID: 0xFD01)

## Installation

### Quick Install

Run the automated installation script:

```bash
sudo chmod +x install.sh
sudo ./install.sh
```

This will:
1. Install system dependencies (libhidapi)
2. Install Python dependencies (hidapi)
3. Copy files to `/opt/s1-display/`
4. Install and start the systemd service

### Manual Installation

If you prefer manual installation:

1. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip libhidapi-hidraw0 libhidapi-libusb0
   sudo pip3 install -r requirements.txt
   ```

2. **Copy files:**
   ```bash
   sudo mkdir -p /opt/s1-display
   sudo cp s1_display.py /opt/s1-display/
   sudo cp time_display.py /opt/s1-display/
   sudo chmod +x /opt/s1-display/time_display.py
   ```

3. **Install service:**
   ```bash
   sudo cp s1-time-display.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable s1-time-display.service
   sudo systemctl start s1-time-display.service
   ```

## Usage

### Running Manually

To test the display without installing the service:

```bash
sudo python3 time_display.py
```

Press `Ctrl+C` to exit. The display will be cleared automatically.

### Service Management

After installation, the service runs automatically at boot:

```bash
# View status
sudo systemctl status s1-time-display.service

# View live logs
sudo journalctl -u s1-time-display.service -f

# Stop the service
sudo systemctl stop s1-time-display.service

# Start the service
sudo systemctl start s1-time-display.service

# Restart the service
sudo systemctl restart s1-time-display.service

# Disable auto-start
sudo systemctl disable s1-time-display.service
```

## Customization

### Changing Time Format

Edit [time_display.py](time_display.py) and modify the `draw_time()` call in the `main()` function:

```python
# 24-hour format (default)
time_renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=255, b=255)

# 12-hour format
time_renderer.draw_time(hour_24=False, show_seconds=False, r=255, g=255, b=255)

# Show seconds
time_renderer.draw_time(hour_24=True, show_seconds=True, r=255, g=255, b=255)
```

### Changing Colors

Modify the RGB values (0-255) in the `draw_time()` call:

```python
# White (default)
time_renderer.draw_time(r=255, g=255, b=255)

# Green
time_renderer.draw_time(r=0, g=255, b=0)

# Cyan
time_renderer.draw_time(r=0, g=255, b=255)

# Red
time_renderer.draw_time(r=255, g=0, b=0)
```

### Changing Background Color

Modify the `clear()` call in `main()`:

```python
# Black background (default)
display.clear(0, 0, 0)

# Dark blue background
display.clear(0, 0, 30)

# Dark gray background
display.clear(20, 20, 20)
```

### Adjusting Digit Size

Edit [time_display.py](time_display.py) and modify the `TimeDisplay` initialization:

```python
# Default size
time_renderer = TimeDisplay(display)
time_renderer.digit_scale = 8  # Scale factor (try 6-10)
time_renderer.digit_spacing = 4  # Space between digits
```

## Architecture

### Files

- **[s1_display.py](s1_display.py)** - Low-level driver for S1 display communication
  - USB HID protocol implementation
  - RGB565 framebuffer management
  - Orientation and heartbeat handling

- **[time_display.py](time_display.py)** - Time display application
  - 7-segment digit rendering
  - Time formatting and display logic
  - Main application loop

- **[s1-time-display.service](s1-time-display.service)** - Systemd service file
- **[install.sh](install.sh)** - Automated installation script
- **[requirements.txt](requirements.txt)** - Python dependencies

### How It Works

1. **Connection**: Opens USB HID connection to the S1 display (VID: 0x04D9, PID: 0xFD01)
2. **Orientation**: Sets display to landscape mode (320x170 pixels)
3. **Rendering**: Draws large 7-segment style digits in a framebuffer
4. **Transfer**: Sends framebuffer to display using full redraw command (27 packets)
5. **Heartbeat**: Sends time sync every second to maintain display internal clock
6. **Updates**: Refreshes display every minute when time changes

## Troubleshooting

### Permission Denied

If you get permission errors, you may need to run with `sudo` or add a udev rule:

```bash
# Create udev rule
sudo nano /etc/udev/rules.d/99-s1-display.rules
```

Add this line:
```
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="04d9", ATTRS{idProduct}=="fd01", MODE="0666"
```

Then reload udev:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Display Not Found

Check if the device is connected:
```bash
lsusb | grep 04d9:fd01
```

You should see:
```
Bus XXX Device XXX: ID 04d9:fd01 Holtek Semiconductor, Inc.
```

### Service Won't Start

Check the service logs for errors:
```bash
sudo journalctl -u s1-time-display.service -n 50
```

Common issues:
- Missing dependencies: Run `sudo pip3 install -r requirements.txt`
- Wrong paths in service file: Verify files exist in `/opt/s1-display/`
- Device permissions: Try adding the udev rule above

## Credits

Based on reverse engineering work by [tjaworski](https://github.com/tjaworski/AceMagic-S1-LED-TFT-Linux) who documented the S1 display protocol.

## License

This project is provided as-is for educational and personal use.
