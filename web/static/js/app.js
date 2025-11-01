// S1 Display Configuration - JavaScript

let config = {};
let availableWidgets = [];
let selectedWidget = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadAvailableWidgets();
    checkStatus();
    setupEventListeners();

    // Check status every 10 seconds
    setInterval(checkStatus, 10000);
});

// Load configuration from server
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        config = await response.json();
        renderDisplay();
        updateDisplaySettings();
    } catch (error) {
        showToast('Failed to load configuration', 'error');
    }
}

// Load available widgets
async function loadAvailableWidgets() {
    try {
        const response = await fetch('/api/widgets');
        availableWidgets = await response.json();
        renderWidgetPalette();
    } catch (error) {
        console.error('Failed to load widgets:', error);
    }
}

// Check service status
async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const status = await response.json();

        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');

        if (status.running) {
            statusDot.className = 'status-dot active';
            statusText.textContent = 'Service Running';
        } else {
            statusDot.className = 'status-dot inactive';
            statusText.textContent = 'Service Stopped';
        }
    } catch (error) {
        const statusDot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        statusDot.className = 'status-dot';
        statusText.textContent = 'Unknown';
    }
}

// Render widget palette
function renderWidgetPalette() {
    const widgetList = document.getElementById('widget-list');
    widgetList.innerHTML = '';

    availableWidgets.forEach(widget => {
        const widgetItem = document.createElement('div');
        widgetItem.className = 'widget-item';
        widgetItem.draggable = true;
        widgetItem.dataset.widgetId = widget.id;
        widgetItem.dataset.configKey = widget.config_key;

        widgetItem.innerHTML = `
            <div class="widget-icon">${widget.icon}</div>
            <div class="widget-info">
                <div class="widget-name">${widget.name}</div>
                <div class="widget-description">${widget.description}</div>
            </div>
        `;

        widgetItem.addEventListener('dragstart', handleDragStart);
        widgetItem.addEventListener('dragend', handleDragEnd);

        widgetList.appendChild(widgetItem);
    });
}

