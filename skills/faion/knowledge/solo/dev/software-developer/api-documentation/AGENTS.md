---
slug: api-documentation
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Document every API with an OpenAPI spec that includes: overview, authentication instructions, working code examples (curl + at least one SDK), all error codes with resolution hints, and a changelog.
content_id: "01de24b2a9730613"
tags: [api-docs, openapi, swagger-ui, redoc, documentation]
---
# API Documentation

## Summary

**One-sentence:** Document every API with an OpenAPI spec that includes: overview, authentication instructions, working code examples (curl + at least one SDK), all error codes with resolution hints, and a changelog.

**One-paragraph:** Document every API with an OpenAPI spec that includes: overview, authentication instructions, working code examples (curl + at least one SDK), all error codes with resolution hints, and a changelog. Host interactive docs via Swagger UI (`/docs`) and readable reference via Redoc (`/redoc`).

## Applies If (ALL must hold)

- Publishing any API consumed by external developers or third-party integrations.
- Setting up a new FastAPI or Django project where OpenAPI is auto-generated.
- Adding examples and error tables to an existing, poorly documented API.
- Preparing an API for SDK generation.

## Skip If (ANY kills it)

- Internal micro-services with no external consumers — a brief AGENTS.md is enough.
- Prototypes that will be redesigned before any consumer integrates.
- CLI tools — man pages and --help flags are the right format.

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
