"""
Semantic Verifier
Uses Sentence-BERT to compare extracted claims with trusted knowledge/sources.
"""

from sentence_transformers import SentenceTransformer, util
import config
from src.utils.logger import get_logger
import torch

logger = get_logger(__name__)

class SemanticVerifier:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = config.SBERT_MODEL_NAME
        self.model = None
        
        self._load_model()

    def _load_model(self):
        """Load Sentence-BERT model"""
        try:
            logger.info(f"Loading Sentence-BERT model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info("Sentence-BERT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Sentence-BERT: {e}")
            raise

    def verify_claims(self, claims: list[str], reliable_sources: list[str]) -> list[dict]:
        """
        Compare extracted claims against a list of reliable source texts/headlines.
        Returns a list of verification results for each claim.
        """
        if not claims or not reliable_sources:
            return []

        results = []
        try:
            # Encode lists
            claim_embeddings = self.model.encode(claims, convert_to_tensor=True)
            source_embeddings = self.model.encode(reliable_sources, convert_to_tensor=True)

            # Compute cosine similarity
            # Output is a matrix [len(claims), len(reliable_sources)]
            cosine_scores = util.cos_sim(claim_embeddings, source_embeddings)

            for i, claim in enumerate(claims):
                # Find the most similar reliable source
                best_match_idx = torch.argmax(cosine_scores[i]).item()
                best_score = cosine_scores[i][best_match_idx].item()
                best_source = reliable_sources[best_match_idx]
                
                status = "Unverified"
                if best_score > 0.75:
                    status = "Verified"
                elif best_score > 0.5:
                    status = "Related"

                results.append({
                    "claim": claim,
                    "match_source": best_source,
                    "similarity_score": float(best_score),
                    "status": status
                })
        except Exception as e:
            logger.error(f"Error in semantic verification: {e}")
            
        return results

    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts"""
        try:
            embeddings1 = self.model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.model.encode(text2, convert_to_tensor=True)
            return util.cos_sim(embeddings1, embeddings2).item()
        except Exception as e:
            logger.error(f"Similarity computation error: {e}")
            return 0.0
