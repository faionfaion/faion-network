"""
Claude structured extraction with markdown-fence stripping and retry loop.

Usage:
    from extraction_schema import ExtractionResult
    result = extract_claude("Elon Musk visited Berlin.", ExtractionResult)
"""
import json
import anthropic
from pydantic import BaseModel, ValidationError

client = anthropic.Anthropic()


def extract_claude(text: str, model_cls: type[BaseModel], max_retries: int = 2) -> BaseModel:
    """
    Extract structured data from text using Claude.

    Strips markdown code fences and retries with corrective message on parse failure.
    """
    schema = json.dumps(model_cls.model_json_schema(), indent=2)
    prompt = f"Return JSON matching this schema:\n{schema}\n\nText:\n{text}"

    for attempt in range(max_retries + 1):
        resp = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()

        # Strip markdown code fences (Claude may add them even when asked not to)
        if raw.startswith("```"):
            raw = raw.split("```")[1].lstrip("json").strip()

        try:
            return model_cls.model_validate_json(raw)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == max_retries:
                raise
            prompt = f"The JSON was invalid: {e}\n\nFix and return only valid JSON."

    raise RuntimeError("unreachable")
