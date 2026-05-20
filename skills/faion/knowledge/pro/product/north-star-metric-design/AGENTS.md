---
slug: north-star-metric-design
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: North Star Metric Design: codified product practice that turns the recurring 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR' decision into a repeatable, auditable artefact.
content_id: "e1ba348e4c936902"
tags: [north-star-metric-design, product, pro]
---
# North Star Metric Design

## Summary

**One-sentence:** North Star Metric Design: codified product practice that turns the recurring 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR' decision into a repeatable, auditable artefact.

**One-paragraph:** North Star Metric Design addresses the gap identified by the role-product-manager/Build a defensible KPI tree from a fuzzy company OKR playbook: Product-analytics covers measurement; nothing covers the act of choosing the north-star itself. PMs need a method for candidate generation, stress-testing, leading-vs-lagging trade-off, and de-coupling from revenue when revenue is too far downstream. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Build a defensible KPI tree from a fuzzy company OKR OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Build a defensible KPI tree from a fuzzy company OKR task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/north-star-metric-design.json` | JSON schema for the North Star Metric Design output contract |
| `templates/north-star-metric-design.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-north-star-metric-design.py` | Enforce North Star Metric Design output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/product-manager/`
- upstream playbook: `role-product-manager/Build a defensible KPI tree from a fuzzy company OKR`
