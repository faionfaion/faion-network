# Micro-MVP Cut Rubric

## Summary

**One-sentence:** Run a 5-question cut rubric to slice an MVP scope down to ≤5 dev-days while preserving the riskiest assumption test.

**One-paragraph:** Solo MVPs bloat. The 5-question rubric is run on every proposed scope item: would-cut-on-deadline / falsifies-the-risk / 3-dev-days-or-less / no-payment-flow-needed / no-user-management-needed. Items failing any question are deferred to v2. Output is a defensible ≤5-day scope.

**Ефективно для:**

- Solo founder whose 'MVP' has crept to 6 weeks of dev work — needs a forcing function to recover the 'minimum' part without losing the risk test.

## Applies If (ALL must hold)

- Current MVP scope >5 dev-days.
- Riskiest assumption can be named.
- Founder ships solo or with ≤1 collaborator.

## Skip If (ANY kills it)

- Compliance / contractual scope cannot be cut.
- MVP already <5 dev-days.
- Pre-discovery — no riskiest assumption yet identified.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current MVP scope list | list | Spec / backlog |
| Riskiest assumption | string | Discovery |
| Dev-day estimates per item | table | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/mvp-scoping` | Source MVP scope candidate. |
| `solo/product/product-manager/product-discovery` | Riskiest assumption source. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-micro-mvp-cut-rubric` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-micro-mvp-cut-rubric` | haiku | Schema check + threshold checks; deterministic. |
| `review-micro-mvp-cut-rubric` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/micro-mvp-cut-rubric.json` | JSON skeleton conforming to the output contract schema. |
| `templates/micro-mvp-cut-rubric.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-micro-mvp-cut-rubric.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[mvp-scoping]]
- [[product-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
