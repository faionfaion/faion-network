---
slug: outcome-based-roadmaps-advanced
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an advanced outcome-roadmap spec (multi-quarter outcome chains + dependency edges + confidence-decay model + portfolio-level swim lanes) for teams beyond single-quarter horizons."
content_id: "22f21b95725411e4"
complexity: deep
produces: spec
est_tokens: 4200
tags: [roadmap, outcomes, multi-quarter, dependency, portfolio]
---

# Outcome Based Roadmaps Advanced

## Summary

**One-sentence:** Produces an advanced outcome-roadmap spec (multi-quarter outcome chains + dependency edges + confidence-decay model + portfolio-level swim lanes) for teams beyond single-quarter horizons.

**Ефективно для:** Senior solopreneur PMs whose 1-quarter outcome roadmap is fine but cross-quarter chains, dependencies, and confidence-decay over 6+ months are invisible.

**One-paragraph:** Single-quarter outcome roadmaps work for 1 product / 1 team / 1 stakeholder. Beyond that, outcomes chain across quarters, solutions develop hard dependencies, and confidence decays predictably the further out you plan. This advanced methodology produces a multi-quarter outcome chain with explicit dependency edges, a confidence-decay model (high < 1Q, medium 1-2Q, low > 2Q), and portfolio-level swim lanes per product. Output is consumed by board / stakeholder reviews + strategic planning.

## Applies If (ALL must hold)

- Operator runs a roadmap across ≥2 quarters / ≥2 products.
- Cross-product or cross-outcome dependencies are real (not just preferences).
- Stakeholders need a multi-quarter horizon.
- Confidence-decay tradeoffs are accepted (not 'just guarantee Q4').

## Skip If (ANY kills it)

- Single-quarter horizon — outcome-based-roadmaps (the base methodology) is enough.
- Single product + no cross-outcome dependencies — base methodology suffices.
- Stakeholders demand exact long-horizon dates — use a date-bound plan instead.
- Pre-PMF — long-horizon planning is theatre at this stage.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| multi-quarter horizon dates | ISO range | operator |
| portfolio swim lanes (per product) | array | operator |
| dependency graph candidates | DAG | operator |
| instrumented metrics per outcome | object | analytics |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/outcome-based-roadmaps` | Base — this is the advanced layer atop the quarterly method. |
| `solo/product/multi-product-portfolio-management` | Sibling — portfolio swim lanes mirror portfolio config. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_multi_q_chain` | sonnet | Bounded judgement on outcome chain across quarters. |
| `attach_dependency_edges` | sonnet | Per-edge judgement on dependency type (hard/soft). |
| `apply_confidence_decay` | opus | Cross-horizon synthesis with decay model. |
| `portfolio_swim_lane_synthesis` | opus | Per-product swim lane reconciliation. |

## Templates

| File | Purpose |
|---|---|
| `templates/outcome-based-roadmaps-advanced.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/outcome-based-roadmaps-advanced.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-outcome-based-roadmaps-advanced.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[outcome-based-roadmaps]] — related methodology.
- [[multi-product-portfolio-management]] — related methodology.
- [[okr-setting]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
