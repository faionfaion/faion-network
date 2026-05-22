---
slug: llm-observability-stack
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production observability stack for LLM systems: tracing, cost analytics, quality evaluation, and alerting via OpenTelemetry.
content_id: "a62b9df426e45416"
tags: [llm, observability, tracing, monitoring, otel, langfuse, prometheus]
---
# LLM Observability Stack

## Summary

**One-sentence:** Production observability stack for LLM systems: tracing, cost analytics, quality evaluation, and alerting via OpenTelemetry.

**One-paragraph:** Production observability stack for LLM systems: tracing, cost analytics, quality evaluation, and alerting via OpenTelemetry. Vendor-neutral approach for 2026.

## Applies If (ALL must hold)

- Going to production with an LLM feature — set up tracing before the first real users
- Diagnosing quality regressions after a model, prompt, or retrieval change
- Enforcing budget controls: daily spend alerts, cost per team/feature
- Debugging agentic loops with nested tool calls and multi-step reasoning
- Compliance contexts requiring audit trails of every LLM interaction
- Daily LLM call volume crosses ~100 calls/day or monthly cost crosses ~$50

## Skip If (ANY kills it)

- Prototype/experiment phase where data volume is negligible — add a TODO for later
- Purely batch offline workloads with no SLA — standard job monitoring suffices
- Primary bottleneck is something other than LLM calls (DB, network) — profile those first

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

- parent skill: `geek/ai/ml-engineer/`
