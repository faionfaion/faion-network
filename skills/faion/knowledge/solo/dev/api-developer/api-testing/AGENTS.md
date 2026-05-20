---
slug: api-testing
tier: solo
group: dev
domain: api-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured methodology for verifying HTTP/gRPC/GraphQL API correctness using a layered pyramid: unit tests (many), integration tests (some), contract tests (consumer-driven, for cross-team interfaces), and E2E tests (few).
content_id: "c80e7177e2b3dc32"
tags: [api-testing, testing, contract-testing, quality-assurance, spec-conformance]
---
# API Testing

## Summary

**One-sentence:** Structured methodology for verifying HTTP/gRPC/GraphQL API correctness using a layered pyramid: unit tests (many), integration tests (some), contract tests (consumer-driven, for cross-team interfaces), and E2E tests (few).

**One-paragraph:** Structured methodology for verifying HTTP/gRPC/GraphQL API correctness using a layered pyramid: unit tests (many), integration tests (some), contract tests (consumer-driven, for cross-team interfaces), and E2E tests (few). Every endpoint must have at least one negative test (missing auth, wrong role, malformed body, rate limit).

## Applies If (ALL must hold)

- Any HTTP/gRPC/GraphQL service heading toward production. The pyramid (unit → integration → contract → e2e) applies.
- Cross-team interfaces where consumer and provider deploy independently — contract tests (Pact / Spring Cloud Contract / pact-broker) catch drift.
- API published with an OpenAPI / GraphQL / Protobuf spec — automatic spec-conformance tests close the spec/code gap.
- Public SaaS API where SLA includes correctness + behavior (rate limit, idempotency, error shape).
- Refactor / version bump — regression suite is the safety net.

## Skip If (ANY kills it)

- Throwaway prototype. Smoke test with curl, ship.
- When the test costs more to maintain than the bug it would catch (low-traffic admin endpoint with no consumers).
- Replacing static type checks with runtime tests — let TypeScript / mypy / pydantic catch what they can.
- 100%-coverage cargo cult — coverage is a leading indicator, not a goal.

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
