# MiiBrowser

A modern Chrome-style Python desktop browser with embedded web viewing and tabbed interface. Features DuckDuckGo search integration and full browsing capabilities.

## Features

- **DuckDuckGo Search**: Direct search integration with automatic redirect handling
- **Chrome-Style Tabs**: Multiple independent tabs with easy switching
- **Embedded Web Viewer**: Browse websites directly within the app using tkinterweb
- **Full Image Support**: Display JPG, PNG, SVG, and other image formats
- **Navigation Controls**: Back, forward, and reload buttons with history tracking
- **Smart URL Handling**: Automatic detection of URLs vs search queries
- **Modern UI**: Clean, Google-inspired design with intuitive controls
- **Fullscreen Mode**: Toggle fullscreen with F11 or the fullscreen button
- **Link Navigation**: Click links within pages to navigate seamlessly
- **Keyboard Shortcuts**: Quick access to common functions
- **CSS Parser**: Full CSS3 parsing with tinycss2 for stylesheet analysis

## Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed.

### Option 1: Install as Package

```bash
git clone https://github.com/dominikkasparspsprosek/MiiBrowser.git
cd MiiBrowser
pip install -e .
```

### Option 2: Install Dependencies Only

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7 or higher
- tkinter (usually included with Python)
- requests (HTTP requests)
- tkinterweb (embedded web browser)
- Pillow (image support: JPG, PNG)
- CairoSVG (SVG image support)
- tinycss2 (CSS parsing)

All dependencies are automatically installed when using `pip install -e .`.

## Usage

### Run as Installed Package

```bash
miibrowser
```

### Run Directly

```bash
python -m miibrowser.main
```

### Quick Start

1. **Search**: Type any query in the address bar and press Enter
2. **Navigate**: Enter a URL (e.g., `github.com`) and press Enter
3. **Browse**: Web pages display embedded within the browser window
4. **New Tab**: Click the `+` button or press `Ctrl+T`
5. **History**: Use the back and forward buttons to navigate history

## Keyboard Shortcuts

### Navigation

- **Alt + Left**: Go back
- **Alt + Right**: Go forward
- **Ctrl+R / F5**: Reload page
- **Ctrl+L / Ctrl+K**: Focus address bar

### Tab Management

- **Ctrl+T**: Open new tab
- **Ctrl+W**: Close current tab
- **Ctrl+Tab**: Switch to next tab
- **Ctrl+Shift+Tab**: Switch to previous tab

### Window Controls

- **F11**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode

## Configuration

MiiBrowser includes a configuration system for customizing behavior. Settings are in [`src/miibrowser/config.py`](src/miibrowser/config.py).

### Default Settings

The browser ships with CSS enhancement disabled for maximum stability:

```python
ENABLE_CSS_ENHANCEMENT = False  # Disabled by default
DEBUG_MODE = False               # Clean output
WINDOW_WIDTH = 1400              # Window width
WINDOW_HEIGHT = 900              # Window height
```

CSS enhancement provides better styling but can cause crashes on some websites (tkinterweb assertion errors) and slower page loading. The default behavior uses direct URL loading without HTML injection, which is more stable.

To enable CSS enhancement, edit `src/miibrowser/config.py` and set `ENABLE_CSS_ENHANCEMENT = True`. See [CONFIGURATION.md](CONFIGURATION.md) for details and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## How It Works

1. **Tab Management**: Create and switch between multiple browser tabs
2. **Search and Navigate**:
   - Enter URLs directly (e.g., `https://example.com` or `example.com`)
   - Enter search queries (automatically searches via DuckDuckGo)
   - The browser detects whether input is a URL or search query
3. **Web Browsing**:
   - Pages load in the embedded browser with full rendering
   - Click links to navigate within the embedded browser
   - Images (JPG, PNG, SVG) display automatically
   - DuckDuckGo redirects are handled seamlessly
4. **History Navigation**:
   - Back/forward buttons track your browsing history per tab
   - Each tab maintains its own independent history
5. **URL Tracking**: The address bar automatically updates when you navigate to new pages

## Development

```bash
git clone https://github.com/dominikkasparspsprosek/MiiBrowser.git
cd MiiBrowser
pip install -e ".[dev]"
python -m miibrowser.main
```

## Testing

```bash
pip install -e ".[dev]"
pytest
pytest --cov=miibrowser --cov-report=html
pytest -v
```

## Known Limitations

- **JavaScript Support**: Limited JavaScript execution compared to Chrome/Firefox
- **CSS Support**: Some modern CSS features may not render perfectly
- **Performance**: Large, complex websites may load slower than native browsers

## Troubleshooting

### Images Not Displaying

```bash
pip install --upgrade Pillow CairoSVG tkinterweb-tkhtml-extras
```

### Pages Not Loading

- Check your internet connection
- Reinstall tkinterweb: `pip install --upgrade --force-reinstall tkinterweb`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made by Dominik Kaspar
