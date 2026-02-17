"""
Quick verification script to test if the package structure is correct
"""

import sys
import os

# Add src to path for testing without installation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Test imports
    from miibrowser import MiiBrowser, __version__, __author__
    from miibrowser.search import DuckDuckGoSearch
    from miibrowser.browser import MiiBrowser as Browser
    
    print("✓ All imports successful!")
    print(f"✓ Package version: {__version__}")
    print(f"✓ Author: {__author__}")
    print("✓ DuckDuckGoSearch class available")
    print("✓ MiiBrowser class available")
    print("\n✅ Package structure is correct!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
