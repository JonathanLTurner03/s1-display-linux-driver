# Quick Update Guide

## When You Update Code

After making any code changes, run:

```bash
sudo ./scripts/update.sh
```

### Git Pull (Optional)

If this is a git repository, the script will ask:
```
Pull latest code from git? (y/N):
```

**If you answer 'y':**
- ✅ Your local `config.yaml` is backed up first (timestamped)
- ✅ Code is pulled from git repository
- ✅ Backup ensures your config isn't lost if git overwrites it

**Default is 'N'** - assumes you already pulled or made local changes.

### Update Options

**1. Python code only** (most common)
- Updates: dashboard.py, widgets, fonts, display driver
- Use when: You modified widget logic, dashboard code, or core drivers

**2. Web interface only**
- Updates: HTML, CSS, JavaScript
- Use when: You modified the web UI appearance or functionality

**3. Everything**
- Updates: All Python code + web interface + config
- Use when: You made changes across multiple areas
- Note: Won't overwrite `/opt/s1-display/config.yaml` to preserve your settings

**4. Just restart**
- No file copying, just restarts services
- Use when: You manually copied files or just want to restart

### Quick Examples

**Pulling updates from git:**
```bash
sudo ./scripts/update.sh
# Pull from git? y
# Choose 1 (Python code)
# Choose 3 (Restart both)
```

**You modified widgets.py locally:**
```bash
sudo ./scripts/update.sh
# Pull from git? N (default)
# Choose 1 (Python code)
# Choose 3 (Restart both)
```

**You modified web interface colors:**
```bash
sudo ./scripts/update.sh
# Pull from git? N
# Choose 2 (Web interface)
# Choose 2 (Restart web only)
```

**Pulling everything from git:**
```bash
sudo ./scripts/update.sh
# Pull from git? y
# Choose 3 (Everything)
# Choose 3 (Restart both)
```

## Manual Update (Alternative)

If you prefer manual control:

### Update Python Code
```bash
sudo cp -r src/* /opt/s1-display/src/
sudo systemctl restart s1-dashboard.service
```

### Update Web Interface
```bash
sudo cp -r web/* /opt/s1-display/web/
sudo systemctl restart s1-web.service
```

### Update Config (careful - will overwrite)
```bash
sudo cp config.yaml /opt/s1-display/config.yaml
sudo systemctl restart s1-dashboard.service
```

## Check if Update Worked

### View Dashboard Logs
```bash
sudo journalctl -u s1-dashboard.service -f
```

Should see recent restart timestamp and no errors.

### View Web Interface Logs
```bash
sudo journalctl -u s1-web.service -f
```

### Check Service Status
```bash
sudo systemctl status s1-dashboard.service
sudo systemctl status s1-web.service
```

Both should show `Active: active (running)` in green.

### Test the Display
Look at your S1 display - changes should be visible within seconds.

### Test Web Interface
Open `http://hecate:5000` - should reload with your changes.

## Troubleshooting Updates

### Service won't restart
```bash
# Check for syntax errors
sudo journalctl -u s1-dashboard.service -n 50
```

Look for Python errors like `SyntaxError`, `ImportError`, etc.

### Changes not appearing
```bash
# Verify files were copied
ls -la /opt/s1-display/src/
ls -la /opt/s1-display/web/

# Check timestamps - should be recent
```

### Web changes not showing
Hard refresh your browser: `Ctrl+F5` or `Cmd+Shift+R`

## Development Workflow

1. **Edit code** in your project directory
2. **Test locally** (optional):
   ```bash
   cd src
   sudo python3 dashboard.py
   ```
3. **Run update script**:
   ```bash
   sudo ./scripts/update.sh
   ```
4. **Check logs**:
   ```bash
   sudo journalctl -u s1-dashboard.service -f
   ```
5. **Verify** on display or web interface

## Config File Handling

The update script **preserves your config.yaml** by default:

### Option 1 & 2: Python/Web Updates
- ✅ Config is NOT touched
- Your settings are completely preserved

### Option 3: Everything Update
You'll be asked what to do with config.yaml:

**1. Keep current config (recommended)**
- ✅ Preserves all your settings
- ⚠️ New options (like `show_am_pm`) need to be added manually

**2. Backup and use new template**
- Creates timestamped backup: `config.yaml.backup.20250101_123456`
- ⚠️ Replaces with new template (loses custom settings)
- Need to copy settings from backup

**3. Show differences**
- Shows diff between current and new
- You decide whether to update

### Adding New Config Options

If you kept your config but need new options:

```bash
sudo ./scripts/update-config.sh
```

This helper script will:
- Show differences between configs
- Offer to automatically add new options (like `show_am_pm`)
- Create backups before any changes

**Example: Adding AM/PM support manually**
```bash
sudo nano /opt/s1-display/config.yaml
```

Add under the `time:` section:
```yaml
time:
  enabled: true
  format: 12h
  show_am_pm: true  # Add this line
```

Save and restart:
```bash
sudo systemctl restart s1-dashboard.service
```

## What Files Are Updated

### Python Code Update (Option 1)
- `/opt/s1-display/src/core/s1_display.py`
- `/opt/s1-display/src/core/fonts.py`
- `/opt/s1-display/src/widgets/widgets.py`
- `/opt/s1-display/src/dashboard.py`
- `/opt/s1-display/src/time_display.py`
- `/opt/s1-display/src/diagnose.py`
- `/opt/s1-display/src/test_display.py`

### Web Interface Update (Option 2)
- `/opt/s1-display/web/app.py`
- `/opt/s1-display/web/templates/index.html`
- `/opt/s1-display/web/static/css/style.css`
- `/opt/s1-display/web/static/js/app.js`

### Everything Update (Option 3)
- All files from Python Code + Web Interface
- Config file (skipped to preserve settings)

## New Features Added

### AM/PM Support

**Via Web Interface:**
1. Click on Time widget in display
2. Change "Time Format" to "12 Hour"
3. Toggle "Show AM/PM" checkbox
4. Click "Save & Restart"

**Via Config File:**
```yaml
time:
  enabled: true
  format: 12h  # Changed from 24h
  show_am_pm: true  # NEW option
  show_seconds: false
  color: [255, 255, 255]
```

**Options:**
- `format: 24h` → Shows "14:30"
- `format: 12h` + `show_am_pm: true` → Shows "2:30 PM"
- `format: 12h` + `show_am_pm: false` → Shows "2:30"

The web interface automatically shows/hides the AM/PM toggle based on format selection!
