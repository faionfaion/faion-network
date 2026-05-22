---
slug: api-documentation
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Developers abandon APIs with poor documentation — missing authentication examples and absent error tables are the top complaints.
content_id: "01de24b2a9730613"
tags: [api, documentation, openapi, swagger, developer-experience]
---
# API Documentation

## Summary

**One-sentence:** Developers abandon APIs with poor documentation — missing authentication examples and absent error tables are the top complaints.

**One-paragraph:** Developers abandon APIs with poor documentation — missing authentication examples and absent error tables are the top complaints. OpenAPI's examples field lets you embed multiple named request variants directly in the spec; Swagger UI renders them as selectable try-it-out presets. Keeping examples verified by tests prevents docs from drifting from the actual API behaviour.

## Applies If (ALL must hold)

- Launching a new API to external or internal consumers
- Migrating from ad-hoc Markdown docs to an OpenAPI-driven setup
- When support tickets repeatedly ask for authentication examples or error code meanings
- Generating client SDKs from the spec

## Skip If (ANY kills it)

- Purely internal service-to-service APIs where code is the contract and no SDK is needed
- Prototype APIs under active design flux — write docs after the contract stabilises
- Micro-service mesh where service mesh observability tools (Envoy, Istio) already surface contracts

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

- parent skill: `solo/dev/api-developer/`
