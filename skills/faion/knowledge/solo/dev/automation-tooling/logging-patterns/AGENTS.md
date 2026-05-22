---
slug: logging-patterns
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured JSON logging with request tracking, PII redaction, and performance visibility.
content_id: "1554d307ae7110f6"
tags: [logging, structured-logging, observability, monitoring, json]
---
# Logging Patterns

## Summary

**One-sentence:** Structured JSON logging with request tracking, PII redaction, and performance visibility.

**One-paragraph:** Structured JSON logging with request tracking, PII redaction, and performance visibility.

## Applies If (ALL must hold)

- Standing up a new service that will hit production: structured JSON from day one.
- Migrating from print() / console.log to a real logger before observability rollout.
- Adding correlation IDs to a multi-service flow so a single trace can be reconstructed.
- Compliance domains needing audit trails (who did what, when, with what payload hash).
- Debugging async/concurrent code where order of execution is non-trivial.

## Skip If (ANY kills it)

- One-off CLI scripts where stderr/stdout suffices.
- Hot loops (>1M iterations/sec) — even structured logging is too slow; use sampling or metrics counters.
- Replacing tracing — logs answer "what happened", traces answer "how long and where". Use both.
- High-PII contexts without scrubbing infra in place — better to not log than to leak.

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

- parent skill: `solo/dev/automation-tooling/`
