---
slug: one-person-rollback-runbook
tier: solo
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: One Person Rollback Runbook: codified infra practice that turns the recurring 'p1-solo-saas-builder/Deploy-day staging-to-prod gate' decision into a repeatable, auditable artefact.
content_id: "53fba2caf5a73bea"
tags: [one-person-rollback-runbook, infra, solo]
---
# One Person Rollback Runbook

## Summary

**One-sentence:** One Person Rollback Runbook: codified infra practice that turns the recurring 'p1-solo-saas-builder/Deploy-day staging-to-prod gate' decision into a repeatable, auditable artefact.

**One-paragraph:** One Person Rollback Runbook addresses the gap identified by the p1-solo-saas-builder/Deploy-day staging-to-prod gate playbook: Verified rollback procedure for code + migrations + flags; missing entirely in solo/infra. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p1-solo-saas-builder/Deploy-day staging-to-prod gate OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p1-solo-saas-builder/Deploy-day staging-to-prod gate task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft` | parent role skill — provides the operating context for this methodology |

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
| `templates/one-person-rollback-runbook.json` | JSON schema for the One Person Rollback Runbook output contract |
| `templates/one-person-rollback-runbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-one-person-rollback-runbook.py` | Enforce One Person Rollback Runbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/infra/server-craft/`
- upstream playbook: `p1-solo-saas-builder/Deploy-day staging-to-prod gate`
