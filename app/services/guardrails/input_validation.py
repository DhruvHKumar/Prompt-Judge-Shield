# app/services/guardrails/input_validation.py

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, List, Dict, Any

import tiktoken

class InputValidationResult(BaseModel):
    is_valid: bool
    message: str = "Input is valid."
    errors: Optional[List[Dict[str, Any]]] = None

def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def validate_text_input(text: str, min_length: int = 1, max_length: int = 500, max_tokens: int = 5000) -> InputValidationResult:
    """
    Validates a generic text input based on length constraints and token limits.
    """
    error_list = []
    if not isinstance(text, str):
        error_list.append({"loc": ("text",), "msg": "Input must be a string.", "type": "type_error"})
        return InputValidationResult(is_valid=False, message="Input validation failed.", errors=error_list)

    if len(text) < min_length:
        error_list.append({"loc": ("text",), "msg": f"Input must be at least {min_length} characters long.", "type": "value_error.str.min_length"})
    if len(text) > max_length:
        error_list.append({"loc": ("text",), "msg": f"Input must not exceed {max_length} characters.", "type": "value_error.str.max_length"})
    
    # Token limit check
    token_count = count_tokens(text)
    if token_count > max_tokens:
        error_list.append({"loc": ("text",), "msg": f"Input exceeds token limit of {max_tokens} (found {token_count}).", "type": "value_error.str.max_tokens"})

    if error_list:
        return InputValidationResult(is_valid=False, message="Input validation failed.", errors=error_list)
    return InputValidationResult(is_valid=True)

# Example of a more specific validation using Pydantic for a request model
class GuardrailInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=20000, description="The user prompt to be analyzed.") # Increased max_length to allow for token check
    user_id: Optional[str] = Field(None, description="Optional user identifier.")

def validate_guardrail_input(data: dict) -> InputValidationResult:
    """
    Validates the incoming request data against the GuardrailInput schema.
    """
    try:
        input_data = GuardrailInput(**data)
        # Additional token check for the prompt field
        token_count = count_tokens(input_data.prompt)
        if token_count > 5000: # Hardcoded limit for now, could be config
             return InputValidationResult(
                is_valid=False, 
                message="Input validation failed.", 
                errors=[{"loc": ("prompt",), "msg": f"Input exceeds token limit of 5000 (found {token_count}).", "type": "value_error.str.max_tokens"}]
            )
            
        return InputValidationResult(is_valid=True)
    except ValidationError as e:
        return InputValidationResult(is_valid=False, message="Schema validation failed.", errors=e.errors())