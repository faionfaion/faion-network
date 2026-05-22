---
slug: interface-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identifies, documents, and validates all connection points between a solution and external systems, users, hardware, or communication channels.
content_id: "2cf51d161bc39848"
tags: [interface-requirements, system-integration, api-contracts, openapi, interface-testing]
---
# Interface Analysis

## Summary

**One-sentence:** Identifies, documents, and validates all connection points between a solution and external systems, users, hardware, or communication channels.

**One-paragraph:** Identifies, documents, and validates all connection points between a solution and external systems, users, hardware, or communication channels. Each interface gets a stable ID (IF-XXX) referenced from requirements.md, design.md, and test-plan.md. Specs are generated from or synced to OpenAPI / AsyncAPI / Protobuf — never hand-typed as the primary source of truth. Breaking changes detected via `oasdiff` in CI.

## Applies If (ALL must hold)

- A new feature in SDD `design.md` introduces system-to-system data flow and the spec lacks payload schemas, error codes, auth, or SLA fields.
- Onboarding a third-party SaaS (Stripe, SendGrid, Twilio) before writing client code.
- Migrating between providers where direction, format, and protocol diff must be documented.
- Decomposing a monolith into services: each split point needs a contract before the team commits.
- Drafting acceptance criteria for `test-plan.md` tasks that test integration boundaries (contract tests, mocks, error scenarios).

## Skip If (ANY kills it)

- Pure-internal refactor where caller and callee live in the same process and module boundary — an ADR is enough.
- Throwaway scripts and one-off data migrations.
- Greenfield prototype before product-market fit — defer formal specs until the contract starts changing under multiple consumers.
- UI-only changes that do not alter the data envelope.

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

- parent skill: `pro/ba/ba-modeling/`
