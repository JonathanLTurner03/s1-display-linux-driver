#!/usr/bin/env python3
"""
Web GUI for S1 Display Configuration
Provides drag-and-drop interface for configuring widgets
"""

from flask import Flask, render_template, request, jsonify
import yaml
import os
import subprocess
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

app = Flask(__name__)

CONFIG_PATH = '/opt/s1-display/config.yaml'
LOCAL_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')

# Use local config if deployed version doesn't exist
ACTIVE_CONFIG_PATH = CONFIG_PATH if os.path.exists(CONFIG_PATH) else LOCAL_CONFIG_PATH


def load_config():
    """Load current configuration"""
    try:
        with open(ACTIVE_CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return get_default_config()


def save_config(config):
    """Save configuration to file"""
    try:
        with open(ACTIVE_CONFIG_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def get_default_config():
    """Return default configuration"""
    return {
        'display': {
            'orientation': 'landscape',
            'background_color': [0, 0, 0],
            'update_interval': 1
        },
        'time': {
            'enabled': True,
            'format': '24h',
            'show_seconds': False,
            'color': [255, 255, 255]
        },
        'date': {
            'enabled': False,
            'format': '%a %b %d',
            'color': [200, 200, 200]
        },
        'hostname': {
            'enabled': False,
            'color': [100, 200, 255],
            'prefix': 'Host: '
        },
        'network': {
            'local_ip': {
                'enabled': False,
                'color': [100, 255, 100],
                'prefix': 'LAN: '
            },
            'tailscale_ip': {
                'enabled': False,
                'color': [200, 100, 255],
                'prefix': 'TS: '
            },
            'public_ip': {
                'enabled': False,
                'color': [255, 200, 100],
                'prefix': 'WAN: ',
                'update_interval': 300
            }
        },
        'system': {
            'cpu_usage': {
                'enabled': False,
                'color': [255, 255, 100],
                'show_bar': True
            },
            'memory_usage': {
                'enabled': False,
                'color': [100, 255, 255],
                'show_bar': True
            },
            'disk_usage': {
                'enabled': False,
                'color': [255, 100, 255],
                'path': '/'
            },
            'temperature': {
                'enabled': False,
                'color': [255, 150, 0]
            }
        },
        'servers': [],
        'custom_text': []
    }


@app.route('/')
def index():
    """Main configuration page"""
    config = load_config()
    return render_template('index.html', config=config)


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    config = load_config()
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        config = request.json
        if save_config(config):
            return jsonify({'success': True, 'message': 'Configuration saved'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save configuration'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/restart', methods=['POST'])
def restart_service():
    """Restart the dashboard service"""
    try:
        # Try to restart the service
        result = subprocess.run(
            ['sudo', 'systemctl', 'restart', 's1-dashboard.service'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return jsonify({'success': True, 'message': 'Service restarted'})
        else:
            return jsonify({'success': False, 'message': f'Failed to restart: {result.stderr}'}), 500
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'message': 'Restart command timed out'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get service status"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 's1-dashboard.service'],
            capture_output=True,
            text=True,
            timeout=2
        )

        is_active = result.stdout.strip() == 'active'

        return jsonify({
            'running': is_active,
            'status': result.stdout.strip()
        })
    except Exception as e:
        return jsonify({
            'running': False,
            'status': 'unknown',
            'error': str(e)
        })


@app.route('/api/widgets', methods=['GET'])
def get_available_widgets():
    """Get list of available widgets"""
    widgets = [
        {
            'id': 'time',
            'name': 'Time',
            'icon': '⏰',
            'description': 'Current time display',
            'config_key': 'time'
        },
        {
            'id': 'date',
            'name': 'Date',
            'icon': '📅',
            'description': 'Current date',
            'config_key': 'date'
        },
        {
            'id': 'hostname',
            'name': 'Hostname',
            'icon': '🖥️',
            'description': 'System hostname',
            'config_key': 'hostname'
        },
        {
            'id': 'local_ip',
            'name': 'Local IP',
            'icon': '🌐',
            'description': 'LAN IP address',
            'config_key': 'network.local_ip'
        },
        {
            'id': 'tailscale_ip',
            'name': 'Tailscale IP',
            'icon': '🔐',
            'description': 'Tailscale VPN IP',
            'config_key': 'network.tailscale_ip'
        },
        {
            'id': 'public_ip',
            'name': 'Public IP',
            'icon': '🌍',
            'description': 'WAN IP address',
            'config_key': 'network.public_ip'
        },
        {
            'id': 'cpu_usage',
            'name': 'CPU Usage',
            'icon': '📊',
            'description': 'CPU percentage',
            'config_key': 'system.cpu_usage'
        },
        {
            'id': 'memory_usage',
            'name': 'Memory Usage',
            'icon': '💾',
            'description': 'RAM percentage',
            'config_key': 'system.memory_usage'
        },
        {
            'id': 'disk_usage',
            'name': 'Disk Usage',
            'icon': '💿',
            'description': 'Disk space usage',
            'config_key': 'system.disk_usage'
        },
        {
            'id': 'temperature',
            'name': 'Temperature',
            'icon': '🌡️',
            'description': 'System temperature',
            'config_key': 'system.temperature'
        }
    ]

    return jsonify(widgets)


if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
