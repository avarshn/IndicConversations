import requests
import logging

logger = logging.getLogger(__name__)

class WikipediaAPI:
    """Clean Wikipedia API wrapper - no scraping needed!"""
    
    BASE_URL = "https://en.wikipedia.org/w/api.php"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_page_content(self, url_or_title):
        """
        Get Wikipedia page content using the official API.
        
        Args:
            url_or_title (str): Wikipedia URL or page title
                              e.g., "https://en.wikipedia.org/wiki/Python_(programming_language)"
                              or "Python (programming language)"
            
        Returns:
            dict: Page content and metadata
        """
        # Step 1: Extract title from URL if URL is provided
        if url_or_title.startswith("http"):
            # Parse the title from URL
            # e.g., https://en.wikipedia.org/wiki/Python_(programming_language)
            title = url_or_title.split("/wiki/")[-1]
            # URL decode the title
            import urllib.parse
            title = urllib.parse.unquote(title)
        else:
            title = url_or_title

        logger.info("Extracted title: '%s'", title)

        # Step 2: Call Wikipedia API
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": False     # If False -> Keep HTML to preserve tables/infoboxes
        }

        # Add headers to avoid 403 error
        headers = {
            "User-Agent": "WikipediaBot/1.0 (Educational purposes; your_email@example.com)"
        }

        response = requests.get(self.BASE_URL, params=params, headers=headers)

        # Step 3: Get the data
        data = response.json()

        # Step 4: Extract the content
        pages = data["query"]["pages"]
        page = next(iter(pages.values()))       # page_id = list(pages.keys())[0]  , and then  page = pages[page_id]
        
        if "missing" in page:
            return {"error": f"Page '{title}' not found"}
        
        return {
            "title": page.get("title"),
            "page_id": page.get("pageid"),
            "url": page.get("fullurl"),
            "content": page.get("extract", ""),
            "word_count": len(page.get("extract", "").split())
        }
