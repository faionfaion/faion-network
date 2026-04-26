# StructuredOutputService: retry, parse fallback, batch extraction
# Usage: svc = StructuredOutputService(client); result = svc.extract(text, MyModel)

from typing import Type, TypeVar, Optional, List
from pydantic import BaseModel, ValidationError
import json
import logging
from openai import OpenAI

T = TypeVar('T', bound=BaseModel)
logger = logging.getLogger(__name__)


class StructuredOutputService:
    """Centralized structured extraction with retry and JSON mode fallback.

    Always use response.model (not requested model) for cost tracking.
    On retry, inject the validation error into the prompt.
    """

    def __init__(self, client: OpenAI, model: str = "gpt-4o",
                 max_retries: int = 3):
        self.client = client
        self.model = model
        self.max_retries = max_retries

    def extract(self, prompt: str, output_class: Type[T],
                system: str = "") -> Optional[T]:
        """Extract structured data. Returns None after max_retries exhausted."""
        last_error: Optional[str] = None

        for attempt in range(self.max_retries):
            retry_hint = (f"\n\nPrevious attempt failed validation: {last_error}. "
                         "Please fix the indicated fields." if last_error else "")
            try:
                resp = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=[
                        *([{"role": "system", "content": system}] if system else []),
                        {"role": "user", "content": prompt + retry_hint},
                    ],
                    response_format=output_class,
                )
                msg = resp.choices[0].message
                if msg.refusal:
                    return None
                return msg.parsed
            except NotImplementedError:
                # Fallback for models not supporting Structured Outputs
                return self._json_mode_extract(prompt + retry_hint,
                                               output_class, system)
            except (ValidationError, Exception) as exc:
                last_error = str(exc)
                logger.warning("Extraction attempt %d failed: %s", attempt + 1, exc)

        return None

    def _json_mode_extract(self, prompt: str, output_class: Type[T],
                           system: str) -> Optional[T]:
        schema = output_class.model_json_schema()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": f"{system}\nReturn valid JSON matching: "
                             f"{json.dumps(schema)}"},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        try:
            data = json.loads(resp.choices[0].message.content)
            return output_class(**data)
        except (json.JSONDecodeError, ValidationError) as exc:
            logger.error("JSON mode extraction failed: %s", exc)
            return None

    def batch_extract(self, items: List[str], output_class: Type[T],
                      system: str = "") -> List[Optional[T]]:
        """Extract from multiple items. Returns None for failed extractions."""
        return [self.extract(item, output_class, system) for item in items]
