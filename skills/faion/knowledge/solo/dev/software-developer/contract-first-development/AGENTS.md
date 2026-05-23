---
slug: contract-first-development
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design OpenAPI contracts before writing implementation code so stubs, SDKs, and mocks all derive from the spec.
content_id: "2bd87b8001fa08e5"
complexity: medium
produces: spec
est_tokens: 4500
tags: [openapi, api-design, contract, codegen]
---
# Contract-First Development

## Summary

**One-sentence:** Design OpenAPI contracts before writing implementation code so stubs, SDKs, and mocks all derive from the spec.

**One-paragraph:** Code-first APIs drift between consumers and providers; contract-first inverts the flow. Authors commit an OpenAPI 3.1 spec, lint it with spectral, regression-check it with oasdiff, and only then generate server stubs, client SDKs, and mock servers from it. The spec is treated like source — PR review, semver, breaking-change gates in CI. Hand-edits to generated stubs are forbidden; changes flow through the spec.

**Ефективно для:**

- New APIs with multiple consumers building in parallel (FE, mobile, partners).
- Public or partner APIs where stable versioning is contractual.
- AI-agent-generated services that need a deterministic contract to anchor regeneration.
- Microservice boundaries where service contracts are the integration surface.

## Applies If (ALL must hold)

- New API with multiple consumers (frontend, mobile, partners) planned or existing.
- Cross-team handoff where BE and FE build in parallel.
- Public or partner APIs needing stable, versioned, machine-readable contracts.
- AI-agent-generated services where spec prevents drift between iterations.
- Microservices where service boundaries are evolving and need explicit contracts.

## Skip If (ANY kills it)

- One-off internal scripts or single-team tools where overhead exceeds value.
- Highly experimental endpoints during prototyping (spec churn dominates).
- Pure GraphQL stacks — schema-first GraphQL achieves the same with different tooling.
- gRPC — `.proto` is already the contract; different tools apply.
- Server-rendered web apps where the API is HTML forms, not JSON.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource model + lifecycle states | bullet list or ERD | product / domain |
| Consumer list with platform + auth model | table | tech-lead |
| Auth scheme + error contract decisions | ADR or note | architect |
| OpenAPI tooling versions (spectral, oasdiff, codegen) | pinned versions | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rest-api-design]] | Defines the REST conventions the spec encodes. |
| [[api-versioning]] | The breaking-change policy oasdiff enforces. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (spec-first, $ref reuse, spectral, oasdiff, codegen-not-handedit, semver) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the spec artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: scope → draft → lint → review → generate → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: paginated resource API | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `spec_drafting` | opus | Schema design + auth + error contract requires deep synthesis. |
| `spectral_rule_authoring` | sonnet | Mechanical: encode lint rules from style guide. |
| `oasdiff_gate_setup` | sonnet | Pipeline plumbing. |
| `codegen_pipeline` | sonnet | Wire generators (openapi-generator / orval) into build. |

## Templates

| File | Purpose |
|------|---------|
| `templates/openapi-scaffold.yaml` | OpenAPI 3.1 skeleton with resource, list, create, errors, security |
| `templates/spectral.yaml` | Spectral ruleset extending `spectral:oas` |
| `templates/check-spec-drift.sh` | CI script that runs spectral + oasdiff between PR and main |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-contract-first-development.py` | Validate the spec artefact metadata against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[rest-api-design]]
- [[api-versioning]]
- [[openapi-specification]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs (consumer count, spec stability, auth complexity) to a rule from `01-core-rules.xml`, telling the agent whether to invoke full contract-first, light SDL-only design, or skip the methodology because preconditions fail. Walk it on every fresh invocation.
