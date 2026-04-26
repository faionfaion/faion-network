# Agent Integration — LLM Observability

## When to use
- Any production LLM application handling real users — tracing from day 1 prevents blind debugging later
- Multi-agent pipelines where a single user request fans out across 5+ LLM calls
- When cost attribution per feature/user/pipeline stage is needed for business decisions
- After deploying a new prompt version — need to compare quality vs. previous version
- Detecting quality regressions: hallucination rate increase, response relevance drop
- Debugging intermittent agent failures that only reproduce in production traffic

## When NOT to use
- Prototyping phase with fewer than 100 requests/day — overhead isn't justified yet
- When data privacy rules prohibit sending prompt/response content to third-party SaaS (use self-hosted Langfuse instead)
- Already have comprehensive OTEL tracing — may be redundant; check if existing stack can be extended with LLM spans

## Where it fails / limitations
- Langfuse/LangSmith add ~10-50ms latency per call (async, but SDK overhead is real)
- Token-level tracing for streaming responses requires buffering, which breaks time-to-first-token measurements
- LLM-as-judge evaluations have their own cost and hallucination risk — don't trust judge verdicts without calibration
- Privacy leakage: raw prompts and responses logged to SaaS contain user data; scrub PII before logging or self-host
- Dashboard alert fatigue: too many metrics → alerts on everything → team ignores alerts; start with 3-5 key metrics
- Agent trace correlation breaks if session/trace IDs are not explicitly propagated through all agent boundaries

## Agentic workflow
Instrument every LLM call at agent boundaries by wrapping the SDK client with the observability layer. For Langfuse, pass the trace object as a context variable through the agent call chain — each agent step creates a child span. For LangSmith, use `@traceable` decorators on agent functions. The critical integration point is ensuring that the `session_id` (user conversation) and `trace_id` (single request) flow through all sub-agents, enabling you to reconstruct the full multi-agent execution path for any production failure.

### Recommended subagents
- `faion-sdd-execution` — can log quality gate decisions as Langfuse events for pipeline debugging
- Any custom agent that calls LLM APIs should wrap calls with observability

### Prompt pattern
Langfuse integration (Python):
```python
from langfuse import Langfuse
from anthropic import Anthropic

langfuse = Langfuse()
client = Anthropic()

def traced_call(prompt: str, session_id: str, agent_name: str) -> str:
    trace = langfuse.trace(name=agent_name, session_id=session_id)
    generation = trace.generation(
        name="llm-call",
        model="claude-sonnet-4-5",
        input=prompt,
    )
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        output = resp.content[0].text
        generation.end(
            output=output,
            usage={"input": resp.usage.input_tokens, "output": resp.usage.output_tokens},
        )
        return output
    except Exception as e:
        generation.end(level="ERROR", status_message=str(e))
        raise
```

LLM-as-judge evaluation trigger:
```python
def evaluate_response(trace_id: str, response: str, expected_criteria: str):
    langfuse.score(
        trace_id=trace_id,
        name="relevance",
        value=judge_relevance(response, expected_criteria),  # 0.0-1.0
        comment="auto-eval",
    )
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langfuse` | OSS observability: tracing, evals, prompt versioning | `pip install langfuse` / langfuse.com/docs |
| `langsmith` | LangChain-native tracing and evaluation | `pip install langsmith` / docs.langchain.com/langsmith |
| `helicone` | Proxy-based logging with semantic cache | `pip install helicone` / helicone.ai/docs |
| `opentelemetry-sdk` | OTEL spans for custom observability stacks | `pip install opentelemetry-sdk` / opentelemetry.io |
| `arize-phoenix` | OSS evaluation + embedding drift detection | `pip install arize-phoenix` / docs.arize.com/phoenix |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | OSS (MIT) + SaaS | Yes | Self-hostable; best for data privacy; 19k+ GitHub stars |
| LangSmith | SaaS/Self-hosted | Yes | Deep LangChain/LangGraph integration; best UX for chains |
| Helicone | SaaS (proxy) | Yes | Drop-in OpenAI proxy; adds 1 line of config |
| Portkey | SaaS | Yes | Multi-provider gateway with built-in logging |
| Arize Phoenix | OSS | Yes | Strong on embedding drift + RAG evaluation |
| Braintrust | SaaS | Yes | Unified eval + CI/CD integration for prompt testing |

## Templates & scripts
See `templates.md` for: Langfuse self-hosting Docker Compose, LangSmith `@traceable` decorator patterns, OTEL span configuration.

Inline: cost + quality dashboard metric emitter (~30 lines):

```python
from dataclasses import dataclass
from langfuse import Langfuse

langfuse = Langfuse()

@dataclass
class CallMetrics:
    trace_id: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    quality_score: float | None = None

COST_PER_M = {"claude-haiku-4-5": {"in": 0.8, "out": 4.0}, "claude-sonnet-4-5": {"in": 3.0, "out": 15.0}}

def emit_metrics(m: CallMetrics):
    p = COST_PER_M.get(m.model, {"in": 3.0, "out": 15.0})
    cost = (m.input_tokens * p["in"] + m.output_tokens * p["out"]) / 1_000_000
    langfuse.score(trace_id=m.trace_id, name="cost_usd", value=cost)
    langfuse.score(trace_id=m.trace_id, name="latency_ms", value=m.latency_ms)
    if m.quality_score is not None:
        langfuse.score(trace_id=m.trace_id, name="quality", value=m.quality_score)
```

## Best practices
- Assign a stable `session_id` to each user conversation and `trace_id` to each agent invocation — link them explicitly
- Log `input_tokens`, `output_tokens`, and `model` on every generation span — this is the minimum for cost attribution
- Implement LLM-as-judge only for sampled traffic (5-20%) to avoid runaway evaluation costs
- Set up cost alerts at 80% of daily budget with Langfuse's `score` API + external alerting (PagerDuty, Telegram)
- Use prompt versioning in Langfuse/LangSmith — never edit prompts in-place; always create a new version and A/B test
- Keep trace context (`trace_id`, `session_id`) in a context variable (Python's `contextvars.ContextVar`) so all nested calls inherit it automatically
- Sample verbose traces in production: log 100% in dev, 10-20% in prod with full content, 100% with metadata only

## AI-agent gotchas
- Human-in-loop checkpoint: if quality scores drop below threshold for >N consecutive calls, pause the pipeline and alert — don't let degraded output accumulate
- LLM-as-judge evaluators are themselves LLMs — they hallucinate scores; validate judge calibration against human labels before trusting automated evals
- Trace correlation breaks across async boundaries; use `contextvars` not thread-locals to propagate trace context through asyncio tasks
- Logging raw prompts/responses in multi-tenant systems leaks one tenant's data into another tenant's trace if session_id is misconfigured — validate isolation
- OTEL exporter batches spans and flushes asynchronously — on sudden process exit, recent spans are lost; call `langfuse.flush()` in shutdown handlers

## References
- https://langfuse.com/docs
- https://docs.langchain.com/langsmith
- https://helicone.ai/docs
- https://portkey.ai/docs
- https://docs.arize.com/phoenix
- https://www.firecrawl.dev/blog/best-llm-observability-tools
