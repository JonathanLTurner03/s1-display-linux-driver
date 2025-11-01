# Quick Start Guide

Get your S1 display showing the time in under 5 minutes!

## Prerequisites

- AceMagic S1 Mini PC running Ubuntu Linux
- Internet connection for downloading dependencies
- Terminal access with sudo privileges

## Installation Steps

### 1. Download or Clone This Repository

If you have git:
```bash
git clone <repository-url>
cd s1-display-linux-driver
```

Or download and extract the files to a directory.

### 2. Make Install Script Executable

```bash
chmod +x install.sh
```

### 3. Run Installation

```bash
sudo ./install.sh
```

The script will:
- Install required system packages
- Install Python dependencies
- Copy files to `/opt/s1-display/`
- Set up and start the systemd service

### 4. Verify It's Working

Your display should now show the current time!

Check the service status:
```bash
sudo systemctl status s1-time-display.service
```

You should see: `Active: active (running)`

## Testing Before Installation

Want to test before installing as a service?

### 1. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip libhidapi-hidraw0 libhidapi-libusb0
sudo pip3 install hidapi
```

### 2. Run Test Suite

```bash
sudo python3 test_display.py
```

This will test all display functions with colored squares and verify connectivity.

### 3. Run Time Display

```bash
sudo python3 time_display.py
```

Press `Ctrl+C` to stop.

## What You'll See

- **Black background** - Minimizes power and looks clean
- **Large white digits** - Easy to read from a distance
- **24-hour format** - Shows hours and minutes (e.g., "14:35")
- **Updates every minute** - No unnecessary refreshes

## Next Steps

- **Customize**: Edit the colors, size, or format (see [README.md](README.md#customization))
- **Monitor**: View logs with `sudo journalctl -u s1-time-display.service -f`
- **Control**: Start/stop the service as needed

## Troubleshooting

**Display not found?**
```bash
lsusb | grep 04d9:fd01
```
Should show: `ID 04d9:fd01 Holtek Semiconductor, Inc.`

**Permission errors?**
Make sure you're running with `sudo` or add the udev rule from [README.md](README.md#permission-denied)

**Service won't start?**
```bash
sudo journalctl -u s1-time-display.service -n 50
```
This shows the last 50 log lines with error messages.

## Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Review the [test_display.py](test_display.py) output for hardware issues
- Verify USB connection with `lsusb`

Enjoy your new time display!
