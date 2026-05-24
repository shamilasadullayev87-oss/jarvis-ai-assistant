"""
News Reader - Real-time News Updates
"""

import logging
import os
import requests
from typing import List

logger = logging.getLogger(__name__)

class NewsReader:
    def __init__(self):
        """Initialize news reader"""
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def get_top_headlines(self, count: int = 5) -> List[str]:
        """Get top headlines"""
        try:
            if not self.api_key or self.api_key == "your_key_here":
                logger.warning("NEWS_API_KEY not configured")
                return []
            
            url = f"{self.base_url}/top-headlines"
            params = {
                "country": os.getenv("NEWS_COUNTRY", "us"),
                "apiKey": self.api_key,
                "pageSize": count
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            headlines = []
            
            for article in data.get("articles", []):
                headlines.append(article["title"])
            
            return headlines
        
        except Exception as e:
            logger.error(f"News fetch error: {e}")
            return []
    
    def search_news(self, query: str) -> List[str]:
        """Search news by keyword"""
        try:
            if not self.api_key or self.api_key == "your_key_here":
                return []
            
            url = f"{self.base_url}/everything"
            params = {
                "q": query,
                "apiKey": self.api_key,
                "pageSize": 5,
                "sortBy": "publishedAt"
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            headlines = [article["title"] for article in data.get("articles", [])]
            
            return headlines
        
        except Exception as e:
            logger.error(f"News search error: {e}")
            return []
