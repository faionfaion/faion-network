# LLM Observability Stack

## Summary

Production observability stack for AI/LLM systems: tracing (Langfuse/Phoenix/LangSmith), cost analytics (Helicone/Portkey), quality evaluation (LLM-as-judge), and alerting (Prometheus/Grafana). OpenTelemetry is the emerging standard for vendor-neutral LLM tracing in 2026.

## Why

LLM systems fail in ways invisible to traditional APM: hallucinations, cost spikes, TTFT degradation, and multi-turn context corruption. A dedicated observability stack exposes token cost per conversation, per-request quality scores, and agent reasoning chains — none of which are visible in CPU/memory metrics.

## When To Use

- Going to production with an LLM feature — set up tracing before the first real users
- Diagnosing quality regressions after a model, prompt, or retrieval change
- Enforcing budget controls: daily spend alerts, cost per team/feature
- Debugging agentic loops with nested tool calls and multi-step reasoning
- Compliance contexts requiring audit trails of every LLM interaction

## When NOT To Use

- Prototype/experiment phase where data volume is negligible — add a TODO for later
- Purely batch offline workloads with no SLA — standard job monitoring suffices
- Primary bottleneck is something other than LLM calls (DB, network) — profile those first

## Content

| File | What's inside |
|------|---------------|
| `content/01-stack-components.xml` | Platform comparison (Langfuse/Phoenix/LangSmith/Helicone), OTEL integration, metrics taxonomy, stack selection decision tree |
| `content/02-instrumentation-rules.xml` | Instrumentation rules, alert thresholds, cost tracking, agent tracing patterns, antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/langfuse-stack.yaml` | Docker Compose: Langfuse + Prometheus + Grafana + OTEL Collector |
| `templates/alert-rules.yaml` | Prometheus alert rules for error rate, latency, cost, quality, cache hit rate |
| `templates/pricing.yaml` | Model pricing config (Q1 2026) for cost calculation |
