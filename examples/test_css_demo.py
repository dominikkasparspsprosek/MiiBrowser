"""
CSS Test Demo for MiiBrowser

This script launches MiiBrowser with a test page that demonstrates
all the enhanced CSS capabilities:
- Colors and backgrounds
- Width and height
- Position and z-index
- Spacing utilities
- Text alignment
- Borders and rounded corners
- Opacity
- Images
- Tables
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from miibrowser.browser import MiiBrowser

def main():
    """Launch browser with CSS test page"""
    # Get the path to the CSS test file
    test_file = Path(__file__).parent / 'css_test.html'
    test_url = test_file.as_uri()
    
    print("=" * 60)
    print("MiiBrowser CSS Enhancement Demo")
    print("=" * 60)
    print(f"\nLoading test page: {test_file}")
    print("\nThis page demonstrates:")
    print("  ✓ Color and background color support")
    print("  ✓ Width and height utilities")
    print("  ✓ Position (relative, absolute, fixed)")
    print("  ✓ Z-index layering")
    print("  ✓ Spacing utilities (margin, padding)")
    print("  ✓ Text alignment")
    print("  ✓ Borders and rounded corners")
    print("  ✓ Opacity")
    print("  ✓ Responsive images")
    print("  ✓ Styled tables")
    print("\n" + "=" * 60)
    
    # Create and start browser
    browser = MiiBrowser()
    
    # Load the test page
    browser.search_entry.delete(0, 'end')
    browser.search_entry.insert(0, test_url)
    browser._perform_search()
    
    # Start the GUI
    browser.root.mainloop()

if __name__ == '__main__':
    main()
