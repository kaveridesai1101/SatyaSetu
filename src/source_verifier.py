"""
Source Verifier (Layer 6)
Checks source credibility against trusted and suspicious domain lists.
"""

from urllib.parse import urlparse
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SourceVerifier:
    def __init__(self):
        # 🛡️ Trusted Domains (White-list)
        self.trusted_domains = {
            "reuters.com", "apnews.com", "bbc.com", "npr.org", "pbs.org",
            "nytimes.com", "washingtonpost.com", "wsj.com", "ft.com", "economist.com",
            "bloomberg.com", "theguardian.com", "snopes.com", "factcheck.org",
            "politifact.com", "nasa.gov", "who.int", "cdc.gov", "nih.gov", "un.org"
        }

        # 🚩 Suspicious Domains (Black-list / Satire)
        self.suspicious_domains = {
            "theonion.com", "babylonbee.com", "infowars.com", "naturalnews.com",
            "zerohedge.com", "breitbart.com", "sputniknews.com", "rt.com",
            "dailymail.co.uk", "newspunch.com", "beforeitsnews.com"
        }

    def verify_source(self, url: str) -> dict:
        """
        Analyze the credibility of a source URL.
        """
        if not url:
            return {"score": 50.0, "status": "Unknown", "domain": None}

        domain = self._extract_domain(url)
        
        if not domain:
            return {"score": 50.0, "status": "Invalid URL", "domain": None}

        # Check Trust Lists
        if any(domain.endswith(trusted) for trusted in self.trusted_domains):
            return {"score": 100.0, "status": "Trusted Source", "domain": domain}
        
        if any(domain.endswith(sus) for sus in self.suspicious_domains):
            return {"score": 0.0, "status": "Suspicious/Satire", "domain": domain}

        # Neutral / Unknown
        return {"score": 50.0, "status": "Unverified Source", "domain": domain}

    def _extract_domain(self, url: str) -> str:
        try:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path
            return domain.lower().replace("www.", "")
        except:
            return None
