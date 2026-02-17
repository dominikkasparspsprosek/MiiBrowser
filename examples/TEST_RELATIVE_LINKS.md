# Testing Relative Links in MiiBrowser

## The Problem

Previously, when you clicked on a relative link like `/add.php` in MiiBrowser, it would incorrectly resolve to:

```
file:///C:\Users\domin\OneDrive\Documents\GitHub\MiiBrowser/add.php
```

Instead of the correct:

```
https://example.com/add.php
```

## The Solution

The fix adds a `<base href="...">` HTML tag to the document head, which tells the browser the correct base URL for resolving all relative links. This is injected automatically along with the CSS enhancements.

## How to Test

### Option 1: Use the Test Server (Recommended)

1. **Start the test server:**

   ```bash
   python examples/test_server.py
   ```

2. **Open MiiBrowser** and navigate to:

   ```
   http://localhost:8000/
   ```

3. **Click the links** on the page:
   - `/about` - Should navigate to http://localhost:8000/about
   - `/contact` - Should navigate to http://localhost:8000/contact
   - `/docs/help` - Should navigate to http://localhost:8000/docs/help

### Option 2: Test with a Real Website

1. **Open MiiBrowser** and navigate to any website
2. **Click relative links** on the page (links that start with `/` or are just filenames)
3. **Verify** they navigate correctly instead of showing `file:///` errors

## Technical Details

### What Changed

The [browser.py](../src/miibrowser/browser.py) `load_url()` method now:

1. **Captures the final URL** (after redirects):

   ```python
   base_url = response.url if response.url else url
   ```

2. **Injects a base tag** along with CSS:

   ```python
   base_tag = f'<base href="{base_url}">'
   enhanced_head = f'{base_tag}{enhanced_css}'
   ```

3. **Preserves URL context** so relative links resolve correctly

### What the Base Tag Does

The `<base>` HTML tag specifies the base URL for all relative URLs in a document:

```html
<head>
	<base href="https://example.com/page/" />
	<!-- Now all relative links resolve relative to this base -->
</head>
```

Examples with `base href="https://example.com/page/"`:

- `/about` → `https://example.com/about`
- `contact.html` → `https://example.com/page/contact.html`
- `../index.html` → `https://example.com/index.html`

## Testing Results

### Before Fix

- ❌ `/add.php` → `file:///C:\Users\...\MiiBrowser/add.php`
- ❌ Relative links broke completely

### After Fix

- ✅ `/add.php` → `https://example.com/add.php`
- ✅ Relative links work correctly
- ✅ Maintains domain context after CSS injection

## Files Modified

- [`src/miibrowser/browser.py`](../src/miibrowser/browser.py) - Added base tag injection in `load_url()` method

## Files Created

- [`examples/test_server.py`](test_server.py) - Local HTTP server for testing relative links
- [`examples/test_relative_links.html`](test_relative_links.html) - Test page demonstrating different link types
- This README

## Compatibility

This fix works with:

- ✅ Absolute URLs (`https://...`)
- ✅ Relative paths (`/about`, `contact.html`)
- ✅ Parent directory references (`../index.html`)
- ✅ Redirects (uses final URL after redirects)
- ✅ CSS enhancement injection
- ✅ Direct URL loading (fallback if enhancement fails)

No breaking changes - the browser still works normally for all existing functionality.
