# MiiBrowser 🌐

A lightweight Python browser application with DuckDuckGo search capabilities. Features a modern, colorful GUI with resizable and fullscreen window support.

## Features ✨

- 🔍 **DuckDuckGo Search Integration**: Search the web using DuckDuckGo API
- 🎨 **Colorful Results Display**: Each search result is displayed with vibrant background colors, custom height and width
- 🖼️ **Resizable Window**: Freely resize the window to your preferred dimensions
- ⛶ **Fullscreen Mode**: Toggle fullscreen with F11 or the fullscreen button
- 🌐 **Online Status Check**: Automatically checks internet connectivity
- 🎯 **Clean UI**: Modern dark-themed interface with intuitive controls
- 🖱️ **Clickable URLs**: Click on any URL to open it in your default browser
- ⚡ **Async Search**: Non-blocking search with threaded background processing

## Installation 📦

### Option 1: Install as Package

```bash
# Clone the repository
git clone https://github.com/yourusername/MiiBrowser.git
cd MiiBrowser

# Install the package
pip install -e .
```

### Option 2: Install Dependencies Only

```bash
# Install required dependencies
pip install -r requirements.txt
```

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

## Keyboard Shortcuts ⌨️

- **F11**: Toggle fullscreen mode
- **Escape**: Exit fullscreen mode
- **Enter**: Perform search (when in search box)

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
- requests library

## How It Works 🔧

1. **Search Input**: Enter your search query in the search box
2. **Online Check**: The app verifies internet connectivity
3. **API Query**: Sends request to DuckDuckGo API
4. **Results Display**: Shows formatted results with:
   - Colorful background colors (cycling through 8 different colors)
   - Title in bold
   - Clickable URL in yellow
   - Description text
   - Custom heights and widths for each result block
5. **Interaction**: Click any URL to open it in your default browser

## Features Breakdown 🎯

### Window Management

- Fully resizable window (drag corners/edges)
- Fullscreen toggle button (⛶)
- F11 keyboard shortcut for fullscreen
- Escape to exit fullscreen

### Search Display

- Each result has a unique background color
- Results include:
  - Title (bold, large font)
  - URL (yellow, clickable, underlines on hover)
  - Description (truncated at 300 characters)
- Scrollable results area
- Mouse wheel support

### Status Indicators

- Green: Ready/Success
- Yellow: Searching
- Red: Error/Offline
- Cyan: Opening URL

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

- [ ] History tracking
- [ ] Bookmarks support
- [ ] Tab browsing
- [ ] Settings/preferences
- [ ] Custom color themes
- [ ] Export search results

---

**Made with ❤️ by the MiiBrowser Team**
