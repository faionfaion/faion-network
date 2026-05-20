---
slug: app-store-and-play-store-release
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: App Store and Play Store Release: codified engineering practice that turns the recurring 'role-software-developer/Ship a Mobile Build on iOS and Android' decision into a repeatable, auditable artefact.
content_id: "417846034394d162"
tags: [app-store-and-play-store-release, dev, pro]
---
# App Store and Play Store Release

## Summary

**One-sentence:** App Store and Play Store Release: codified engineering practice that turns the recurring 'role-software-developer/Ship a Mobile Build on iOS and Android' decision into a repeatable, auditable artefact.

**One-paragraph:** App Store and Play Store Release addresses the gap identified by the role-software-developer/Ship a Mobile Build on iOS and Android playbook: Store submission flow, review-rejection patterns, staged rollouts, version bumping policy. No methodology references either store. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-software-developer/Ship a Mobile Build on iOS and Android OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-software-developer/Ship a Mobile Build on iOS and Android task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/app-store-and-play-store-release.json` | JSON schema for the App Store and Play Store Release output contract |
| `templates/app-store-and-play-store-release.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-app-store-and-play-store-release.py` | Enforce App Store and Play Store Release output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-developer/Ship a Mobile Build on iOS and Android`
