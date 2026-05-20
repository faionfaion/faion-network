---
slug: substack-beehiiv-pick
tier: free
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c753d2dfb6f5d8d0"
summary: "Substack Beehiiv Pick: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Weekly newsletter ideation + draft'."
tags: [substack-beehiiv-pick, marketing, free]
---
# Substack Beehiiv Pick

## Summary

**One-sentence:** Substack Beehiiv Pick: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Weekly newsletter ideation + draft'.

**One-paragraph:** Addresses the gap surfaced by 'p2-indie-hacker/Weekly newsletter ideation + draft': Newsletter-growth methodology assumes you already chose a tool; indie hackers need a fast pick-one decision matrix between Substack/Beehiiv/ConvertKit/Ghost. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a substack beehiiv pick artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p2-indie-hacker/Weekly newsletter ideation + draft' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == free or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working substack beehiiv pick artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p2-indie-hacker/Weekly newsletter ideation + draft' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/marketing/marketing` | parent domain group — provides operating context for Substack Beehiiv Pick |

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
| `templates/substack-beehiiv-pick.json` | JSON schema for the Substack Beehiiv Pick output contract |
| `templates/substack-beehiiv-pick.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-substack-beehiiv-pick.py` | Enforce Substack Beehiiv Pick output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `free/marketing/`
- upstream playbook: `p2-indie-hacker/Weekly newsletter ideation + draft`
- free/marketing/p2-indie-hacker
