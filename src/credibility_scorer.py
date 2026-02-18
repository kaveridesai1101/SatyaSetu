"""
Credibility Scorer
Calculates the final credibility score based on multiple signals.
"""

from typing import Dict, Any, List
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CredibilityScorer:
    def __init__(self):
        # User Defined Weights
        # (ML*0.5) + (Keyword_Risk*0.15) + (Sentiment*0.10) + (Source*0.15) + (Entity*0.10)
        self.weights = {
            "ml_model": 0.50,
            "keyword_risk": 0.15,
            "sentiment": 0.10,
            "source_credibility": 0.15,
            "entity_verification": 0.10
        }

    def calculate_score(self, 
                        ml_score: float,
                        keyword_risk_score: float,
                        sentiment_risk_score: float,
                        source_score: float,
                        entity_score: float) -> Dict[str, Any]:
        """
        Compute weighted credibility score.
        IMPORTANT: Inputs like 'keyword_risk_score' are RISKS (High=Bad).
        We convert them to SAFETY scores (100 - Risk) for the additive formula.
        """
        
        # Prepare safety metrics (100 - Risk)
        keyword_safety = max(0, 100 - keyword_risk_score)
        sentiment_safety = max(0, 100 - sentiment_risk_score)

        # 1. ML Score (Probability Real 0-100)
        w_ml = ml_score * self.weights["ml_model"]
        
        # 2. Keyword/Linguistic Safety
        w_keyword = keyword_safety * self.weights["keyword_risk"]
        
        # 3. Sentiment Safety
        w_sentiment = sentiment_safety * self.weights["sentiment"]
        
        # 4. Source Credibility (Trust Score 0-100)
        w_source = source_score * self.weights["source_credibility"]
        
        # 5. Entity Verification (Verification Score 0-100)
        w_entity = entity_score * self.weights["entity_verification"]
        
        # FINAL SCORE (Weighted Sum)
        total_score = w_ml + w_keyword + w_sentiment + w_source + w_entity
        actual_final_score = max(0.0, min(100.0, total_score))
        
        # Determine Rating and Aesthetic Color
        if actual_final_score >= 70:
            rating = "Likely Reliable"
            color = "#10B981" # Emerald 500
        elif actual_final_score >= 40:
            rating = "Uncertain / Verification Needed"
            color = "#F59E0B" # Amber 500
        else:
            rating = "Likely Fake / Misleading"
            color = "#EF4444" # Red 500
            
        # Comprehensive breakdown for UI transparency
        analysis_breakdown = {
            "ml_model": round(float(ml_score), 1),
            "keyword_risk": round(float(keyword_safety), 1),
            "sentiment": round(float(sentiment_safety), 1),
            "source": round(float(source_score), 1),
            "entity": round(float(entity_score), 1)
        }

        return {
            "score": round(float(actual_final_score), 1),
            "rating": rating,
            "color": color,
            "breakdown": analysis_breakdown
        }
