---
slug: audience-to-paid-conversion-loop
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Audience to Paid Conversion Loop: codified growth-marketing practice that turns the recurring 'p2-indie-hacker/Audience-to-customer conversion sprint' decision into a repeatable, auditable artefact.
content_id: "472fec3e032bc407"
tags: [audience-to-paid-conversion-loop, marketing, solo]
---
# Audience to Paid Conversion Loop

## Summary

**One-sentence:** Audience to Paid Conversion Loop: codified growth-marketing practice that turns the recurring 'p2-indie-hacker/Audience-to-customer conversion sprint' decision into a repeatable, auditable artefact.

**One-paragraph:** Audience to Paid Conversion Loop addresses the gap identified by the p2-indie-hacker/Audience-to-customer conversion sprint playbook: The funnel from audience → signup → paid is the indie-hacker bottleneck. Conversion-optimizer/landing-page-design exists, but no end-to-end conversion-sprint methodology. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p2-indie-hacker/Audience-to-customer conversion sprint OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p2-indie-hacker/Audience-to-customer conversion sprint task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-conversion-window | ~900 |
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
| `templates/audience-to-paid-conversion-loop.json` | JSON schema for the Audience to Paid Conversion Loop output contract |
| `templates/audience-to-paid-conversion-loop.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audience-to-paid-conversion-loop.py` | Enforce Audience to Paid Conversion Loop output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `p2-indie-hacker/Audience-to-customer conversion sprint`
