# purpose: safe-parse with one-shot repair retry for structured LLM output
# consumes: raw model output text, target Pydantic class
# produces: code (drop-in module returning typed value + repair_attempts)
# depends-on: pydantic >=2
# token-budget-impact: ~200 tokens if loaded into LLM context
"""
Safe structured output extraction: strips markdown fences, validates, retries with error context.
Use when not using instructor's automatic retry (e.g., with prompt-based JSON output).
"""
import json
import re
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)


def safe_parse(raw: str, model: Type[T], retries: int = 3) -> T:
    """
    Strip markdown fences and validate JSON against a Pydantic model.
    Raises RuntimeError after all retries are exhausted.
    """
    content = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` wrappers
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    for attempt in range(retries):
        try:
            return model.model_validate_json(content)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == retries - 1:
                raise RuntimeError(
                    f"Structured output parse failed after {retries} attempts: {e}\n"
                    f"Raw output: {raw[:500]}"
                ) from e
    raise RuntimeError("unreachable")


def extract_with_retry(prompt: str, model_class: Type[T], llm_fn, max_retries: int = 3) -> T:
    """
    Call llm_fn(prompt) and parse with retry.
    On failure, inject the validation error into the next prompt.
    """
    current_prompt = prompt
    for attempt in range(max_retries):
        raw = llm_fn(current_prompt)
        try:
            return safe_parse(raw, model_class)
        except RuntimeError as e:
            if attempt == max_retries - 1:
                raise
            current_prompt = f"{prompt}\n\nPrevious attempt failed validation:\n{e}\n\nPlease correct and try again."
    raise RuntimeError("unreachable")
