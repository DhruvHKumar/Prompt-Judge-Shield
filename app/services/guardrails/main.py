# app/services/guardrails/main.py

from pydantic import BaseModel
from typing import Optional, Dict, Any

from .input_validation import validate_guardrail_input, InputValidationResult
from .content_moderation import moderate_content, ContentModerationResult
from .prompt_injection import analyze_prompt_for_injection, PromptInjectionResult

class GuardrailResult(BaseModel):
    status: str  # e.g., "SAFE", "BLOCKED"
    error_type: Optional[str] = None  # e.g., "InputValidationError", "ContentModerationError"
    details: Dict[str, Any] = {}

def run_guardrails(request_data: dict) -> GuardrailResult:
    """
    Orchestrates the execution of all guardrail checks.
    """
    # 1. Input Validation
    validation_result = validate_guardrail_input(request_data)
    if not validation_result.is_valid:
        return GuardrailResult(
            status="BLOCKED",
            error_type="InputValidationError",
            details={"validation_errors": validation_result.errors}
        )

    prompt = request_data.get("prompt", "")

    # 2. Content Moderation
    moderation_result = moderate_content(prompt)
    if not moderation_result.is_safe:
        return GuardrailResult(
            status="BLOCKED",
            error_type="ContentModerationError",
            details={
                "flagged_categories": moderation_result.flagged_categories,
                "moderation_details": moderation_result.details
            }
        )

    # 3. Prompt Injection
    injection_result = analyze_prompt_for_injection(prompt)
    if injection_result.classification == "INJECTION_ATTEMPT":
        return GuardrailResult(
            status="BLOCKED",
            error_type="PromptInjectionError",
            details={
                "risk_score": injection_result.risk_score,
                "injection_details": injection_result.details
            }
        )

    return GuardrailResult(
        status="SAFE",
        details={
            "validation": validation_result.model_dump(),
            "moderation": moderation_result.model_dump(),
            "injection": injection_result.model_dump()
        }
    )