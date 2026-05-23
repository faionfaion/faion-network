---
slug: tech-debt-management
tier: solo
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a tech-debt management plan artefact picking one of four payoff strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig) per item with CI gates against re-accumulation.
content_id: "a3813b675c136f7f"
complexity: medium
produces: spec
est_tokens: 3700
tags: [tech-debt, refactoring, prioritization, strangler-fig, quality-gates]
---
# Technical Debt Management

## Summary

**One-sentence:** Picks one of four payoff strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig) per scored debt item and wires CI/pre-commit gates that prevent re-accumulation.

**One-paragraph:** Most teams have a debt register; few have a strategy for paying it. This methodology takes a scored debt item (see `debt-scoring-rubric`) and proposes one of four strategies: Boy Scout (rule of "clean up around you"), feature-attached (debt fix piggybacks on a feature touching the same area), dedicated sprint (when debt is too large to chunk), or Strangler Fig (build alongside and switch traffic). Each strategy has a fit profile and an exit criterion. The artefact also lists the CI/pre-commit gates that prevent the debt category from re-accumulating (lint rule, complexity cap, dependency policy).

**Ефективно для:**

- Solo dev / outsource lead deciding how to chunk debt payoff into the sprint cadence.
- Tech lead arguing for a dedicated sprint vs. ongoing Boy Scout work.
- Strangler-Fig migrations where the rewrite is too big for one PR.
- AI-pair coding shops codifying "clean up the file the AI just edited" as a Boy Scout rule.

## Applies If (ALL must hold)

- A scored debt register exists (see `debt-scoring-rubric`).
- Team has CI / pre-commit infrastructure to enforce post-payoff gates.
- At least one debt item scores above the threshold and warrants action.
- Engagement length covers the chosen strategy's horizon.

## Skip If (ANY kills it)

- No scored debt register — produce it first.
- Single-PR engagement — no sprint cadence to attach to.
- Greenfield project &lt; 3 months — too early.
- Org pays no attention to debt regardless — escalate before producing the artefact.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scored debt register | JSON | `debt-scoring-rubric` output |
| CI config | YAML | repo |
| Sprint cadence | doc | team handbook |
| Threshold for payoff | number | `debt-scoring-rubric` artefact |
| Owner per item | email | tracker |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/code-quality/debt-scoring-rubric` | Upstream — produces the scored register this methodology consumes. |
| `solo/dev/ci-quality-gate-design` | CI gates against re-accumulation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: strategy-by-score, exit criteria, gate-the-fix, no-separate-backlog, named owner, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the plan artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: separate backlog, no exit, fix-without-gate, owner-team-alias | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: classify → strategy → exit criteria → wire gate → schedule | 700 |
| `content/06-decision-tree.xml` | essential | Tree: score band → strategy → gate available? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `assign-strategy` | sonnet | Per-item judgment matching score + area + cadence. |
| `draft-gate` | sonnet | Coding task: lint rule / complexity threshold for re-accumulation. |
| `schedule` | haiku | Mechanical: insert items into sprint plan / Boy-Scout file. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tech-debt-management.json` | JSON Schema for the management-plan artefact. |
| `templates/strategy-fit-table.md` | Per-strategy fit profile + exit criteria. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-management.py` | Validate plan JSON against schema + strategy/score consistency. | After plan drafted; quarterly review. |

## Related

- [[code-quality/debt-scoring-rubric]] — upstream input.
- [[ci-quality-gate-design]] — gate the fix joins.
- [[code-quality/framework-decomposition-patterns]] — common Boy-Scout move.

## Decision tree

See `content/06-decision-tree.xml`. The tree picks strategy by score: low (Boy Scout), medium-and-localized (feature-attached), high-and-broad (dedicated sprint or Strangler Fig). It then verifies a CI gate exists for the debt category. Leaves emit `adopt-plan`, `block-no-gate`, `block-no-exit-criteria`, or `block-low-score-skip`. Each leaf references a rule in `01-core-rules.xml`.
