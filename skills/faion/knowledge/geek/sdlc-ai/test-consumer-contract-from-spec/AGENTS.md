---
slug: test-consumer-contract-from-spec
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pact consumer contracts have one classic weakness: the consumer team has to write them.
content_id: "575eaf06f7644a7f"
tags: [pact, consumer-contract, openapi, can-i-deploy, microservices]
---
# Consumer Contract Tests Generated from OpenAPI / Traffic

## Summary

**One-sentence:** Pact consumer contracts have one classic weakness: the consumer team has to write them.

**One-paragraph:** Pact consumer contracts have one classic weakness: the consumer team has to write them. When that author is an LLM hand-rolling Pact JSON, the contract drifts from the actual provider spec and can-i-deploy becomes noise. The fix is to point an MCP server or skill at the canonical artifact — OpenAPI spec, recorded HTTP traffic, or typed client code — and have it generate the consumer Pact file plus matching client test. The generated contract is then committed as the source of truth and never edited by hand. PactFlow reports up to 60% reduction in test creation time and the AI-generated contracts are deterministic enough to gate provider deploys with can-i-deploy.

## Applies If (ALL must hold)

- Microservices with more than two consumers per provider, where mock drift is a recurring incident driver.
- Polyglot stacks where each consumer uses a different mock library and contracts diverge silently.
- Consumer services authored or maintained by a coding agent that has access to the provider's OpenAPI/AsyncAPI spec.
- Third-party API integrations where you control only the consumer side and need a reproducible mock.

## Skip If (ANY kills it)

- Single-consumer monolith calling a provider it owns — no contract gap to close, just integration tests.
- GraphQL providers with strong codegen — schema-diff plus typed client gives the same guarantee cheaper.
- One-off internal cron-callers or scripts — the Pact broker overhead exceeds the benefit.
- Providers without any spec artifact (no OpenAPI, no recorded traffic) — generate the spec first, then the Pact.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
