"""
DeBERTa Fake News Classifier
Wrapper for the Hugging Face Transformers DeBERTa-v3 model
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import config
from src.utils.logger import get_logger
import os

logger = get_logger(__name__)

class DebertaClassifier:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = config.DEBERTA_MODEL_NAME
        self.tokenizer = None
        self.model = None
        
        self._load_model()

    def _load_model(self):
        """Load model and tokenizer"""
        try:
            logger.info(f"Loading DeBERTa model: {self.model_name} on {self.device}")
            
            # Using a simplified approach: In a real scenario, this would load a FINE-TUNED model
            # For this codebase, we will initialize the base model related to fake news if available
            # or default to the config content.
            # Ideally, we would load from a local path `config.MODEL_CACHE_DIR` if saved.
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Note: In a production app, we would load a model trained specifically for 2 labels (Fake, Real)
            # Here we initialize with 2 labels for demonstration. 
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name, 
                num_labels=2,
                ignore_mismatched_sizes=True
            )
            
            self.model.to(self.device)
            self.model.eval() # Set to evaluation mode
            
            logger.info("DeBERTa model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load DeBERTa model: {e}")
            raise

    def predict(self, text: str) -> dict:
        """
        Classify text as Fake or Real
        Returns dictionary with probabilities and label
        """
        if not text:
            return {"label": "Error", "score": 0.0, "fake_prob": 0.0, "real_prob": 0.0}
            
        try:
            # Tokenize
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512,
                padding=True
            ).to(self.device)
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = F.softmax(logits, dim=1)
            
            # Map output to labels (Assuming 0=Fake, 1=Real for this specific mapping, 
            # this often depends on the training dataset. We'll standardise 0=Fake, 1=Real)
            fake_prob = probs[0][0].item()
            real_prob = probs[0][1].item()
            
            label = "Real" if real_prob > fake_prob else "Fake"
            score = max(fake_prob, real_prob)
            
            result = {
                "label": label,
                "confidence": score,
                "fake_prob": fake_prob,
                "real_prob": real_prob
            }
            
            logger.debug(f"Prediction result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"label": "Error", "score": 0.0, "fake_prob": 0.0, "real_prob": 0.0}

    def get_tokenizer(self):
        return self.tokenizer
        
    def get_model(self):
        return self.model
