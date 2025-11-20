# app/api/v1/endpoints/guardrails.py

from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.guardrails import GuardrailRequest, GuardrailResponse
from app.services.guardrails.main import run_guardrails

router = APIRouter()

@router.post("/check", response_model=GuardrailResponse)
def check_guardrails(request: GuardrailRequest):
    """
    Runs a comprehensive check of all guardrails on a given prompt.
    """
    guardrail_result = run_guardrails(request.model_dump())

    if guardrail_result.status == "BLOCKED":
        status_code = 400
        if guardrail_result.error_type in ["ContentModerationError", "PromptInjectionError"]:
            status_code = 403
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "error_type": guardrail_result.error_type,
                "message": f"Request blocked by {guardrail_result.error_type}",
                "details": guardrail_result.details
            }
        )

    return GuardrailResponse(
        status=guardrail_result.status,
        details=guardrail_result.details
    )