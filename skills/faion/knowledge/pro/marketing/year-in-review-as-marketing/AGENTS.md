---
slug: year-in-review-as-marketing
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "06f6f2d232adb7a3"
summary: "Year In Review As Marketing: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close'."
tags: [year-in-review-as-marketing, marketing, pro]
---
# Year In Review As Marketing

## Summary

**One-sentence:** Year In Review As Marketing: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close'.

**One-paragraph:** Addresses the gap surfaced by 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close': How to turn the year-end close into a public retrospective that doubles as pipeline content — bridges ops + content marketing for solo operators. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a year in review as marketing artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working year in review as marketing artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p3-technical-freelancer/Year-end tax, legal, and cash-flow close' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Year In Review As Marketing |

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
| `templates/year-in-review-as-marketing.json` | JSON schema for the Year In Review As Marketing output contract |
| `templates/year-in-review-as-marketing.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-year-in-review-as-marketing.py` | Enforce Year In Review As Marketing output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `p3-technical-freelancer/Year-end tax, legal, and cash-flow close`
- pro/marketing/p3-technical-freelancer
