---
slug: twitter-x-monetization-thread-to-product
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3d170bd5b9d55921"
summary: "Twitter X Monetization Thread To Product: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Distribution-First Idea Validation (audience before product)'."
tags: [twitter-x-monetization-thread-to-product, marketing, solo]
---
# Twitter X Monetization Thread To Product

## Summary

**One-sentence:** Twitter X Monetization Thread To Product: produces a versioned, owner-signed artefact that closes the gap 'p2-indie-hacker/Distribution-First Idea Validation (audience before product)'.

**One-paragraph:** Addresses the gap surfaced by 'p2-indie-hacker/Distribution-First Idea Validation (audience before product)': `growth-twitter-x-growth` covers reach. Missing: the conversion mechanic — pinned tweet, link-in-bio funnel, thread CTA patterns, DM-to-demo flow. P2's primary acquisition channel deserves its own conversion methodology. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a twitter x monetization thread to product artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p2-indie-hacker/Distribution-First Idea Validation (audience before product)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working twitter x monetization thread to product artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p2-indie-hacker/Distribution-First Idea Validation (audience before product)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing` | parent domain group — provides operating context for Twitter X Monetization Thread To Product |

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
| `templates/twitter-x-monetization-thread-to-product.json` | JSON schema for the Twitter X Monetization Thread To Product output contract |
| `templates/twitter-x-monetization-thread-to-product.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-twitter-x-monetization-thread-to-product.py` | Enforce Twitter X Monetization Thread To Product output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `p2-indie-hacker/Distribution-First Idea Validation (audience before product)`
- solo/marketing/p2-indie-hacker
