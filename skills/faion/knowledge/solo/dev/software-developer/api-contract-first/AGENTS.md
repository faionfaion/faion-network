---
slug: api-contract-first
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Write the OpenAPI spec before any implementation code, get it reviewed like a PR, then generate server stubs and client SDKs from it.
content_id: "f1552678fa2df930"
tags: [api-design, openapi, contract-testing, code-generation, specification]
---
# API Contract-First Development

## Summary

**One-sentence:** Write the OpenAPI spec before any implementation code, get it reviewed like a PR, then generate server stubs and client SDKs from it.

**One-paragraph:** Write the OpenAPI spec before any implementation code, get it reviewed like a PR, then generate server stubs and client SDKs from it. The spec is the source of truth; CI validates that the running implementation still matches it. Breaking changes require spec version bumps.

## Applies If (ALL must hold)

- Starting a new API that will have external consumers or multiple client teams.
- Adding a significant new resource or workflow to an existing API.
- Integrating with a partner that requires a published contract.
- Any API where mobile and backend teams work in parallel.

## Skip If (ANY kills it)

- Internal APIs consumed only by one service written by the same team.
- Rapid prototyping where the API shape is still being discovered.
- APIs that are wrappers over a third-party spec (just import their spec).
- Micro-services that communicate exclusively over gRPC/protobuf.

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

- parent skill: `solo/dev/software-developer/`
