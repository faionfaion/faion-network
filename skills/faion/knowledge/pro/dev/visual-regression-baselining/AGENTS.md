---
slug: visual-regression-baselining
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "69d21094a5b4fdc9"
summary: "Visual Regression Baselining: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Unflake and parallelize a slow E2E suite'."
tags: [visual-regression-baselining, dev, pro]
---
# Visual Regression Baselining

## Summary

**One-sentence:** Visual Regression Baselining: produces a versioned, owner-signed artefact that closes the gap 'role-qa-engineer/Unflake and parallelize a slow E2E suite'.

**One-paragraph:** Addresses the gap surfaced by 'role-qa-engineer/Unflake and parallelize a slow E2E suite': Free-tier e2e-testing examples briefly mention 'visual regression' but ship no methodology: tool choice (Percy/Chromatic/Playwright snapshots/Loki), baseline management, diff-review workflow, deterministic rendering (fonts, animations), and handling intentional visual changes. Critical for FE teams and design-system regression. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a visual regression baselining artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-qa-engineer/Unflake and parallelize a slow E2E suite' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working visual regression baselining artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-qa-engineer/Unflake and parallelize a slow E2E suite' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Visual Regression Baselining |

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
| `templates/visual-regression-baselining.json` | JSON schema for the Visual Regression Baselining output contract |
| `templates/visual-regression-baselining.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-visual-regression-baselining.py` | Enforce Visual Regression Baselining output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-qa-engineer/Unflake and parallelize a slow E2E suite`
- pro/dev/role-qa-engineer
