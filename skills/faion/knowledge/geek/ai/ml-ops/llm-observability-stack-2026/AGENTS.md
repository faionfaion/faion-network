---
slug: llm-observability-stack-2026
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive monitoring for production AI applications requires integrating multiple platforms: tracing (Langfuse), cost analytics (Helicone), evaluation (Arize Phoenix), and multi-agent tracing (Braintrust).
content_id: "850643e647547f3d"
tags: [observability, monitoring, llm, tracing, cost-analytics]
---
# LLM Observability Stack (2026)

## Summary

**One-sentence:** Comprehensive monitoring for production AI applications requires integrating multiple platforms: tracing (Langfuse), cost analytics (Helicone), evaluation (Arize Phoenix), and multi-agent tracing (Braintrust).

**One-paragraph:** Comprehensive monitoring for production AI applications requires integrating multiple platforms: tracing (Langfuse), cost analytics (Helicone), evaluation (Arize Phoenix), and multi-agent tracing (Braintrust). The 2026 stack combines self-hostable open-source tools with SaaS options, enabling cost tracking, quality metrics, performance monitoring, and reliability analysis across production LLM pipelines.

## Applies If (ALL must hold)

- Deploying any LLM-powered feature to production that requires quality, cost, or latency monitoring.
- Diagnosing unexpected behavior in a multi-step agent pipeline (which tool call failed? which prompt version regressed?).
- Running A/B tests on prompt variants with statistical tracking of quality metrics.
- Setting up cost alerts before a large-scale rollout to avoid budget overruns.
- Auditing an existing LLM system with no observability to identify the highest-impact gaps.

## Skip If (ANY kills it)

- The system is a prototype or one-off script making fewer than 100 LLM calls — the setup cost exceeds the value; use provider dashboards directly.
- The team has no process for reviewing dashboards — observability tooling without a review cadence generates noise, not insight.
- Real-time latency budget is so tight that proxy-based tools (Helicone) add unacceptable overhead — use SDK-based tools (Langfuse decorators) which add <1ms.
- The application handles highly sensitive PII and the observability vendor is not cleared for that data class — use self-hosted Langfuse or Phoenix only.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ml-ops/`
