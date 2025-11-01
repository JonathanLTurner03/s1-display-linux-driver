#!/usr/bin/env python3
"""
Test script for S1 Display
Performs basic tests to verify display is working
"""

import time
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from core.s1_display import S1Display


def test_connection():
    """Test basic connection to display"""
    print("Test 1: Testing connection...")
    with S1Display() as display:
        if display.device:
            print("  ✓ Successfully connected to display")
            return True
        else:
            print("  ✗ Failed to connect to display")
            return False


def test_orientation():
    """Test orientation setting"""
    print("\nTest 2: Testing orientation...")
    with S1Display() as display:
        if not display.device:
            print("  ✗ Display not connected")
            return False

        display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        time.sleep(0.1)
        print("  ✓ Set to landscape orientation")
        return True


def test_clear_colors():
    """Test clearing display to different colors"""
    print("\nTest 3: Testing color display...")
    with S1Display() as display:
        if not display.device:
            print("  ✗ Display not connected")
            return False

        display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        time.sleep(0.1)

        colors = [
            ("Red", 255, 0, 0),
            ("Green", 0, 255, 0),
            ("Blue", 0, 0, 255),
            ("White", 255, 255, 255),
            ("Black", 0, 0, 0)
        ]

        for name, r, g, b in colors:
            print(f"  Testing {name}...")
            display.clear(r, g, b)
            display.update_display()
            time.sleep(1)

        print("  ✓ Color test complete")
        return True


def test_rectangle():
    """Test drawing rectangles"""
    print("\nTest 4: Testing rectangle drawing...")
    with S1Display() as display:
        if not display.device:
            print("  ✗ Display not connected")
            return False

        display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        time.sleep(0.1)

        # Clear to black
        display.clear(0, 0, 0)

        # Draw colored rectangles
        display.fill_rect(10, 10, 50, 50, 255, 0, 0)    # Red
        display.fill_rect(70, 10, 50, 50, 0, 255, 0)    # Green
        display.fill_rect(130, 10, 50, 50, 0, 0, 255)   # Blue
        display.fill_rect(190, 10, 50, 50, 255, 255, 0) # Yellow
        display.fill_rect(250, 10, 50, 50, 255, 0, 255) # Magenta

        display.update_display()
        print("  ✓ Rectangle drawing test complete")
        time.sleep(3)
        return True


def test_heartbeat():
    """Test heartbeat functionality"""
    print("\nTest 5: Testing heartbeat...")
    with S1Display() as display:
        if not display.device:
            print("  ✗ Display not connected")
            return False

        for i in range(3):
            display.send_heartbeat()
            print(f"  Sent heartbeat {i+1}/3")
            time.sleep(1)

        print("  ✓ Heartbeat test complete")
        return True


def main():
    """Run all tests"""
    print("AceMagic S1 Display Test Suite")
    print("=" * 40)

    tests = [
        test_connection,
        test_orientation,
        test_clear_colors,
        test_rectangle,
        test_heartbeat
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
            failed += 1

    print("\n" + "=" * 40)
    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n✓ All tests passed! Display is working correctly.")
    else:
        print(f"\n✗ {failed} test(s) failed. Check the errors above.")


if __name__ == "__main__":
    main()
