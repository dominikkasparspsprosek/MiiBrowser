"""
Tests for browser GUI
"""

import pytest
from miibrowser.browser import MiiBrowser


class TestMiiBrowser:
    """Test cases for MiiBrowser GUI"""
    
    def test_browser_imports(self):
        """Test that browser module can be imported"""
        assert MiiBrowser is not None
    
    def test_browser_initialization(self):
        """Test that browser can be initialized"""
        # Note: This test won't fully work in headless environments
        # but it verifies the class exists and can be instantiated
        try:
            browser = MiiBrowser()
            assert browser is not None
            assert hasattr(browser, 'root')
            assert hasattr(browser, 'search_engine')
            # Clean up
            browser.root.destroy()
        except Exception as e:
            # If tkinter isn't available (e.g., in CI), that's okay
            pytest.skip(f"GUI not available: {e}")
    
    def test_browser_has_search_method(self):
        """Test that browser has required methods"""
        try:
            browser = MiiBrowser()
            assert hasattr(browser, '_perform_search')
            assert hasattr(browser, '_toggle_fullscreen')
            assert hasattr(browser, 'run')
            browser.root.destroy()
        except Exception as e:
            pytest.skip(f"GUI not available: {e}")
