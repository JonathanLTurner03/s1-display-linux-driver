#!/usr/bin/env python3
"""
Diagnostic tool for S1 Display connection issues
Run this to troubleshoot connection problems
"""

import hid
import sys
import os

# No display imports needed for diagnostics


def check_usb_device():
    """Check if USB device is visible"""
    print("=" * 60)
    print("1. Checking USB Device Detection")
    print("=" * 60)

    print("\nRunning: lsusb | grep 04d9")
    result = os.system("lsusb | grep 04d9")

    if result != 0:
        print("\n⚠ Device NOT found via lsusb")
        print("  - Is the S1 mini PC connected and powered on?")
        print("  - Try: lsusb (to see all USB devices)")
        return False
    else:
        print("\n✓ Device found via lsusb")
        return True


def check_hid_permissions():
    """Check HID device permissions"""
    print("\n" + "=" * 60)
    print("2. Checking HID Device Permissions")
    print("=" * 60)

    print("\nLooking for /dev/hidraw* devices...")
    os.system("ls -la /dev/hidraw* 2>/dev/null | head -10")

    print("\nChecking ownership and permissions...")
    print("If you see 'crw-------' (mode 600), only root can access")
    print("If you see 'crw-rw-rw-' (mode 666), everyone can access")

    print("\nYour user groups:")
    os.system("groups")


def check_hid_enumeration():
    """Check if HID library can enumerate device"""
    print("\n" + "=" * 60)
    print("3. Checking HID Library Enumeration")
    print("=" * 60)

    VID = 0x04D9
    PID = 0xFD01

    print(f"\nSearching for VID={hex(VID)}, PID={hex(PID)}...")

    try:
        devices = hid.enumerate(VID, PID)

        if not devices:
            print("✗ No HID devices found with this VID/PID")
            print("\nPossible issues:")
            print("  1. Device not connected")
            print("  2. Wrong VID/PID")
            print("  3. Driver/permission issues")
            return False

        print(f"✓ Found {len(devices)} HID interface(s)\n")

        for idx, dev in enumerate(devices):
            print(f"Interface {idx}:")
            print(f"  Path: {dev['path']}")
            print(f"  Manufacturer: {dev['manufacturer_string']}")
            print(f"  Product: {dev['product_string']}")
            print(f"  Serial: {dev['serial_number']}")
            print(f"  VID:PID: {hex(dev['vendor_id'])}:{hex(dev['product_id'])}")
            print(f"  Release: {dev['release_number']}")
            print(f"  Interface: {dev['interface_number']}")
            print(f"  Usage Page: {hex(dev['usage_page'])}")
            print(f"  Usage: {hex(dev['usage'])}")
            print()

        return True

    except Exception as e:
        print(f"✗ Error during enumeration: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_hid_open():
    """Try to open HID device"""
    print("=" * 60)
    print("4. Attempting to Open HID Device")
    print("=" * 60)

    VID = 0x04D9
    PID = 0xFD01

    try:
        devices = hid.enumerate(VID, PID)

        if not devices:
            print("✗ No devices to open")
            return False

        for idx, dev in enumerate(devices):
            print(f"\nTrying interface {idx} (usage_page={hex(dev['usage_page'])})...")
            print(f"  Path: {dev['path']}")

            try:
                h = hid.device()
                h.open_path(dev['path'])
                print(f"  ✓ Successfully opened!")

                # Try to get device info
                print(f"  Manufacturer: {h.get_manufacturer_string()}")
                print(f"  Product: {h.get_product_string()}")

                h.close()
                print(f"  ✓ Successfully closed")

            except PermissionError as e:
                print(f"  ✗ Permission denied: {e}")
                print(f"     → Run with sudo, or install udev rules")
                return False

            except Exception as e:
                print(f"  ✗ Failed to open: {e}")
                continue

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_recommendations():
    """Print recommendations based on findings"""
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)

    print("\nIf you're getting 'Permission denied' errors:")
    print("\nOption 1: Run with sudo (quick test)")
    print("  sudo python3 test_display.py")

    print("\nOption 2: Install udev rules (permanent fix)")
    print("  sudo cp 99-s1-display.rules /etc/udev/rules.d/")
    print("  sudo udevadm control --reload-rules")
    print("  sudo udevadm trigger")
    print("  # Then unplug/replug device or reboot")

    print("\nOption 3: Add user to plugdev group")
    print("  sudo usermod -a -G plugdev $USER")
    print("  # Then log out and log back in")

    print("\nIf device is not found at all:")
    print("  - Check physical connection")
    print("  - Try different USB port")
    print("  - Check dmesg for USB errors: dmesg | tail -50")


def main():
    print("AceMagic S1 Display - Diagnostic Tool")
    print()

    # Check if running as root
    if os.geteuid() == 0:
        print("ℹ Running as root (sudo)")
    else:
        print("ℹ Running as regular user")

    print()

    # Run checks
    usb_ok = check_usb_device()
    check_hid_permissions()
    enum_ok = check_hid_enumeration()
    open_ok = check_hid_open()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"USB Device Detected: {'✓' if usb_ok else '✗'}")
    print(f"HID Enumeration: {'✓' if enum_ok else '✗'}")
    print(f"HID Device Open: {'✓' if open_ok else '✗'}")

    if usb_ok and enum_ok and open_ok:
        print("\n✓ All checks passed! The display should work.")
    else:
        print_recommendations()


if __name__ == "__main__":
    main()
