#!/usr/bin/env python3
"""
Time Display for AceMagic S1 Display
Shows current time in large format on horizontal display
"""

import time
import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from core.s1_display import S1Display


# 7-segment style digit patterns (5x7 pixels each, scaled up)
# Each digit is represented as a list of rows
DIGIT_PATTERNS = {
    '0': [
        " ### ",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " ### "
    ],
    '1': [
        "  #  ",
        " ##  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        " ### "
    ],
    '2': [
        " ### ",
        "#   #",
        "    #",
        "   # ",
        "  #  ",
        " #   ",
        "#####"
    ],
    '3': [
        " ### ",
        "#   #",
        "    #",
        "  ## ",
        "    #",
        "#   #",
        " ### "
    ],
    '4': [
        "   # ",
        "  ## ",
        " # # ",
        "#  # ",
        "#####",
        "   # ",
        "   # "
    ],
    '5': [
        "#####",
        "#    ",
        "#    ",
        "#### ",
        "    #",
        "#   #",
        " ### "
    ],
    '6': [
        " ### ",
        "#    ",
        "#    ",
        "#### ",
        "#   #",
        "#   #",
        " ### "
    ],
    '7': [
        "#####",
        "    #",
        "   # ",
        "  #  ",
        " #   ",
        " #   ",
        " #   "
    ],
    '8': [
        " ### ",
        "#   #",
        "#   #",
        " ### ",
        "#   #",
        "#   #",
        " ### "
    ],
    '9': [
        " ### ",
        "#   #",
        "#   #",
        " ####",
        "    #",
        "    #",
        " ### "
    ],
    ':': [
        "     ",
        "  #  ",
        "  #  ",
        "     ",
        "  #  ",
        "  #  ",
        "     "
    ],
    ' ': [
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ]
}


class TimeDisplay:
    """Renders time on S1 display"""

    def __init__(self, display: S1Display):
        self.display = display
        self.digit_scale = 8  # Scale factor for digits
        self.digit_spacing = 4  # Space between digits

    def draw_digit(self, x: int, y: int, digit: str, r: int, g: int, b: int):
        """Draw a single scaled digit at position"""
        if digit not in DIGIT_PATTERNS:
            return

        pattern = DIGIT_PATTERNS[digit]
        for row_idx, row in enumerate(pattern):
            for col_idx, char in enumerate(row):
                if char == '#':
                    # Draw scaled pixel block
                    px = x + (col_idx * self.digit_scale)
                    py = y + (row_idx * self.digit_scale)
                    self.display.fill_rect(px, py, self.digit_scale, self.digit_scale, r, g, b)

    def draw_text(self, x: int, y: int, text: str, r: int, g: int, b: int):
        """Draw text string"""
        current_x = x
        digit_width = 5 * self.digit_scale

        for char in text:
            self.draw_digit(current_x, y, char, r, g, b)
            current_x += digit_width + self.digit_spacing

    def get_text_width(self, text: str) -> int:
        """Calculate width of text in pixels"""
        digit_width = 5 * self.digit_scale
        return len(text) * (digit_width + self.digit_spacing) - self.digit_spacing

    def draw_time(self, hour_24: bool = True, show_seconds: bool = False,
                  r: int = 255, g: int = 255, b: int = 255):
        """Draw current time centered on display"""
        now = datetime.now()

        # Format time string
        if hour_24:
            time_str = now.strftime("%H:%M")
        else:
            time_str = now.strftime("%I:%M")

        if show_seconds:
            time_str += now.strftime(":%S")

        # Calculate centering
        text_width = self.get_text_width(time_str)
        text_height = 7 * self.digit_scale

        x = (self.display.WIDTH - text_width) // 2
        y = (self.display.HEIGHT - text_height) // 2

        # Draw the time
        self.draw_text(x, y, time_str, r, g, b)

    def draw_date(self, x: int, y: int, r: int = 200, g: int = 200, b: int = 200):
        """Draw date in small text below time"""
        # For now, use simple pixel font for date
        # This would need a smaller font implementation
        # Placeholder for future enhancement
        pass


def main():
    """Main loop for time display"""
    print("AceMagic S1 Time Display")
    print("Connecting to display...")

    with S1Display() as display:
        if not display.device:
            print("Failed to connect to display")
            return

        # Set to horizontal orientation
        print("Setting landscape orientation...")
        display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        time.sleep(0.1)

        # Initialize time renderer
        time_renderer = TimeDisplay(display)

        print("Starting time display loop (Ctrl+C to exit)...")

        last_minute = -1

        try:
            while True:
                # Send heartbeat every second
                display.send_heartbeat()

                # Check if minute has changed
                current_minute = datetime.now().minute

                if current_minute != last_minute:
                    # Clear display (black background)
                    display.clear(0, 0, 0)

                    # Draw time in white
                    time_renderer.draw_time(
                        hour_24=True,
                        show_seconds=False,
                        r=255, g=255, b=255
                    )

                    # Update display
                    display.update_display()

                    last_minute = current_minute
                    print(f"Updated display: {datetime.now().strftime('%H:%M')}")

                # Wait 1 second before next heartbeat
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping time display...")
            # Clear display before exit
            display.clear(0, 0, 0)
            display.update_display()
            print("Display cleared and disconnected.")


if __name__ == "__main__":
    main()
