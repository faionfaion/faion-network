---
slug: vdi-vs-byod-decision-matrix
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "05e5c301d95fa261"
summary: "Vdi Vs Byod Decision Matrix: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/New-project machine setup (laptop + desktop)'."
tags: [vdi-vs-byod-decision-matrix, infra, pro]
---
# Vdi Vs Byod Decision Matrix

## Summary

**One-sentence:** Vdi Vs Byod Decision Matrix: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/New-project machine setup (laptop + desktop)'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/New-project machine setup (laptop + desktop)': Banking/health clients increasingly mandate VDI. Decision rules + productivity-recovery patterns inside VDI constraints are missing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vdi vs byod decision matrix artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/New-project machine setup (laptop + desktop)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vdi vs byod decision matrix artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/New-project machine setup (laptop + desktop)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infra` | parent domain group — provides operating context for Vdi Vs Byod Decision Matrix |

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
| `templates/vdi-vs-byod-decision-matrix.json` | JSON schema for the Vdi Vs Byod Decision Matrix output contract |
| `templates/vdi-vs-byod-decision-matrix.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vdi-vs-byod-decision-matrix.py` | Enforce Vdi Vs Byod Decision Matrix output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- upstream playbook: `p4-outsource-specialist/New-project machine setup (laptop + desktop)`
- pro/infra/p4-outsource-specialist
