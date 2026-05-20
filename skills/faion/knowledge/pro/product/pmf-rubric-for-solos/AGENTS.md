---
slug: pmf-rubric-for-solos
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Pmf Rubric For Solos: codified product practice that turns the recurring 'p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction)' decision into a repeatable, auditable artefact.
content_id: "3f0dc2042bf64913"
tags: [pmf-rubric-for-solos, product, pro]
---
# Pmf Rubric For Solos

## Summary

**One-sentence:** Pmf Rubric For Solos: codified product practice that turns the recurring 'p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction)' decision into a repeatable, auditable artefact.

**One-paragraph:** Pmf Rubric For Solos addresses the gap identified by the p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction) playbook: Pirate metrics and retention curves exist but a synthesizing rubric for a solo (small N, no analytics team) is missing. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction) task (last 30 days)
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
| `templates/pmf-rubric-for-solos.json` | JSON schema for the Pmf Rubric For Solos output contract |
| `templates/pmf-rubric-for-solos.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pmf-rubric-for-solos.py` | Enforce Pmf Rubric For Solos output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/product-manager/`
- upstream playbook: `p1-solo-saas-builder/Product/Market Fit hunt (post-MVP, pre-traction)`
