---
slug: weekly-gsc-diagnostic-template
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "13393509123578fc"
summary: "Weekly Gsc Diagnostic Template: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Weekly Search Console + analytics review (60 min)'."
tags: [weekly-gsc-diagnostic-template, marketing, solo]
---
# Weekly Gsc Diagnostic Template

## Summary

**One-sentence:** Weekly Gsc Diagnostic Template: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Weekly Search Console + analytics review (60 min)'.

**One-paragraph:** Addresses the gap surfaced by 'role-growth-marketing/Weekly Search Console + analytics review (60 min)': GSC dumps numbers but not a verdict. Need a structured 'why did this win/lose' rubric so reviews end with decisions, not vibes. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly gsc diagnostic template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Weekly Search Console + analytics review (60 min)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly gsc diagnostic template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-growth-marketing/Weekly Search Console + analytics review (60 min)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing` | parent domain group — provides operating context for Weekly Gsc Diagnostic Template |

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
| `templates/weekly-gsc-diagnostic-template.json` | JSON schema for the Weekly Gsc Diagnostic Template output contract |
| `templates/weekly-gsc-diagnostic-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-gsc-diagnostic-template.py` | Enforce Weekly Gsc Diagnostic Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `role-growth-marketing/Weekly Search Console + analytics review (60 min)`
- solo/marketing/role-growth-marketing
