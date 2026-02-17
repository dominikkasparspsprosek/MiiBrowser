# MiiBrowser - File Descriptions

This document describes every file in the project, what it does, and how it fits together.

## How the Browser Works

MiiBrowser is a desktop web browser built with Python. The GUI is built using **tkinter** (Python's built-in GUI toolkit). Web pages are rendered using **tkinterweb**, which embeds an HTML renderer inside a tkinter window. When you type a URL or search query in the address bar, the browser either loads the page directly via tkinterweb or constructs a DuckDuckGo search URL and loads that instead.

The rendering flow:
1. User types in the address bar and presses Enter
2. The browser detects if input is a URL or a search query
3. For URLs, it loads the page directly using `tkinterweb.HtmlFrame.load_url()`
4. For search queries, it builds a DuckDuckGo URL and loads that
5. tkinterweb renders the HTML/CSS and displays it in the window
6. The browser polls for URL changes to track navigation within the page

## Source Files

### src/miibrowser/main.py
Entry point for the application. Imports and calls `main()` from `browser.py`. This is what runs when you type `miibrowser` on the command line or `python -m miibrowser.main`.

### src/miibrowser/browser.py
The main browser application. Contains two classes:

- **BrowserTab**: Represents a single browser tab. Handles URL loading via tkinterweb, navigation history (back/forward), DuckDuckGo redirect detection, and URL change polling.
- **MiiBrowser**: The main window. Manages the tab bar, address bar, navigation buttons (back, forward, reload), keyboard shortcuts, and fullscreen mode. Uses tkinter for the GUI layout.

This is the largest and most important file. It handles all user interaction and web page display.

### src/miibrowser/search.py
DuckDuckGo search integration. Contains the `DuckDuckGoSearch` class that can query the DuckDuckGo Instant Answer API and return structured results. Also has an `is_online()` method to check internet connectivity.

### src/miibrowser/config.py
Configuration settings for the browser. Controls:
- `ENABLE_CSS_ENHANCEMENT` - Whether to inject custom CSS into pages (disabled by default for stability)
- `DEBUG_MODE` - Whether to print debug messages
- `WINDOW_WIDTH` / `WINDOW_HEIGHT` - Initial window size
- `REQUEST_TIMEOUT` - Network timeout in seconds
- `USER_AGENT` - Browser user agent string

### src/miibrowser/css_parser.py
A CSS parsing utility built with the `tinycss2` library. Provides the `CSSParser` class for parsing stylesheets, extracting colors, selectors, properties, media queries, and for minifying/prettifying CSS. This is a standalone utility and is not directly used for page rendering.

### src/miibrowser/css_enhancer.py
Provides enhanced CSS that can be injected into web pages when `ENABLE_CSS_ENHANCEMENT` is True. Contains Bootstrap-style utility classes for colors, positioning, spacing, etc. This CSS is injected into HTML before rendering to improve tkinterweb's limited CSS support.

### src/miibrowser/__init__.py
Package initialization. Exports the main classes and utility functions so they can be imported as `from miibrowser import MiiBrowser, CSSParser`.

## Configuration and Build Files

### pyproject.toml
Modern Python package configuration. Defines the project metadata, dependencies, build system, pytest settings, and coverage configuration. This is the primary build configuration file.

### setup.py
Legacy Python package setup script. Reads from README.md and requirements.txt for compatibility with older pip versions.

### requirements.txt
Lists all Python package dependencies with minimum version numbers.

### MANIFEST.in
Specifies additional files to include in source distributions.

## Test Files

### tests/test_browser.py
Tests for the browser GUI. Verifies that the MiiBrowser class can be imported and initialized, and that required methods exist. Tests are skipped in headless environments where tkinter is not available.

### tests/test_search.py
Tests for the DuckDuckGo search module. Verifies search returns results with the correct structure.

### tests/test_css_parser.py
Tests for the CSS parser. Covers stylesheet parsing, color extraction, selector extraction, media queries, minification, prettification, and validation.

## Documentation

### README.md
Main project documentation with installation instructions, usage guide, keyboard shortcuts, and configuration overview.

### CONFIGURATION.md
Detailed configuration guide explaining all settings in config.py.

### TROUBLESHOOTING.md
Common problems and their solutions.

### LICENSE
MIT License.

## Examples

### examples/css_parser_demo.py
Demonstration script showing CSS parser capabilities.

### examples/css_test.html
Test HTML page for CSS features.

### examples/test_css_demo.py
Script for testing CSS demo features.

### examples/test_relative_links.html
Test HTML page for verifying relative link resolution.

### examples/test_server.py
Simple local HTTP server for testing the browser with local pages.
