"""
Search module using DuckDuckGo API
"""

import requests
from typing import List, Dict
import json


class DuckDuckGoSearch:
    """Handle DuckDuckGo search queries"""
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.instant_answer_url = "https://html.duckduckgo.com/html/"
    
    def search(self, query: str) -> List[Dict[str, str]]:
        """
        Search using DuckDuckGo API
        
        Args:
            query: Search query string
            
        Returns:
            List of search results with title, url, and description
        """
        try:
            # DuckDuckGo Instant Answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Parse AbstractText
            if data.get('AbstractText'):
                results.append({
                    'title': data.get('Heading', 'Result'),
                    'url': data.get('AbstractURL', ''),
                    'description': data.get('AbstractText', '')
                })
            
            # Parse RelatedTopics
            for topic in data.get('RelatedTopics', [])[:10]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('Text', '')[:100],
                        'url': topic.get('FirstURL', ''),
                        'description': topic.get('Text', '')
                    })
            
            # If no results from instant answer, return a basic result
            if not results:
                results.append({
                    'title': f'Search: {query}',
                    'url': f'https://html.duckduckgo.com/html/?q={query}',
                    'description': f'Click to search "{query}" on DuckDuckGo'
                })
            
            return results
            
        except requests.exceptions.RequestException as e:
            return [{
                'title': 'Error',
                'url': '',
                'description': f'Search failed: {str(e)}'
            }]
    
    def is_online(self) -> bool:
        """Check if internet connection is available"""
        try:
            response = requests.get('https://www.duckduckgo.com', timeout=5)
            return response.status_code == 200
        except:
            return False
