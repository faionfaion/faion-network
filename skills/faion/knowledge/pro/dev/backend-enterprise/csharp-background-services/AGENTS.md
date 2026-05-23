---
slug: csharp-background-services
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a robust BackgroundService / IHostedService implementation with graceful shutdown, retry, idempotency, and metrics.
content_id: "f5279dc4c64dcab9"
complexity: medium
produces: code
est_tokens: 4500
tags: [csharp, background-service, ihostedservice, queue, code]
---

# C# Background Services

## Summary

**One-sentence:** Produces a robust BackgroundService / IHostedService implementation with graceful shutdown, retry, idempotency, and metrics.

**One-paragraph:** Produces a robust BackgroundService / IHostedService implementation with graceful shutdown, retry, idempotency, and metrics. Mechanism: typed input → bounded transformation → contract-checked output. The artefact carries owner + version + last_reviewed so downstream consumers can verify freshness.

**Ефективно для:**

- Queue consumer / scheduler / file watcher з graceful shutdown і bounded drain.
- Idempotent work units під at-least-once delivery.
- Observability як first-class concern (metrics + tracing per work unit).

## Applies If (ALL must hold)

- Service runs a long-lived background loop (queue consumer, scheduler, watcher).
- Process must shut down gracefully on SIGTERM with bounded drain time.
- Work units must be idempotent to survive at-least-once delivery.

## Skip If (ANY kills it)

- One-shot CLI / job runner — Worker Service overkill.
- Periodic job better expressed as a cron-triggered Function / Lambda.
- Hosted in IIS in-process — BackgroundService lifecycle does not align cleanly.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Worker scope (queue / scheduler / watcher) | markdown | product |
| Idempotency key strategy | markdown | architecture |
| Observability stack (metrics + tracing) | config | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[csharp-aspnet-core]] | Hosted service runs inside the same Generic Host as the API |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output per step | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-skeleton` | haiku | Mechanical template emission |
| `wire-feature-logic` | sonnet | Per-feature judgment with bounded inputs |
| `audit-output` | sonnet | Verify rules in 01-core-rules.xml hold |

## Templates

| File | Purpose |
|------|---------|
| `templates/queue-consumer.cs` | BackgroundService queue-consumer skeleton with retry + idempotency |
| `templates/registration.cs` | Hosted-service registration snippet for Program.cs |
| `templates/_smoke-test.cs` | Filled-in minimal queue consumer for a Users.Created topic |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-csharp-background-services.py` | Validate output against 02-output-contract JSON Schema; exit 0 on pass, 1 on fail with violation list | After subagent returns, before downstream consumer reads; pre-commit |

## Related

- [[csharp-aspnet-core]]
- [[audit-grade-api-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals (input shape, evidence quality, scope, stakes) to a concrete action; every leaf references a rule id from `01-core-rules.xml` so the chosen action is grounded in a testable rule. Use it when in doubt about which variant of the methodology to apply.
