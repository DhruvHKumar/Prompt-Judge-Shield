# app/services/guardrails/content_moderation.py

from pydantic import BaseModel
from typing import List, Dict

# A simple list of keywords for content moderation.
# In a real-world scenario, this would be a more sophisticated system,
# possibly using a third-party API or a machine learning model.
MODERATION_KEYWORDS = {
    "hate_speech": ["hate", "kill", "despise"],
    "violence": ["violence", "attack", "brutality"],
    "self_harm": ["suicide", "self-harm", "depressed"],
}

class ContentModerationResult(BaseModel):
    is_safe: bool
    flagged_categories: List[str] = []
    details: Dict[str, List[str]] = {}

def moderate_content(text: str) -> ContentModerationResult:
    """
    Analyzes text for inappropriate content based on a keyword list.
    """
    text_lower = text.lower()
    flagged_categories = []
    details = {}

    for category, keywords in MODERATION_KEYWORDS.items():
        found_keywords = [kw for kw in keywords if kw in text_lower]
        if found_keywords:
            flagged_categories.append(category)
            details[category] = found_keywords

    if flagged_categories:
        return ContentModerationResult(is_safe=False, flagged_categories=flagged_categories, details=details)
    
    return ContentModerationResult(is_safe=True)