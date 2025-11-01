# S1 Display - Quick Reference

## After Making Code Changes

```bash
sudo ./scripts/update.sh
```

Choose option 1 (Python code) or 2 (Web interface), then restart services.

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

## Enable AM/PM

**Web Interface:**
1. Click Time widget
2. Select "12 Hour" format
3. Toggle "Show AM/PM"
4. Save & Restart

**Config File:**
```yaml
time:
  format: 12h
  show_am_pm: true
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
