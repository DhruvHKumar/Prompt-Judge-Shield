# app/services/guardrails/prompt_injection.py

from pydantic import BaseModel
from typing import List, Dict

# This is the same keyword-based detection logic from the original detection_service.py
INJECTION_KEYWORDS = {
    "ignore your previous instructions": 1.0,
    "ignore your previous instruction": 1.0,
    "disregard the above": 1.0,
    "you are now in developer mode": 0.8,
    "act as": 0.5,
    "confidential": 0.3,
    "system prompt": 0.5,
    "jailbreak": 0.8,
    "dan": 0.8,
    "ignore": 0.2,
    "forget": 0.2,
    "pretend": 0.2,
    "imagine you are my grandma": 0.3,
    "sudo mode": 0.8,
    "do anything now": 0.8,
    "start a new conversation": 0.6,
    "playing a role": 0.6,
    "simulate": 0.6,
    "bypass": 0.6,
    "rules": 0.4,
}

class PromptInjectionResult(BaseModel):
    classification: str
    risk_score: float
    details: Dict[str, List[str]]

def analyze_prompt_for_injection(prompt: str) -> PromptInjectionResult:
    """
    Analyzes a prompt for potential injection attacks based on a set of heuristics.
    """
    risk_score = 0.0
    prompt_lower = prompt.lower()
    
    found_keywords = []
    for keyword, weight in INJECTION_KEYWORDS.items():
        if keyword in prompt_lower:
            risk_score += weight
            found_keywords.append(keyword)

    risk_score = min(risk_score, 1.0)

    classification = "SAFE"
    if risk_score > 0.5:
        classification = "INJECTION_ATTEMPT"
        
    return PromptInjectionResult(
        classification=classification,
        risk_score=risk_score,
        details={"found_keywords": found_keywords}
    )