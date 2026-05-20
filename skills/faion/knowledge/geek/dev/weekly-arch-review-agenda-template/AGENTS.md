---
slug: weekly-arch-review-agenda-template
tier: geek
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "682f53563d6aa208"
summary: "Weekly Arch Review Agenda Template: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Weekly architectural review (45 min)'."
tags: [weekly-arch-review-agenda-template, dev, geek]
---
# Weekly Arch Review Agenda Template

## Summary

**One-sentence:** Weekly Arch Review Agenda Template: produces a versioned, owner-signed artefact that closes the gap 'p6-product-dev-team/Weekly architectural review (45 min)'.

**One-paragraph:** Addresses the gap surfaced by 'p6-product-dev-team/Weekly architectural review (45 min)': design-docs-* pages exist but no agenda template for the recurring 45-min ritual. Without it, the meeting drifts into status. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly arch review agenda template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Weekly architectural review (45 min)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly arch review agenda template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p6-product-dev-team/Weekly architectural review (45 min)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/dev/dev` | parent domain group — provides operating context for Weekly Arch Review Agenda Template |

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
| `templates/weekly-arch-review-agenda-template.json` | JSON schema for the Weekly Arch Review Agenda Template output contract |
| `templates/weekly-arch-review-agenda-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-arch-review-agenda-template.py` | Enforce Weekly Arch Review Agenda Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/dev/`
- upstream playbook: `p6-product-dev-team/Weekly architectural review (45 min)`
- geek/dev/p6-product-dev-team
