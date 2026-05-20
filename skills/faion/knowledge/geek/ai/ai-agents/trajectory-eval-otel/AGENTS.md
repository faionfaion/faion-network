---
slug: trajectory-eval-otel
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Score agent runs on three axes simultaneously: outcome (was the answer right?), trajectory (was the path optimal?), and resources (tokens, cost, steps).
content_id: "2c330c6255a56561"
tags: [evaluation, observability, otel, telemetry]
---
# Trajectory Evaluation with OTel GenAI Spans

## Summary

**One-sentence:** Score agent runs on three axes simultaneously: outcome (was the answer right?), trajectory (was the path optimal?), and resources (tokens, cost, steps).

**One-paragraph:** Score agent runs on three axes simultaneously: outcome (was the answer right?), trajectory (was the path optimal?), and resources (tokens, cost, steps). Capture trajectories using OpenTelemetry GenAI semantic conventions so traces flow uniformly to any OTLP backend.

## Applies If (ALL must hold)

- Production agents where you need to debug regressions
- A/B comparing prompts, models, or trajectories
- Cost optimization finding which tasks burn the most
- Compliance and audit (regulated industries need replayable traces)
- Multi-agent systems where you need to know which subagent did what

## Skip If (ANY kills it)

- One-shot personal scripts where instrumenting takes longer than the script
- When telemetry would leak PII; redact at the span boundary or use a privacy-preserving collector
- When the OTel overhead matters in latency-critical paths (rare; instrumentation is usually less than 1ms per span)

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

- parent skill: `geek/ai/ai-agents/`
