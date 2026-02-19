"""
Article Summarizer
Generates concise, trustworthy summaries using abstractive summarization.
"""

from transformers import pipeline
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Summarizer:
    def __init__(self):
        self.model_name = "sshleifer/distilbart-cnn-6-6" # Ultra-fast distillation
        self.pipeline = None
        self._load_model()
        
    def _load_model(self):
        try:
            logger.info(f"Loading Summarization model: {self.model_name}")
            self.pipeline = pipeline(
                "summarization", 
                model=self.model_name,
                device=-1 # CPU
            )
        except Exception as e:
            logger.error(f"Failed to load summarizer: {e}")
            
    def generate_summary(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Generate summary of the text
        """
        if not text or not self.pipeline:
            return "Summary unavailable."
            
        try:
            # Handle text length limitations of the model
            input_len = len(text.split())
            if input_len < 30:
                return text # Too short to summarize
                
            # Truncate input to model's likely max limit (~1024 tokens)
            # Rough char limit 4000
            input_text = text[:4000]
            
            summary_output = self.pipeline(
                input_text, 
                max_length=max_length, 
                min_length=min_length, 
                do_sample=False
            )
            
            return summary_output[0]['summary_text']
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            return "Error generating summary."
