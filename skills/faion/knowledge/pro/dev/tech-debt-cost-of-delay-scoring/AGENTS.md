---
slug: tech-debt-cost-of-delay-scoring
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a590fc463d7ec76e"
summary: "Tech Debt Cost Of Delay Scoring: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Weekly tech-debt prioritisation session'."
tags: [tech-debt-cost-of-delay-scoring, dev, pro]
---
# Tech Debt Cost Of Delay Scoring

## Summary

**One-sentence:** Tech Debt Cost Of Delay Scoring: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Weekly tech-debt prioritisation session'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-architect/Weekly tech-debt prioritisation session': Current tech-debt-management is descriptive; no scoring rubric to defend prioritisation to PMs / leadership. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tech debt cost of delay scoring artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Weekly tech-debt prioritisation session' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tech debt cost of delay scoring artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-architect/Weekly tech-debt prioritisation session' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Tech Debt Cost Of Delay Scoring |

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
| `templates/tech-debt-cost-of-delay-scoring.json` | JSON schema for the Tech Debt Cost Of Delay Scoring output contract |
| `templates/tech-debt-cost-of-delay-scoring.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-cost-of-delay-scoring.py` | Enforce Tech Debt Cost Of Delay Scoring output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Weekly tech-debt prioritisation session`
- pro/dev/role-software-architect
