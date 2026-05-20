---
slug: api-contract-first
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design the OpenAPI spec before writing any implementation code.
content_id: "f1552678fa2df930"
tags: [contract-first, openapi, code-generation, api-design, specification]
---
# API Contract-First Development

## Summary

**One-sentence:** Design the OpenAPI spec before writing any implementation code.

**One-paragraph:** Design the OpenAPI spec before writing any implementation code. The spec is reviewed like a PR, then used to generate server stubs, typed client SDKs, and contract test scaffolding via openapi-generator. CI lints the spec with Spectral on every change and validates the running implementation against the spec with openapi-core. The spec is the single source of truth, reviewed before any code exists, making breaking changes visible at design time.

## Applies If (ALL must hold)

- New APIs where frontend and backend are developed in parallel (spec enables frontend to mock immediately)
- APIs that will be versioned and shared with external consumers
- Multi-team / multi-language platforms where producers and consumers develop in parallel from a shared OpenAPI / AsyncAPI / Protobuf contract
- B2B partner integrations where the contract is a published, versioned artifact subject to change-management
- LLM-driven backend authoring where agents thrive on a strict spec; codegen + contract tests catch drift before merge
- Migration projects (legacy → modular monolith → microservices) where the spec freezes external behavior while internals change
- SDK-distribution products where TypeScript / Python / Go clients must regenerate from one source on every release
- Teams that want spec-driven SDK generation to avoid hand-written client code
- When breaking change detection is required in CI

## Skip If (ANY kills it)

- Internal scripts or glue APIs used only by one service—spec overhead is disproportionate
- Rapidly evolving prototypes where the contract changes every day—lock it down first
- Solo prototypes / spike code where the API is volatile and round-trip codegen overhead exceeds the design value
- Teams without OpenAPI / Protobuf fluency—premature contracts written by non-fluent authors produce worse APIs than code-first iteration
- Domains where the contract genuinely cannot be predicted (research / ML scoring with evolving outputs)
- GraphQL APIs—use SDL as the contract instead of OpenAPI

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
