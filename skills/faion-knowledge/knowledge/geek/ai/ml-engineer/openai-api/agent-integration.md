# Agent Integration — OpenAI API

## When to use
- Production app requiring best-in-class structured output with native schema enforcement
- Vision tasks requiring GPT-4o's image understanding
- Batch processing of non-time-sensitive data (50% cost discount via Batch API)
- Function calling / tool use as the primary agentic mechanism
- Audio transcription (Whisper) or TTS in agent pipelines
- When you need the Responses API's built-in conversation state management

## When NOT to use
- Privacy-sensitive data that must not leave your infrastructure (use local Ollama instead)
- Very long context (>128K tokens) — use Claude (200K) or Gemini (2M)
- When Anthropic Claude's instruction-following is more reliable for your specific task
- Tight budget with high-volume simple tasks — Gemini Flash ($0.10/M) is cheaper than gpt-4o-mini ($0.15/M)
- When you need >128K context for a single call (use gpt-4.1 with 1M context or alternatives)

## Where it fails / limitations
- Rate limits are hard walls: tier-based (3–10K RPM); no graceful degradation by default
- Model versions are periodically deprecated without warning — pin exact versions in production (`gpt-4o-2024-08-06`)
- JSON mode does NOT guarantee schema compliance — use Structured Outputs (`response_format=MyModel`) instead
- Streaming + structured output: `beta.chat.completions.parse` buffers internally; latency gain is minimal
- Context length limit (128K for gpt-4o) is strict — exceeded requests fail with 400, not a graceful fallback
- Costs scale unpredictably with agentic loops that generate long outputs; always set `max_tokens`
- Responses API (2025+) does not support all parameters available in Chat Completions; check docs before migrating

## Agentic workflow
Agents use OpenAI via function calling (tools array) for structured decisions and the Batch API for high-volume background processing. The Responses API (`/v1/responses`) simplifies stateful multi-turn conversations by managing history server-side via `previous_response_id`, reducing the payload size agents must pass around. For tool-using agents, define tools as Pydantic models converted to JSON Schema; the model will call them deterministically. Always handle `tool_calls` in agent loops with explicit retry on parsing failures.

### Recommended subagents
- `faion-sdd-execution` — uses OpenAI structured output for quality gate decisions
- Any custom extraction agent using `client.beta.chat.completions.parse`

### Prompt pattern
Function-calling agent loop:
```python
import openai, json
from pydantic import BaseModel

client = openai.OpenAI()

class SearchQuery(BaseModel):
    query: str
    max_results: int

tools = [openai.pydantic_function_tool(SearchQuery)]

def agent_loop(task: str, max_steps: int = 5):
    messages = [{"role": "user", "content": task}]
    for _ in range(max_steps):
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message
        messages.append(msg)
        if msg.finish_reason == "stop":
            return msg.content
        for tc in msg.tool_calls or []:
            result = handle_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
    return "max steps reached"
```

Batch API pattern:
```python
import json
requests = [
    {"custom_id": f"item-{i}", "method": "POST", "url": "/v1/chat/completions",
     "body": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": text}], "max_tokens": 512}}
    for i, text in enumerate(texts)
]
batch = client.batches.create(input_file_id=upload_jsonl(requests), endpoint="/v1/chat/completions", completion_window="24h")
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `openai` (Python SDK) | All API endpoints, streaming, structured output | `pip install openai` / github.com/openai/openai-python |
| `openai` (Node SDK) | TypeScript/JS applications | `npm install openai` / github.com/openai/openai-node |
| `tiktoken` | Token counting for budget/context management | `pip install tiktoken` / github.com/openai/tiktoken |
| `instructor` | Structured output with retry across providers | `pip install instructor` / python.useinstructor.com |
| OpenAI CLI (`openai`) | Upload files, manage fine-tunes, batches | installed with SDK |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenAI Platform | SaaS | Yes | Primary; usage dashboard, rate limit self-service |
| OpenAI Batch API | SaaS | Yes | 50% discount, 24h window; ideal for bulk agent tasks |
| LangSmith | SaaS | Yes | Full OpenAI call tracing; prompt versioning |
| Langfuse | OSS | Yes | Self-hosted tracing for OpenAI calls via OTEL |
| Helicone | SaaS (proxy) | Yes | 1-line integration; caches, rate-limits, logs OpenAI calls |
| Portkey | SaaS | Yes | Multi-provider fallback: OpenAI → Anthropic → Gemini |

## Templates & scripts
See `templates.md` for: streaming response handler, exponential backoff wrapper, Batch API JSONL builder.

Inline: robust API call with exponential backoff (~25 lines):

```python
import time, openai
from openai import RateLimitError, APIStatusError

def call_with_backoff(client, **kwargs):
    for attempt in range(6):
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except APIStatusError as e:
            if e.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
    raise RuntimeError("Exceeded retry limit")
```

## Best practices
- Pin exact model versions: `gpt-4o-2024-08-06` not `gpt-4o` — snapshot versions don't change behavior
- Use Structured Outputs (`beta.chat.completions.parse`) instead of JSON mode for schema compliance
- Set `max_tokens` on every call — unbounded output generation runs up costs and stalls agents
- Implement exponential backoff for 429s: start at 1s, cap at 60s, max 6 retries
- Use `usage` from response to track input/output token spend per agent step
- Enable prompt caching by placing static system prompts first and never modifying their prefix
- Use `gpt-4o-mini` for routing/classification steps, `gpt-4o` only for complex reasoning
- Use service account keys (`sk-svcacct-*`) for automated systems, not user keys

## AI-agent gotchas
- Tool call responses must include `tool_call_id` matching exactly — mismatches cause 400 errors
- The Responses API removes messages from history automatically; Chat Completions requires manual history management — pick one pattern and stick with it
- Human-in-loop checkpoint required before executing any tool call that modifies external state (write files, POST to APIs, send emails)
- `finish_reason: "length"` means the model was cut off — your agent may be passing incomplete data downstream; check `max_tokens`
- Batch API results arrive asynchronously (up to 24h); agents that wait synchronously for batch results will stall indefinitely

## References
- https://platform.openai.com/docs/api-reference
- https://platform.openai.com/docs/guides/structured-outputs
- https://platform.openai.com/docs/guides/migrate-to-responses
- https://platform.openai.com/docs/guides/production-best-practices
- https://cookbook.openai.com/
- https://github.com/openai/openai-python
