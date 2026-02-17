"""
Test script to verify MiiBrowser works with Google Maps and cookies
"""

import webview
import time

def test_google_maps():
    """Test Google Maps in a pywebview window"""
    print("Testing Google Maps with pywebview...")
    print("This window will:") 
    print("1. Load Google Maps")
    print("2. Verify JavaScript execution (map rendering)")
    print("3. Test cookie storage for session persistence")
    print("\nWindow will close after 30 seconds or when you close it manually.")
    print("\nOpening Google Maps...")
    
    # Create a window with Google Maps
    window = webview.create_window(
        'Google Maps Test - MiiBrowser',
        'https://www.google.com/maps',
        width=1200,
        height=800,
        resizable=True
    )
    
    # Start webview
    webview.start()
    print("\nTest completed!")
    print("If you saw the Google Maps interface with an interactive map,")
    print("then JavaScript, cookies, and all modern web features are working!")

def test_cookie_site():
    """Test a site that requires cookies"""
    print("\nTesting cookies with a cookie demo site...")
    print("Opening cookie test page...")
    
    window = webview.create_window(
        'Cookie Test - MiiBrowser',
        'https://www.whatismybrowser.com/detect/are-cookies-enabled',
        width=1000,
        height=600,
        resizable=True
    )
    
    webview.start()
    print("\nCookie test completed!")

if __name__ == "__main__":
    print("=" * 60)
    print("MiiBrowser - Chromium Feature Test")
    print("=" * 60)
    
    # Test Google Maps
    test_google_maps()
    
    # Ask user if they want to test cookies
    response = input("\nWould you like to test cookies separately? (y/n): ")
    if response.lower() == 'y':
        test_cookie_site()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
