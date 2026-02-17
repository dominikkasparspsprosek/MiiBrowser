"""
Tests for DuckDuckGo search module
"""

import pytest
from miibrowser.search import DuckDuckGoSearch


class TestDuckDuckGoSearch:
    """Test cases for DuckDuckGo search functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.search_engine = DuckDuckGoSearch()
    
    def test_search_engine_initialization(self):
        """Test that search engine initializes correctly"""
        assert self.search_engine is not None
        assert hasattr(self.search_engine, 'base_url')
        assert 'duckduckgo.com' in self.search_engine.base_url
    
    def test_search_returns_list(self):
        """Test that search returns a list"""
        results = self.search_engine.search("python programming")
        assert isinstance(results, list)
        assert len(results) > 0
    
    def test_search_result_structure(self):
        """Test that search results have correct structure"""
        results = self.search_engine.search("python")
        
        for result in results:
            assert isinstance(result, dict)
            assert 'title' in result
            assert 'url' in result
            assert 'description' in result
    
    def test_empty_search_query(self):
        """Test search with empty query"""
        results = self.search_engine.search("")
        assert isinstance(results, list)
    
    def test_is_online_method_exists(self):
        """Test that is_online method exists"""
        assert hasattr(self.search_engine, 'is_online')
        assert callable(self.search_engine.is_online)
