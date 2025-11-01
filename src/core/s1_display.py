#!/usr/bin/env python3
"""
AceMagic S1 TFT Display Driver
Controls the 320x170 RGB565 display via USB HID
"""

import hid
import struct
import time
from typing import List, Tuple


class S1Display:
    """Driver for AceMagic S1 TFT LCD Display"""

    # Device identification
    VID = 0x04D9
    PID = 0xFD01

    # Orientation constants
    ORIENTATION_LANDSCAPE = 0x01
    ORIENTATION_PORTRAIT = 0x02

    # Display dimensions (landscape mode)
    WIDTH = 320
    HEIGHT = 170

    # Command codes
    CMD_SET_ORIENTATION = (0xA1, 0xF1)
    CMD_SET_TIME = (0xA1, 0xF2)
    CMD_HEARTBEAT = (0xA1, 0xF3)
    CMD_PARTIAL_UPDATE = (0xA2, 0xF0)
    CMD_FULL_REDRAW_START = (0xA3, 0xF0)
    CMD_FULL_REDRAW_CONTINUE = (0xA3, 0xF1)
    CMD_FULL_REDRAW_END = (0xA3, 0xF2)

    # Packet size
    HEADER_SIZE = 8
    DATA_SIZE = 4096
    PACKET_SIZE = HEADER_SIZE + DATA_SIZE

    def __init__(self):
        """Initialize connection to S1 display"""
        self.device = None
        self.framebuffer = [0] * (self.WIDTH * self.HEIGHT)

    def connect(self) -> bool:
        """Connect to the S1 display device"""
        try:
            # Enumerate all matching devices
            devices = hid.enumerate(self.VID, self.PID)

            if not devices:
                print(f"No devices found with VID={hex(self.VID)}, PID={hex(self.PID)}")
                print("\nTroubleshooting:")
                print("1. Check if device is connected: lsusb | grep 04d9:fd01")
                print("2. You may need to run with sudo")
                print("3. Or install udev rules (see 99-s1-display.rules)")
                return False

            print(f"Found {len(devices)} device interface(s)")

            # Try each interface
            for idx, dev in enumerate(devices):
                print(f"\nInterface {idx}:")
                print(f"  Path: {dev['path']}")
                print(f"  Manufacturer: {dev['manufacturer_string']}")
                print(f"  Product: {dev['product_string']}")
                print(f"  Usage Page: {hex(dev['usage_page'])}")
                print(f"  Usage: {hex(dev['usage'])}")
                print(f"  Interface: {dev['interface_number']}")

                # Skip consumer control interface (usage_page 0x0C)
                # We want the vendor-defined interface
                if dev['usage_page'] == 0x0C:
                    print("  -> Skipping (consumer control interface)")
                    continue

                # Try to open this interface
                try:
                    print("  -> Attempting to open...")
                    self.device = hid.device()
                    self.device.open_path(dev['path'])
                    print(f"  -> Successfully opened!")
                    print(f"\nConnected to S1 Display: {dev['product_string']}")
                    return True
                except Exception as open_error:
                    print(f"  -> Failed to open: {open_error}")
                    self.device = None
                    continue

            print("\nFailed to open any suitable interface")
            print("\nIf you see 'Permission denied' errors:")
            print("1. Run with sudo: sudo python3 test_display.py")
            print("2. Or install udev rules: sudo cp 99-s1-display.rules /etc/udev/rules.d/")
            return False

        except Exception as e:
            print(f"Error during device enumeration: {e}")
            import traceback
            traceback.print_exc()
            return False

    def disconnect(self):
        """Disconnect from the device"""
        if self.device:
            self.device.close()
            self.device = None

    def _create_packet(self, cmd: Tuple[int, int], params: List[int] = None) -> bytearray:
        """Create a command packet with header and data payload"""
        packet = bytearray(self.PACKET_SIZE)

        # Header: signature (0x55) + command bytes
        packet[0] = 0x55
        packet[1] = cmd[0]
        packet[2] = cmd[1]

        # Add parameters if provided
        if params:
            for i, param in enumerate(params[:5]):  # Max 5 param bytes
                packet[3 + i] = param

        return packet

    def _send_packet(self, packet: bytearray) -> bool:
        """Send a packet to the device"""
        try:
            if self.device:
                # HID write requires prepending report ID (0x00)
                self.device.write(bytes([0x00]) + packet)
                return True
            return False
        except Exception as e:
            print(f"Error sending packet: {e}")
            return False

    def set_orientation(self, orientation: int = ORIENTATION_LANDSCAPE):
        """Set display orientation (0x01 = landscape, 0x02 = portrait)"""
        packet = self._create_packet(self.CMD_SET_ORIENTATION, [orientation])
        self._send_packet(packet)

    def send_heartbeat(self):
        """Send heartbeat to maintain internal clock and animations"""
        current_time = time.localtime()
        params = [
            current_time.tm_year % 100,  # Year (2 digits)
            current_time.tm_mon,          # Month
            current_time.tm_mday,         # Day
            current_time.tm_hour,         # Hour
            current_time.tm_min           # Minute
        ]
        packet = self._create_packet(self.CMD_HEARTBEAT, params)
        self._send_packet(packet)

    @staticmethod
    def rgb565(r: int, g: int, b: int) -> int:
        """Convert RGB888 to RGB565 with endian swap"""
        # Convert 8-bit RGB to 5-6-5 format
        r5 = (r >> 3) & 0x1F
        g6 = (g >> 2) & 0x3F
        b5 = (b >> 3) & 0x1F

        # Combine into 16-bit value
        rgb = (r5 << 11) | (g6 << 5) | b5

        # Swap endianness
        return ((rgb >> 8) | (rgb << 8)) & 0xFFFF

    def clear(self, r: int = 0, g: int = 0, b: int = 0):
        """Clear framebuffer to specified color"""
        color = self.rgb565(r, g, b)
        self.framebuffer = [color] * (self.WIDTH * self.HEIGHT)

    def set_pixel(self, x: int, y: int, r: int, g: int, b: int):
        """Set a pixel in the framebuffer"""
        if 0 <= x < self.WIDTH and 0 <= y < self.HEIGHT:
            color = self.rgb565(r, g, b)
            self.framebuffer[y * self.WIDTH + x] = color

    def fill_rect(self, x: int, y: int, width: int, height: int, r: int, g: int, b: int):
        """Fill a rectangle in the framebuffer"""
        color = self.rgb565(r, g, b)
        for py in range(y, min(y + height, self.HEIGHT)):
            for px in range(x, min(x + width, self.WIDTH)):
                self.framebuffer[py * self.WIDTH + px] = color

    def update_display(self):
        """Send full framebuffer to display using full redraw"""
        # Send framebuffer in chunks
        # Each packet can hold 2048 pixels (4096 bytes / 2 bytes per pixel)
        pixels_per_packet = self.DATA_SIZE // 2
        total_pixels = self.WIDTH * self.HEIGHT
        num_packets = (total_pixels + pixels_per_packet - 1) // pixels_per_packet

        for packet_idx in range(num_packets):
            # Determine command type based on position
            if packet_idx == 0:
                cmd = self.CMD_FULL_REDRAW_START
            elif packet_idx == num_packets - 1:
                cmd = self.CMD_FULL_REDRAW_END
            else:
                cmd = self.CMD_FULL_REDRAW_CONTINUE

            # Create packet
            packet = self._create_packet(cmd)

            # Fill data portion with pixel data
            start_pixel = packet_idx * pixels_per_packet
            end_pixel = min(start_pixel + pixels_per_packet, total_pixels)

            data_offset = self.HEADER_SIZE
            for pixel_idx in range(start_pixel, end_pixel):
                color = self.framebuffer[pixel_idx]
                # Pack as little-endian 16-bit value
                packet[data_offset] = color & 0xFF
                packet[data_offset + 1] = (color >> 8) & 0xFF
                data_offset += 2

            # Send packet
            self._send_packet(packet)
            time.sleep(0.01)  # Small delay between packets

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
