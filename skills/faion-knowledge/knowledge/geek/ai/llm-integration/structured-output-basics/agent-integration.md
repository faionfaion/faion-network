# Agent Integration — Structured Output Basics

## When to use
- Any agent pipeline step that must pass data to a downstream system (database write, API call, UI render)
- Data extraction from unstructured text (invoices, forms, articles, emails)
- Classification tasks where the output enum must be validated
- When Pydantic models already exist for the domain — reuse them as response schemas
- Replacing regex-based parsing of LLM output with schema-enforced extraction

## When NOT to use
- Simple yes/no or short free-text responses where schema overhead adds latency without value
- Tasks that inherently require narrative output (copywriting, explanations, debugging commentary)
- When OpenAI `beta.parse` is unavailable for the target model — fall back to function-forcing pattern instead
- When the schema changes frequently at runtime — static Pydantic models are difficult to generate dynamically

## Where it fails / limitations
- JSON Mode (OpenAI, Anthropic) guarantees valid JSON but NOT schema compliance — downstream validation is still required
- OpenAI Structured Outputs (`beta.parse`) is gpt-4o family only; not available for o1/o3 reasoning models
- Claude has no native Structured Outputs equivalent — must use prompt engineering + `json.loads` with retry
- Deeply nested schemas with many optional fields produce inconsistent results even with Structured Outputs
- Very large schemas (>50 fields) increase prompt token cost and reduce model accuracy
- Pydantic validators run client-side after parsing — API errors and validation errors need separate handling

## Agentic workflow
Agents use Pydantic models as the canonical contract between pipeline stages: the model is defined once and used both as the LLM response schema and as the type annotation for the next step's input. For OpenAI, `client.beta.chat.completions.parse` eliminates the `json.loads` + validation step. For Claude, wrap the call in a retry loop that sends a corrective message if parsing fails. Always log both the raw text and the parsed result for debugging.

### Recommended subagents
- `faion-sdd-executor-agent` — uses Pydantic models to enforce spec/design/task output shapes
- `nero-sdd-executor-agent` — same for NERO pipelines; task outputs typed as dataclasses

### Prompt pattern
```python
# OpenAI Structured Outputs — schema-guaranteed
from openai import OpenAI
from pydantic import BaseModel
from typing import List

client = OpenAI()

class ExtractionResult(BaseModel):
    entities: List[str]
    sentiment: str
    confidence: float

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract entities and sentiment."},
        {"role": "user", "content": text}
    ],
    response_format=ExtractionResult
)
result: ExtractionResult = response.choices[0].message.parsed
```

```python
# Claude fallback — prompt + retry
import json, anthropic
from pydantic import BaseModel, ValidationError

client = anthropic.Anthropic()

def extract_claude(text: str, model: type[BaseModel], max_retries=2) -> BaseModel:
    schema = json.dumps(model.model_json_schema(), indent=2)
    prompt = f"Return JSON matching this schema:\n{schema}\n\nText:\n{text}"
    for attempt in range(max_retries + 1):
        resp = client.messages.create(
            model="claude-sonnet-4-20250514", max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = resp.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1].lstrip("json").strip()
        try:
            return model.model_validate_json(raw)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == max_retries:
                raise
            prompt = f"Invalid JSON: {e}\n\nFix and return only valid JSON."
    raise RuntimeError("unreachable")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pydantic` | Schema definition and validation | `pip install pydantic` → https://docs.pydantic.dev |
| `jsonschema` | Validate arbitrary JSON against JSON Schema | `pip install jsonschema` |
| `openai` SDK | `beta.parse` for schema-enforced completions | `pip install openai` |
| `instructor` | Pydantic + retry wrapper for all providers | `pip install instructor` → https://python.useinstructor.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Platform | SaaS | Yes | Native Structured Outputs via `beta.parse` (gpt-4o only) |
| Instructor (OSS) | OSS library | Yes | Adds Pydantic + auto-retry to OpenAI, Anthropic, Gemini, Mistral |
| Marvin | OSS | Yes | High-level extraction API on top of OpenAI Structured Outputs |
| Outlines | OSS | Yes | Constrained generation for local models; JSON Schema enforcement |
| Guidance | OSS (Microsoft) | Partial | Structured generation for local + Azure models |

## Templates & scripts
See `templates.md` for full invoice and project-extraction schemas. Short function-forcing pattern (works on any provider):

```python
def extract_via_tool(prompt: str, schema: dict, client, model="gpt-4o") -> dict:
    """Force structured output via function calling — works on any OpenAI model."""
    import json
    tools = [{"type": "function", "function": {
        "name": "output", "description": "Return result", "parameters": schema
    }}]
    resp = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}],
        tools=tools, tool_choice={"type": "function", "function": {"name": "output"}}
    )
    return json.loads(resp.choices[0].message.tool_calls[0].function.arguments)
```

## Best practices
- Define schemas in Pydantic, not raw dicts — IDE type-checking, `.model_validate`, and `.model_json_schema()` come for free
- Use `Field(description=...)` on every field — descriptions become part of the JSON Schema and improve model accuracy
- Prefer `Optional[str]` over `str` for fields that may be absent — forces model to handle missing data explicitly
- Use enums (`Literal["positive","negative","neutral"]`) instead of free strings for fixed-vocabulary fields
- Always validate the parsed result before passing to the next pipeline step — even Structured Outputs can produce semantically wrong data
- Keep schemas flat (2 levels max) for highest reliability; deeply nested schemas degrade accuracy
- Log the raw LLM text alongside the parsed model for debugging — parsing errors are easier to diagnose with raw output

## AI-agent gotchas
- `response.choices[0].message.parsed` is `None` when the model refuses to generate structured output (content policy) — always check for `None` before accessing
- OpenAI Structured Outputs are not supported for streaming + parse simultaneously (as of 2026) — choose one
- Pydantic `@validator` (v1) and `@field_validator` (v2) run after LLM parsing, not during — schema constraints like `ge=0` are not enforced by the LLM itself
- Claude sometimes wraps JSON in ` ```json ``` ` even when told not to — always strip markdown code fences before parsing
- `instructor` library adds retry overhead but can mask model failures; set a max retry limit and surface errors explicitly
- Large schemas (>20 fields) increase prompt tokens significantly — measure token cost before shipping complex extraction pipelines

## References
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.pydantic.dev/latest/
- https://python.useinstructor.com/
- https://json-schema.org/understanding-json-schema/
- https://github.com/outlines-dev/outlines
