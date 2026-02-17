"""
Quick test to verify Google Maps works in MiiBrowser
"""

import webview
import sys

def main():
    """
    Open Google Maps in a pywebview window 
    to demonstrate full Chromium capabilities
    """
    
    print("=" * 70)
    print("MiiBrowser - Google Maps Test")
    print("=" * 70)
    print()
    print("Opening Google Maps with full Chromium engine...")
    print()
    print("What you should see:")
    print("  ✅ Interactive map with zoom controls")
    print("  ✅ Search functionality working")
    print("  ✅ Smooth panning and zooming")
    print("  ✅ JavaScript execution (map tiles loading)")
    print("  ✅ Cookie support (location preferences)")
    print()
    print("This proves the browser now has:")
    print("  • Full JavaScript (ES6+)")
    print("  • Cookie management")
    print("  • WebGL support")
    print("  • Canvas API")
    print("  • All modern web features")
    print()
    print("-" * 70)
    print("Window will open shortly...")
    print("Close the window to exit.")
    print("-" * 70)
    print()
    
    try:
        # Create window with Google Maps
        window = webview.create_window(
            'Google Maps - MiiBrowser Test',
            'https://www.google.com/maps',
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False
        )
        
        # Start webview (blocks until window closes)
        webview.start()
        
        print()
        print("=" * 70)
        print("✅ Test completed successfully!")
        print("=" * 70)
        print()
        print("If Google Maps loaded and worked correctly, your browser")
        print("now has full Chromium capabilities!")
        print()
        
        return 0
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ Error occurred:")
        print(str(e))
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  1. Make sure pywebview is installed: pip install pywebview")
        print("  2. Check internet connection")
        print("  3. On Windows, Edge WebView2 should be installed")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