// Render display with enabled widgets
function renderDisplay() {
    const container = document.getElementById('widget-container');
    const dropHint = document.getElementById('drop-hint');
    container.innerHTML = '';

    let hasWidgets = false;
    let yOffset = 10;

    // Render enabled widgets
    if (config.time && config.time.enabled) {
        addPlacedWidget('time', 'Time', yOffset);
        yOffset += 60;
        hasWidgets = true;
    }

    if (config.date && config.date.enabled) {
        addPlacedWidget('date', 'Date', yOffset);
        yOffset += 30;
        hasWidgets = true;
    }

    if (config.hostname && config.hostname.enabled) {
        addPlacedWidget('hostname', 'Hostname', yOffset);
        yOffset += 30;
        hasWidgets = true;
    }

    if (config.network) {
        if (config.network.local_ip && config.network.local_ip.enabled) {
            addPlacedWidget('local_ip', 'Local IP', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
        if (config.network.tailscale_ip && config.network.tailscale_ip.enabled) {
            addPlacedWidget('tailscale_ip', 'Tailscale IP', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
        if (config.network.public_ip && config.network.public_ip.enabled) {
            addPlacedWidget('public_ip', 'Public IP', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
    }

    if (config.system) {
        if (config.system.cpu_usage && config.system.cpu_usage.enabled) {
            addPlacedWidget('cpu_usage', 'CPU Usage', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
        if (config.system.memory_usage && config.system.memory_usage.enabled) {
            addPlacedWidget('memory_usage', 'Memory Usage', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
        if (config.system.disk_usage && config.system.disk_usage.enabled) {
            addPlacedWidget('disk_usage', 'Disk Usage', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
        if (config.system.temperature && config.system.temperature.enabled) {
            addPlacedWidget('temperature', 'Temperature', yOffset);
            yOffset += 30;
            hasWidgets = true;
        }
    }

    // Render servers
    if (config.servers && config.servers.length > 0) {
        config.servers.forEach((server, idx) => {
            if (server.enabled) {
                addPlacedWidget(`server_${idx}`, server.name, yOffset);
                yOffset += 30;
                hasWidgets = true;
            }
        });
    }

    dropHint.style.display = hasWidgets ? 'none' : 'block';
}

// Add a placed widget to the display
function addPlacedWidget(id, name, yOffset) {
    const container = document.getElementById('widget-container');
    const widget = document.createElement('div');
    widget.className = 'placed-widget';
    widget.dataset.widgetId = id;
    widget.style.top = yOffset + 'px';
    widget.style.left = '10px';

    const widgetInfo = availableWidgets.find(w => w.id === id);
    const icon = widgetInfo ? widgetInfo.icon : '📌';

    widget.innerHTML = `
        <div class="widget-label">
            <span>${icon}</span>
            <span>${name}</span>
        </div>
        <div class="widget-remove" onclick="removeWidget('${id}')">×</div>
    `;

    widget.addEventListener('click', () => selectWidget(id));

    container.appendChild(widget);
}

// Setup event listeners
function setupEventListeners() {
    const displayScreen = document.getElementById('display-screen');

    // Drag and drop
    displayScreen.addEventListener('dragover', handleDragOver);
    displayScreen.addEventListener('drop', handleDrop);
    displayScreen.addEventListener('dragleave', handleDragLeave);

    // Buttons
    document.getElementById('save-btn').addEventListener('click', saveConfig);
    document.getElementById('restart-btn').addEventListener('click', saveAndRestart);
    document.getElementById('clear-all-btn').addEventListener('click', clearAll);
    document.getElementById('add-server-btn').addEventListener('click', () => {
        document.getElementById('server-modal').classList.add('active');
    });

    // Modal
    document.getElementById('close-modal').addEventListener('click', closeServerModal);
    document.getElementById('cancel-server').addEventListener('click', closeServerModal);
    document.getElementById('add-server').addEventListener('click', addServer);

    // Display settings
    document.getElementById('bg-color').addEventListener('input', updateBgColor);
    document.getElementById('update-interval').addEventListener('change', updateInterval);
}

// Drag handlers
function handleDragStart(e) {
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'copy';
    e.dataTransfer.setData('text/plain', this.dataset.widgetId);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    this.classList.remove('drag-over');

    const widgetId = e.dataTransfer.getData('text/plain');
    enableWidget(widgetId);
}

// Enable a widget
function enableWidget(widgetId) {
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);
    if (!widgetInfo) return;

    const keys = widgetInfo.config_key.split('.');
    let target = config;

    for (let i = 0; i < keys.length - 1; i++) {
        if (!target[keys[i]]) target[keys[i]] = {};
        target = target[keys[i]];
    }

    const lastKey = keys[keys.length - 1];
    if (!target[lastKey]) {
        target[lastKey] = { enabled: true };
    } else {
        target[lastKey].enabled = true;
    }

    renderDisplay();
    showToast(`${widgetInfo.name} enabled`);
}

// Remove a widget
function removeWidget(widgetId) {
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);
    if (!widgetInfo) {
        // Check if it's a server
        if (widgetId.startsWith('server_')) {
            const idx = parseInt(widgetId.split('_')[1]);
            if (config.servers && config.servers[idx]) {
                config.servers.splice(idx, 1);
            }
        }
        renderDisplay();
        return;
    }

    const keys = widgetInfo.config_key.split('.');
    let target = config;

    for (let i = 0; i < keys.length - 1; i++) {
        target = target[keys[i]];
    }

    const lastKey = keys[keys.length - 1];
    if (target[lastKey]) {
        target[lastKey].enabled = false;
    }

    renderDisplay();
    showToast(`${widgetInfo.name} removed`);
}

// Select a widget for editing
function selectWidget(widgetId) {
    selectedWidget = widgetId;

    // Highlight selected widget
    document.querySelectorAll('.placed-widget').forEach(w => {
        w.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');

    // Show properties
    showWidgetProperties(widgetId);
}

// Show widget properties panel
function showWidgetProperties(widgetId) {
    const panel = document.getElementById('properties-content');
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);

    if (!widgetInfo) {
        panel.innerHTML = '<p class="no-selection">No properties available</p>';
        return;
    }

    const keys = widgetInfo.config_key.split('.');
    let widgetConfig = config;
    for (const key of keys) {
        widgetConfig = widgetConfig[key];
    }

    let html = `<h3>${widgetInfo.icon} ${widgetInfo.name}</h3>`;

    // Color picker
    if (widgetConfig.color) {
        const color = widgetConfig.color;
        const hexColor = rgbToHex(color[0], color[1], color[2]);
        html += `
            <div class="form-group">
                <label>Color</label>
                <input type="color" value="${hexColor}"
                       onchange="updateWidgetColor('${widgetId}', this.value)">
            </div>
        `;
    }

    // Prefix
    if (widgetConfig.prefix !== undefined) {
        html += `
            <div class="form-group">
                <label>Prefix Text</label>
                <input type="text" value="${widgetConfig.prefix || ''}"
                       onchange="updateWidgetPrefix('${widgetId}', this.value)">
            </div>
        `;
    }

    // Show bar option
    if (widgetConfig.show_bar !== undefined) {
        html += `
            <div class="form-group">
                <label>
                    <input type="checkbox" ${widgetConfig.show_bar ? 'checked' : ''}
                           onchange="updateWidgetShowBar('${widgetId}', this.checked)">
                    Show Progress Bar
                </label>
            </div>
        `;
    }

    panel.innerHTML = html;
}

// Update widget color
function updateWidgetColor(widgetId, hexColor) {
    const rgb = hexToRgb(hexColor);
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);
    if (!widgetInfo) return;

    const keys = widgetInfo.config_key.split('.');
    let target = config;
    for (const key of keys) {
        target = target[key];
    }

    target.color = [rgb.r, rgb.g, rgb.b];
    showToast('Color updated');
}

// Update widget prefix
function updateWidgetPrefix(widgetId, prefix) {
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);
    if (!widgetInfo) return;

    const keys = widgetInfo.config_key.split('.');
    let target = config;
    for (const key of keys) {
        target = target[key];
    }

    target.prefix = prefix;
    showToast('Prefix updated');
}

// Update widget show bar
function updateWidgetShowBar(widgetId, showBar) {
    const widgetInfo = availableWidgets.find(w => w.id === widgetId);
    if (!widgetInfo) return;

    const keys = widgetInfo.config_key.split('.');
    let target = config;
    for (const key of keys) {
        target = target[key];
    }

    target.show_bar = showBar;
    showToast('Setting updated');
}

// Clear all widgets
function clearAll() {
    if (!confirm('Remove all widgets?')) return;

    // Disable all widgets
    if (config.time) config.time.enabled = false;
    if (config.date) config.date.enabled = false;
    if (config.hostname) config.hostname.enabled = false;
    if (config.network) {
        if (config.network.local_ip) config.network.local_ip.enabled = false;
        if (config.network.tailscale_ip) config.network.tailscale_ip.enabled = false;
        if (config.network.public_ip) config.network.public_ip.enabled = false;
    }
    if (config.system) {
        if (config.system.cpu_usage) config.system.cpu_usage.enabled = false;
        if (config.system.memory_usage) config.system.memory_usage.enabled = false;
        if (config.system.disk_usage) config.system.disk_usage.enabled = false;
        if (config.system.temperature) config.system.temperature.enabled = false;
    }
    config.servers = [];

    renderDisplay();
    showToast('All widgets removed');
}

// Save configuration
async function saveConfig() {
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });

        const result = await response.json();
        if (result.success) {
            showToast('Configuration saved', 'success');
        } else {
            showToast('Failed to save: ' + result.message, 'error');
        }
    } catch (error) {
        showToast('Failed to save configuration', 'error');
    }
}

// Save and restart
async function saveAndRestart() {
    await saveConfig();

    try {
        const response = await fetch('/api/restart', {
            method: 'POST'
        });

        const result = await response.json();
        if (result.success) {
            showToast('Service restarted', 'success');
            setTimeout(checkStatus, 2000);
        } else {
            showToast('Failed to restart: ' + result.message, 'error');
        }
    } catch (error) {
        showToast('Failed to restart service', 'error');
    }
}

// Server modal
function closeServerModal() {
    document.getElementById('server-modal').classList.remove('active');
}

function addServer() {
    const name = document.getElementById('server-name').value;
    const host = document.getElementById('server-host').value;
    const port = document.getElementById('server-port').value;
    const interval = parseInt(document.getElementById('server-interval').value);
    const colorOnline = hexToRgb(document.getElementById('server-color-online').value);
    const colorOffline = hexToRgb(document.getElementById('server-color-offline').value);

    if (!name || !host) {
        alert('Please enter server name and host');
        return;
    }

    if (!config.servers) config.servers = [];

    config.servers.push({
        name,
        host,
        port: port ? parseInt(port) : null,
        enabled: true,
        check_interval: interval,
        color_online: [colorOnline.r, colorOnline.g, colorOnline.b],
        color_offline: [colorOffline.r, colorOffline.g, colorOffline.b]
    });

    renderDisplay();
    closeServerModal();
    showToast(`Server ${name} added`);

    // Clear form
    document.getElementById('server-name').value = '';
    document.getElementById('server-host').value = '';
    document.getElementById('server-port').value = '';
}

// Display settings
function updateDisplaySettings() {
    if (config.display) {
        const bgColor = config.display.background_color || [0, 0, 0];
        const hexColor = rgbToHex(bgColor[0], bgColor[1], bgColor[2]);
        document.getElementById('bg-color').value = hexColor;
        document.getElementById('bg-color-text').value = bgColor.join(', ');
        document.getElementById('update-interval').value = config.display.update_interval || 1;
    }
}

function updateBgColor() {
    const hexColor = this.value;
    const rgb = hexToRgb(hexColor);

    if (!config.display) config.display = {};
    config.display.background_color = [rgb.r, rgb.g, rgb.b];

    document.getElementById('bg-color-text').value = `${rgb.r}, ${rgb.g}, ${rgb.b}`;
    document.getElementById('display-screen').style.background = hexColor;
}

function updateInterval() {
    if (!config.display) config.display = {};
    config.display.update_interval = parseInt(this.value);
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const messageEl = document.getElementById('toast-message');

    messageEl.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Color conversion helpers
function rgbToHex(r, g, b) {
    return '#' + [r, g, b].map(x => {
        const hex = x.toString(16);
        return hex.length === 1 ? '0' + hex : hex;
    }).join('');
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 0, g: 0, b: 0 };
}
