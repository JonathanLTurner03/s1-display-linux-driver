#!/usr/bin/env python3
"""
Advanced Dashboard for AceMagic S1 Display
Shows customizable widgets with system info, network, monitoring, etc.
"""

import time
import yaml
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from core.s1_display import S1Display
from core.fonts import FontRenderer
from widgets.widgets import (
    TimeWidget, DateWidget, HostnameWidget,
    LocalIPWidget, TailscaleIPWidget, PublicIPWidget,
    CPUUsageWidget, MemoryUsageWidget, DiskUsageWidget,
    TemperatureWidget, ServerMonitorWidget, CustomTextWidget
)


class Dashboard:
    """Main dashboard manager"""

    def __init__(self, config_file='config.yaml'):
        self.config = self.load_config(config_file)
        self.display = None
        self.font = None
        self.widgets = []
        self.layout_y = 5  # Current Y position for auto layout

    def load_config(self, config_file):
        """Load configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using defaults")
            return self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.get_default_config()

    def get_default_config(self):
        """Return default configuration"""
        return {
            'display': {
                'orientation': 'landscape',
                'background_color': [0, 0, 0],
                'update_interval': 1
            },
            'time': {'enabled': True, 'format': '24h', 'show_seconds': False},
            'hostname': {'enabled': True},
            'network': {
                'local_ip': {'enabled': True, 'prefix': 'LAN: '}
            }
        }

    def setup(self):
        """Initialize display and widgets"""
        print("Setting up dashboard...")

        # Connect to display
        self.display = S1Display()
        if not self.display.connect():
            print("Failed to connect to display")
            return False

        # Set orientation
        orientation = self.config.get('display', {}).get('orientation', 'landscape')
        if orientation == 'landscape':
            self.display.set_orientation(S1Display.ORIENTATION_LANDSCAPE)
        else:
            self.display.set_orientation(S1Display.ORIENTATION_PORTRAIT)

        time.sleep(0.1)

        # Initialize font renderer
        self.font = FontRenderer(self.display)

        # Create widgets
        self.create_widgets()

        print(f"Dashboard initialized with {len(self.widgets)} widgets")
        return True

    def create_widgets(self):
        """Create enabled widgets from config"""
        self.widgets = []

        # Time widget
        if self.config.get('time', {}).get('enabled', False):
            self.widgets.append(('time', TimeWidget(self.config['time'], self.font)))

        # Date widget
        if self.config.get('date', {}).get('enabled', False):
            self.widgets.append(('date', DateWidget(self.config['date'], self.font)))

        # Hostname
        if self.config.get('hostname', {}).get('enabled', False):
            self.widgets.append(('hostname', HostnameWidget(self.config['hostname'], self.font)))

        # Network widgets
        network_cfg = self.config.get('network', {})

        if network_cfg.get('local_ip', {}).get('enabled', False):
            self.widgets.append(('local_ip', LocalIPWidget(network_cfg['local_ip'], self.font)))

        if network_cfg.get('tailscale_ip', {}).get('enabled', False):
            self.widgets.append(('tailscale_ip', TailscaleIPWidget(network_cfg['tailscale_ip'], self.font)))

        if network_cfg.get('public_ip', {}).get('enabled', False):
            self.widgets.append(('public_ip', PublicIPWidget(network_cfg['public_ip'], self.font)))

        # System monitoring
        system_cfg = self.config.get('system', {})

        if system_cfg.get('cpu_usage', {}).get('enabled', False):
            self.widgets.append(('cpu', CPUUsageWidget(system_cfg['cpu_usage'], self.font)))

        if system_cfg.get('memory_usage', {}).get('enabled', False):
            self.widgets.append(('memory', MemoryUsageWidget(system_cfg['memory_usage'], self.font)))

        if system_cfg.get('disk_usage', {}).get('enabled', False):
            self.widgets.append(('disk', DiskUsageWidget(system_cfg['disk_usage'], self.font)))

        if system_cfg.get('temperature', {}).get('enabled', False):
            self.widgets.append(('temp', TemperatureWidget(system_cfg['temperature'], self.font)))

        # Server monitoring
        servers = self.config.get('servers', [])
        for server_cfg in servers:
            if server_cfg.get('enabled', False):
                name = server_cfg.get('name', 'Server')
                self.widgets.append((f'server_{name}', ServerMonitorWidget(server_cfg, self.font)))

        # Custom text
        custom_texts = self.config.get('custom_text', [])
        for idx, text_cfg in enumerate(custom_texts):
            if text_cfg.get('enabled', False):
                self.widgets.append((f'custom_{idx}', CustomTextWidget(text_cfg, self.font)))

    def render(self):
        """Render all widgets to display"""
        # Clear display
        bg_color = self.config.get('display', {}).get('background_color', [0, 0, 0])
        self.display.clear(*bg_color)

        # Reset layout position
        self.layout_y = 5
        line_spacing = self.config.get('layout', {}).get('line_spacing', 2)
        padding = self.config.get('layout', {}).get('padding', 5)

        # Render each widget
        for name, widget in self.widgets:
            text = widget.get_display_text()
            if not text:
                continue

            color = widget.get_color()

            # Get font scale from widget config
            font_scale = widget.get_font_scale()

            # Handle special rendering for certain widgets
            if name == 'time':
                # Large time at top center (use configured scale or default to 6)
                time_scale = font_scale if font_scale > 2 else 6
                self.font.draw_text_centered_5x7(self.layout_y, text, *color, scale=time_scale)
                self.layout_y += (7 * time_scale) + line_spacing + 3
            elif name == 'date':
                # Centered date (use configured scale or default to 2)
                date_scale = font_scale if font_scale <= 3 else 2
                self.font.draw_text_centered_3x5(self.layout_y, text, *color, scale=date_scale)
                self.layout_y += (5 * date_scale) + line_spacing + 3
            elif name in ['cpu', 'memory']:
                # System widgets with progress bars
                self.font.draw_text_3x5(padding, self.layout_y, text, *color, scale=font_scale)

                if hasattr(widget, 'get_usage_percent') and widget.show_bar:
                    # Draw progress bar
                    bar_x = padding + (40 * font_scale)
                    bar_y = self.layout_y
                    bar_width = 60
                    bar_height = max(8, font_scale * 4)
                    percent = widget.get_usage_percent()
                    self.font.draw_progress_bar(bar_x, bar_y, bar_width, bar_height,
                                                percent, color)

                self.layout_y += (5 * font_scale) + line_spacing
            else:
                # Regular text with configurable scale
                self.font.draw_text_3x5(padding, self.layout_y, text, *color, scale=font_scale)
                self.layout_y += (5 * font_scale) + line_spacing

        # Update display
        self.display.update_display()

    def run(self):
        """Main dashboard loop"""
        if not self.setup():
            return

        update_interval = self.config.get('display', {}).get('update_interval', 1)
        last_render = 0

        print("Dashboard running (Ctrl+C to exit)...")

        try:
            while True:
                # Send heartbeat
                self.display.send_heartbeat()

                # Render if enough time has passed
                current_time = time.time()
                if (current_time - last_render) >= update_interval:
                    self.render()
                    last_render = current_time

                    # Debug output
                    widget_summary = ', '.join([name for name, _ in self.widgets[:5]])
                    if len(self.widgets) > 5:
                        widget_summary += f', ... ({len(self.widgets)} total)'
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Updated - Widgets: {widget_summary}")

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nStopping dashboard...")
            self.cleanup()

    def cleanup(self):
        """Clean up and disconnect"""
        if self.display:
            bg_color = self.config.get('display', {}).get('background_color', [0, 0, 0])
            self.display.clear(*bg_color)
            self.display.update_display()
            self.display.disconnect()
        print("Dashboard stopped")


def main():
    """Entry point"""
    config_file = 'config.yaml'
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    print(f"AceMagic S1 Dashboard")
    print(f"Using config: {config_file}")
    print()

    dashboard = Dashboard(config_file)
    dashboard.run()


if __name__ == "__main__":
    main()
