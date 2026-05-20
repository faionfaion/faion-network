---
slug: agency-cashflow-management
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "663887549c0fc274"
summary: "Agency Cashflow Management: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/general'."
tags: [agency-cashflow-management, marketing, pro]
---
# Agency Cashflow Management

## Summary

**One-sentence:** Agency Cashflow Management: produces a versioned, owner-signed artefact that closes the gap 'p5-micro-agency-founder/general'.

**One-paragraph:** Addresses the gap surfaced by 'p5-micro-agency-founder/general': ops-financial-basics is generic founder-finance. Micro-agencies have a specific cashflow shape: deposits + milestone payments + net-30 retainers + contractor-payable-on-receipt = constant 30–60 day gaps. They need a methodology for cashflow forecasting at this granularity, deposit policy, late-payment escalation, contractor-payment-timing. Currently undercovered. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a agency cashflow management artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p5-micro-agency-founder/general' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working agency cashflow management artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p5-micro-agency-founder/general' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Agency Cashflow Management |

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
| `templates/agency-cashflow-management.json` | JSON schema for the Agency Cashflow Management output contract |
| `templates/agency-cashflow-management.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-cashflow-management.py` | Enforce Agency Cashflow Management output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: ``
- pro/marketing/p5-micro-agency-founder
