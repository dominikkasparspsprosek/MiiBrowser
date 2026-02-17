# MiiBrowser 🌐

A modern Chrome-style Python browser with tabbed interface, embedded web viewing, and DuckDuckGo search integration. Features full browsing capabilities with history tracking, image support, and a clean UI.

## Features ✨

- 🔍 **DuckDuckGo Search**: Direct search integration with automatic redirect handling
- 🗂️ **Chrome-Style Tabs**: Multiple independent tabs with easy switching
- 🌐 **Embedded Web Viewer**: Browse websites directly within the app using tkinterweb
- 🖼️ **Full Image Support**: Display JPG, PNG, and SVG images within web pages
- ⏮️ **Navigation Controls**: Back, forward, and reload buttons with history tracking
- 🔄 **Smart URL Handling**: Automatic detection of URLs vs search queries
- 🎨 **Modern UI**: Clean, Google-inspired design with intuitive controls
- ⛶ **Fullscreen Mode**: Toggle fullscreen with F11 or the fullscreen button
- 🖱️ **Link Navigation**: Click links within pages to navigate seamlessly
- ⌨️ **Keyboard Shortcuts**: Quick access to common functions

## Installation 📦

### Prerequisites

Make sure you have Python 3.7 or higher installed.

### Option 1: Install as Package

```bash
# Clone the repository
git clone https://github.com/yourusername/MiiBrowser.git
cd MiiBrowser

# Install the package with all dependencies
pip install -e .
```

### Option 2: Install Dependencies Only

```bash
# Install required dependencies
pip install -r requirements.txt
```

## Requirements 📋

- Python 3.7 or higher
- tkinter (usually included with Python)
- requests>=2.31.0 (HTTP requests)
- tkinterweb>=3.18.0 (embedded web browser)
- Pillow>=9.0.0 (image support: JPG, PNG)
- CairoSVG>=2.5.0 (SVG image support)
- tkinterweb-tkhtml-extras>=1.3.0 (enhanced browser features)

All dependencies are automatically installed when using `pip install -e .`.

## Usage 🚀

### Run as Installed Package

```bash
miibrowser
```

### Run Directly

```bash
python -m miibrowser.main
```

Or:

```bash
python miibrowser/browser.py
```

### Quick Start

1. **Search**: Type any query in the address bar and press Enter
2. **Navigate**: Enter a URL (e.g., `github.com`) and press Enter
3. **Browse**: Click links within pages to navigate
4. **New Tab**: Click the `+` button or press `Ctrl+T`
5. **History**: Use the back `◄` and forward `►` buttons to navigate history

## Keyboard Shortcuts ⌨️

- **F11**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode
- **Enter**: Navigate to URL or perform search (when in address bar)
- **Ctrl+T**: Open new tab
- **Ctrl+W**: Close current tab
- **Ctrl+Tab**: Switch to next tab

## Navigation Controls 🧭

- **Back Button (◄)**: Navigate to previous page in history
- **Forward Button (►)**: Navigate to next page in history
- **Reload Button (⟳)**: Refresh current page
- **Search Button**: Submit search query or URL
- **New Tab (+)**: Create a new browser tab
- **Close Tab (×)**: Close individual tabs

## Project Structure 📁

```
MiiBrowser/
├── LICENSE                # MIT License
├── pyproject.toml        # Modern Python package configuration
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── setup.py             # Legacy setup (kept for compatibility)
├── src/
│   └── miibrowser/
│       ├── __init__.py   # Package initialization
│       ├── main.py       # Entry point
│       ├── browser.py    # Main browser GUI
│       └── search.py     # DuckDuckGo search module
└── tests/
    ├── __init__.py       # Tests package
    ├── test_browser.py   # Browser GUI tests
    └── test_search.py    # Search functionality tests
```

## Requirements 📋

- Python 3.7 or higher
- tkinter (usually included with Python)
- requests>=2.31.0 (HTTP requests)
- tkinterweb>=3.18.0 (embedded web browser)
- Pillow>=9.0.0 (image support: JPG, PNG)
- CairoSVG>=2.5.0 (SVG image support)
- tkinterweb-tkhtml-extras>=1.3.0 (enhanced browser features)

All dependencies are automatically installed when using `pip install -e .`.

## How It Works 🔧

1. **Tab Management**: Create and switch between multiple browser tabs
2. **Search & Navigate**:
   - Enter URLs directly (e.g., `https://example.com` or `example.com`)
   - Enter search queries (automatically searches via DuckDuckGo)
   - The browser detects whether input is a URL or search query
3. **Web Browsing**:
   - Pages load in embedded browser with full rendering
   - Click links to navigate within the embedded browser
   - Images (JPG, PNG, SVG) display automatically
   - DuckDuckGo redirects are handled seamlessly
4. **History Navigation**:
   - Back/forward buttons track your browsing history per tab
   - Each tab maintains its own independent history
5. **URL Tracking**: Address bar automatically updates when you navigate to new pages

## Features Breakdown 🎯

### Tab Management

- Chrome-style tab interface
- Create unlimited tabs
- Switch between tabs easily
- Close tabs individually (except last tab)
- Independent browsing history per tab

### Web Browsing

- Embedded browser using tkinterweb
- Full HTML/CSS rendering
- Image support (JPG, PNG, SVG)
- Clickable links within pages
- Automatic DuckDuckGo redirect handling
- URL detection and smart navigation

### Window Management

- Fully resizable window (1400x900 default)
- Fullscreen toggle button (⛶)
- F11 keyboard shortcut for fullscreen
- Escape to exit fullscreen
- Clean, modern Chrome-inspired UI

### Navigation Features

- Back/Forward buttons with history tracking
- Reload button for refreshing pages
- Smart address bar (URL + search)
- Real-time URL updates during navigation
- History tracking per tab with index management

## Development 🛠️

To contribute or modify:

```bash
# Clone the repository
git clone https://github.com/yourusername/MiiBrowser.git
cd MiiBrowser

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Make your changes
# Test the application
python -m miibrowser.main
```

## Testing 🧪

Run tests using pytest:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=miibrowser --cov-report=html

# Run specific test file
pytest tests/test_search.py

# Run with verbose output
pytest -v
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- DuckDuckGo for their search API
- Python tkinter for GUI capabilities
- The open-source community

## Future Enhancements 🚀

- [x] Tab browsing
- [x] History tracking (per tab)
- [x] Embedded web viewer
- [x] Image support (JPG, PNG, SVG)
- [ ] Bookmarks support
- [ ] Download manager
- [ ] Settings/preferences
- [ ] Custom color themes
- [ ] Browser extensions
- [ ] Enhanced JavaScript support
- [ ] Private browsing mode

## Known Limitations ⚠️

- **JavaScript Support**: Limited JavaScript execution compared to Chrome/Firefox
- **CSS Support**: Some modern CSS features may not render perfectly
- **Performance**: Large, complex websites may load slower than native browsers
- **Plugins**: No support for browser plugins like Flash or WebAssembly

## Troubleshooting 🔧

### Images Not Displaying

If you see errors about PIL or CairoSVG, reinstall dependencies:

```bash
pip install --upgrade Pillow CairoSVG tkinterweb-tkhtml-extras
```

### Links Not Working

Make sure `messages_enabled=False` is set in the HtmlFrame configuration (already configured by default).

### Pages Not Loading

- Check your internet connection
- Try clearing Python cache: `python -Bc "import shutil; shutil.rmtree('__pycache__', ignore_errors=True)"`
- Reinstall tkinterweb: `pip install --upgrade --force-reinstall tkinterweb`

---

**Made with ❤️ by the Dominik Kaspar**
