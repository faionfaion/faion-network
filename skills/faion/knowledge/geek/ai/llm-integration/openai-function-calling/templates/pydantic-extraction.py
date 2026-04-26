# Pydantic structured extraction with OpenAI parse() + JSON mode fallback
# Usage: call extract(client, text, MyModel) → MyModel instance or None

from typing import Type, TypeVar, Optional
from pydantic import BaseModel, ValidationError
import json
from openai import OpenAI

T = TypeVar('T', bound=BaseModel)


def extract(
    client: OpenAI,
    text: str,
    output_class: Type[T],
    model: str = "gpt-4o",
    max_retries: int = 3,
) -> Optional[T]:
    """Extract structured data using OpenAI Structured Outputs.

    Falls back to json_object mode if parse raises (model not supported).
    Returns None after max_retries exhausted — never raises.
    """
    for attempt in range(max_retries):
        try:
            response = client.beta.chat.completions.parse(
                model=model,
                messages=[{"role": "user", "content": text}],
                response_format=output_class,
            )
            msg = response.choices[0].message
            if msg.refusal:
                return None
            return msg.parsed
        except NotImplementedError:
            # Model does not support Structured Outputs — use JSON mode
            schema = output_class.model_json_schema()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": f"Return valid JSON matching: {json.dumps(schema)}"},
                    {"role": "user", "content": text},
                ],
                response_format={"type": "json_object"},
            )
            try:
                data = json.loads(response.choices[0].message.content)
                return output_class(**data)
            except (json.JSONDecodeError, ValidationError):
                pass
        except (json.JSONDecodeError, ValidationError):
            pass
    return None
