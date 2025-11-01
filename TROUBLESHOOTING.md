# Troubleshooting Guide

## Quick Diagnosis

Run the diagnostic tool to identify the issue:

```bash
python3 diagnose.py
```

This will check:
1. USB device detection
2. HID permissions
3. HID enumeration
4. Device open capability

## Common Issues

### Issue 1: "Permission denied" or "open failed"

This is the most common issue. The HID device requires special permissions.

**Quick Fix (works immediately):**
```bash
sudo python3 test_display.py
```

**Permanent Fix (recommended):**
```bash
sudo chmod +x fix-permissions.sh
sudo ./fix-permissions.sh
```

Then **unplug and replug the device** (or reboot).

After that, run without sudo:
```bash
python3 diagnose.py
```

### Issue 2: "No devices found"

Check if the device is connected:

```bash
lsusb | grep 04d9
```

You should see:
```
Bus XXX Device XXX: ID 04d9:fd01 Holtek Semiconductor, Inc.
```

If you don't see it:
- Check physical USB connection
- Try a different USB port
- Check if device is powered on
- Look for USB errors: `dmesg | tail -50`

### Issue 3: "hidapi not found"

Install the Python HID library:

```bash
# On Ubuntu/Debian
sudo apt-get install python3-pip libhidapi-hidraw0 libhidapi-libusb0
pip3 install hidapi

# Or with --break-system-packages on newer Ubuntu
pip3 install hidapi --break-system-packages
```

### Issue 4: Wrong interface selected

The S1 has two HID interfaces:
- **Interface 0**: Consumer control (usage_page 0x0C) - NOT what we want
- **Interface 1**: Vendor-defined - This is the display

The driver automatically skips the consumer control interface.

Run `diagnose.py` to see which interfaces are detected.

### Issue 5: Display shows garbled output

This usually means:
1. Wrong orientation - make sure it's set to landscape (0x01)
2. Endianness issue with RGB565 colors
3. Packet size mismatch

Try the test script:
```bash
sudo python3 test_display.py
```

This will show colored rectangles if working correctly.

## Manual Permission Setup

If the automatic fix doesn't work, try these steps:

### Method 1: udev rules (recommended)

```bash
# Copy udev rules
sudo cp 99-s1-display.rules /etc/udev/rules.d/

# Reload rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Unplug and replug device
# OR reboot
```

### Method 2: Add user to plugdev group

```bash
# Add your user to plugdev group
sudo usermod -a -G plugdev $USER

# Log out and log back in for group to take effect
# OR run: newgrp plugdev
```

### Method 3: Chmod the hidraw device (temporary)

```bash
# Find the device
ls -la /dev/hidraw*

# Look for one owned by root with mode 600
# Then change permissions (TEMPORARY - resets on reboot/replug)
sudo chmod 666 /dev/hidraw0  # adjust number as needed
```

## Checking Permissions

See what's blocking access:

```bash
# List all hidraw devices
ls -la /dev/hidraw*

# Should show something like:
# crw-rw-rw- 1 root plugdev ... /dev/hidrawX

# Check your groups
groups

# You should see 'plugdev' in the list
```

## Still Not Working?

1. **Check dmesg for USB errors:**
   ```bash
   dmesg | grep -i usb | tail -20
   ```

2. **Verify HID driver is loaded:**
   ```bash
   lsmod | grep hid
   ```

3. **Check USB device details:**
   ```bash
   lsusb -v -d 04d9:fd01
   ```

4. **Try a different USB port**
   - Some USB3 ports have compatibility issues
   - Try USB2 ports

5. **Check if another program is using the device**
   ```bash
   lsof | grep hidraw
   ```

## Platform-Specific Issues

### Ubuntu 24.04+ (with externally-managed-environment)

If you get an error about externally-managed-environment:

```bash
pip3 install hidapi --break-system-packages
```

Or use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install hidapi
```

### Raspberry Pi

Same as Ubuntu, but you might need:
```bash
sudo apt-get install python3-dev libusb-1.0-0-dev libudev-dev
```

### Arch Linux

```bash
sudo pacman -S python-hid
```

## Getting More Help

If none of this works, run the diagnostic and share the output:

```bash
python3 diagnose.py > diagnosis.txt 2>&1
```

Then review `diagnosis.txt` for clues.

## Success!

Once working, you should see:

```
AceMagic S1 Display Test Suite
========================================
Test 1: Testing connection...
  ✓ Successfully connected to display

Test 2: Testing orientation...
  ✓ Set to landscape orientation

Test 3: Testing color display...
  Testing Red...
  Testing Green...
  Testing Blue...
  Testing White...
  Testing Black...
  ✓ Color test complete

...
```

Then you can run the time display:
```bash
sudo python3 time_display.py
```

Or install as a service:
```bash
sudo ./install.sh
```
