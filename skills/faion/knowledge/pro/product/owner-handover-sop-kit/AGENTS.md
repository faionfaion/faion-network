---
slug: owner-handover-sop-kit
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Owner Handover Sop Kit: codified product practice that turns the recurring 'p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away)' decision into a repeatable, auditable artefact.
content_id: "3d78ee0d51754269"
tags: [owner-handover-sop-kit, product, pro]
---
# Owner Handover Sop Kit

## Summary

**One-sentence:** Owner Handover Sop Kit: codified product practice that turns the recurring 'p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away)' decision into a repeatable, auditable artefact.

**One-paragraph:** Owner Handover Sop Kit addresses the gap identified by the p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away) playbook: Whether selling, hiring a manager, or going on a 3-month sabbatical, the founder needs a handover-kit template: 'if I disappear, here is the book.' product-operations is too abstract. Needs to be concrete: vendor list, credential vault structure, client-by-client brief, decision-authority matrix. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away) task (last 30 days)
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
| `templates/owner-handover-sop-kit.json` | JSON schema for the Owner Handover Sop Kit output contract |
| `templates/owner-handover-sop-kit.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-owner-handover-sop-kit.py` | Enforce Owner Handover Sop Kit output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/product-manager/`
- upstream playbook: `p5-micro-agency-founder/Prep the agency for acquisition (or graceful walk-away)`
