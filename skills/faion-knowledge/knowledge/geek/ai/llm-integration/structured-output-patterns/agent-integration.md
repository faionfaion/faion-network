# Agent Integration — Structured Output Patterns

## When to use
- Agent pipelines that pass data between steps — structured output prevents parse errors at handoff points
- Extracting information from unstructured text (emails, docs, PDFs) for downstream processing
- Any agent output that feeds into a database, API, or another service expecting typed data
- Multi-agent coordination where subagent outputs must conform to a contract
- Replacing regex-based parsing with LLM extraction for complex, variable-format inputs

## When NOT to use
- Free-form conversational responses — forcing JSON on chat outputs degrades quality
- When the schema changes frequently — Pydantic + JSON schema re-generation overhead is unnecessary if shape is unknown at design time
- Simple string outputs (yes/no, short answers) — structured output adds token overhead for no gain
- When OpenAI Structured Outputs beta is unavailable for your model tier — fall back to JSON mode with validation

## Where it fails / limitations
- Complex nested schemas (5+ levels) confuse models and produce partial or malformed outputs even in structured output mode
- OpenAI Structured Outputs (`response_format=OutputClass`) is only available for `gpt-4o` and newer — older models need JSON mode fallback
- Pydantic `ValidationError` on LLM output is not always recoverable by retrying — sometimes the schema is genuinely too complex for the model
- Streaming JSON parsing is fragile; partial JSON is not valid JSON and `json.loads` will fail on every chunk except the last
- Very large schemas inflate system prompt token usage; schemas over ~2K tokens should be split across multiple extraction calls

## Agentic workflow
Agents should define output schemas as Pydantic models in a shared `schemas.py` module and pass them to a `StructuredOutputService` instance (see README.md). The service handles retries, schema injection, and validation. Subagents receive typed Pydantic objects as inputs and outputs — not raw strings — ensuring type safety at every pipeline stage. When a structured extraction fails after `max_retries`, the agent should log the raw LLM output and return `None`, not crash.

### Recommended subagents
- `faion-sdd-executor-agent` — receives structured task specs as Pydantic objects, enforcing the SDD contract
- Any extraction subagent that reads documents and emits typed data for storage

### Prompt pattern
Force JSON extraction via system prompt (JSON mode):
```
System: Extract data from the user's text. Return valid JSON matching exactly this schema:
{schema_json}
Do not add keys not in the schema. Use null for missing optional fields.
```

OpenAI Structured Outputs (no schema in prompt needed):
```python
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": text}],
    response_format=MyPydanticModel
)
result = response.choices[0].message.parsed  # already validated Pydantic instance
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pydantic` | Schema definition and validation | `pip install pydantic` / https://docs.pydantic.dev |
| `openai` (Python SDK) | Structured outputs + JSON mode | `pip install openai` |
| `anthropic` (Python SDK) | Claude tool-use as structured output | `pip install anthropic` |
| `tenacity` | Retry on `ValidationError` / `JSONDecodeError` | `pip install tenacity` |
| `instructor` | Thin wrapper for structured outputs across providers | `pip install instructor` / https://python.useinstructor.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI (gpt-4o+) | SaaS | Yes | Native Structured Outputs via `response_format=Model` |
| Anthropic Claude | SaaS | Yes | Tool-use pattern for structured output (see claude-tool-use) |
| Gemini (Google) | SaaS | Yes | `response_schema` parameter for structured output |
| Ollama (local) | OSS | Partial | JSON mode available; structured outputs depend on model |
| Instructor lib | OSS | Yes | Unified structured output across OpenAI, Anthropic, Gemini |

## Templates & scripts
See `templates.md` for `StructuredOutputService` class. Schema design pattern for agent pipelines:

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal

class AgentTaskResult(BaseModel):
    status: Literal["success", "partial", "failed"]
    output: str = Field(description="Primary result text")
    confidence: float = Field(ge=0.0, le=1.0)
    missing_data: list[str] = Field(default_factory=list,
        description="Fields the agent could not extract")
    next_action: Optional[str] = None
```

## Best practices
- Keep schemas flat (1–2 levels of nesting) — models handle flat schemas with near-zero errors
- Use `Literal["a", "b", "c"]` instead of `str` for enumerated fields — hard constraint, not soft instruction
- Add `Field(description="...")` to all non-obvious fields — the description is injected into the schema and guides the model
- Always validate with Pydantic — never `json.loads()` + manual field access without type checking
- Use `instructor` library if you need cross-provider structured output without duplicating logic
- For bulk extraction, use OpenAI Batch API — 50% cost reduction, async 24h window
- Log all `ValidationError` instances with the raw LLM output — patterns in failures reveal schema improvement opportunities

## AI-agent gotchas
- `response.choices[0].message.parsed` is `None` if the model produced invalid JSON even in Structured Outputs mode — always null-check
- Schema changes break existing extraction without a version bump — treat Pydantic models as API contracts and version them
- An agent that retries on `ValidationError` must modify the prompt on each retry (add the error message) — blind retries rarely improve results
- Optional fields with no default are still required in practice — use `Optional[X] = None` or `Field(default=None)` explicitly
- Claude tool-use for structured output returns `block.input` as a dict, not a Pydantic model — validate it manually: `MyModel(**block.input)`
- Very large output schemas can cause the model to produce only the first few fields and stop at `max_tokens` — increase `max_tokens` or split the schema

## References
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.pydantic.dev/latest/
- https://python.useinstructor.com/ (instructor library)
- https://json-schema.org/
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use (Claude tool-use for structured output)
