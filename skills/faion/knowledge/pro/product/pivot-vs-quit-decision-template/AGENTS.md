---
slug: pivot-vs-quit-decision-template
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Pivot Vs Quit Decision Template: codified product practice that turns the recurring 'p1-solo-saas-builder/Pivot from failed v1 to v2' decision into a repeatable, auditable artefact.
content_id: "9477397d563128be"
tags: [pivot-vs-quit-decision-template, product, pro]
---
# Pivot Vs Quit Decision Template

## Summary

**One-sentence:** Pivot Vs Quit Decision Template: codified product practice that turns the recurring 'p1-solo-saas-builder/Pivot from failed v1 to v2' decision into a repeatable, auditable artefact.

**One-paragraph:** Pivot Vs Quit Decision Template addresses the gap identified by the p1-solo-saas-builder/Pivot from failed v1 to v2 playbook: Pivots and sunsets are emotionally hard for solos; need a structured worksheet separating sunk cost, optionality, and personal runway. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p1-solo-saas-builder/Pivot from failed v1 to v2 OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p1-solo-saas-builder/Pivot from failed v1 to v2 task (last 30 days)
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
| `templates/pivot-vs-quit-decision-template.json` | JSON schema for the Pivot Vs Quit Decision Template output contract |
| `templates/pivot-vs-quit-decision-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pivot-vs-quit-decision-template.py` | Enforce Pivot Vs Quit Decision Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/product-manager/`
- upstream playbook: `p1-solo-saas-builder/Pivot from failed v1 to v2`
