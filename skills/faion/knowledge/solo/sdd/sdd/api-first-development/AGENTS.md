---
slug: api-first-development
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design the OpenAPI 3.
content_id: "64f2f21f004d320e"
tags: [api-design, openapi, specification, contract-driven, code-generation]
---
# API-First Development

## Summary

**One-sentence:** Design the OpenAPI 3.

**One-paragraph:** Design the OpenAPI 3.1 specification before writing any implementation code. The spec is the contract: it drives mock server generation (Prism), server stub generation (OpenAPI Generator), client SDK creation, and contract testing (schemathesis/dredd). The spec must be kept in sync with the implementation via CI contract tests — a spec that lies is worse than no spec.

## Applies If (ALL must hold)

- Starting a new API — design the spec before writing any implementation code.
- Frontend and backend developed in parallel — spec enables Prism mock server for frontend.
- Generating server stubs, client SDKs, or TypeScript types from spec rather than writing by hand.
- Onboarding an LLM to implement or test an API — full OpenAPI spec as context eliminates ambiguity.
- Multiple consumers (web, mobile, third-party) will use the API — spec is the shared contract.

## Skip If (ANY kills it)

- Internal one-off scripts or single-consumer CLI tools with no formal contract.
- Rapidly prototyping throw-away spikes — write code first, extract spec after it stabilizes.
- GraphQL APIs — GraphQL has its own SDL-first approach; OpenAPI does not map cleanly.
- Simple CRUD with no external consumers — spec maintenance overhead exceeds benefit.

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

- parent skill: `solo/sdd/sdd/`
