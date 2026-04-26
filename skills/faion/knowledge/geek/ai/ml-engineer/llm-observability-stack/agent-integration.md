# Agent Integration — LLM Observability Stack (2026)

## When to use
- Deploying any LLM feature to production — baseline requirement, not optional
- Debugging why an agent produces wrong or inconsistent outputs (trace the full span tree)
- Cost anomaly detected: a single pipeline consumes 10x expected tokens
- Evaluating prompt changes with before/after quality metrics
- Compliance audit requires an immutable record of every LLM call (PII, content safety)
- Multi-provider setup (OpenAI + Claude + Gemini) needs unified cost attribution

## When NOT to use
- Prototype or local dev where full tracing adds friction without benefit — use structured logging instead
- Offline batch jobs that run once; simple CSV output of token counts is enough
- Ultra-low-latency paths where the SDK instrumentation overhead (2-5ms) is unacceptable — sample at 1%

## Where it fails / limitations
- OpenTelemetry auto-instrumentation misses custom LLM wrappers — must add manual spans
- Langfuse/LangSmith traces become unreadable with >50 nested spans; prune intermediate steps
- LLM-as-judge evaluations are themselves non-deterministic — use temperature=0 and fixed seed
- Cost tracking via proxy (Helicone) adds a network hop; p99 latency may increase 5-15ms
- Self-hosted Langfuse requires Postgres + ClickHouse; Docker Compose setup breaks under high ingest
- Token counts from observability SDKs may differ from provider-reported counts by 1-3% (encoding differences)
- Agent loop iterations multiply trace depth quickly — set `max_depth` limits to keep dashboards usable

## Agentic workflow
Instrument every subagent call as a child span under the parent trace using OpenTelemetry or the platform's native SDK. For multi-agent pipelines, propagate `trace_id` through the task context so all subagent calls appear in one unified trace. Add a `session_id` attribute to group all turns of a multi-turn conversation. Use async flush to avoid blocking the critical path; buffer events locally and ship in batches every 1-2 seconds.

### Recommended subagents
- `faion-sdd-executor-agent` — can be instructed to wrap its LLM calls in a named trace and report span IDs back to the orchestrator

### Prompt pattern
```python
# Propagate trace context to subagent tasks
task_context = {
    "trace_id": current_span.get_span_context().trace_id,
    "session_id": session_id,
    "task": "Summarize the following document...",
}
```

```python
# Minimal Langfuse instrumentation
from langfuse.decorators import observe, langfuse_context

@observe(name="rag_pipeline")
def run_rag(query: str) -> str:
    langfuse_context.update_current_observation(input=query)
    result = retrieve_and_generate(query)
    langfuse_context.update_current_observation(output=result)
    return result
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `langfuse` SDK | Trace + prompt management + evals | `pip install langfuse` / [docs](https://langfuse.com/docs) |
| `openllmetry` | OTEL-based auto-instrumentation for 20+ frameworks | `pip install opentelemetry-sdk traceloop-sdk` / [github](https://github.com/traceloop/openllmetry) |
| `phoenix` (Arize) | Local OSS tracing + evaluation UI | `pip install arize-phoenix` / [docs](https://docs.arize.com/phoenix) |
| `helicone` proxy | Drop-in cost analytics via baseURL swap | `pip install helicone` / [docs](https://docs.helicone.ai) |
| `otel-cli` | Send OTEL spans from shell scripts | [github](https://github.com/equinix-labs/otel-cli) |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Langfuse | OSS + SaaS | Yes | Best OSS option; MIT; self-host on Docker Compose; native Python/JS SDKs |
| LangSmith | SaaS | Yes | Deep LangChain/LangGraph integration; limited self-host |
| Helicone | OSS proxy + SaaS | Yes | Drop-in via `openai(base_url=helicone_url)`; caching built-in |
| Arize Phoenix | OSS | Yes | Best for embedding analysis + RAG evals; runs fully local |
| Portkey | SaaS gateway | Yes | Multi-provider routing + observability; good for cost arbitrage |
| OpenLLMetry | OSS SDK | Yes | OTEL-native; 23 backends; pairs with any OTEL-compatible backend |
| Datadog LLM Obs. | SaaS | Partial | Enterprise APM integration; expensive; auto-instrumentation via ddtrace |
| Grafana + Prometheus | OSS | Partial | Custom dashboards only; pair with OpenLLMetry for LLM-specific metrics |

## Templates & scripts
```yaml
# docker-compose.yml — Langfuse self-hosted (minimal, ≤30 lines)
version: "3.8"
services:
  langfuse:
    image: langfuse/langfuse:latest
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgresql://langfuse:langfuse@db:5432/langfuse
      NEXTAUTH_SECRET: changeme
      SALT: changeme
    depends_on: [db]
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: langfuse
      POSTGRES_DB: langfuse
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

See `templates.md` for full alert rules and Grafana dashboard JSON.

## Best practices
- Instrument at the pipeline level first (one trace per user request), then add child spans per subagent call
- Tag every span with `user_id`, `session_id`, `model`, `pipeline_version` — enables segmented cost attribution
- Use sampling (10-20%) for high-volume paths; always record 100% of errors and slow traces (>5s)
- Export to OTEL collector so you can swap backends without code changes
- Run LLM-as-judge evals on a random 5% sample in a nightly job — avoid blocking production response
- Set cost alerts at 2x baseline; page at 5x — prevents runaway agent loops from draining budget
- Store raw prompts and completions encrypted at rest if they may contain PII; redact before display
- Pin observability SDK versions — breaking changes in Langfuse/Phoenix ship frequently

## AI-agent gotchas
- Multi-agent traces need explicit parent span propagation; without it each subagent creates a disconnected root trace
- Agentic loops generate O(N) spans for N iterations — set `max_iterations` or traces become unmanageable
- LLM-as-judge evaluations must use a different model from the one being evaluated to avoid self-serving bias
- Helicone proxy caching can return stale results to agents that expect fresh tool outputs — disable caching for tools
- OTEL batch exporter can drop spans under high load if queue is full; tune `max_export_batch_size` and `schedule_delay`
- Prompt version tracking: if you update a prompt mid-session, tag each span with `prompt_version` to avoid mixing metrics

## References
- [Langfuse Docs](https://langfuse.com/docs)
- [OpenLLMetry GitHub](https://github.com/traceloop/openllmetry)
- [Arize Phoenix Docs](https://docs.arize.com/phoenix)
- [Helicone Docs](https://docs.helicone.ai)
- [OpenTelemetry Semantic Conventions for LLMs](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [LLM Observability Tools 2026 — lakeFS](https://lakefs.io/blog/llm-observability-tools/)
- [Datadog LLM Observability](https://www.datadoghq.com/product/llm-observability/)
