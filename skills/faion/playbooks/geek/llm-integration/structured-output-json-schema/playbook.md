---
name: structured-output-json-schema
description: Define a Pydantic v2 model, derive its JSON schema, and force Claude to return valid structured data via the tool-choice API.
tier: geek
group: llm-integration
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a working Python function that accepts a Pydantic v2 `BaseModel` subclass, converts it to a JSON Schema tool definition, calls `claude-sonnet-4-6` with `tool_choice={"type":"tool","name":"..."}` to force structured output, validates the result against the model, and retries once on a schema mismatch — all without prompt-engineering tricks.

## Prerequisites

- Python 3.11+.
- `anthropic>=0.28.0` installed (`pip install anthropic`).
- `pydantic>=2.0` installed (`pip install pydantic`).
- `ANTHROPIC_API_KEY` set in the environment.
- Familiarity with Pydantic v2 `BaseModel` and `model_json_schema()`.

## Steps

1. Install the required packages:

   ```bash
   pip install "anthropic>=0.28.0" "pydantic>=2.0"
   ```

2. Define your output schema as a Pydantic v2 model. Add `Field(description=...)` to every field — descriptions are included in the JSON Schema and improve model accuracy on ambiguous fields:

   ```python
   from pydantic import BaseModel, Field
   from typing import Optional
   from enum import Enum

   class Sentiment(str, Enum):
       POSITIVE = "positive"
       NEGATIVE = "negative"
       NEUTRAL = "neutral"

   class ReviewAnalysis(BaseModel):
       sentiment: Sentiment = Field(
           description="Overall sentiment of the review text"
       )
       score: float = Field(
           ge=0.0, le=1.0,
           description="Confidence score for the sentiment, 0.0 to 1.0"
       )
       key_topics: list[str] = Field(
           description="Up to 5 main topics mentioned in the review"
       )
       summary: str = Field(
           max_length=200,
           description="One-sentence summary of the review content"
       )
       language: Optional[str] = Field(
           default=None,
           description="ISO 639-1 language code of the review, e.g. 'en'"
       )
   ```

3. Convert the Pydantic model to a JSON Schema tool definition. Use `model_json_schema()` to derive the schema — this preserves `Field` descriptions, validators, and enum values:

   ```python
   import json

   def make_tool(model_cls: type[BaseModel], tool_name: str = "structured_output") -> dict:
       schema = model_cls.model_json_schema()
       # Remove $defs/$schema keys not needed by the Anthropic API
       schema.pop("$schema", None)
       return {
           "name": tool_name,
           "description": f"Return a {model_cls.__name__} object as structured JSON.",
           "input_schema": schema,
       }
   ```

4. Call `client.messages.create` with `tools=[tool]` and `tool_choice={"type":"tool","name":tool_name}`. This forces Claude to call the named tool on every response — no prompt engineering required:

   ```python
   import anthropic

   client = anthropic.Anthropic()

   def call_structured(
       prompt: str,
       model_cls: type[BaseModel],
       tool_name: str = "structured_output",
       model: str = "claude-sonnet-4-6",
       max_tokens: int = 1024,
   ) -> dict:
       tool = make_tool(model_cls, tool_name)
       response = client.messages.create(
           model=model,
           max_tokens=max_tokens,
           tools=[tool],
           tool_choice={"type": "tool", "name": tool_name},
           messages=[{"role": "user", "content": prompt}],
       )
       # stop_reason is "tool_use" when tool_choice forces the call
       tool_block = next(
           b for b in response.content if b.type == "tool_use"
       )
       return tool_block.input  # dict matching the schema
   ```

5. Validate the raw dict against your Pydantic model and add a single retry on `ValidationError`. Structural compliance is guaranteed by the tool-forcing pathway, but semantic validators (`ge`, `max_length`, enum membership) run client-side and can still fail:

   ```python
   from pydantic import ValidationError

   def extract(
       prompt: str,
       model_cls: type[BaseModel],
       tool_name: str = "structured_output",
       max_retries: int = 1,
   ) -> BaseModel:
       last_error: Exception | None = None
       for attempt in range(max_retries + 1):
           raw = call_structured(prompt, model_cls, tool_name)
           try:
               return model_cls.model_validate(raw)
           except ValidationError as exc:
               last_error = exc
               if attempt < max_retries:
                   # Feed the error back so the model can correct itself
                   prompt = (
                       f"The previous output failed validation:\n{exc}\n\n"
                       f"Fix the issues and return a valid {model_cls.__name__}."
                   )
       raise last_error  # type: ignore[misc]
   ```

