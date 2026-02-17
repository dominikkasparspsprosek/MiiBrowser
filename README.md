# MiiBrowser 🌐

A modern Chrome-style Python browser with embedded web viewing and tabbed interface. Features DuckDuckGo search integration, full browsing capabilities, and powerful CSS/JavaScript parsing tools.

## Features ✨

- 🔍 **DuckDuckGo Search**: Direct search integration with automatic redirect handling
- 🗂️ **Chrome-Style Tabs**: Multiple independent tabs with easy switching
- 🌐 **Embedded Web Viewer**: Browse websites directly within the app using tkinterweb
- 🖼️ **Full Image Support**: Display JPG, PNG, SVG, and other image formats
- ⏮️ **Navigation Controls**: Back, forward, and reload buttons with history tracking
- 🔄 **Smart URL Handling**: Automatic detection of URLs vs search queries
- 🎨 **Modern UI**: Clean, Google-inspired design with intuitive controls
- ⛶ **Fullscreen Mode**: Toggle fullscreen with F11 or the fullscreen button
- 🖱️ **Link Navigation**: Click links within pages to navigate seamlessly
- ⌨️ **Keyboard Shortcuts**: Quick access to common functions
- 🎯 **CSS Parser**: Full CSS3 parsing with tinycss2 for advanced stylesheet analysis
- 🔧 **JavaScript Parser**: Complete ECMAScript parsing with esprima for code analysis

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
- tinycss2>=1.2.0 (CSS parsing)
- esprima>=4.0.0 (JavaScript parsing)

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
3. **Browse**: Web pages display embedded within the browser window
4. **New Tab**: Click the `+` button or press `Ctrl+T`
5. **History**: Use the back `◄` and forward `►` buttons to navigate history

### Best For

- 📰 **Static Websites**: News sites, blogs, documentation
- 🔍 **Search Results**: DuckDuckGo search with colorful results
- 📄 **Simple Pages**: HTML pages with CSS and images
- 🎨 **CSS/JS Analysis**: Built-in parsers for code analysis

## Keyboard Shortcuts ⌨️

### Navigation

- **Alt+←**: Go back
- **Alt+→**: Go forward
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

## Configuration & Stability ⚙️

MiiBrowser includes a configuration system for customizing behavior. Settings are in [`src/miibrowser/config.py`](src/miibrowser/config.py).

### Default Settings (Stable)

The browser ships with **CSS enhancement disabled** for maximum stability:

```python
ENABLE_CSS_ENHANCEMENT = False  # Disabled by default
DEBUG_MODE = False               # Clean output
WINDOW_WIDTH = 1400              # Window width
WINDOW_HEIGHT = 900              # Window height
```

### Why CSS Enhancement is Disabled

CSS enhancement provides better styling but can cause:

- ⚠️ Crashes on some websites (tkinterweb assertion errors)
- ⚠️ `file:///` redirect issues with relative links
- ⚠️ Slower page loading

**Current behavior (stable):** Direct URL loading, no HTML injection

### Enabling CSS Enhancement

If you want enhanced CSS support (colors, backgrounds, positioning, etc.):

1. Edit `src/miibrowser/config.py`
2. Set `ENABLE_CSS_ENHANCEMENT = True`
3. Optionally enable `DEBUG_MODE = True` to see errors
4. Restart the browser

See [CONFIGURATION.md](CONFIGURATION.md) for detailed options and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

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
├── CHROMIUM_UPGRADE.md   # Detailed upgrade documentation
├── src/
│   └── miibrowser/
│       ├── __init__.py   # Package initialization
│       ├── main.py       # Entry point
│       ├── browser.py    # Main browser GUI (Chromium-powered)
│       ├── browser_backup.py # Original tkinterweb version (backup)
│       ├── search.py     # DuckDuckGo search module
│       ├── css_parser.py # Full CSS3 parser with tinycss2
│       └── js_parser.py  # Full ECMAScript parser with esprima
└── tests/
    ├── __init__.py       # Tests package
    ├── test_browser.py   # Browser GUI tests
    ├── test_search.py    # Search functionality tests
    ├── test_css_parser.py # CSS parser tests (41 tests)
    └── test_js_parser.py  # JavaScript parser tests (57 tests)
```

## CSS Parsing Capabilities 🎨

MiiBrowser includes a powerful CSS parser built with `tinycss2` that provides full CSS parsing capabilities:

```python
from miibrowser import CSSParser, parse_inline_style, extract_css_colors

# Parse a complete stylesheet
parser = CSSParser()
rules = parser.parse_stylesheet("""
    body { background-color: #f0f0f0; margin: 0; }
    .header { color: #333; font-size: 24px; }
""")

