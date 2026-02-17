"""
Configuration file for MiiBrowser

This file contains settings to customize browser behavior.
"""

# CSS Enhancement
# ===============
# CSS enhancement injects custom CSS into web pages for better styling support.
# However, it can cause stability issues with some websites due to tkinterweb limitations.
#
# Set to True: Enhanced CSS support (colors, positioning, etc.) but may crash on some sites
# Set to False: More stable browsing, but limited CSS support (RECOMMENDED)
ENABLE_CSS_ENHANCEMENT = False

# Search Engine
# =============
# The default search engine to use
DEFAULT_SEARCH_ENGINE = "duckduckgo"  # Options: "duckduckgo", "google", "bing"

# Browser Settings
# ================
# Initial window size
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Enable/disable debug messages
DEBUG_MODE = False

# Network timeout for page loads (seconds)
REQUEST_TIMEOUT = 10

# User Agent string
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
