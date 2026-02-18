"""
Google Fact Check API Integration
"""

import requests
import urllib.parse
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FactCheckAPI:
    def __init__(self):
        self.api_key = config.GOOGLE_FACTCHECK_API_KEY
        self.api_url = config.FACTCHECK_API_URL

    def search_claims(self, query: str) -> list[dict]:
        """
        Search for existing fact checks related to a query/claim
        """
        if not query or not self.api_key:
            return []
            
        try:
            params = {
                "query": query,
                "key": self.api_key,
                "languageCode": "en",
                "pageSize": 3
            }
            
            logger.info(f"Querying Fact Check API for: {query[:30]}...")
            response = requests.get(self.api_url, params=params, timeout=config.REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_response(data)
            else:
                logger.warning(f"Fact Check API Error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Fact Check API call failed: {e}")
            return []

    def _parse_response(self, data: dict) -> list[dict]:
        """Parse API response into standardized format"""
        parsed_results = []
        
        claims = data.get("claims", [])
        for claim in claims:
            # Look at multiple reviews if available
            reviews = claim.get("claimReview", [])
            for review in reviews:
                publisher = review.get("publisher", {}).get("name", "Unknown Publisher")
                rating = review.get("textualRating", "Unknown")
                url = review.get("url", "")
                title = review.get("title", "")
                
                parsed_results.append({
                    "text": claim.get("text", ""),
                    "publisher": publisher,
                    "rating": rating,
                    "url": url,
                    "review_title": title
                })
                
        return parsed_results
