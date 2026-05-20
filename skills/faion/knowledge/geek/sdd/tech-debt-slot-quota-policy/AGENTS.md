---
slug: tech-debt-slot-quota-policy
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ae3b82d931b03a38"
summary: "Tech Debt Slot Quota Policy: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)'."
tags: [tech-debt-slot-quota-policy, sdd, geek]
---
# Tech Debt Slot Quota Policy

## Summary

**One-sentence:** Tech Debt Slot Quota Policy: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)'.

**One-paragraph:** Addresses the gap surfaced by 'p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)': Teams keep deferring tech debt because there's no explicit quota policy. Faion's tech-debt-management page covers the why but not the operational quota. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tech debt slot quota policy artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tech debt slot quota policy artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdd/sdd` | parent domain group — provides operating context for Tech Debt Slot Quota Policy |

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
| `templates/tech-debt-slot-quota-policy.json` | JSON schema for the Tech Debt Slot Quota Policy output contract |
| `templates/tech-debt-slot-quota-policy.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-slot-quota-policy.py` | Enforce Tech Debt Slot Quota Policy output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/sdd/`
- upstream playbook: `p6-product-dev-team/Backlog grooming with PM + tech lead (weekly)`
- geek/sdd/p6-product-dev-team
