# Troubleshooting MiiBrowser

## Common Problems

### 1. Assertion Failed Error from tkinterweb

```
Assertion failed: pItem->x.marker.flags, file ../src/htmldraw.c, line 761
```

**Cause:** This error occurs when tkinterweb's HTML renderer encounters problematic HTML structure, especially when CSS is being injected via `load_html()`.

**Solution:** CSS enhancement is disabled by default. This uses the more stable `load_url()` method instead of HTML injection. Check that `ENABLE_CSS_ENHANCEMENT = False` in `src/miibrowser/config.py`.

### 2. Redirecting to `file:///` Paths

**Cause:** When using `load_html()` with modified HTML content, tkinterweb can lose the URL context, causing relative links to resolve as file paths.

**Solution:** CSS enhancement is disabled by default, which prevents this issue. Direct URL loading maintains proper URL context.

### 3. Images Not Displaying

```bash
pip install --upgrade Pillow CairoSVG tkinterweb-tkhtml-extras
```

### 4. Pages Not Loading

- Check your internet connection
- Reinstall tkinterweb: `pip install --upgrade --force-reinstall tkinterweb`

## Configuration

Edit `src/miibrowser/config.py` to customize browser behavior:

```python
ENABLE_CSS_ENHANCEMENT = False  # Disabled by default for stability
DEBUG_MODE = False               # Set to True to see error messages
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
REQUEST_TIMEOUT = 10
```

## Debug Mode

Enable debug mode to diagnose issues:

```python
# In src/miibrowser/config.py
DEBUG_MODE = True
```

This will print messages showing loading status and any errors encountered.

## Recommended Settings

For most users:

```python
ENABLE_CSS_ENHANCEMENT = False
DEBUG_MODE = False
```

For developers/testers:

```python
ENABLE_CSS_ENHANCEMENT = True
DEBUG_MODE = True
```
