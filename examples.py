#!/usr/bin/env python3
"""
Examples of different displays you can create with the S1 Display
Run this file to cycle through various time display styles
"""

import time
from datetime import datetime
from s1_display import S1Display
from time_display import TimeDisplay


def example_basic_white(display, renderer):
    """Basic white time on black background"""
    print("Example 1: Basic white time on black")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=255, b=255)
    display.update_display()
    time.sleep(5)


def example_with_seconds(display, renderer):
    """Time with seconds"""
    print("Example 2: Time with seconds")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=True, r=255, g=255, b=255)
    display.update_display()
    time.sleep(5)


def example_12_hour(display, renderer):
    """12-hour format"""
    print("Example 3: 12-hour format")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=False, show_seconds=False, r=255, g=255, b=255)
    display.update_display()
    time.sleep(5)


def example_green_matrix(display, renderer):
    """Green on black (matrix style)"""
    print("Example 4: Green matrix style")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=False, r=0, g=255, b=0)
    display.update_display()
    time.sleep(5)


def example_cyan_futuristic(display, renderer):
    """Cyan on dark blue (futuristic)"""
    print("Example 5: Cyan futuristic style")
    display.clear(0, 0, 30)  # Dark blue background
    renderer.draw_time(hour_24=True, show_seconds=False, r=0, g=255, b=255)
    display.update_display()
    time.sleep(5)


def example_amber_retro(display, renderer):
    """Amber/orange on black (retro terminal)"""
    print("Example 6: Amber retro terminal style")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=180, b=0)
    display.update_display()
    time.sleep(5)


def example_red_alarm(display, renderer):
    """Red on black (alarm clock style)"""
    print("Example 7: Red alarm clock style")
    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=0, b=0)
    display.update_display()
    time.sleep(5)


def example_purple_neon(display, renderer):
    """Purple/magenta (neon style)"""
    print("Example 8: Purple neon style")
    display.clear(10, 0, 20)  # Dark purple background
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=0, b=255)
    display.update_display()
    time.sleep(5)


def example_small_digits(display, renderer):
    """Smaller digits"""
    print("Example 9: Smaller digits")
    original_scale = renderer.digit_scale
    original_spacing = renderer.digit_spacing

    renderer.digit_scale = 6
    renderer.digit_spacing = 3

    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=True, r=255, g=255, b=255)
    display.update_display()

    # Restore original size
    renderer.digit_scale = original_scale
    renderer.digit_spacing = original_spacing
    time.sleep(5)


def example_large_digits(display, renderer):
    """Larger digits"""
    print("Example 10: Larger digits")
    original_scale = renderer.digit_scale
    original_spacing = renderer.digit_spacing

    renderer.digit_scale = 10
    renderer.digit_spacing = 5

    display.clear(0, 0, 0)
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=255, b=255)
    display.update_display()

    # Restore original size
    renderer.digit_scale = original_scale
    renderer.digit_spacing = original_spacing
    time.sleep(5)


def example_gradient_background(display, renderer):
    """Time with gradient background"""
    print("Example 11: Gradient background")

    # Create horizontal gradient
    for y in range(display.HEIGHT):
        # Fade from dark blue to black
        blue = int(40 * (1 - y / display.HEIGHT))
        for x in range(display.WIDTH):
            display.set_pixel(x, y, 0, 0, blue)

    # Draw time
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=255, b=255)
    display.update_display()
    time.sleep(5)


def example_color_border(display, renderer):
    """Time with colored border"""
    print("Example 12: Colored border")

    # Clear to black
    display.clear(0, 0, 0)

    # Draw rainbow border
    border_width = 5
    colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]

    # Top border
    for i, (r, g, b) in enumerate(colors):
        x_start = i * (display.WIDTH // len(colors))
        x_end = (i + 1) * (display.WIDTH // len(colors))
        display.fill_rect(x_start, 0, x_end - x_start, border_width, r, g, b)

    # Bottom border
    for i, (r, g, b) in enumerate(colors):
        x_start = i * (display.WIDTH // len(colors))
        x_end = (i + 1) * (display.WIDTH // len(colors))
        display.fill_rect(x_start, display.HEIGHT - border_width,
                         x_end - x_start, border_width, r, g, b)

    # Left and right borders
    display.fill_rect(0, 0, border_width, display.HEIGHT, 255, 0, 0)
    display.fill_rect(display.WIDTH - border_width, 0, border_width,
                     display.HEIGHT, 148, 0, 211)

    # Draw time
    renderer.draw_time(hour_24=True, show_seconds=False, r=255, g=255, b=255)
    display.update_display()
    time.sleep(5)


def main():
    """Run all examples"""
    print("S1 Display Examples")
    print("Cycling through different display styles...")
    print("Press Ctrl+C to exit\n")

    with S1Display() as display:
        if not display.device:
            print("Failed to connect to display")
            return

        # Set to landscape orientation
        display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        time.sleep(0.1)

        # Create renderer
        renderer = TimeDisplay(display)

        examples = [
            example_basic_white,
            example_with_seconds,
            example_12_hour,
            example_green_matrix,
            example_cyan_futuristic,
            example_amber_retro,
            example_red_alarm,
            example_purple_neon,
            example_small_digits,
            example_large_digits,
            example_gradient_background,
            example_color_border
        ]

        try:
            # Run examples in a loop
            while True:
                for example_func in examples:
                    example_func(display, renderer)
                    display.send_heartbeat()

                print("\nRestarting examples loop...\n")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            display.clear(0, 0, 0)
            display.update_display()
            print("Display cleared.")


if __name__ == "__main__":
    main()