6. Run an end-to-end example against a real review text:

   ```python
   review = (
       "Absolutely loved the new noise-cancelling headphones. "
       "Sound quality is superb and battery lasts all day. "
       "Delivery was a day late but support was quick to help."
   )

   result: ReviewAnalysis = extract(
       prompt=f"Analyse this product review:\n\n{review}",
       model_cls=ReviewAnalysis,
   )

   print(result.sentiment)      # Sentiment.POSITIVE
   print(result.score)          # e.g. 0.87
   print(result.key_topics)     # ['sound quality', 'battery life', 'delivery', 'support']
   print(result.summary)        # "Highly positive review praising sound and battery..."
   print(result.language)       # 'en'
   ```

7. Pass the validated Pydantic instance to the next pipeline step. Because `extract()` returns a typed model — not a raw dict — the IDE enforces field access and downstream code benefits from type checking:

   ```python
   def handle_review(analysis: ReviewAnalysis) -> None:
       if analysis.sentiment == Sentiment.NEGATIVE and analysis.score > 0.8:
           trigger_escalation(analysis.summary)
       store_to_db(analysis.model_dump())
   ```

## Verify

Run the following and confirm Python exits with code 0 and prints a `Sentiment` value:

```bash
python3 - <<'EOF'
import os, anthropic, json
from pydantic import BaseModel, Field
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Result(BaseModel):
    sentiment: Sentiment = Field(description="Sentiment of the text")
    confidence: float = Field(ge=0, le=1, description="Confidence 0-1")

client = anthropic.Anthropic()
tool = {
    "name": "output",
    "description": "Return Result as structured JSON.",
    "input_schema": Result.model_json_schema(),
}
resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=256,
    tools=[tool],
    tool_choice={"type": "tool", "name": "output"},
    messages=[{"role": "user", "content": "Analyse: I love this product!"}],
)
raw = next(b for b in resp.content if b.type == "tool_use").input
parsed = Result.model_validate(raw)
print(parsed.sentiment)
assert parsed.sentiment == Sentiment.POSITIVE
EOF
```

Expected output: `Sentiment.POSITIVE` (or `positive`). Any `ValidationError` or `StopIteration` indicates the API call or schema derivation failed.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `StopIteration` on `next(b for b in ...)` | `stop_reason` is `"end_turn"` instead of `"tool_use"` | Confirm `tool_choice={"type":"tool","name":"..."}` exactly matches the tool `name` field — a name mismatch causes Claude to ignore the forced call |
| `ValidationError: score must be >= 0` | Claude returned a value outside the Pydantic constraint even though the schema was passed | The JSON Schema `minimum`/`maximum` keywords are advisory to the LLM; add the retry loop (Step 5) and feed the error back |
| `pydantic_core.InitErrorDetails: Input should be 'positive'...` | Enum value casing mismatch | Ensure the enum uses lowercase values and the schema `enum` array matches — `model_json_schema()` derives this correctly from `str, Enum` |
| `anthropic.BadRequestError: tools must be a list` | `tools` arg passed as a single dict, not a list | Wrap the tool in a list: `tools=[tool]` |
| `KeyError: '$defs'` on the Anthropic API side | Pydantic generated a `$defs` block for nested models | The Anthropic API accepts `$defs`; the error is elsewhere — check that `input_schema` is the full `model_json_schema()` dict, not just the `properties` sub-key |
| Retry loop does not converge after 1 retry | The model misunderstands the corrective prompt | Include the raw offending output alongside the `ValidationError` message in the retry prompt so the model has concrete context |

## Next

- `claude-tool-use` — understand the full agentic loop and parallel tool dispatch for multi-step pipelines that build on structured extraction.
- Add `model_config = ConfigDict(extra="ignore")` to your Pydantic models when the API occasionally returns extra fields outside the schema.
- Move to `claude-opus-4-7` for extraction tasks where accuracy on ambiguous or multilingual text outweighs per-token cost.

## References

- [knowledge/geek/ai/llm-integration/structured-output-basics](../../../knowledge/geek/ai/llm-integration/structured-output-basics) — supplies the core rule that `Field(description=...)` improves model accuracy and the retry-loop pattern used in Step 5; this playbook operationalises both for the Claude tool-forcing pathway.
- [knowledge/geek/ai/llm-integration/claude-tool-use](../../../knowledge/geek/ai/llm-integration/claude-tool-use) — provides the forced-tool-call rule (`tool_choice={"type":"tool","name":"..."}`) and the `stop_reason == "tool_use"` detection pattern used in Steps 4–5.
- [knowledge/geek/ai/llm-integration/function-calling-patterns](../../../knowledge/geek/ai/llm-integration/function-calling-patterns) — defines the canonical pattern of deriving JSON Schema from Pydantic and passing it as `input_schema`; backs Step 3 of this playbook.
