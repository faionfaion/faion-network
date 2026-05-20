---
slug: v1-to-v2-migration-playbook
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "54d5008643123502"
summary: "V1 To V2 Migration Playbook: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pivot from failed v1 to v2'."
tags: [v1-to-v2-migration-playbook, dev, pro]
---
# V1 To V2 Migration Playbook

## Summary

**One-sentence:** V1 To V2 Migration Playbook: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pivot from failed v1 to v2'.

**One-paragraph:** Addresses the gap surfaced by 'p1-solo-saas-builder/Pivot from failed v1 to v2': Pivots break paying users; faion lacks a methodology on data + auth + billing migration when the schema/business model shifts. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a v1 to v2 migration playbook artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/Pivot from failed v1 to v2' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working v1 to v2 migration playbook artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p1-solo-saas-builder/Pivot from failed v1 to v2' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for V1 To V2 Migration Playbook |

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
| `templates/v1-to-v2-migration-playbook.json` | JSON schema for the V1 To V2 Migration Playbook output contract |
| `templates/v1-to-v2-migration-playbook.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-v1-to-v2-migration-playbook.py` | Enforce V1 To V2 Migration Playbook output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `p1-solo-saas-builder/Pivot from failed v1 to v2`
- pro/dev/p1-solo-saas-builder