# Extract all colors from CSS
colors = parser.extract_colors(css_text)
# Returns: ['#f0f0f0', '#333']

# Extract all selectors
selectors = parser.extract_selectors(css_text)
# Returns: ['body', '.header']

# Parse inline styles
style_dict = parse_inline_style("color: red; font-size: 16px;")
# Returns: {'color': 'red', 'font-size': '16px'}

# Extract specific properties with their selectors
font_sizes = parser.extract_properties(css_text, "font-size")
# Returns: [('.header', '24px')]

# Get all declarations organized by selector
all_decls = parser.get_all_declarations(css_text)

# Parse media queries
media_queries = parser.parse_media_queries(css_text)

# Minify CSS
minified = parser.minify_css(css_text)

# Prettify CSS with proper indentation
prettified = parser.prettify_css(css_text, indent="  ")

# Validate CSS syntax
is_valid, error_msg = validate_css(css_text)
```

### CSS Parser Features

- ✅ **Full CSS3 Support**: Parse modern CSS syntax including nested rules
- 🎨 **Color Extraction**: Extract all color values from stylesheets
- 🔍 **Selector Parsing**: Get all CSS selectors from a stylesheet
- 📋 **Declaration Extraction**: Extract specific properties with values
- 📱 **Media Query Parsing**: Parse and extract media query conditions
- 🗜️ **CSS Minification**: Minify CSS by removing whitespace
- ✨ **CSS Prettification**: Format CSS with proper indentation
- ✔️ **Validation**: Validate CSS syntax
- 🎯 **Inline Style Parsing**: Parse HTML inline style attributes

## JavaScript Parsing Capabilities 🚀

MiiBrowser includes a comprehensive JavaScript parser built with `esprima` that provides full ECMAScript parsing:

```python
from miibrowser import JSParser, parse_javascript, validate_javascript, extract_functions

# Parse JavaScript code
parser = JSParser()
ast = parser.parse("""
    function greet(name) {
        return `Hello, ${name}!`;
    }

    const add = (a, b) => a + b;

    class Calculator {
        multiply(x, y) {
            return x * y;
        }
    }
""")

# Extract all functions
functions = parser.extract_functions()
# Returns: [{'name': 'greet', 'params': ['name'], 'async': False, ...}, ...]

# Extract all variables
variables = parser.extract_variables()
# Returns: [{'kind': 'const', 'name': 'add'}, ...]

# Extract all classes
classes = parser.extract_classes()
# Returns: [{'name': 'Calculator', 'superClass': None}, ...]

# Parse ES6 modules
ast = parser.parse_module("""
    import React from 'react';
    export default function App() {}
""")

# Extract imports and exports
imports = parser.extract_imports()
exports = parser.extract_exports()

# Find all dependencies
deps = parser.find_dependencies(js_code)
# Returns: {'imports': ['react', 'axios'], 'requires': ['fs', 'path']}

# Analyze code complexity
metrics = parser.analyze_complexity(js_code)
# Returns: {'functions': 5, 'variables': 10, 'classes': 2, 'loops': 3, ...}

# Validate JavaScript syntax
is_valid, error = parser.validate_syntax(js_code)

# Tokenize JavaScript
tokens = parser.tokenize("const x = 42;")

# Get all identifiers
identifiers = parser.get_all_identifiers(js_code)

# Extract comments
comments = parser.extract_comments(js_code)

# Detect module type
module_type = parser.detect_module_type(js_code)
# Returns: 'es6', 'commonjs', or 'none'

# Convert AST to JSON
json_ast = parser.to_json(js_code, indent=2)
```

### JavaScript Parser Features

- ✅ **Full ES6+ Support**: Parse modern JavaScript including async/await, generators, classes
- 🔍 **Function Extraction**: Extract all function declarations, expressions, and arrow functions
- 📦 **Variable Extraction**: Extract const, let, and var declarations
- 🎓 **Class Extraction**: Extract class declarations with inheritance info
- 📥 **Import/Export Analysis**: Parse ES6 module imports and exports
- 📊 **Complexity Analysis**: Calculate code metrics (functions, loops, conditionals, depth)
- 🔎 **Dependency Detection**: Find all imports and requires
- ✔️ **Syntax Validation**: Validate JavaScript syntax
- 🎯 **AST Generation**: Generate Abstract Syntax Tree for analysis
- 🏷️ **Tokenization**: Break code into tokens
- 💬 **Comment Extraction**: Extract all comments from code
- 🔧 **Module Detection**: Detect CommonJS vs ES6 modules
- 🌐 **JSX Support**: Optional JSX parsing for React code

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
