# Agent Integration — Claude Best Practices

## When to use
- Building any production system that calls the Anthropic Messages API.
- Optimizing cost/quality tradeoff across multi-agent pipelines.
- When system prompts are large and repeated across many requests (→ prompt caching).
- Implementing retry logic, fallback models, or monitoring for Claude API calls.
- Selecting the right Claude model tier for a given agent role (Opus/Sonnet/Haiku).

## When NOT to use
- Quick scripted one-off calls with no cost or reliability concerns.
- When the task is provider-neutral and you want to abstract over multiple LLM providers — use an abstraction layer instead of Claude-specific patterns.
- Token counting pre-flight adds latency; skip for simple short prompts.

## Where it fails / limitations
- Prompt caching requires the cached prefix to be identical byte-for-byte across requests; any dynamic content injected before the cached block invalidates the cache.
- Batch API has up to 24-hour turnaround — unsuitable for user-facing calls.
- Model fallback (Sonnet → Haiku) silently degrades capability; downstream agents may produce worse outputs without knowing why.
- `max_tokens` set too low silently truncates structured output mid-JSON; always set it generously for structured responses.
- Rate limit backoff with exponential jitter works per-process; orchestrators with many parallel workers need a shared rate-limit token bucket.
- Monitoring client adds overhead; keep logging async or fire-and-forget.

## Agentic workflow
The orchestrator constructs a reusable system prompt containing static context (docs, instructions) and marks it `cache_control: ephemeral`. Each subagent call reuses this cached prefix, appending only the per-turn user message. Costs for repeated large-context calls drop ~90% on cache hits. A thin monitoring wrapper tracks token usage and cost per subagent role; the orchestrator uses this to select the cheapest model capable of the task (Haiku for formatting/routing, Sonnet for generation, Opus for complex reasoning).

### Recommended subagents
- `claude-router` — Selects model tier (Haiku/Sonnet/Opus) based on task complexity signal.
- `cost-monitor` — Aggregates token usage per pipeline run; alerts when cost per run exceeds threshold.
- `retry-wrapper` — Implements exponential backoff for `RateLimitError` and 5xx; falls back to Haiku on sustained Sonnet rate limiting.

### Prompt pattern
```python
# Cached system prompt structure
system = [
    {
        "type": "text",
        "text": STATIC_DOCS,  # 10k+ tokens, never changes
        "cache_control": {"type": "ephemeral"}
    },
    {
        "type": "text",
        "text": dynamic_instructions  # Per-run, not cached
    }
]
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system=system,
    messages=[{"role": "user", "content": user_task}]
)
```

Tool definition best practice:
```python
# Description must answer "when should I call this?" — not "what does it do?"
tool = {
    "name": "search_docs",
    "description": "Search internal knowledge base. Call when user asks about product features, APIs, or configuration. Do NOT call for general knowledge questions.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "2-5 keyword search query"},
            "category": {"type": "string", "enum": ["api", "config", "features"]}
        },
        "required": ["query"]
    }
}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` Python SDK | Official client; supports streaming, caching, batches | `pip install anthropic` / docs.anthropic.com |
| `claude` CLI (Claude Code) | Interactive + scriptable Claude access | docs.anthropic.com/en/docs/claude-code |
| `llm` (Simon Willison) | Multi-provider CLI including Claude | `pip install llm llm-claude-3` |
| `tokencost` | Estimate cost before calling API | `pip install tokencost` / github.com/AgentOps-AI/tokencost |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic Messages API | SaaS | Yes | Core; supports caching, batch, streaming, tool use |
| Anthropic Batch API | SaaS | Yes (async) | 50% cost reduction; 24h max latency |
| LangSmith | SaaS | Yes | Traces Claude calls; tags by agent role |
| Weights & Biases | SaaS | Yes | Log token usage metrics per pipeline run |
| AWS Bedrock (Claude) | SaaS | Yes | Enterprise; adds IAM auth layer |

## Templates & scripts
See `templates.md` for cached system prompt, async batch, and monitored client templates.

Minimal monitored client:
```python
import anthropic, logging, time

log = logging.getLogger(__name__)
client = anthropic.Anthropic()

def call(model: str, system: list, messages: list, max_tokens: int = 2048):
    t0 = time.monotonic()
    r = client.messages.create(
        model=model, max_tokens=max_tokens,
        system=system, messages=messages
    )
    elapsed = time.monotonic() - t0
    total_tok = r.usage.input_tokens + r.usage.output_tokens
    log.info("model=%s tokens=%d elapsed=%.2fs", model, total_tok, elapsed)
    return r
```

## Best practices
- Always set `max_tokens` explicitly — the default is low and silently truncates long structured outputs.
- Place the largest, most stable content at the top of the system prompt and mark it cached; dynamic instructions go last.
- Use `client.messages.count_tokens()` for pre-flight checks on large inputs before paying for the full call.
- Set `tool_choice={"type": "tool", "name": "specific_tool"}` when you know which tool should be called — avoids spurious reasoning overhead.
- Model names are date-versioned; pin exact model IDs in production configs to avoid breaking changes from alias updates.
- For async batch workloads, use `AsyncAnthropic` + `asyncio.gather` — do not spawn threads, the SDK is async-native.
- Log `cache_read_input_tokens` from usage to verify caching is working; zero means cache miss.

## AI-agent gotchas
- Cache hit requires identical prefix — any runtime injection (timestamps, request IDs) placed before the cached block breaks the cache silently.
- `RateLimitError` from Anthropic includes a `retry-after` header; parse it instead of guessing the backoff.
- Fallback to Haiku on rate limiting is invisible to the orchestrator; log the model used in every response, not just the model requested.
- Tool schemas with `additionalProperties: false` reject unexpected keys; LLMs sometimes add extra fields — strip unknown keys before passing tool results back.
- Extended thinking (`thinking` param) blocks count toward output tokens but are non-cacheable; large think budgets can 5-10x the cost of a single call.
- Human-in-loop checkpoint: when `stop_reason == "max_tokens"` on a structured output call, the JSON is truncated and invalid — do not parse it; retry with higher `max_tokens`.

## References
- https://docs.anthropic.com/en/api — Anthropic API Reference
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching — Prompt Caching
- https://docs.anthropic.com/en/docs/build-with-claude/batch — Batch API
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use — Tool Use
- https://www.anthropic.com/pricing — Current model pricing
