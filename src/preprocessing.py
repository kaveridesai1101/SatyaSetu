"""
Text Preprocessing Module
Uses spaCy for text cleaning, tokenization, and normalization
"""

import spacy
import re
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TextPreprocessor:
    def __init__(self):
        """Initialize spaCy model"""
        try:
            # Try to load the model, download if missing
            if not spacy.util.is_package(config.SPACY_MODEL):
                spacy.cli.download(config.SPACY_MODEL)
            self.nlp = spacy.load(config.SPACY_MODEL)
            logger.info(f"Loaded spaCy model: {config.SPACY_MODEL}")
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            raise RuntimeError("NLP model initialization failed")

    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning:
        - Remove extra whitespace
        - Remove URLs (optional, sometimes useful to keep domains)
        - Fix encoding issues
        """
        if not text:
            return ""
            
        # 1. Remove URLs (and store them? Caller should extract first if needed)
        text = re.sub(r'http\S+|www\.\S+', '', text)
            
        # 2. Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 3. Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # 4. Remove special characters (keep punctuation for sentence segmentation if needed, 
        # but for pure ML/cleaning we often remove them. Keeping basic sentence structure for now)
        # text = re.sub(r'[^a-zA-Z0-9\s.]', '', text) 
        
        return text.lower() # Enforce lowercase as per Step 1

    def extract_urls(self, text: str) -> list[str]:
        """Extract all URLs from text before cleaning"""
        return re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    def clean_and_tokenize(self, text: str) -> str:
        """
        Full preprocessing pipeline:
        - Clean text
        - Remove stopwords and punctuation
        - Lemmatize tokens
        Returns cleaned string associated with tokens
        """
        text = self.clean_text(text)
        doc = self.nlp(text)
        
        # Keep only alphabetic tokens, remove stopwords
        tokens = [
            token.lemma_.lower() 
            for token in doc 
            if not token.is_stop and not token.is_punct and token.is_alpha
        ]
        
        return " ".join(tokens)

    def extract_claims(self, text: str) -> list[str]:
        """
        Extract sentences that look like factual claims
        Uses dependency parsing and entity recognition
        """
        doc = self.nlp(self.clean_text(text))
        claims = []
        
        for sent in doc.sents:
            # Heuristic: Sentences with entities and a verb are more likely to be claims
            has_entity = len(sent.ents) > 0
            has_verb = any(token.pos_ == "VERB" for token in sent)
            
            # Filter short sentences
            if len(sent) > 5 and (has_entity or has_verb):
                claims.append(sent.text)
                
        return claims

    def get_entities(self, text: str) -> list[tuple]:
        """Extract Named Entities"""
        doc = self.nlp(self.clean_text(text))
        return [(ent.text, ent.label_) for ent in doc.ents]
