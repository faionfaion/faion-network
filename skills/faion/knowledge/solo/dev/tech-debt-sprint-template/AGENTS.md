---
slug: tech-debt-sprint-template
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "6bf49557153d6b74"
summary: "Tech Debt Sprint Template: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Quarterly tech-debt sprint (2 weeks)'."
tags: [tech-debt-sprint-template, dev, solo]
---
# Tech Debt Sprint Template

## Summary

**One-sentence:** Tech Debt Sprint Template: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Quarterly tech-debt sprint (2 weeks)'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-developer/Quarterly tech-debt sprint (2 weeks)': Two-week debt sprints are a recurring P6 ritual. A reusable template (scope, guardrails, daily sync, retro, metrics) would lift this from ad-hoc to repeatable. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a tech debt sprint template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Quarterly tech-debt sprint (2 weeks)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working tech debt sprint template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-developer/Quarterly tech-debt sprint (2 weeks)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Tech Debt Sprint Template |

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
| `templates/tech-debt-sprint-template.json` | JSON schema for the Tech Debt Sprint Template output contract |
| `templates/tech-debt-sprint-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-debt-sprint-template.py` | Enforce Tech Debt Sprint Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `role-software-developer/Quarterly tech-debt sprint (2 weeks)`
- solo/dev/role-software-developer
