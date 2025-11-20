# app/api/v1/schemas/guardrails.py

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class GuardrailRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500, description="The user prompt to be analyzed.")
    user_id: Optional[str] = Field(None, description="Optional user identifier.")

class GuardrailResponse(BaseModel):
    status: str
    error_type: Optional[str] = None
    details: Dict[str, Any]