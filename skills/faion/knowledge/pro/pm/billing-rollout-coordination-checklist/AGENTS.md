---
slug: billing-rollout-coordination-checklist
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Billing Rollout Coordination Checklist: codified delivery-management practice that turns the recurring 'role-product-manager/Pricing experiment, hypothesis to result' decision into a repeatable, auditable artefact.
content_id: "a08611e3205818a4"
tags: [billing-rollout-coordination-checklist, pm, pro]
---
# Billing Rollout Coordination Checklist

## Summary

**One-sentence:** Billing Rollout Coordination Checklist: codified delivery-management practice that turns the recurring 'role-product-manager/Pricing experiment, hypothesis to result' decision into a repeatable, auditable artefact.

**One-paragraph:** Billing Rollout Coordination Checklist addresses the gap identified by the role-product-manager/Pricing experiment, hypothesis to result playbook: Pricing changes break billing / finance / legal more than they break product. No cross-functional checklist exists. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Pricing experiment, hypothesis to result OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Pricing experiment, hypothesis to result task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/billing-rollout-coordination-checklist.json` | JSON schema for the Billing Rollout Coordination Checklist output contract |
| `templates/billing-rollout-coordination-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-billing-rollout-coordination-checklist.py` | Enforce Billing Rollout Coordination Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `role-product-manager/Pricing experiment, hypothesis to result`
