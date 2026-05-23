---
slug: writing-design-documents
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Author design.md that answers HOW to build the feature via numbered architectural decisions (AD-X), file structure, data models, sequence diagrams, and API contracts — all linked back to the spec's FR-X requirements.
content_id: "2c73123f27f6b9f6"
complexity: deep
produces: spec
est_tokens: 4300
tags: [design, architecture, sdd, decisions]
---
# Writing Design Documents

## Summary

**One-sentence:** Author design.md that answers HOW to build the feature via numbered architectural decisions (AD-X), file structure, data models, sequence diagrams, and API contracts — all linked back to the spec's FR-X requirements.

**One-paragraph:** Author design.md that answers HOW to build the feature via numbered architectural decisions (AD-X), file structure, data models, sequence diagrams, and API contracts — all linked back to the spec's FR-X requirements. The methodology pins the artefact: every AD-X has an alternative + tradeoff + chosen option + traced requirement; every API contract has an example request, example response, and error matrix.

**Ефективно для:**

- Engineers committing to an approach before writing code.
- Reviewers verifying that design covers every spec requirement.
- Hand-off to impl-plan: design.md is the contract that impl-plan decomposes.
- Audit surface: every architectural decision has a recorded alternative + rationale.

## Applies If (ALL must hold)

- Spec is approved and locked.
- Implementation choices are non-trivial (multiple valid options).
- Multiple developers or agents will consume the design.

## Skip If (ANY kills it)

- Trivial implementation with one obvious approach.
- Spec already names the implementation in detail (rare and discouraged).
- Throwaway prototype.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved spec.md | markdown | Spec phase |
| Constitution.md | markdown | Repo root |
| Existing module map | tree | Codebase |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd-planning/writing-specifications` | Provides the FR-X / NFR-X / AC-X identifiers that this design traces against. |

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
| `draft-writing-design-documents` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-writing-design-documents` | haiku | Schema check + threshold checks; deterministic. |
| `review-writing-design-documents` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/writing-design-documents.json` | JSON skeleton conforming to the output contract schema. |
| `templates/writing-design-documents.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-writing-design-documents.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[writing-specifications]]
- [[writing-implementation-plans]]
- [[sdd-workflow-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
