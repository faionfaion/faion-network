---
slug: swipe-file-tweet-hooks
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4bd2d230d125e326"
summary: "Swipe File Tweet Hooks: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months'."
tags: [swipe-file-tweet-hooks, marketing, solo]
---
# Swipe File Tweet Hooks

## Summary

**One-sentence:** Swipe File Tweet Hooks: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months'.

**One-paragraph:** Addresses the gap surfaced by 'p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months': Solo creators stall on blank-page hook problem. A curated library of 60–100 hook patterns (build-log, story, contrarian, metric-flex) tied to content pillars converts the daily-cadence engine into a runnable system. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a swipe file tweet hooks artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working swipe file tweet hooks artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing` | parent domain group — provides operating context for Swipe File Tweet Hooks |

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
| `templates/swipe-file-tweet-hooks.json` | JSON schema for the Swipe File Tweet Hooks output contract |
| `templates/swipe-file-tweet-hooks.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-swipe-file-tweet-hooks.py` | Enforce Swipe File Tweet Hooks output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `p2-indie-hacker/Build-in-public audience growth: 0 to 5K followers over 6 months`
- solo/marketing/p2-indie-hacker
