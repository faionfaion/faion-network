---
slug: api-first-development
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design the OpenAPI 3.1 contract before writing implementation code so that consumers, mocks, SDKs, and contract tests are all generated from a single source of truth.
content_id: "64f2f21f004d320e"
complexity: deep
produces: spec
est_tokens: 4200
tags: ["api", "openapi", "contract", "specification", "design-first"]
---
# API-First Development

## Summary

**One-sentence:** Design the OpenAPI 3.1 contract before writing implementation code so that consumers, mocks, SDKs, and contract tests are all generated from a single source of truth.

**One-paragraph:** API-first development pins the OpenAPI 3.1 contract as the first artefact: server stubs, client SDKs, Prism mock servers, and Dredd/Pact contract tests are all generated from it. The spec is reviewed, linted (Spectral), and gated in CI before any backend code lands. Frontend and backend agents work in parallel against the mock; breaking changes are surfaced by bump diff on every PR.

**Ефективно для:**

- Solo PM/founder shipping a public or partner API where contract stability matters more than internal velocity.
- Frontend + backend split across agents/teams that need to start in parallel via a mock server.
- Microservice boundaries that require a signed contract before either side begins implementation.
- Projects emitting client SDKs in multiple languages from a single generator pipeline.

## Applies If (ALL must hold)

- Multiple consumers planned (frontend, mobile, third-party) before backend is written.
- Frontend and backend agents or teams work in parallel: mock server unblocks frontend.
- Public or partner-facing API where contract stability is a hard requirement.
- CI pipeline can enforce Spectral lint + contract tests on every PR.

## Skip If (ANY kills it)

- Internal single-consumer service where the spec would be written after implementation anyway (YAGNI).
- Rapid prototype with fewer than 3 endpoints — design overhead exceeds benefit.
- GraphQL-first or event-driven projects — use AsyncAPI instead.
- No CI to enforce lint/contract tests — drift will appear within weeks.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature spec.md | markdown | Spec methodology output |
| Endpoint list | markdown / sheet | Discovery + PM doc |
| Auth strategy decision | ADR or design.md | architecture-decision-records |
| Spectral ruleset | yaml | .spectral.yaml in repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/spec-structure` | Feature spec.md is the input to endpoint extraction. |
| `solo/sdd/sdd-planning/architecture-decision-records` | Auth + versioning decisions are sourced from ADRs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-openapi-spec` | sonnet | Per-endpoint judgement on path shape, schemas, error responses. |
| `lint-spec` | haiku | Deterministic Spectral run + violation tabulation. |
| `review-breaking-changes` | opus | Cross-version diff with downstream impact assessment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-first-development.json` | JSON skeleton conforming to the output contract schema. |
| `templates/api-first-development.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-first-development.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[spec-structure]]
- [[design-doc-structure]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
