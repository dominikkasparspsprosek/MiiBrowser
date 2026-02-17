"""
Standalone pywebview browser window for MiiBrowser
This runs in a separate process to avoid main thread conflicts
"""

import sys
import webview

def main():
    """Launch a pywebview window with the given URL"""
    if len(sys.argv) < 2:
        print("Usage: python pywebview_window.py <url> [title]")
        sys.exit(1)
    
    url = sys.argv[1]
    title = sys.argv[2] if len(sys.argv) > 2 else "MiiBrowser"
    
    # Create and start webview window
    window = webview.create_window(
        title=title,
        url=url,
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False,
        min_size=(400, 300)
    )
    
    # Start on main thread (required by pywebview)
    webview.start()

if __name__ == "__main__":
    main()
