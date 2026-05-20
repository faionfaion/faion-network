---
slug: contract-first-development
tier: solo
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design API contracts (OpenAPI spec) before writing implementation code.
content_id: "2bd87b8001fa08e5"
tags: [openapi, api-design, contract, codegen]
---
# Contract-First Development

## Summary

**One-sentence:** Design API contracts (OpenAPI spec) before writing implementation code.

**One-paragraph:** Design API contracts (OpenAPI spec) before writing implementation code. The spec is the source of truth: server stubs, client SDKs, mock servers, and contract tests are all generated from it. No server code is written until the spec passes spectral lint and human review. Spec changes are treated like code — PR review, semver, oasdiff breaking-change detection in CI.

## Applies If (ALL must hold)

- New API with multiple consumers (frontend, mobile, partners) planned or existing.
- Cross-team handoff where BE and FE build in parallel.
- Public or partner APIs needing stable, versioned, machine-readable contracts.
- AI-agent-generated services — spec prevents drift between iterations.
- Microservices where service boundaries are evolving and need explicit contracts to prevent drift.

## Skip If (ANY kills it)

- One-off internal scripts or single-team tools where overhead exceeds value.
- Highly experimental endpoints during prototyping (spec churn dominates).
- Pure GraphQL stacks — schema-first GraphQL achieves the same with different tooling.
- gRPC — .proto is already the contract; different tools apply.
- Server-rendered web apps where the API is HTML forms, not JSON.

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
