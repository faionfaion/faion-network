---
slug: beta-charter-template
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Beta Charter Template: codified product-management practice that turns the recurring 'p1-solo-saas-builder/Pre-launch beta program' decision into a repeatable, auditable artefact.
content_id: "18b4dc8ae6e619b0"
tags: [beta-charter-template, product, solo]
---
# Beta Charter Template

## Summary

**One-sentence:** Beta Charter Template: codified product-management practice that turns the recurring 'p1-solo-saas-builder/Pre-launch beta program' decision into a repeatable, auditable artefact.

**One-paragraph:** Beta Charter Template addresses the gap identified by the p1-solo-saas-builder/Pre-launch beta program playbook: Beta programs without a written charter degrade into ad-hoc support; no faion methodology currently codifies the charter pattern. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p1-solo-saas-builder/Pre-launch beta program OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p1-solo-saas-builder/Pre-launch beta program task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/beta-charter-template.json` | JSON schema for the Beta Charter Template output contract |
| `templates/beta-charter-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-beta-charter-template.py` | Enforce Beta Charter Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `p1-solo-saas-builder/Pre-launch beta program`
