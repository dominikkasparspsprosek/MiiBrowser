"""
MiiBrowser - A simple web browser with DuckDuckGo search
"""

__version__ = "1.0.0"
__author__ = "MiiBrowser Team"

from miibrowser.browser import MiiBrowser
from miibrowser.css_parser import CSSParser, parse_inline_style, extract_css_colors, validate_css
from miibrowser.js_parser import JSParser, parse_javascript, validate_javascript, extract_functions, extract_variables, get_dependencies

__all__ = [
    'MiiBrowser',
    'CSSParser', 'parse_inline_style', 'extract_css_colors', 'validate_css',
    'JSParser', 'parse_javascript', 'validate_javascript', 'extract_functions', 'extract_variables', 'get_dependencies'
]
