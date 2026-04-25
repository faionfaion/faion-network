# Agent Integration — Structured Output

## When to use
- Agent tool calls must return typed data consumed by downstream code
- Extracting structured records from unstructured documents (invoices, forms, emails)
- Building pipelines where each stage's input is the previous stage's validated output
- Any place where a parsing failure would silently corrupt downstream state
- Multi-model workflows where one model's output feeds into another model's prompt

## When NOT to use
- Free-form creative generation where schema would over-constrain the response
- Exploratory research where the structure isn't known in advance
- Very long outputs (>2K tokens) with complex nested schemas — reliability degrades
- Streaming responses where structured output can't be validated until complete

## Where it fails / limitations
- Claude has no native `response_format` parameter — tool-calling or prompt-injection required; adds 50-200 extra prompt tokens per call
- Deeply nested schemas (>3 levels) increase hallucinated field values significantly
- Optional fields with no `default` cause inconsistent output: model sometimes includes them, sometimes omits
- Large Pydantic models (>20 fields) confuse models; split into smaller sub-schemas
- Validation retry loops add latency; each retry doubles time and cost
- JSON mode (not structured output) does NOT guarantee schema compliance — fields can be missing or wrong types

## Agentic workflow
Agents should define output schemas as Pydantic models and pass them as tools (via `instructor` or native SDK `beta.chat.completions.parse`). Each agent boundary becomes a typed contract: if parsing fails, the agent retries with the validation error in the prompt rather than propagating bad data. Use `instructor` with `max_retries=3` for automatic retry; log all failures for schema refinement. For Claude, always use tool-call-based structured output over prompt injection — it's more reliable.

### Recommended subagents
- `faion-sdd-execution` — uses structured output for quality gate results and task state
- `faion-feature-executor` — each task step returns a typed status/result schema

### Prompt pattern
OpenAI (native structured output):
```python
from openai import OpenAI
from pydantic import BaseModel

class ExtractionResult(BaseModel):
    entities: list[str]
    summary: str
    confidence: float

client = OpenAI()
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract from: ..."}],
    response_format=ExtractionResult,
)
result: ExtractionResult = response.choices[0].message.parsed
```

Claude via instructor:
```python
import anthropic
import instructor
from pydantic import BaseModel

client = instructor.from_anthropic(anthropic.Anthropic())

class Summary(BaseModel):
    points: list[str]
    verdict: str

result = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Summarize: ..."}],
    response_model=Summary,
)
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `instructor` | Structured output for any LLM provider with auto-retry | `pip install instructor` / python.useinstructor.com |
| `pydantic` | Schema definition and validation | `pip install pydantic` / docs.pydantic.dev |
| `outlines` | Grammar-constrained generation for local models | `pip install outlines` / github.com/outlines-dev/outlines |
| `jsonschema` | Validate arbitrary JSON against schema | `pip install jsonschema` / python-jsonschema.readthedocs.io |
| `tiktoken` | Count tokens before sending large schemas | `pip install tiktoken` / github.com/openai/tiktoken |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI API | SaaS | Yes | Native structured output via `beta.chat.completions.parse`; best reliability |
| Anthropic API | SaaS | Yes | Via tool-calling or instructor; no native `response_format` |
| Google Gemini | SaaS | Yes | Native JSON schema support via `response_schema` |
| Ollama | OSS | Partial | JSON format flag available; schema compliance varies by model |
| Langfuse | OSS | Yes | Logs structured output calls with schema info for debugging |

## Templates & scripts
See `templates.md` for Pydantic schema templates (entity extraction, document classification, code review output).

Inline: safe extraction with markdown stripping and retry (Python, ~30 lines):

```python
import json, re
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type

T = TypeVar("T", bound=BaseModel)

def safe_parse(raw: str, model: Type[T], retries: int = 3) -> T:
    """Strip markdown fences and validate JSON against Pydantic model."""
    content = raw.strip()
    # Strip ```json ... ``` or ``` ... ``` wrappers
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    for attempt in range(retries):
        try:
            return model.model_validate_json(content)
        except (json.JSONDecodeError, ValidationError) as e:
            if attempt == retries - 1:
                raise RuntimeError(f"Structured output parse failed after {retries} attempts: {e}") from e
    raise RuntimeError("unreachable")
```

## Best practices
- Define `Field(description="...")` on every field — models read descriptions, not just type names
- Use `str` enums for controlled vocabularies: model must pick from your list, not invent values
- Keep required fields minimal; mark uncertain data `Optional[str] = None`
- Never put schema JSON into user messages — put it in tool definitions or system prompt only
- Log every validation error with the raw model output for offline schema refinement
- Version schemas in code (`class OutputV2(BaseModel)`) to track changes across deployments
- For extraction tasks, add a `raw_quote: str` field — forces model to ground its answer in source text

## AI-agent gotchas
- Retry loops are a human-in-loop breakpoint: if validation fails >3 times, escalate — the schema may be wrong, not the model
- Never retry with `temperature=0` on the same prompt — if it failed once, it will fail again; inject the error message as additional context
- Schema complexity compounds with context length — test schema reliability at your actual production context length, not on toy examples
- Streaming + structured output conflict: you cannot validate incrementally; buffer the full response before parsing
- In multi-agent pipelines, always re-validate on receipt even if the sending agent validated on emit — serialization can corrupt data

## References
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.anthropic.com/en/docs/tool-use
- https://python.useinstructor.com/
- https://docs.pydantic.dev/
- https://github.com/outlines-dev/outlines
- https://ai.google.dev/gemini-api/docs/json-mode
