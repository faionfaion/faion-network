---
slug: timezone-overlap-comms-charter
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "8f90c4aefad91832"
summary: "Timezone Overlap Comms Charter: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap'."
tags: [timezone-overlap-comms-charter, pm, pro]
---
# Timezone Overlap Comms Charter

## Summary

**One-sentence:** Timezone Overlap Comms Charter: produces a versioned, owner-signed artefact that closes the gap 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap'.

**One-paragraph:** Addresses the gap surfaced by 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap': Multi-month engagement with US/EU/APAC clients lives or dies on async-first comms. Existing stakeholder-engagement is org-internal. A charter template that explicitly defines overlap windows, decision-record SLAs, and 'written-first' rituals would directly impact retention. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a timezone overlap comms charter artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working timezone overlap comms charter artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p4-outsource-specialist/Foreign-Client Engagement Bootstrap' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Timezone Overlap Comms Charter |

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
| `templates/timezone-overlap-comms-charter.json` | JSON schema for the Timezone Overlap Comms Charter output contract |
| `templates/timezone-overlap-comms-charter.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-timezone-overlap-comms-charter.py` | Enforce Timezone Overlap Comms Charter output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p4-outsource-specialist/Foreign-Client Engagement Bootstrap`
- pro/pm/p4-outsource-specialist
