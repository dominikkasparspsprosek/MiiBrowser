# MiiBrowser Configuration Guide

## Quick Start

MiiBrowser uses a configuration file for easy customization. The default settings prioritize stability over features.

## Default Settings (Recommended)

The browser ships with these settings:

```python
ENABLE_CSS_ENHANCEMENT = False  # Disabled for stability
DEBUG_MODE = False               # Clean output
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
REQUEST_TIMEOUT = 10
```

## How to Change Settings

1. Open `src/miibrowser/config.py` with any text editor
2. Change the setting you want
3. Save the file
4. Restart MiiBrowser - changes take effect immediately

## Configuration Options

### CSS Enhancement

```python
ENABLE_CSS_ENHANCEMENT = False  # or True
```

**False (Default):**
- Stable browsing, no crashes
- Relative links work correctly
- Limited CSS support

**True (Experimental):**
- Enhanced colors, backgrounds, positioning
- Bootstrap-style utility classes
- May crash on some websites
- Slower page loading

### Debug Mode

```python
DEBUG_MODE = False  # or True
```

When enabled, shows loading messages and error details.

### Window Size

```python
WINDOW_WIDTH = 1400   # pixels
WINDOW_HEIGHT = 900   # pixels
```

Common presets: 1920x1080, 1400x900 (default), 1280x720, 800x600.

### Request Timeout

```python
REQUEST_TIMEOUT = 10  # seconds
```

How long to wait for page loading. Increase for slow connections.

### User Agent

```python
USER_AGENT = "Mozilla/5.0 ..."
```

The browser identifier sent to websites. Default mimics Chrome 120.

## Common Configurations

### Maximum Stability (Recommended)

```python
ENABLE_CSS_ENHANCEMENT = False
DEBUG_MODE = False
REQUEST_TIMEOUT = 10
```

### Testing/Development

```python
ENABLE_CSS_ENHANCEMENT = True
DEBUG_MODE = True
REQUEST_TIMEOUT = 15
```

## Reset to Default

Restore from Git:

```bash
git checkout src/miibrowser/config.py
```
