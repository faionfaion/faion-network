---
slug: api-first-development
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an OpenAPI-3.1 contract (spec + Prism mock config + contract-test fixture) so the API surface is locked before implementation and CI catches drift on every change."
content_id: "48be9d8f116592d5"
complexity: medium
produces: spec
est_tokens: 4100
tags: [api-design, openapi, specification, contract-driven, code-generation]
---

# API-First Development

## Summary

**One-sentence:** Produces an OpenAPI-3.1 contract (spec + Prism mock config + contract-test fixture) so the API surface is locked before implementation and CI catches drift on every change.

**Ефективно для:** Solo backend devs whose 'I'll document it later' API contracts drift from implementation within two sprints and break every client.

**One-paragraph:** Implementation-first API work produces specs that lie within weeks. This methodology pins the OpenAPI 3.1 spec as the contract source-of-truth, requires Prism mock generation, server-stub generation (OpenAPI Generator), and schemathesis/dredd contract tests in CI. Drift between spec and implementation breaks CI before it breaks clients. Output is consumed by code-review-cycle and api-versioning.

## Applies If (ALL must hold)

- New API surface (public or internal) needs versioned contract.
- Multiple clients (FE, mobile, partner) consume the same API.
- Implementation will be split across people or sessions.
- CI/CD pipeline available to enforce contract tests.

## Skip If (ANY kills it)

- Throwaway prototype with one client and a 1-week lifespan.
- Internal tool with one developer and one consumer.
- GraphQL-first stacks — schema-first replaces this methodology.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| API surface scope | endpoint list | PM |
| OpenAPI 3.1 toolchain | cli | engineer |
| CI pipeline with contract-test stage | yaml | engineer |
| mock target environment | url | infra |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/architecture-decision-records` | Sibling — ADR records the API-first decision. |
| `solo/sdd/sdd/code-review-cycle` | Downstream — review checks contract-test coverage. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/api-first-development.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/api-first-development.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-api-first-development.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[architecture-decision-records]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[design-docs-patterns]] — related methodology.
- [[living-documentation]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
