---
slug: sunset-customer-comms-template
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "245257f60a7b6e2a"
summary: "Sunset Customer Comms Template: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pivot from failed v1 to v2'."
tags: [sunset-customer-comms-template, marketing, solo]
---
# Sunset Customer Comms Template

## Summary

**One-sentence:** Sunset Customer Comms Template: produces a versioned, owner-signed artefact that closes the gap 'p1-solo-saas-builder/Pivot from failed v1 to v2'.

**One-paragraph:** Addresses the gap surfaced by 'p1-solo-saas-builder/Pivot from failed v1 to v2': Refund-handling exists but the narrative comms (email + landing) that protect founder reputation through a sunset/pivot is uncovered. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a sunset customer comms template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p1-solo-saas-builder/Pivot from failed v1 to v2' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working sunset customer comms template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p1-solo-saas-builder/Pivot from failed v1 to v2' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/marketing` | parent domain group — provides operating context for Sunset Customer Comms Template |

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
| `templates/sunset-customer-comms-template.json` | JSON schema for the Sunset Customer Comms Template output contract |
| `templates/sunset-customer-comms-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sunset-customer-comms-template.py` | Enforce Sunset Customer Comms Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/`
- upstream playbook: `p1-solo-saas-builder/Pivot from failed v1 to v2`
- solo/marketing/p1-solo-saas-builder
