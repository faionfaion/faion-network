---
slug: traceability-matrix-template-csv
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "76e3617970ca133a"
summary: "Traceability Matrix Template Csv: produces a versioned, owner-signed artefact that closes the gap 'role-business-analyst/Traceability matrix weekly refresh'."
tags: [traceability-matrix-template-csv, ba, pro]
---
# Traceability Matrix Template Csv

## Summary

**One-sentence:** Traceability Matrix Template Csv: produces a versioned, owner-signed artefact that closes the gap 'role-business-analyst/Traceability matrix weekly refresh'.

**One-paragraph:** Addresses the gap surfaced by 'role-business-analyst/Traceability matrix weekly refresh': BAs need a ready-to-use matrix template + Jira export script for weekly refresh; current methodology is conceptual only. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a traceability matrix template csv artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-business-analyst/Traceability matrix weekly refresh' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working traceability matrix template csv artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-business-analyst/Traceability matrix weekly refresh' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/ba` | parent domain group — provides operating context for Traceability Matrix Template Csv |

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
| `templates/traceability-matrix-template-csv.json` | JSON schema for the Traceability Matrix Template Csv output contract |
| `templates/traceability-matrix-template-csv.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-traceability-matrix-template-csv.py` | Enforce Traceability Matrix Template Csv output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Traceability matrix weekly refresh`
- pro/ba/role-business-analyst
