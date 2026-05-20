---
slug: build-log-content-template-pack
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Build Log Content Template Pack: codified growth-marketing practice that turns the recurring 'p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source)' decision into a repeatable, auditable artefact.
content_id: "17b45fa6152b499a"
tags: [build-log-content-template-pack, marketing, solo]
---
# Build Log Content Template Pack

## Summary

**One-sentence:** Build Log Content Template Pack: codified growth-marketing practice that turns the recurring 'p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source)' decision into a repeatable, auditable artefact.

**One-paragraph:** Build Log Content Template Pack addresses the gap identified by the p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source) playbook: Indie hackers need repeatable templates: weekly build log, monthly MRR report, milestone celebration post, pivot announcement, sunset announcement. Templates dir under indiehackers strategy covers 3; need a full pack across X, IH, newsletter, blog. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing-manager` | parent role skill — provides the operating context for this methodology |

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
| `templates/build-log-content-template-pack.json` | JSON schema for the Build Log Content Template Pack output contract |
| `templates/build-log-content-template-pack.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-build-log-content-template-pack.py` | Enforce Build Log Content Template Pack output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `p2-indie-hacker/Build-in-Public Weekly Cadence (X + IH + newsletter, single source)`
