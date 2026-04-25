# Templates — Schema Field Order

## Pydantic + OpenAI / Anthropic SDK

```python
from pydantic import BaseModel, Field

class ArticleDraft(BaseModel):
    body: str = Field(description="Full article content. Write this first.")
    summary: str = Field(description="3-sentence summary of the body above.")
    title: str = Field(description="Sharp 6-10 word title derived from body and summary.")
    slug: str = Field(description="URL slug — lowercase, hyphenated, derived from title.")
    tags: list[str] = Field(description="3-5 keywords, taken from the body.")
```

## Anthropic tool input schema (JSON)

```json
{
  "name": "save_article",
  "description": "Persist a finished article",
  "input_schema": {
    "type": "object",
    "properties": {
      "body":    {"type": "string", "description": "Full content. Write first."},
      "summary": {"type": "string", "description": "3-sentence summary of body above."},
      "title":   {"type": "string", "description": "Sharp title derived from body."},
      "tags":    {"type": "array",  "items": {"type": "string"}}
    },
    "required": ["body", "summary", "title", "tags"]
  }
}
```

JSON Schema preserves declaration order in modern parsers; both OpenAI structured outputs and Anthropic tool input respect property order.

## OpenAI Responses API `response_format`

```python
response = client.responses.create(
    model="gpt-...",
    input=...,
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Article",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "body": {"type": "string"},
                    "summary": {"type": "string"},
                    "title": {"type": "string"},
                },
                "required": ["body", "summary", "title"],
                "additionalProperties": False,
            },
        },
    },
)
```

## Gemini controlled generation

```python
from google.genai import types

response_schema = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "body":    types.Schema(type=types.Type.STRING),
        "summary": types.Schema(type=types.Type.STRING),
        "title":   types.Schema(type=types.Type.STRING),
    },
    required=["body", "summary", "title"],
    property_ordering=["body", "summary", "title"],  # Gemini-specific
)
```

Gemini supports `property_ordering` explicitly — use it.

## Reasoning-before-answer template

```python
class Critique(BaseModel):
    restate_intent: str = Field(description="Restate what the user asked.")
    observations: list[str] = Field(description="Concrete observations from the input.")
    risks: list[str] = Field(description="Risks identified.")
    verdict: Literal["approve", "reject"] = Field(description="Final verdict — based on observations and risks above.")
    rationale: str = Field(description="One sentence explaining the verdict.")
```

## Generic dependency-ordering template

```
schema = {
    inputs / echoes,           # restate, ground
    intermediate observations, # what you see
    intermediate plans,        # what you propose
    final answer,              # what you commit to
    metadata about answer,     # confidence, tags, slug
}
```
