# Agent Integration — Claude API Basics

## When to use
- Bootstrapping any Anthropic SDK integration from scratch
- Selecting the right Claude model for a task (cost vs. capability trade-off)
- Implementing retry/backoff for production LLM calls
- Tracking token usage and API costs per request or session
- Debugging authentication and rate-limit failures

## When NOT to use
- When you already have a working client setup — don't re-implement auth/retry patterns per-call
- When batch-processing non-time-sensitive workloads — use the Batch API (50% cheaper) instead
- When you need streaming output — see claude-messages-api methodology
- When the task requires tool use or structured JSON output — see claude-tool-use methodology

## Where it fails / limitations
- Tier 1 rate limits (50 req/min, 40K tokens/min) break quickly in concurrent agent workflows
- `overloaded_error` (529) is transient but frequent during peak hours — retry logic is mandatory
- Token counting via `count_tokens` endpoint adds a round trip; avoid in hot paths
- Cost tracking requires matching model ID strings exactly — model aliases break the lookup
- API key management at scale (rotation, per-team keys) is not handled by the SDK

## Agentic workflow
An agent bootstraps the Anthropic client once, injects it via dependency injection or a shared context object, and passes it to all subagent modules. Rate-limit and retry logic should live in a shared utility, not duplicated per-subagent. Cost tracking wraps each API call transparently and writes aggregated usage to a session log. Model selection is driven by a task-routing table, not hardcoded per-call.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates multi-step Claude calls with shared client and cost tracking

### Prompt pattern
```
System: You are a [role]. Return only what is requested.
User: [minimal, focused task description]
```

Force structured output via tool-choice when you need machine-readable results:
```python
tool_choice={"type": "tool", "name": "output_result"}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `anthropic` (Python SDK) | Official Python client | `pip install anthropic` / https://github.com/anthropics/anthropic-sdk-python |
| `@anthropic-ai/sdk` (Node SDK) | Official TypeScript client | `npm install @anthropic-ai/sdk` / https://github.com/anthropics/anthropic-sdk-typescript |
| `curl` | Raw API testing | built-in / https://docs.anthropic.com/en/api/getting-started |
| `tenacity` | Retry with backoff | `pip install tenacity` / https://tenacity.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Anthropic API | SaaS | Yes | Primary — REST + SDK |
| AWS Bedrock | SaaS | Yes | Enterprise proxy for Claude, same models |
| Google Cloud Vertex AI | SaaS | Yes | Claude via Vertex, IAM-based auth |
| LangSmith | SaaS | Yes | Tracing/observability for LLM calls |
| Helicone | SaaS | Yes | Drop-in proxy for cost/usage tracking |

## Templates & scripts
See `templates.md` for the retry wrapper template. Inline cost tracker (fits in one module):

```python
class CostTracker:
    PRICES = {
        "claude-opus-4-5-20251101":   {"in": 15.00, "out": 75.00, "cw": 18.75, "cr": 1.50},
        "claude-sonnet-4-20250514":   {"in":  3.00, "out": 15.00, "cw":  3.75, "cr": 0.30},
        "claude-3-5-haiku-20241022":  {"in":  0.80, "out":  4.00, "cw":  1.00, "cr": 0.08},
    }
    def __init__(self): self.total = 0.0; self.calls = 0
    def track(self, model, usage):
        p = self.PRICES.get(model, {"in":0,"out":0,"cw":0,"cr":0})
        cost = (
            usage.input_tokens * p["in"] +
            usage.output_tokens * p["out"] +
            getattr(usage,"cache_creation_input_tokens",0) * p["cw"] +
            getattr(usage,"cache_read_input_tokens",0) * p["cr"]
        ) / 1_000_000
        self.total += cost; self.calls += 1; return cost
```

## Best practices
- Store `ANTHROPIC_API_KEY` in environment — never in source code or agent prompts
- Use `tenacity` `@retry` decorator with `wait_exponential` rather than custom sleep loops
- Check `response.stop_reason` — `"max_tokens"` means output was truncated, not complete
- Enable prompt caching (`anthropic-beta: prompt-caching-2024-07-31`) for repeated system prompts; cache write is 25% more expensive but read is 90% cheaper
- Pin model IDs with full dates (e.g., `claude-sonnet-4-20250514`) to avoid silent behavior changes on alias updates
- Log `x-request-id` response header for every call; essential for Anthropic support debugging
- For high-throughput agents, track remaining tokens via rate-limit headers and throttle before hitting the limit

## AI-agent gotchas
- Agents must handle `529 overloaded_error` with exponential backoff — this is not a client error
- `max_tokens` is a hard ceiling, not a target; if output is routinely hitting it, the task decomposition needs fixing
- Parallel subagents sharing one API key share rate limits — budget requests/min per subagent thread
- Do NOT cache API key in module-level globals across forked processes (multiprocessing) — each worker needs its own client instance
- Token counting before a call adds latency; only use it when budget enforcement is strict
- Response `model` field may differ from requested model if Anthropic aliases resolve differently — always use the response field for cost tracking

## References
- https://docs.anthropic.com/en/api/getting-started
- https://docs.anthropic.com/en/docs/about-claude/models
- https://docs.anthropic.com/en/api/errors
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching
