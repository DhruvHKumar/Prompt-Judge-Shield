# app/services/guardrails/input_validation.py

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any

class InputValidationResult(BaseModel):
    is_valid: bool
    message: str = "Input is valid."
    errors: Optional[List[Dict[str, Any]]] = None

def validate_text_input(text: str, min_length: int = 1, max_length: int = 500) -> InputValidationResult:
    """
    Validates a generic text input based on length constraints.
    """
    error_list = []
    if not isinstance(text, str):
        error_list.append({"loc": ("text",), "msg": "Input must be a string.", "type": "type_error"})
    if len(text) < min_length:
        error_list.append({"loc": ("text",), "msg": f"Input must be at least {min_length} characters long.", "type": "value_error.str.min_length"})
    if len(text) > max_length:
        error_list.append({"loc": ("text",), "msg": f"Input must not exceed {max_length} characters.", "type": "value_error.str.max_length"})

    if error_list:
        return InputValidationResult(is_valid=False, message="Input validation failed.", errors=error_list)
    return InputValidationResult(is_valid=True)

# Example of a more specific validation using Pydantic for a request model
class GuardrailInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=500, description="The user prompt to be analyzed.")
    user_id: Optional[str] = Field(None, description="Optional user identifier.")

def validate_guardrail_input(data: dict) -> InputValidationResult:
    """
    Validates the incoming request data against the GuardrailInput schema.
    """
    try:
        GuardrailInput(**data)
        return InputValidationResult(is_valid=True)
    except ValidationError as e:
        return InputValidationResult(is_valid=False, message="Schema validation failed.", errors=e.errors())