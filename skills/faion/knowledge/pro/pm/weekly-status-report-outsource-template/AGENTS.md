---
slug: weekly-status-report-outsource-template
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ea11aa767c56121d"
summary: "Weekly Status Report Outsource Template: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Weekly client status report'."
tags: [weekly-status-report-outsource-template, pm, pro]
---
# Weekly Status Report Outsource Template

## Summary

**One-sentence:** Weekly Status Report Outsource Template: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Weekly client status report'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/Weekly client status report': Existing status-report template in project-manager skill is generic PMI. Outsource specialist needs an offshore-shop-to-onshore-client variant that the client PM can forward unchanged. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly status report outsource template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/Weekly client status report' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly status report outsource template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/Weekly client status report' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Weekly Status Report Outsource Template |

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
| `templates/weekly-status-report-outsource-template.json` | JSON schema for the Weekly Status Report Outsource Template output contract |
| `templates/weekly-status-report-outsource-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-status-report-outsource-template.py` | Enforce Weekly Status Report Outsource Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/Weekly client status report`
- pro/pm/p4-outsource-specialist
