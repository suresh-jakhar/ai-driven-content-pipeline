from config import SCORE_WEIGHTS
import re

def evaluate_quality(original, reviewed):
    """Evaluate chapter quality using heuristic scoring"""
    # Heuristic scoring
    scores = {
        "grammar": min(10, 10 - (len(re.findall(r'\b(?:am|is|are|was|were|be|being|been)\b', reviewed)) / 50)),
        "clarity": min(10, (len(reviewed) / max(1, len(original))) * 2),
        "structure": min(10, reviewed.count('\n\n') / 5),
        "faithfulness": min(10, 10 - (len(set(original.split()) - set(reviewed.split())) / 100)),
        "fluency": min(10, (len(reviewed.split()) / len(original.split())) * 5)
    }
    
    # Calculate total score
    total = sum(scores[category] * weight * 2 
               for category, weight in SCORE_WEIGHTS.items())
    
    return {
        "scores": scores,
        "total_score": round(total, 2),
        "notes": "Evaluated using heuristic rules"
    }