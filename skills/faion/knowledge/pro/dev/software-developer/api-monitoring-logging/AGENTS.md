---
slug: api-monitoring-logging
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Every API request MUST be logged in JSON format with a unique request_id, HTTP metadata, response status and duration.
content_id: "7cddc7ebfb2007d1"
tags: [api-monitoring, structured-logging, opentelemetry, observability, tracing]
---
# API Structured Logging with Trace Context

## Summary

**One-sentence:** Every API request MUST be logged in JSON format with a unique request_id, HTTP metadata, response status and duration.

**One-paragraph:** Every API request MUST be logged in JSON format with a unique request_id, HTTP metadata, response status and duration. Logs MUST include trace_id and span_id from OpenTelemetry context so logs and traces join in the observability platform. Sensitive fields (passwords, tokens, PAN) MUST be redacted before export.

## Applies If (ALL must hold)

- Any API shipping to production that needs searchable request history.
- When migrating from print() or unstructured logger calls to a production logging setup.
- When instrumenting with OpenTelemetry and wanting logs to join traces.
- Before onboarding a service into a log aggregation platform (Loki, Datadog, CloudWatch).

## Skip If (ANY kills it)

- Pre-product-fit prototypes — log-to-stdout with print() or basic logger is sufficient; structured logging adds setup cost without proportional value.
- Internal scripts and one-shot tools — structured logging overhead (JSON serialization, context propagation) is not justified for tools that run for minutes.
- Compliance contexts (HIPAA, PCI) where log export pipelines are not yet cleared for PHI/PAN — establish redaction and encryption first, then add structured logging.

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

- parent skill: `pro/dev/software-developer/`
