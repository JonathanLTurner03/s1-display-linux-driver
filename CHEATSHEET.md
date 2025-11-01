# S1 Display - Quick Reference

## After Making Code Changes

```bash
sudo ./scripts/update.sh
```

Choose option 1 (Python code) or 2 (Web interface), then restart services.

**Your config.yaml is always preserved!**

## Adding New Config Options

```bash
sudo ./scripts/update-config.sh
```

Helps merge new options (like `show_am_pm`) into your existing config.

## Common Commands

```bash
# View dashboard logs
sudo journalctl -u s1-dashboard.service -f

# View web interface logs
sudo journalctl -u s1-web.service -f

# Restart dashboard
sudo systemctl restart s1-dashboard.service

# Restart web interface
sudo systemctl restart s1-web.service

# Check status
sudo systemctl status s1-dashboard.service
sudo systemctl status s1-web.service
```

## Access Web Interface

```
http://hecate:5000
```

## Enable AM/PM & Change Font Size

**Web Interface:**
1. Click any widget on display
2. Adjust "Font Size" slider (1-5)
3. For time: Select "12 Hour" format
4. Toggle "Show AM/PM"
5. Save & Restart

**Config File:**
```yaml
time:
  format: 12h
  show_am_pm: true
  font_scale: 6  # 1-5 (or higher for time)

hostname:
  font_scale: 2  # 1=tiny, 2=small, 3=medium, 4=large, 5=huge
```

## Quick Config Examples

**Time only:**
```yaml
time: {enabled: true, format: 12h, show_am_pm: true}
date: {enabled: false}
hostname: {enabled: false}
```

**System monitor:**
```yaml
time: {enabled: true}
system:
  cpu_usage: {enabled: true, show_bar: true}
  memory_usage: {enabled: true, show_bar: true}
```

**Server monitor:**
```yaml
time: {enabled: true}
servers:
  - {name: "Router", host: "192.168.1.1", enabled: true}
```

## Troubleshooting

**Display not updating?**
```bash
sudo systemctl restart s1-dashboard.service
sudo journalctl -u s1-dashboard.service -n 20
```

**Web changes not showing?**
- Hard refresh: `Ctrl+F5`
- Or restart: `sudo systemctl restart s1-web.service`

**Permission errors?**
```bash
sudo ./scripts/fix-permissions.sh
# Unplug/replug device
```
