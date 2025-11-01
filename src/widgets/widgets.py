#!/usr/bin/env python3
"""
Widget system for S1 Display
Modular information display components
"""

import socket
import subprocess
import time
import psutil
import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class Widget(ABC):
    """Base class for display widgets"""

    def __init__(self, config: dict, font_renderer):
        self.config = config
        self.font = font_renderer
        self.last_update = 0
        self.cached_value = None
        self.update_interval = config.get('update_interval', 1)

    @abstractmethod
    def get_value(self) -> str:
        """Get the current value to display"""
        pass

    def should_update(self) -> bool:
        """Check if widget should update"""
        return (time.time() - self.last_update) >= self.update_interval

    def update(self):
        """Update cached value if needed"""
        if self.should_update():
            self.cached_value = self.get_value()
            self.last_update = time.time()

    def get_display_text(self) -> str:
        """Get text to display (with prefix if configured)"""
        self.update()
        prefix = self.config.get('prefix', '')
        return f"{prefix}{self.cached_value}" if self.cached_value else ""

    def get_color(self) -> Tuple[int, int, int]:
        """Get RGB color for this widget"""
        color = self.config.get('color', [255, 255, 255])
        return tuple(color)


class TimeWidget(Widget):
    """Display current time"""

    def get_value(self) -> str:
        now = datetime.now()
        fmt = self.config.get('format', '24h')
        show_seconds = self.config.get('show_seconds', False)

        if fmt == '24h':
            if show_seconds:
                return now.strftime("%H:%M:%S")
            return now.strftime("%H:%M")
        else:  # 12h
            if show_seconds:
                return now.strftime("%I:%M:%S %p")
            return now.strftime("%I:%M %p")


class DateWidget(Widget):
    """Display current date"""

    def get_value(self) -> str:
        fmt = self.config.get('format', '%a %b %d')
        return datetime.now().strftime(fmt)


class HostnameWidget(Widget):
    """Display hostname"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 3600  # Update once per hour

    def get_value(self) -> str:
        return socket.gethostname()


class LocalIPWidget(Widget):
    """Display local IP address"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 30  # Update every 30 seconds

    def get_value(self) -> str:
        interface = self.config.get('interface', 'auto')

        try:
            if interface == 'auto':
                # Get primary interface IP
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
                return ip
            else:
                # Get specific interface
                addrs = psutil.net_if_addrs()
                if interface in addrs:
                    for addr in addrs[interface]:
                        if addr.family == socket.AF_INET:
                            return addr.address
                return "N/A"
        except Exception:
            return "N/A"


class TailscaleIPWidget(Widget):
    """Display Tailscale IP address"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 30

    def get_value(self) -> str:
        try:
            # Try to get tailscale0 interface
            addrs = psutil.net_if_addrs()
            if 'tailscale0' in addrs:
                for addr in addrs['tailscale0']:
                    if addr.family == socket.AF_INET:
                        return addr.address

            # Alternative: use tailscale ip command
            result = subprocess.run(['tailscale', 'ip', '-4'],
                                  capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                return result.stdout.strip()

            return "N/A"
        except Exception:
            return "N/A"


class PublicIPWidget(Widget):
    """Display public IP address"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = config.get('update_interval', 300)  # 5 minutes default

    def get_value(self) -> str:
        try:
            result = subprocess.run(['curl', '-s', '--max-time', '3', 'ifconfig.me'],
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                ip = result.stdout.strip()
                if ip and '.' in ip:
                    return ip
            return "N/A"
        except Exception:
            return "N/A"


class CPUUsageWidget(Widget):
    """Display CPU usage"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 2
        self.show_bar = config.get('show_bar', True)

    def get_value(self) -> str:
        try:
            usage = psutil.cpu_percent(interval=0.1)
            return f"{int(usage)}%"
        except Exception:
            return "N/A"

    def get_usage_percent(self) -> float:
        """Get usage as percentage for progress bar"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0.0


class MemoryUsageWidget(Widget):
    """Display memory usage"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 2
        self.show_bar = config.get('show_bar', True)

    def get_value(self) -> str:
        try:
            mem = psutil.virtual_memory()
            return f"{int(mem.percent)}%"
        except Exception:
            return "N/A"

    def get_usage_percent(self) -> float:
        """Get usage as percentage for progress bar"""
        try:
            return psutil.virtual_memory().percent
        except Exception:
            return 0.0


class DiskUsageWidget(Widget):
    """Display disk usage"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 60
        self.path = config.get('path', '/')

    def get_value(self) -> str:
        try:
            usage = psutil.disk_usage(self.path)
            return f"{int(usage.percent)}%"
        except Exception:
            return "N/A"


class TemperatureWidget(Widget):
    """Display system temperature"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.update_interval = 5
        self.source = config.get('source', 'auto')

    def get_value(self) -> str:
        try:
            if self.source == 'auto':
                # Try psutil first
                temps = psutil.sensors_temperatures()
                if temps:
                    # Get first available temperature
                    for name, entries in temps.items():
                        if entries:
                            return f"{int(entries[0].current)}C"

            # Try reading from thermal zone
            thermal_file = '/sys/class/thermal/thermal_zone0/temp'
            if os.path.exists(thermal_file):
                with open(thermal_file, 'r') as f:
                    temp = int(f.read().strip()) / 1000
                    return f"{int(temp)}C"

            return "N/A"
        except Exception:
            return "N/A"


class ServerMonitorWidget(Widget):
    """Monitor server availability"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.name = config.get('name', 'Server')
        self.host = config.get('host')
        self.port = config.get('port', None)
        self.update_interval = config.get('check_interval', 10)
        self.is_online = False
        self.color_online = tuple(config.get('color_online', [0, 255, 0]))
        self.color_offline = tuple(config.get('color_offline', [255, 0, 0]))

    def get_value(self) -> str:
        if not self.host:
            return f"{self.name}: N/A"

        try:
            if self.port:
                # Try TCP connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.host, self.port))
                sock.close()
                self.is_online = (result == 0)
            else:
                # Use ping
                result = subprocess.run(['ping', '-c', '1', '-W', '2', self.host],
                                      capture_output=True, timeout=3)
                self.is_online = (result.returncode == 0)

            status = "UP" if self.is_online else "DOWN"
            return f"{self.name}: {status}"
        except Exception:
            self.is_online = False
            return f"{self.name}: ERR"

    def get_color(self) -> Tuple[int, int, int]:
        """Return color based on online status"""
        return self.color_online if self.is_online else self.color_offline


class CustomTextWidget(Widget):
    """Display custom static text"""

    def __init__(self, config: dict, font_renderer):
        super().__init__(config, font_renderer)
        self.text = config.get('text', '')

    def get_value(self) -> str:
        return self.text
