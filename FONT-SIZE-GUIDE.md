# Font Size Control Guide

## Overview

Every widget now has adjustable font size! Control it via the web interface or config file.

## Font Size Scale

```
1 = Tiny     (very compact, fits lots of info)
2 = Small    (default for most widgets)
3 = Medium   (good for important info)
4 = Large    (easy to read from distance)
5 = Huge     (takes up lots of space)
6+ = Extra   (time widget can go higher)
```

## Using the Web Interface

1. **Click any widget** on the display preview
2. **Drag the "Font Size" slider** in the properties panel
   - See live number update as you drag
   - 1 (Small) ← → 5 (Large)
3. **Click "Save & Restart"** to apply
4. **Check your display** - size updates immediately

### Visual Preview

The slider shows:
```
Small ←————●————→ Large
       1  2  3  4  5
```

## Using Config File

Add `font_scale` to any widget:

```yaml
time:
  enabled: true
  font_scale: 6  # Extra large time

hostname:
  enabled: true
  font_scale: 2  # Small hostname

network:
  local_ip:
    enabled: true
    font_scale: 3  # Medium IP address

system:
  cpu_usage:
    enabled: true
    font_scale: 2  # Small CPU reading
```

## Size Examples

### Small Display (lots of info)

```yaml
time: {enabled: true, font_scale: 4}
date: {enabled: true, font_scale: 1}
hostname: {enabled: true, font_scale: 1}
local_ip: {enabled: true, font_scale: 1}
cpu_usage: {enabled: true, font_scale: 1}
memory_usage: {enabled: true, font_scale: 1}
# Fits 6+ items on screen
```

### Large Display (easy to read)

```yaml
time: {enabled: true, font_scale: 8}
date: {enabled: true, font_scale: 3}
hostname: {enabled: true, font_scale: 3}
# Fits 3-4 items on screen
```

### Mixed Sizes (hierarchical)

```yaml
time: {enabled: true, font_scale: 6}        # Most important
hostname: {enabled: true, font_scale: 3}    # Important
local_ip: {enabled: true, font_scale: 2}    # Less important
cpu_usage: {enabled: true, font_scale: 2}   # Less important
```

## Per-Widget Behavior

### Time Widget
- Default: 6 (extra large)
- Range: 3-10
- Centered on display
- Can go larger than other widgets

### Date Widget
- Default: 2 (small)
- Range: 1-3
- Centered below time
- Kept smaller to not overwhelm

### All Other Widgets
- Default: 2 (small)
- Range: 1-5
- Left-aligned with padding
- Same font available to all

### Server Monitor Widgets
- Default: 2 (small)
- Range: 1-5
- Supports font_scale like all other widgets
- Set individually for each server

## Tips & Tricks

### Fit More Info

Set everything to `font_scale: 1`:
```yaml
# All widgets
font_scale: 1
```

Can fit 8-10+ items on display!

### Emphasize Important Info

Make important items larger:
```yaml
time: {font_scale: 8}      # Biggest
hostname: {font_scale: 3}  # Medium
everything_else: {font_scale: 1}  # Small
```

### Consistent Look

Use same size for everything:
```yaml
# All widgets
font_scale: 2
```

Clean, uniform appearance.

### Optimize for Distance

Viewing from far away? Go bigger:
```yaml
time: {font_scale: 10}
everything_else: {font_scale: 4}
```

### Dense Information Display

System monitoring setup:
```yaml
time: {font_scale: 3}
cpu_usage: {font_scale: 1, show_bar: true}
memory_usage: {font_scale: 1, show_bar: true}
local_ip: {font_scale: 1}
servers:
  - {name: "Web", host: "192.168.1.10", font_scale: 1, enabled: true}
  - {name: "DB", host: "192.168.1.11", font_scale: 1, enabled: true}
  - {name: "Cache", host: "192.168.1.12", font_scale: 1, enabled: true}
# Fits time + 6 monitoring items
```

### Priority Server Monitoring

Emphasize critical server:
```yaml
time: {font_scale: 4}
servers:
  - {name: "PROD-WEB", host: "10.0.1.100", font_scale: 3, enabled: true}  # Critical
  - {name: "DEV-WEB", host: "10.0.2.100", font_scale: 2, enabled: true}   # Normal
  - {name: "TEST-WEB", host: "10.0.3.100", font_scale: 1, enabled: true}  # Small
```

## How It Works

### Font Rendering

Uses bitmap fonts scaled by pixel multiplication:
- Scale 1 = 1×1 pixels per font pixel
- Scale 2 = 2×2 pixels per font pixel
- Scale 3 = 3×3 pixels per font pixel
- Etc.

### Display Layout

Auto-layout system adjusts spacing based on font size:
- Larger fonts = more vertical space used
- Smaller fonts = more items fit
- Progress bars scale with font size

### Performance

No performance impact! Font scaling is efficient:
- Same rendering speed regardless of size
- No additional memory used
- Display updates at same rate (1 sec default)

## Common Configurations

### Clock Only (Large)

```yaml
time:
  font_scale: 10
  show_seconds: true
# Massive clock display
```

### Server Room Monitor

```yaml
time: {font_scale: 4}
cpu_usage: {font_scale: 2, show_bar: true}
memory_usage: {font_scale: 2, show_bar: true}
servers:
  - {name: "Server1", host: "192.168.1.10", font_scale: 2, enabled: true}
  - {name: "Server2", host: "192.168.1.11", font_scale: 2, enabled: true}
  - {name: "Server3", host: "192.168.1.12", font_scale: 2, enabled: true}
```

### Information Dashboard

```yaml
time: {font_scale: 5}
date: {font_scale: 2}
hostname: {font_scale: 2}
local_ip: {font_scale: 2}
tailscale_ip: {font_scale: 2}
cpu_usage: {font_scale: 1}
memory_usage: {font_scale: 1}
```

## Troubleshooting

### Text Too Large (Items Cut Off)

Reduce font_scale:
```yaml
# Change from
font_scale: 5

# To
font_scale: 3
```

### Text Too Small (Can't Read)

Increase font_scale:
```yaml
# Change from
font_scale: 1

# To
font_scale: 3
```

### Widget Not Fitting on Screen

Either:
1. Reduce font_scale
2. Disable some widgets
3. Remove `show_bar` from system widgets

### Inconsistent Sizes

Set `font_scale` explicitly for all widgets:
```yaml
time: {font_scale: 6}
date: {font_scale: 2}
hostname: {font_scale: 2}
local_ip: {font_scale: 2}
# etc.
```

## Summary

✅ **Every widget** has font size control
✅ **Web interface** has slider for easy adjustment
✅ **Live preview** while dragging slider
✅ **Config file** supports font_scale: 1-5 (or higher)
✅ **Auto-layout** adjusts spacing automatically
✅ **No performance impact** regardless of size

Make your display exactly how you want it! 🎨
