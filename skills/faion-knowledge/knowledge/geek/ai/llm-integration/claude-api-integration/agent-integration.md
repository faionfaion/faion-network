# Agent Integration — Claude API Integration

## When to use
- Tasks requiring deep instruction-following across long contexts (up to 200K tokens)
- Code generation, review, or refactoring where nuance and safety matter
- Multi-turn conversation pipelines where system prompt stability is critical
- Long document processing (legal, technical, medical) — single-shot with 200K context
- Extended Thinking tasks: multi-step math, architecture decisions, strategic planning
- When Anthropic's safety defaults are a feature, not a bug (enterprise, sensitive data)

## When NOT to use
- High-volume, low-cost inner loops where gpt-4o-mini is sufficient (Claude Haiku excepted)
- When OpenAI Structured Outputs (`beta.parse`) schema enforcement is required — Claude lacks this feature
- Tasks needing OpenAI Assistants' persistent thread + file storage model
- When Google Search grounding is required (use Gemini instead)
- Workflows that require Batch API cost savings already provided by Anthropic's own batch API at 50% off

## Where it fails / limitations
- No native Structured Outputs equivalent — must use prompt engineering + `json.loads` + retry loop
- Extended Thinking adds significant latency (budget_tokens of thinking = extra wait time)
- Computer Use (beta) requires a sandboxed VM environment; not safe to run directly on production hosts
- Prompt Caching requires minimum 1024 tokens and prefix matching — cache invalidates if system prompt changes at all
- `temperature` is not supported when Extended Thinking is enabled
- `stop_reason == "max_tokens"` is silent — truncated responses must be detected explicitly
- Token counting via `client.count_tokens()` is an extra API call; use sparingly

## Agentic workflow
Claude is well-suited as the primary reasoning engine in a multi-step agent: a Claude subagent receives a structured task, produces analysis or code, and the result is validated before being passed downstream. For cost efficiency, use Haiku for triage/classification steps and Sonnet for main reasoning. Enable Prompt Caching on the system prompt when the same assistant is called many times per session. Use the Batch API for offline enrichment tasks (content pipelines, nightly analysis).

### Recommended subagents
- `faion-sdd-executor-agent` — uses Claude Sonnet as the primary reasoning model for SDD task execution
- `nero-sdd-executor-agent` — same pattern; Claude Opus for architecture decisions, Haiku for classification

### Prompt pattern
```python
# Standard agentic call with system prompt and error handling
from anthropic import Anthropic, RateLimitError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

client = Anthropic()

@retry(
    retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    wait=wait_exponential(min=4, max=60),
    stop=stop_after_attempt(3)
)
def call_claude(system: str, messages: list, model="claude-sonnet-4-20250514", max_tokens=2048) -> str:
    resp = client.messages.create(
        model=model, max_tokens=max_tokens,
        system=system, messages=messages
    )
    if resp.stop_reason == "max_tokens":
        raise RuntimeError("Response truncated — increase max_tokens or split task")
    return resp.content[0].text
```

```python
# Extended Thinking for complex reasoning
def deep_reason(problem: str) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5-20251101",
        max_tokens=16000,
        thinking={"type": "enabled", "budget_tokens": 8000},
        messages=[{"role": "user", "content": problem}]
    )
    return {
        "thinking": next((b.thinking for b in resp.content if b.type == "thinking"), ""),
        "answer": next((b.text for b in resp.content if b.type == "text"), "")
    }
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` SDK | Primary Python client | `pip install anthropic` → https://github.com/anthropics/anthropic-sdk-python |
| `tenacity` | Retry with backoff | `pip install tenacity` |
| `instructor` | Pydantic structured output layer | `pip install instructor[anthropic]` |
| `claude` CLI | Interactive shell (if installed) | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Primary endpoint; 200K context, batch, caching |
| AWS Bedrock | SaaS | Yes | Claude via AWS; useful for enterprise IAM + VPC isolation |
| Google Vertex AI | SaaS | Yes | Claude 3 available on Vertex; useful when already on GCP |
| LiteLLM | OSS proxy | Yes | Unified interface; routes to Anthropic with fallback to OpenAI |
| Helicone | SaaS | Yes | Drop-in proxy for logging, caching, cost tracking |
| Langfuse | OSS/SaaS | Yes | Trace multi-step Claude pipelines; prompt versioning |

## Templates & scripts
See `templates.md` for `ClaudeService` wrapper and `ClaudeConfig` dataclass. Short Batch API helper:

```python
def create_batch(requests: list[dict]) -> str:
    """Submit requests to Claude Batch API. Returns batch ID."""
    batch = client.beta.messages.batches.create(requests=[
        {"custom_id": r["id"], "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": r.get("max_tokens", 1024),
            "messages": r["messages"]
        }} for r in requests
    ])
    return batch.id

def poll_batch(batch_id: str, interval=30) -> list[dict]:
    """Poll until batch is done. Returns list of {id, text} results."""
    import time
    while True:
        batch = client.beta.messages.batches.retrieve(batch_id)
        if batch.processing_status == "ended":
            return [
                {"id": r.custom_id, "text": r.result.message.content[0].text}
                for r in client.beta.messages.batches.results(batch_id)
                if r.result.type == "succeeded"
            ]
        time.sleep(interval)
```

## Best practices
- Use `system` parameter (not a system-role message) — it gets cached separately and is more efficient
- Always check `stop_reason` — `"max_tokens"` means silent truncation; `"end_turn"` is normal completion
- Use `AsyncAnthropic` for pipelines with > 2 concurrent Claude calls; `asyncio.gather` for parallel batch
- Enable Prompt Caching on any system prompt > 1024 tokens that stays constant across calls
- Use Haiku for triage/routing steps, Sonnet for main tasks, Opus only for complex reasoning or architecture
- Validate structured JSON output with Pydantic before passing to downstream steps — never trust raw text
- Set `timeout=60.0` on API calls to prevent stuck pipelines on slow responses
- Track `usage.input_tokens + usage.output_tokens` per call; alert if cost per run exceeds threshold

## AI-agent gotchas
- `tool_use` stop reason: model wants to call a tool — if your agent doesn't handle this, the conversation hangs
- Extended Thinking is incompatible with `temperature` — setting both raises an API error
- Prompt Caching requires the cached prefix to be byte-identical — a single extra space invalidates the cache
- Computer Use (beta) executes arbitrary OS actions — always sandbox in a VM with network isolation and no credentials
- `response.content` is a list, not a single text — always iterate or index explicitly; `content[0].text` fails if there's a tool_use block first
- Rate limits for Opus are significantly lower than Sonnet — a pipeline that works with Sonnet may 429 immediately with Opus
- The Batch API has up to 24-hour processing time — not suitable for real-time workflows; use only for offline enrichment

## References
- https://docs.anthropic.com/en/api/getting-started
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- https://github.com/anthropics/anthropic-cookbook
- https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
