"""
Bias and Sentiment Analyzer
Analyzes text for emotional tone, political bias indicators, and sensationalism.
"""

from transformers import pipeline
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BiasSentimentAnalyzer:
    def __init__(self):
        self.sentiment_model = "distilbert-base-uncased-finetuned-sst-2-english"
        self.pipeline = None
        self._load_model()
        
        # Heuristic lists for bias/sensationalism (Simplified for efficacy vs efficiency)
        self.sensational_words = {
            "shocking", "unbelievable", "mind-blowing", "secret", "exposed", 
            "breaking", "urgent", "you won't believe", "miracle", "cure",
            "conspiracy", "mainstream media", "hidden agenda", "destroy"
        }

    def _load_model(self):
        try:
            logger.info("Loading Sentiment Analysis pipeline...")
            self.pipeline = pipeline(
                "sentiment-analysis", 
                model=self.sentiment_model,
                device=-1 # CPU for this lighter model to save GPU for DeBERTa
            )
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            self.pipeline = None
            
    def analyze(self, text: str) -> dict:
        """
        Analyze text for sentiment and sensationalism
        """
        if not text:
            return {}
            
        result = {
            "sentiment": "Neutral",
            "sentiment_score": 0.0,
            "sensationalism_score": 0.0,
            "bias_label": "Unknown"
        }
        
        # 1. Sentiment Analysis
        if self.pipeline:
            try:
                # Truncate to 512 tokens for distilbert
                short_text = text[:1500] 
                res = self.pipeline(short_text)[0]
                result["sentiment"] = res["label"] # POSITIVE / NEGATIVE
                result["sentiment_score"] = res["score"]
                
                # Risk Logic: Extreme sentiment (very close to 1.0) is suspicious
                # If score > 0.95 (Positive or Negative), it's highly emotional
                result["sentiment_intensity"] = res["score"]
            except Exception as e:
                logger.error(f"Sentiment analysis failed: {e}")
        
        # 2. Sensationalism Score (Heuristic)
        words = text.lower().split()
        word_count = len(words)
        if word_count > 0:
            match_count = sum(1 for w in words if w in self.sensational_words)
            # Normalize: matches per 100 words
            result["sensationalism_score"] = min(1.0, (match_count / word_count) * 10) 
            
        # 3. Combined Risk Calculation
        # Risk is higher if Sensationalism is high OR Sentiment is extreme
        # Heuristic: Risk = (Sensationalism * 0.7) + (SentimentIntensity > 0.9 ? 0.3 : 0)
        
        sentiment_risk = 0.0
        if result.get("sentiment_intensity", 0) > 0.9:
            sentiment_risk = 1.0
            
        final_risk = (result["sensationalism_score"] * 0.7) + (sentiment_risk * 0.3)
        result["risk_score"] = min(1.0, final_risk) * 100 # 0-100 scale
            
        return result
