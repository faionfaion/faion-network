---
slug: microservices-observability
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Distributed tracing is the API for debugging microservices.
content_id: "fc3bd4df0e8408a5"
tags: [microservices, observability, distributed-tracing, schema-registry, opentelemetry]
---
# Microservices Observability and Boundary Integrity

## Summary

**One-sentence:** Distributed tracing is the API for debugging microservices.

**One-paragraph:** Distributed tracing is the API for debugging microservices. Every inbound request opens a span; every outbound call propagates traceparent. Schema registry with compatibility checks is non-optional once event payloads become public APIs. A boundary lint script detects sync chains, missing timeouts, and shared-DB imports before they reach production.

## Applies If (ALL must hold)

- Any microservices system in production where "which service caused this error?" is a real question.
- Systems with more than two services publishing events that other services consume.
- CI pipelines for any microservices codebase where boundary violations need automated detection.
- Teams onboarding a new service: tracing and schema registry must be configured before the first production deploy.

## Skip If (ANY kills it)

- Single-service monoliths — standard logging and APM are sufficient; distributed tracing adds complexity without value.
- Prototypes and throwaway experiments where operational overhead exceeds value.

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
