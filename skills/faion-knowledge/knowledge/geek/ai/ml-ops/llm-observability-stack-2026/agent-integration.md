# Agent Integration — LLM Observability Stack (2026)

## When to use
- Deploying any LLM-powered feature to production that requires quality, cost, or latency monitoring
- Diagnosing unexpected behavior in a multi-step agent pipeline (which tool call failed? which prompt version regressed?)
- Running A/B tests on prompt variants with statistical tracking of quality metrics
- Setting up cost alerts before a large-scale rollout to avoid budget overruns
- Auditing an existing LLM system with no observability to identify the highest-impact gaps

## When NOT to use
- The system is a prototype or one-off script making fewer than 100 LLM calls — the setup cost exceeds the value; use provider dashboards directly
- The team has no process for reviewing dashboards — observability tooling without a review cadence generates noise, not insight
- Real-time latency budget is so tight that proxy-based tools (Helicone) add unacceptable overhead — use SDK-based tools (Langfuse decorators) which add <1ms
- The application handles highly sensitive PII and the observability vendor is not cleared for that data class — use self-hosted Langfuse or Phoenix only

## Where it fails / limitations
- Langfuse `@observe` decorator traces synchronous calls cleanly but requires manual span management for async agents; missed spans produce incomplete traces
- Helicone proxy caching can serve stale cached responses if prompt templates use dynamic date/time fields — cache keys must include variable portions or caching must be disabled per endpoint
- Arize Phoenix `llm_classify` uses an LLM call to evaluate outputs — evaluation cost can approach 50-100% of production call cost if sample rate is too high
- Alert fatigue is a real failure mode: setting thresholds too tight produces dozens of alerts per day that get ignored; calibrate thresholds against 2 weeks of baseline data first
- Braintrust does not support self-hosting — if data residency or air-gapped deployment is required, it cannot be used
- Weights & Biases experiment tracking captures training metrics well but is not designed for production inference monitoring; do not use it as a Langfuse replacement

## Agentic workflow
An agent implementing observability should instrument all LLM calls with trace IDs from the start of the pipeline, attach cost and latency metadata to each span, and push quality scores (via LLM-as-judge or heuristic checks) to the same trace. A monitoring subagent can query the observability platform API daily, detect metric regressions vs. the 7-day rolling baseline, and create SDD tasks for investigation when thresholds are breached.

### Recommended subagents
- `faion-sdd-executor-agent` — drives observability setup tasks from an SDD task card
- A monitoring subagent (custom) — queries Langfuse API for daily aggregates, compares to baseline, creates alerts or SDD tasks on regression

### Prompt pattern
```
Review these LLM observability metrics for the past 24h:
- Error rate: {error_rate}% (baseline: {baseline_error}%)
- P95 latency: {p95_ms}ms (baseline: {baseline_p95}ms)
- Avg cost/request: ${avg_cost} (baseline: ${baseline_cost})
- Cache hit rate: {cache_rate}%

Identify which metrics are outside acceptable range (>20% deviation from baseline).
Return JSON: {"alerts": [{"metric": str, "severity": "warn|critical", "action": str}]}
```

