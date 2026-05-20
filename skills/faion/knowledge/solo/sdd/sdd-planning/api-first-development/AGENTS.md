---
slug: api-first-development
tier: solo
group: sdd
domain: sdd-planning
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design the OpenAPI 3.
content_id: "64f2f21f004d320e"
tags: [api, openapi, contract, specification, design-first]
---
# API-First Development

## Summary

**One-sentence:** Design the OpenAPI 3.

**One-paragraph:** Design the OpenAPI 3.1 contract before writing any implementation code. The spec is the single source of truth: generate server stubs, client SDKs, mock servers, and contract tests from it. Every endpoint, schema, and error format is decided in YAML before a line of backend code exists. API-first design surfaces usability problems early, enables parallel frontend and backend development via mock servers (Prism), and prevents implementation-driven inconsistency across services.

## Applies If (ALL must hold)

- Multiple consumers planned (frontend, mobile, third-party) before backend is written.
- Frontend and backend agents or teams work in parallel: mock server unblocks frontend.
- Public or partner-facing API where contract stability is a hard requirement.
- Microservice boundaries require agreed contracts before implementation begins.
- SDK generation is needed (client libraries from spec).
- API governance required: linting rules enforce naming, versioning, error format.

## Skip If (ANY kills it)

- Internal single-consumer service where spec would be written after implementation anyway (YAGNI).
- Rapid prototype with fewer than 3 endpoints: design overhead exceeds benefit.
- GraphQL-first projects: OpenAPI is REST-specific; use AsyncAPI for event-driven.
- No CI pipeline to enforce spec compliance: spec drift will occur within weeks.

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

- parent skill: `solo/sdd/sdd-planning/`
