# Quick Reference - MiiBrowser Stability

## Problem: Browser Crashes & File Path Redirects

### Symptoms

```
❌ Assertion failed: pItem->x.marker.flags, file ../src/htmldraw.c, line 761
❌ Redirecting to: file:///C:\Users\...\MiiBrowser/
```

## Solution: CSS Enhancement Disabled by Default

### Current Status ✅

- CSS enhancement: **DISABLED** (stable mode)
- Direct URL loading (no HTML injection)
- No crashes
- Relative links work correctly

## Quick Checks

### 1. Verify Configuration

```bash
python -c "from miibrowser import config; print(config.ENABLE_CSS_ENHANCEMENT)"
```

**Expected:** `False`

### 2. Test Browser

```bash
python -m miibrowser.main
```

**Expected:** Opens without errors

### 3. Check for Errors

Set `DEBUG_MODE = True` in `src/miibrowser/config.py` to see detailed error messages.

## Configuration File

Location: `src/miibrowser/config.py`

```python
# Default (Stable) Settings
ENABLE_CSS_ENHANCEMENT = False  # ✅ Stability first
DEBUG_MODE = False               # Clean output
WINDOW_WIDTH = 1400              # Adjust as needed
WINDOW_HEIGHT = 900
```

## Trade-offs

### CSS Enhancement DISABLED (Current Default)

| Pros                   | Cons                          |
| ---------------------- | ----------------------------- |
| ✅ No crashes          | ❌ Basic CSS only             |
| ✅ Fast loading        | ❌ No enhanced styling        |
| ✅ Stable              | ❌ Limited colors/positioning |
| ✅ Relative links work |                               |

### CSS Enhancement ENABLED (Experimental)

| Pros                 | Cons                        |
| -------------------- | --------------------------- |
| ✅ Enhanced CSS      | ❌ May crash                |
| ✅ Better colors     | ❌ Slower loading           |
| ✅ Position support  | ❌ Can have file:/// issues |
| ✅ Bootstrap classes | ❌ Less stable              |

## Enabling CSS Enhancement

**Only if you need enhanced styling:**

1. Edit `src/miibrowser/config.py`:

   ```python
   ENABLE_CSS_ENHANCEMENT = True
   DEBUG_MODE = True  # See errors
   ```

2. Save and restart browser

3. Test on simple sites first

## Common Commands

```bash
# Run browser
python -m miibrowser.main

# Check config
python -c "from miibrowser import config; print(f'CSS: {config.ENABLE_CSS_ENHANCEMENT}, Debug: {config.DEBUG_MODE}')"

# Test imports
python -c "from miibrowser import MiiBrowser; print('OK')"
```

## Documentation

- [CONFIGURATION.md](CONFIGURATION.md) - Detailed settings guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
- [STABILITY_FIX.md](STABILITY_FIX.md) - Technical details
- [CSS_ENHANCEMENT_REFERENCE.md](CSS_ENHANCEMENT_REFERENCE.md) - CSS features

## In Case of Problems

1. **Ensure CSS enhancement is disabled:**

   ```python
   ENABLE_CSS_ENHANCEMENT = False
   ```

2. **Enable debug mode:**

   ```python
   DEBUG_MODE = True
   ```

3. **Check terminal output** for error messages

4. **Test with simple sites** first

## Bottom Line

🎯 **Default settings prioritize stability over features**  
🎯 **CSS enhancement is optional and experimental**  
🎯 **Configuration is easy - edit one file**  
🎯 **Fallback is automatic if enhancement fails**

---

**TL;DR:** Browser now stable by default. Edit `config.py` to enable advanced features if needed.