```
Given the following Langfuse trace for a failed agent run:
{trace_json}
Identify: which step failed, what error occurred, and whether it's a prompt, tool, or model issue.
Return: {"failed_step": str, "error_type": str, "root_cause": str, "fix": str}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langfuse` (Python SDK) | Trace LLM calls, score outputs, version prompts | `pip install langfuse` / [langfuse.com/docs](https://langfuse.com/docs) |
| `helicone` (proxy) | Cost analytics, caching, rate limiting via URL change | Change `base_url` only / [docs.helicone.ai](https://docs.helicone.ai) |
| `arize-phoenix` | Evaluation, embedding visualization, RAG metrics | `pip install arize-phoenix` / [docs.arize.com/phoenix](https://docs.arize.com/phoenix) |
| `opentelemetry-sdk` | Vendor-neutral tracing instrumentation | `pip install opentelemetry-sdk openinference-instrumentation-openai` / [opentelemetry.io](https://opentelemetry.io/) |
| `wandb` | Experiment tracking for fine-tuning runs | `pip install wandb` / [docs.wandb.ai](https://docs.wandb.ai/) |
| Portkey CLI | Gateway setup with fallbacks and load balancing | [portkey.ai/docs](https://portkey.ai/docs) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | SaaS + OSS (MIT) | Yes — Python/JS SDK, REST API | Self-hostable; best for prompt versioning + tracing |
| Helicone | SaaS + OSS | Yes — proxy, no SDK change | Fastest setup; 20-30% cost savings via semantic caching |
| Arize Phoenix | SaaS + OSS | Yes — `phoenix.evals` module | Best for RAG evaluation and embedding drift detection |
| Braintrust | SaaS only | Yes — SDK + REST | Strong multi-agent tracing; no self-host |
| Portkey | SaaS + limited OSS | Yes — REST gateway | Fallback routing, load balancing across providers |
| Weights & Biases | SaaS | Yes — `wandb` Python SDK | Fine-tuning experiment tracking; not for prod inference |
| Datadog LLM Observability | SaaS | Yes — `ddtrace` | Best if team already uses Datadog; adds LLM spans |

## Templates & scripts
See `templates.md` for full Langfuse self-hosted Docker Compose and alert configuration.

Inline — Langfuse decorator + cost tagging for any LLM call (≤30 lines):

```python
import os
from langfuse.decorators import observe, langfuse_context
from openai import OpenAI

client = OpenAI()

@observe(name="llm-call")
def call_llm(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    # Attach cost metadata to the trace span
    langfuse_context.update_current_observation(
        usage={
            "input": response.usage.prompt_tokens,
            "output": response.usage.completion_tokens,
            "unit": "TOKENS",
        },
        model=model,
    )
    return content

# All calls to call_llm() are automatically traced in Langfuse
# with latency, token usage, and cost breakdown per model.
```

## Best practices
- Start with Helicone (15-minute setup, immediate cost dashboard) before adding Langfuse — getting baseline cost data first makes Langfuse alert calibration much easier
- Self-host Langfuse (`docker compose up`) if the application handles customer PII — the MIT license permits it and the setup is under 30 minutes
- Set TTFT (time to first token) as a separate metric from total latency for streaming endpoints — TTFT is what users perceive as "responsiveness"
- Use `langfuse_context.update_current_observation` to attach business metadata (user_id, session_id, feature_name) to every trace — this enables per-feature cost attribution
- Calibrate alert thresholds on 7-14 days of production baseline data before enabling alerts; premature thresholds produce alert fatigue that causes real issues to be ignored
- Version prompts in Langfuse before any A/B test — unversioned prompts make it impossible to correlate metric changes to specific prompt edits after the fact
- Cache only idempotent, deterministic requests (knowledge lookups, classification) — never cache personalized or time-sensitive responses

## AI-agent gotchas
- Async agent pipelines break Langfuse `@observe` context propagation — use explicit `trace_id` threading via `langfuse_context.get_current_trace_id()` and pass it to subagents
- Helicone proxy adds ~20-50ms round-trip latency; agents with sub-100ms latency budgets must use SDK-based instrumentation instead
- Phoenix `llm_classify` for evaluation makes one LLM call per evaluated response — at 10% sample rate on 10k daily requests, this is 1k additional calls per day; budget for it explicitly
- Trace IDs must be propagated across agent boundaries (subagent calls) or the observability view will show disconnected traces rather than a unified pipeline view
- Langfuse scores (quality metrics) must be submitted asynchronously after the response is returned — blocking the main response on score submission adds 200-500ms latency per call

## References
- [Langfuse Documentation](https://langfuse.com/docs)
- [Helicone Documentation](https://docs.helicone.ai)
- [Arize Phoenix](https://docs.arize.com/phoenix)
- [Braintrust AI](https://www.braintrust.dev/docs)
- [OpenTelemetry for LLMs (OpenInference)](https://github.com/Arize-ai/openinference)
- [Portkey — AI Gateway](https://portkey.ai/docs)
- [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/)
