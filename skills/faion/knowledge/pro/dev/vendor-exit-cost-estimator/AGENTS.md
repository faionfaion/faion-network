---
slug: vendor-exit-cost-estimator
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "bdf8c670705225d3"
summary: "Vendor Exit Cost Estimator: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Vendor / library evaluation gate'."
tags: [vendor-exit-cost-estimator, dev, pro]
---
# Vendor Exit Cost Estimator

## Summary

**One-sentence:** Vendor Exit Cost Estimator: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Vendor / library evaluation gate'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-architect/Vendor / library evaluation gate': Build-vs-buy methodologies exist but ignore exit cost. Exit cost is what bites in year 2. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vendor exit cost estimator artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Vendor / library evaluation gate' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vendor exit cost estimator artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-architect/Vendor / library evaluation gate' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Vendor Exit Cost Estimator |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/vendor-exit-cost-estimator.json` | JSON schema for the Vendor Exit Cost Estimator output contract |
| `templates/vendor-exit-cost-estimator.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-exit-cost-estimator.py` | Enforce Vendor Exit Cost Estimator output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Vendor / library evaluation gate`
- pro/dev/role-software-architect
