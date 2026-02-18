"""
SHAP Explainability Module
Generates model explanations to highlight which parts of text contributed to fake/real classification.
"""

import shap
import torch
import numpy as np
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ExplainabilityEngine:
    def __init__(self, classifier_model, tokenizer):
        """
        Initialize SHAP explainer
        Args:
            classifier_model: The loaded DeBERTa model
            tokenizer: The DeBERTa tokenizer
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = classifier_model
        self.tokenizer = tokenizer
        self.explainer = None
        
        # We initialize explainer lazily or here
        try:
            # We construct a prediction pipeline function for SHAP
            # SHAP works best with a callable that takes strings and returns probabilities
            self._init_explainer()
        except Exception as e:
            logger.error(f"Failed to init SHAP: {e}")

    def _predictor(self, texts):
        """
        Wrapper function for the model to be compatible with SHAP
        Input: list of strings
        Output: numpy array of probabilities
        """
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]
            
        inputs = self.tokenizer(
            texts, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            
        return probs.cpu().numpy()

    def _init_explainer(self):
        """
        Initialize the Partition Explainer (good for text) or similar.
        Note: DeepExplainer or similar might be heavy. 
        We use the generic Explainer which usually picks PartitionExplainer for text.
        """
        # SHAP's text explainer needs a masker. 
        # For transformers, it can use the tokenizer as masker.
        logger.info("Initializing SHAP Explainer...")
        self.explainer = shap.Explainer(
            self._predictor, 
            self.tokenizer
        )

    def explain(self, text: str):
        """
        Generate SHAP values for the given text.
        Returns the shap_values object which can be visualized.
        """
        if not text or not self.explainer:
            return None
            
        try:
            # Limit text length to avoid memory issues on large explainers
            short_text = text[:1000] if len(text) > 1000 else text
            shap_values = self.explainer([short_text])
            return shap_values
        except Exception as e:
            logger.error(f"SHAP explanation failed: {e}")
            return None

    def get_html_plot(self, shap_values):
        """
        Generate HTML visualization of the SHAP values
        """
        if shap_values is None:
            return "<div><p>Explanation unavailable</p></div>"
        
        try:
            # force_plot returns HTML javascript
            # We use shap.plots.text which is better for NLP
            # but it returns HTML wrapped in IFrame typically.
            # We can extract the HTML string from shap.plots.text calls if we render to string.
            # A simpler way for Streamlit is to use shap.plots.force and save/render html.
            
            # For this implementation we will return the shap_values object 
            # and handle rendering in Streamlit using st_shap or custom component
            pass
        except Exception as e:
            logger.error(f"Plot generation failed: {e}")
            return ""
