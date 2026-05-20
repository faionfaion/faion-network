---
slug: usability-test-session-tracker-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "9bff924abd2880b3"
summary: "Usability Test Session Tracker Template: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Usability-test moderation (single session)'."
tags: [usability-test-session-tracker-template, ux, solo]
---
# Usability Test Session Tracker Template

## Summary

**One-sentence:** Usability Test Session Tracker Template: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Usability-test moderation (single session)'.

**One-paragraph:** Addresses the gap surfaced by 'role-ux-ui-designer/Usability-test moderation (single session)': Per-session task success/failure logging across many sessions needs a single normalized tracker — current usability-testing methodology is conceptual, not operational. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a usability test session tracker template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ux-ui-designer/Usability-test moderation (single session)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working usability test session tracker template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ux-ui-designer/Usability-test moderation (single session)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux` | parent domain group — provides operating context for Usability Test Session Tracker Template |

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
| `templates/usability-test-session-tracker-template.json` | JSON schema for the Usability Test Session Tracker Template output contract |
| `templates/usability-test-session-tracker-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-usability-test-session-tracker-template.py` | Enforce Usability Test Session Tracker Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/ux/`
- upstream playbook: `role-ux-ui-designer/Usability-test moderation (single session)`
- solo/ux/role-ux-ui-designer
