"""
Quick test to verify the browser opens and can load URLs
"""

import sys
import time
from miibrowser.browser import MiiBrowser

def test_browser():
    """Test browser creation and basic functionality"""
    print("=" * 60)
    print("MiiBrowser - Quick Test")
    print("=" * 60)
    print()
    print("Creating browser window...")
    
    try:
        browser = MiiBrowser()
        print("✅ Browser created successfully!")
        print()
        print("The browser window should now be open.")
        print()
        print("To test:")
        print("  1. Type 'maps.google.com' in the address bar")
        print("  2. Press Enter")
        print("  3. A separate Chromium window should open with Google Maps")
        print()
        print("Close the main browser window to exit this test.")
        print()
        print("-" * 60)
        
        # Run the browser
        browser.run()
        
        print()
        print("✅ Browser closed successfully!")
        print()
        return 0
        
    except Exception as e:
        print()
        print("❌ Error occurred:")
        print(str(e))
        print()
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_browser())
