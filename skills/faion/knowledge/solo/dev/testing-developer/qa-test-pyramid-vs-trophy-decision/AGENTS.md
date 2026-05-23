---
slug: qa-test-pyramid-vs-trophy-decision
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a per-module test-strategy record — pyramid vs trophy vs hybrid — gated by a 5-question diagnostic on stack, change frequency, integration risk, runtime cost, and AC shape.
content_id: "ec9bd4e32b7a1161"
complexity: medium
produces: decision-record
est_tokens: 4600
tags: ["test-pyramid", "testing-trophy", "test-strategy", "integration-tests", "decision-framework"]
---
# Test Pyramid vs Testing Trophy: Per-Module Decision

## Summary

**One-sentence:** Generates a per-module test-strategy record — pyramid vs trophy vs hybrid — gated by a 5-question diagnostic on stack, change frequency, integration risk, runtime cost, and AC shape.

**One-paragraph:** Generates a per-module test-strategy record — pyramid vs trophy vs hybrid — gated by a 5-question diagnostic on stack, change frequency, integration risk, runtime cost, and AC shape.

**Ефективно для:**

- Solo team running ≥5 modules with diverging test investment per module.
- Backend team where mocked unit tests prove nothing about integration.
- Frontend team where e2e suite is slow and flaky.
- Quarterly review when CI runtime explodes.

## Applies If (ALL must hold)

- Repo has ≥5 distinct modules with non-trivial test investment.
- Team experienced ≥1 of: e2e too slow, integration gap, unit-only suite missed bug.
- Team has authority to adopt different test-shape per module.
- At least one engineer can spend 1-2 hours on the per-module decision.

## Skip If (ANY kills it)

- Single mostly-pure-logic library — pyramid is the obvious answer.
- Single end-to-end SaaS UI with no internal modules — trophy is the obvious answer.
- Compliance environment with mandated test-shape — apply the mandate.
- Pre-MVP — test shape is over-engineering before architecture stabilises.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Module list | yaml | produced by risk-matrix run |
| CI runtime breakdown | json | CI pipeline timing report |
| Recent incident log | csv | issue tracker last 90d |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| qa-risk-matrix-method | Risk matrix produces module list and impact scores. |
| qa-changed-lines-coverage-dashboard | Coverage data feeds the decision. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-five-question-diagnostic, r2-per-module-not-global, r3-runtime-budget-named, r4-named-owner, r5-quarterly-review | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Test Pyramid vs Testing Trophy: Per-Module Decision artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: org-wide-mandate, never-revisit, unit-test-snobbery | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-qa-test-pyramid-vs-trophy-decision` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-qa-test-pyramid-vs-trophy-decision` | sonnet | Bounded structural check against the output contract. |
| `review-qa-test-pyramid-vs-trophy-decision` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qa-test-pyramid-vs-trophy-decision.json` | JSON skeleton matching the output contract. |
| `templates/qa-test-pyramid-vs-trophy-decision.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-test-pyramid-vs-trophy-decision.py` | Validate Test Pyramid vs Testing Trophy: Per-Module Decision output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[qa-risk-matrix-method]]
- [[qa-changed-lines-coverage-dashboard]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
