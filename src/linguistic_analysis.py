"""
Linguistic Analyzer (Layer 2)
Detects "Red Flags" using rule-based stylistic analysis.
"""

import re
import textstat
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LinguisticAnalyzer:
    def __init__(self):
        # 🚩 1. Extreme Claims / Absolutism
        self.extreme_patterns = [
            r"100% cure", r"miracle cure", r"guaranteed", r"secret exposed", 
            r"hidden truth", r"shocking revelation", r"once in a lifetime",
            r"doctors hate this", r"banned by", r"proven"
        ]
        
        # 🚩 4. Conspiracy Language
        self.conspiracy_patterns = [
            r"they don't want you to know", r"mainstream media", r"deep state",
            r"new world order", r"globalist", r"agenda", r"hoax", r"plandemic",
            r"sheeple", r"wake up"
        ]

    def analyze(self, text: str) -> dict:
        """
        Analyze text for linguistic red flags.
        Returns a dictionary with scores and details.
        """
        if not text:
            return {"risk_score": 0.0, "details": [], "readability": 0.0}

        flags = []
        score = 0.0
        
        # 1. Check Extreme Claims
        extreme_matches = [p for p in self.extreme_patterns if re.search(p, text, re.IGNORECASE)]
        if extreme_matches:
            score += 20 * len(extreme_matches) # 20 points per match
            flags.append(f"Contains extreme claims: {', '.join(extreme_matches)}")

        # 2. Check Conspiracy Language
        conspiracy_matches = [p for p in self.conspiracy_patterns if re.search(p, text, re.IGNORECASE)]
        if conspiracy_matches:
            score += 25 * len(conspiracy_matches)
            flags.append(f"Uses conspiracy terminology: {', '.join(conspiracy_matches)}")

        # 3. Excessive Capitalization (SHOUTING)
        caps_ratio = self._calculate_caps_ratio(text)
        if caps_ratio > 0.15: # If > 15% of text is CAPS (excluding common proper nouns heuristic sort of)
             score += 15
             flags.append("Excessive use of Capital Letters")

        # 4. Exclamation Mark Abuse !!!
        exc_count = text.count("!")
        if exc_count > 3:
            score += 10
            flags.append("Excessive exclamation marks")

        # 🧠 Advanced Add-On: Readability Score
        # Fake news often has lower readability (simple, emotional)
        try:
            readability = textstat.flesch_reading_ease(text)
            # Flesch Score: 90-100 (Very Easy), 0-30 (Very Confusing)
            # If extremely simple and high risk elsewhere -> suspicious
            # We won't add to score directly but return it
        except:
            readability = 50.0

        # Normalize score (Risk Score 0-100)
        final_risk = min(100.0, score)

        return {
            "risk_score": final_risk,
            "linguistic_flags": flags,
            "readability_score": readability,
            "caps_ratio": caps_ratio
        }

    def _calculate_caps_ratio(self, text: str) -> float:
        clean_text = re.sub(r'[^a-zA-Z]', '', text)
        if not clean_text:
            return 0.0
        caps_count = sum(1 for c in clean_text if c.isupper())
        return caps_count / len(clean_text)
