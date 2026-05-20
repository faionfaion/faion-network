---
slug: visual-regression-testing
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4fe43c41d3e06159"
summary: "Visual Regression Testing: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance'."
tags: [visual-regression-testing, dev, pro]
---
# Visual Regression Testing

## Summary

**One-sentence:** Visual Regression Testing: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance'.

**One-paragraph:** Addresses the gap surfaced by 'role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance': Storybook + Chromatic / Percy / Loki / Playwright-snapshot — no methodology in corpus for catching unintended visual drift, even though it is a daily pain for designers. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a visual regression testing artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working visual regression testing artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Visual Regression Testing |

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
| `templates/visual-regression-testing.json` | JSON schema for the Visual Regression Testing output contract |
| `templates/visual-regression-testing.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-visual-regression-testing.py` | Enforce Visual Regression Testing output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-ux-ui-designer/Design-system-as-code lifecycle: tokens → Storybook → Figma library → PR → governance`
- pro/dev/role-ux-ui-designer
