---
slug: timeboxed-refactor-session-template
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3a03eef1e3666d18"
summary: "Timeboxed Refactor Session Template: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Two-hour refactor block on one module'."
tags: [timeboxed-refactor-session-template, dev, solo]
---
# Timeboxed Refactor Session Template

## Summary

**One-sentence:** Timeboxed Refactor Session Template: produces a versioned, owner-signed artefact that closes the gap 'role-software-developer/Two-hour refactor block on one module'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-developer/Two-hour refactor block on one module': Refactoring-patterns exists as catalog; missing the 'two-hour session contract' template that prevents scope creep — the actual daily-cadence need. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a timeboxed refactor session template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-developer/Two-hour refactor block on one module' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working timeboxed refactor session template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-developer/Two-hour refactor block on one module' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/dev` | parent domain group — provides operating context for Timeboxed Refactor Session Template |

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
| `templates/timeboxed-refactor-session-template.json` | JSON schema for the Timeboxed Refactor Session Template output contract |
| `templates/timeboxed-refactor-session-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-timeboxed-refactor-session-template.py` | Enforce Timeboxed Refactor Session Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/dev/`
- upstream playbook: `role-software-developer/Two-hour refactor block on one module`
- solo/dev/role-software-developer
