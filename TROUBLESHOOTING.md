# Troubleshooting MiiBrowser Crashes and Issues

## Common Problems

### 1. Assertion Failed Error from tkinterweb

```
Assertion failed: pItem->x.marker.flags, file ../src/htmldraw.c, line 761
```

**Cause:** This error occurs when tkinterweb's HTML renderer encounters problematic HTML structure, especially when CSS/HTML is being injected via `load_html()`.

**Solution:** CSS enhancement is now **disabled by default**. This uses the more stable `load_url()` method instead of HTML injection.

### 2. Redirecting to `file:///C:\Users\...\MiiBrowser/`

**Cause:** When using `load_html()` with modified HTML content, tkinterweb can lose the URL context, causing relative links to resolve as file paths.

**Solution:** CSS enhancement is disabled by default, which prevents this issue. Direct URL loading maintains proper URL context.

## Configuration

Edit `src/miibrowser/config.py` to customize browser behavior:

```python
# CSS Enhancement (DISABLED by default for stability)
ENABLE_CSS_ENHANCEMENT = False  # Set to True to enable

# Window size
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Debug mode
DEBUG_MODE = False  # Set to True to see error messages

# Network timeout
REQUEST_TIMEOUT = 10

# User agent
USER_AGENT = "Mozilla/5.0 ..."
```

## CSS Enhancement Trade-offs

### When Disabled (Default - RECOMMENDED)

✅ **Pros:**

- More stable - no crashes
- Relative links work correctly
- Faster page loading
- Better compatibility with websites

❌ **Cons:**

- Limited CSS support (tkinterweb limitations)
- Basic styling only

### When Enabled

✅ **Pros:**

- Enhanced CSS support (colors, backgrounds, positioning, etc.)
- Better visual appearance
- Bootstrap-style utility classes

❌ **Cons:**

- May crash on some websites
- Can cause file:/// redirect issues
- Slower page loading (fetches and modifies HTML)
- Less stable overall

## Enabling CSS Enhancement

If you want to try CSS enhancement despite the risks:

1. **Edit the config file:**

   ```python
   # In src/miibrowser/config.py
   ENABLE_CSS_ENHANCEMENT = True
   ```

2. **Enable debug mode to see errors:**

   ```python
   DEBUG_MODE = True
   ```

3. **Test carefully:**
   - Start with simple websites
   - Watch for crash messages
   - If it crashes on a site, it will fallback to direct loading

## Debug Mode

Enable debug mode to diagnose issues:

```python
# In src/miibrowser/config.py
DEBUG_MODE = True
```

This will print messages like:

- `"Loading URL directly (CSS enhancement disabled): https://..."`
- `"CSS enhancement failed, using direct load: <error message>"`

## Quick Fix Commands

**If browser crashes frequently:**

```python
# In src/miibrowser/config.py
ENABLE_CSS_ENHANCEMENT = False
DEBUG_MODE = False
```

**If you want to see what's happening:**

```python
DEBUG_MODE = True
```

**If you want better styling (at stability cost):**

```python
ENABLE_CSS_ENHANCEMENT = True
DEBUG_MODE = True  # So you can see if/when it fails
```

## Technical Details

### Why Direct URL Loading is More Stable

- tkinterweb's `load_url()` method handles:
  - Base URL context automatically
  - Relative link resolution
  - Proper document state management
  - Better error handling

- tkinterweb's `load_html()` method:
  - Loses URL context
  - Requires manual base tag injection
  - More prone to parsing errors
  - Can crash on malformed HTML

### Why CSS Enhancement Can Crash

1. **HTML injection** modifies the document structure
2. **String replacement** can create malformed HTML
3. **tkinterweb's C code** has assertion checks that fail on certain structures
4. **Base tag injection** doesn't always work perfectly with all HTML

## Recommended Settings

For most users:

```python
ENABLE_CSS_ENHANCEMENT = False  # Stability first
DEBUG_MODE = False               # Clean output
```

For developers/testers:

```python
ENABLE_CSS_ENHANCEMENT = True   # Test enhanced features
DEBUG_MODE = True                # See what breaks
```

## Verifying Your Settings

Run this command to check current configuration:

```bash
python -c "from miibrowser import config; print(f'CSS Enhancement: {config.ENABLE_CSS_ENHANCEMENT}'); print(f'Debug Mode: {config.DEBUG_MODE}')"
```

Expected output with default settings:

```
CSS Enhancement: False
Debug Mode: False
```
