---
slug: mvp-scoping
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an MVP scope spec (named-AHA-moment + ≤4-week build + must-have user journey + explicit cut list + readiness checklist) so the MVP ships viable, not maximal."
content_id: "6f182dccaa299f07"
complexity: medium
produces: spec
est_tokens: 4200
tags: [mvp, scoping, product-management, scope-control]
---

# MVP Scoping

## Summary

**One-sentence:** Produces an MVP scope spec (named-AHA-moment + ≤4-week build + must-have user journey + explicit cut list + readiness checklist) so the MVP ships viable, not maximal.

**Ефективно для:** Solopreneur PMs whose MVP scope quietly drifts from 'minimum viable' to 'minimum complete' and ships 4 months late.

**One-paragraph:** MVP scope creep is the default failure mode: every stakeholder adds 'one more thing' that 'must be in the MVP'. This methodology pins MVP scope to a named AHA-moment (the single moment a user feels the product works), enforces a ≤4-week build window, forces an explicit cut-list (features removed with rationale), and ships only when the readiness checklist passes. Output is consumed by sprint planning + launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator is building toward a launch event with named users.
- Build budget is ≤4 weeks (one calendar month).
- A named AHA-moment exists (the single feature path that delivers value).
- Stakeholders agree to a cut-list discipline.

## Skip If (ANY kills it)

- No named AHA-moment — fix product positioning first.
- Build budget > 4 weeks planned — that's a small product, use roadmap methodology instead.
- Pre-validated micro-test needed first — run micro-mvps before scoping a full MVP.
- Heavily regulated product — MVP scoping ignores compliance overhead.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| AHA-moment statement | string | founder |
| must-have user journey | step list | founder |
| build budget (≤4 weeks) | weeks | operator |
| readiness checklist | array | team |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/micro-mvps` | Upstream — micro-MVP validates hypothesis before MVP scope is locked. |
| `solo/product/mvp-instrumentation-checklist` | Downstream — readiness checklist includes instrumentation gate. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_scope` | haiku | Template fill from prereqs. |
| `audit_cut_list` | sonnet | Bounded judgement: are cut items rationalised vs AHA-moment? |
| `readiness_sign_off` | opus | Synthesis at scope-freeze gate. |

## Templates

| File | Purpose |
|---|---|
| `templates/mvp-scoping.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/mvp-scoping.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mvp-scoping.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[micro-mvps]] — related methodology.
- [[mvp-instrumentation-checklist]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.
- [[launch-tier-decision-frame]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
