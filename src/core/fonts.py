#!/usr/bin/env python3
"""
Font rendering for S1 Display
Includes multiple font sizes for different information density
"""

# Small 3x5 font (compact, good for labels and info)
FONT_3X5 = {
    'A': ["111", "101", "111", "101", "101"],
    'B': ["110", "101", "110", "101", "110"],
    'C': ["111", "100", "100", "100", "111"],
    'D': ["110", "101", "101", "101", "110"],
    'E': ["111", "100", "110", "100", "111"],
    'F': ["111", "100", "110", "100", "100"],
    'G': ["111", "100", "101", "101", "111"],
    'H': ["101", "101", "111", "101", "101"],
    'I': ["111", "010", "010", "010", "111"],
    'J': ["111", "001", "001", "101", "111"],
    'K': ["101", "110", "100", "110", "101"],
    'L': ["100", "100", "100", "100", "111"],
    'M': ["101", "111", "111", "101", "101"],
    'N': ["101", "111", "111", "111", "101"],
    'O': ["111", "101", "101", "101", "111"],
    'P': ["111", "101", "111", "100", "100"],
    'Q': ["111", "101", "101", "111", "001"],
    'R': ["111", "101", "110", "101", "101"],
    'S': ["111", "100", "111", "001", "111"],
    'T': ["111", "010", "010", "010", "010"],
    'U': ["101", "101", "101", "101", "111"],
    'V': ["101", "101", "101", "101", "010"],
    'W': ["101", "101", "111", "111", "101"],
    'X': ["101", "101", "010", "101", "101"],
    'Y': ["101", "101", "010", "010", "010"],
    'Z': ["111", "001", "010", "100", "111"],
    '0': ["111", "101", "101", "101", "111"],
    '1': ["010", "110", "010", "010", "111"],
    '2': ["111", "001", "111", "100", "111"],
    '3': ["111", "001", "111", "001", "111"],
    '4': ["101", "101", "111", "001", "001"],
    '5': ["111", "100", "111", "001", "111"],
    '6': ["111", "100", "111", "101", "111"],
    '7': ["111", "001", "010", "010", "010"],
    '8': ["111", "101", "111", "101", "111"],
    '9': ["111", "101", "111", "001", "111"],
    ':': ["000", "010", "000", "010", "000"],
    '.': ["000", "000", "000", "000", "010"],
    '-': ["000", "000", "111", "000", "000"],
    '_': ["000", "000", "000", "000", "111"],
    '/': ["001", "001", "010", "100", "100"],
    ' ': ["000", "000", "000", "000", "000"],
    '(': ["010", "100", "100", "100", "010"],
    ')': ["010", "001", "001", "001", "010"],
    '%': ["101", "001", "010", "100", "101"],
    '*': ["000", "101", "010", "101", "000"],
}


# Medium 5x7 font (balanced, good for main content)
FONT_5X7 = {
    # This is the same as the original DIGIT_PATTERNS but extended
    '0': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': [" ### ", "#   #", "    #", "  ## ", "    #", "#   #", " ### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#    ", "#### ", "    #", "#   #", " ### "],
    '6': [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    ':': ["     ", "  #  ", "  #  ", "     ", "  #  ", "  #  ", "     "],
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ### "],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"],
    '-': ["     ", "     ", "#####", "     ", "     ", "     ", "     "],
    '.': ["     ", "     ", "     ", "     ", "     ", "  #  ", "  #  "],
    '/': ["    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "],
}


class FontRenderer:
    """Renders text using bitmap fonts"""

    def __init__(self, display):
        self.display = display

    def draw_char_3x5(self, x: int, y: int, char: str, r: int, g: int, b: int, scale: int = 1):
        """Draw a 3x5 character"""
        char = char.upper()
        if char not in FONT_3X5:
            char = ' '

        pattern = FONT_3X5[char]
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == '1':
                    px = x + (col_idx * scale)
                    py = y + (row_idx * scale)
                    self.display.fill_rect(px, py, scale, scale, r, g, b)

    def draw_char_5x7(self, x: int, y: int, char: str, r: int, g: int, b: int, scale: int = 1):
        """Draw a 5x7 character"""
        char = char.upper()
        if char not in FONT_5X7:
            char = ' '

        pattern = FONT_5X7[char]
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == '#':
                    px = x + (col_idx * scale)
                    py = y + (row_idx * scale)
                    self.display.fill_rect(px, py, scale, scale, r, g, b)

    def draw_text_3x5(self, x: int, y: int, text: str, r: int, g: int, b: int, scale: int = 1):
        """Draw text using 3x5 font"""
        current_x = x
        char_width = 3 * scale
        spacing = 1 * scale

        for char in text:
            self.draw_char_3x5(current_x, y, char, r, g, b, scale)
            current_x += char_width + spacing

        return current_x

    def draw_text_5x7(self, x: int, y: int, text: str, r: int, g: int, b: int, scale: int = 1):
        """Draw text using 5x7 font"""
        current_x = x
        char_width = 5 * scale
        spacing = 1 * scale

        for char in text:
            self.draw_char_5x7(current_x, y, char, r, g, b, scale)
            current_x += char_width + spacing

        return current_x

    def measure_text_3x5(self, text: str, scale: int = 1) -> int:
        """Get width of text in pixels"""
        char_width = 3 * scale
        spacing = 1 * scale
        return len(text) * (char_width + spacing) - spacing

    def measure_text_5x7(self, text: str, scale: int = 1) -> int:
        """Get width of text in pixels"""
        char_width = 5 * scale
        spacing = 1 * scale
        return len(text) * (char_width + spacing) - spacing

    def draw_text_centered_3x5(self, y: int, text: str, r: int, g: int, b: int, scale: int = 1):
        """Draw centered text using 3x5 font"""
        width = self.measure_text_3x5(text, scale)
        x = (self.display.WIDTH - width) // 2
        self.draw_text_3x5(x, y, text, r, g, b, scale)

    def draw_text_centered_5x7(self, y: int, text: str, r: int, g: int, b: int, scale: int = 1):
        """Draw centered text using 5x7 font"""
        width = self.measure_text_5x7(text, scale)
        x = (self.display.WIDTH - width) // 2
        self.draw_text_5x7(x, y, text, r, g, b, scale)

    def draw_progress_bar(self, x: int, y: int, width: int, height: int,
                         percentage: float, fg_color: tuple, bg_color: tuple = (50, 50, 50)):
        """Draw a progress bar"""
        # Draw background
        self.display.fill_rect(x, y, width, height, *bg_color)

        # Draw fill
        fill_width = int(width * (percentage / 100.0))
        if fill_width > 0:
            self.display.fill_rect(x, y, fill_width, height, *fg_color)

        # Draw border
        border_color = (100, 100, 100)
        # Top
        self.display.fill_rect(x, y, width, 1, *border_color)
        # Bottom
        self.display.fill_rect(x, y + height - 1, width, 1, *border_color)
        # Left
        self.display.fill_rect(x, y, 1, height, *border_color)
        # Right
        self.display.fill_rect(x + width - 1, y, 1, height, *border_color)
