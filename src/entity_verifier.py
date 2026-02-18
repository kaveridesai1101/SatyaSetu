"""
Entity Verifier (Layer 5)
Extracts and verifies named entities (People, Orgs, Locs) to check context validity.
"""

from src.utils.logger import get_logger

logger = get_logger(__name__)

class EntityVerifier:
    def __init__(self):
        # In a real system, this would connect to a Knowledge Graph (Wikidata/Google KG)
        # For this standalone version, we use heuristics and simulation.
        pass

    def verify_entities(self, entities: list) -> dict:
        """
        Analyze extracted entities.
        Entities should be a list of tuples: [(text, label), ...] from spaCy.
        """
        if not entities:
            # No entities mentioned might be suspicious for news
            return {"score": 40.0, "reason": "No specific entities mentioned (vague)."}

        # Filter relevant types
        relevant_ents = [e for e in entities if e[1] in ["ORG", "PERSON", "GPE", "LOC"]]
        
        if not relevant_ents:
             return {"score": 50.0, "reason": "No verifies people or organizations found."}

        # Simulation Logic:
        # If entities match known "high credibility" anchors (simulated list), boost score.
        # Use a small set of universally known entities to demonstrate logic.
        known_anchors = {
            "WHO", "NASA", "CDC", "UN", "FBI", "Apple", "Google", "Microsoft",
            "White House", "Parliament", "Supreme Court", "BBC", "CNN"
        }
        
        matches = [e[0] for e in relevant_ents if any(k in e[0] for k in known_anchors)]
        
        if matches:
            return {
                "score": 80.0,
                "reason": f"References recognized entities: {', '.join(matches[:3])}",
                "entity_count": len(relevant_ents)
            }

        # Fallback for unknown entities (Neutral)
        return {
            "score": 60.0, 
            "reason": f"Contains specific entities ({len(relevant_ents)} found), but unverified context.",
            "entity_count": len(relevant_ents)
        }
