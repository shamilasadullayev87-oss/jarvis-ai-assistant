"""
Browser Control - Web Automation
"""

import logging
import webbrowser

logger = logging.getLogger(__name__)

class BrowserControl:
    def search_google(self, query: str):
        """Search Google"""
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Search error: {e}")
    
    def open_youtube(self, query: str):
        """Open YouTube"""
        try:
            if query.strip():
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            else:
                url = "https://www.youtube.com"
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"YouTube error: {e}")
