from fastapi import APIRouter, HTTPException
from app.api.v1.schemas.injection import PromptRequest, PromptResponse
from app.services.guardrails.main import run_guardrails

router = APIRouter()

@router.post("/detect", response_model=PromptResponse)
def detect_injection(request: PromptRequest):
    """
    Analyzes a prompt for potential injection attacks using the guardrails service.
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

    # If safe, return the injection analysis details
    injection_details = guardrail_result.details.get("injection", {})
    return PromptResponse(
        prompt=request.prompt,
        classification=injection_details.get("classification", "SAFE"),
        risk_score=injection_details.get("risk_score", 0.0)
    )