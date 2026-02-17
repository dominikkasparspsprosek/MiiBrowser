# MiiBrowser Configuration Guide

## Quick Start

MiiBrowser now uses a configuration file for easy customization. The default settings prioritize **stability over features**.

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

1. **Open the config file:**
   - Location: `src/miibrowser/config.py`
   - Edit with any text editor

2. **Change the setting you want:**

   ```python
   ENABLE_CSS_ENHANCEMENT = True  # Enable CSS enhancement
   DEBUG_MODE = True               # Show debug messages
   WINDOW_WIDTH = 1920             # Wider window
   ```

3. **Save the file**

4. **Restart MiiBrowser** - changes take effect immediately

## Configuration Options

### CSS Enhancement

```python
ENABLE_CSS_ENHANCEMENT = False  # or True
```

**False (Default):**

- ✅ Stable browsing
- ✅ No crashes
- ✅ Relative links work
- ❌ Limited CSS support

**True (Experimental):**

- ✅ Enhanced colors, backgrounds, positioning
- ✅ Bootstrap-style utility classes
- ❌ May crash on some websites
- ❌ Slower page loading

### Debug Mode

```python
DEBUG_MODE = False  # or True
```

**False (Default):**

- Clean output
- No error messages

**True:**

- Shows loading messages
- Shows error details
- Useful for troubleshooting

### Window Size

```python
WINDOW_WIDTH = 1400   # pixels
WINDOW_HEIGHT = 900   # pixels
```

Adjust to your screen size. Common presets:

- **1920x1080** - Full HD
- **1400x900** - Default (balanced)
- **1280x720** - Smaller screens
- **800x600** - Compact

### Request Timeout

```python
REQUEST_TIMEOUT = 10  # seconds
```

How long to wait for page loading. Increase if you have a slow connection.

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

### Large Screen

```python
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
```

### Slow Connection

```python
REQUEST_TIMEOUT = 30  # Wait longer for pages
```

## Checking Current Settings

Run this command to see active configuration:

```bash
python -c "from miibrowser import config; import inspect; print('Current Configuration:'); print('=' * 40); [print(f'{name}: {value}') for name, value in inspect.getmembers(config) if not name.startswith('_')]"
```

## Reset to Default

If you've changed settings and want to reset:

1. Delete `src/miibrowser/config.py`
2. Recreate it with the content from this guide (see Default Settings above)

Or restore from Git:

```bash
git checkout src/miibrowser/config.py
```

## Environment-Specific Configs

You can create multiple config files for different scenarios:

1. **Create copies:**
   - `config_stable.py` - Stability-focused
   - `config_fancy.py` - All features enabled
   - `config_dev.py` - Development settings

2. **Rename to use:**
   ```bash
   copy config_stable.py config.py
   ```

## Need Help?

- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [CSS_ENHANCEMENT_REFERENCE.md](CSS_ENHANCEMENT_REFERENCE.md) for CSS features
- Enable `DEBUG_MODE = True` to see what's happening
