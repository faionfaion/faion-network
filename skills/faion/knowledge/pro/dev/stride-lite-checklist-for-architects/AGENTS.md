---
slug: stride-lite-checklist-for-architects
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "a79d34499de6f728"
summary: "Stride Lite Checklist For Architects: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Security review of a new dependency or service edge'."
tags: [stride-lite-checklist-for-architects, dev, pro]
---
# Stride Lite Checklist For Architects

## Summary

**One-sentence:** Stride Lite Checklist For Architects: produces a versioned, owner-signed artefact that closes the gap 'role-software-architect/Security review of a new dependency or service edge'.

**One-paragraph:** Addresses the gap surfaced by 'role-software-architect/Security review of a new dependency or service edge': Security-architecture exists but no lightweight STRIDE-per-PR / per-edge variant suitable for weekly cadence. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a stride lite checklist for architects artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Security review of a new dependency or service edge' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working stride lite checklist for architects artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-software-architect/Security review of a new dependency or service edge' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/dev` | parent domain group — provides operating context for Stride Lite Checklist For Architects |

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
| `templates/stride-lite-checklist-for-architects.json` | JSON schema for the Stride Lite Checklist For Architects output contract |
| `templates/stride-lite-checklist-for-architects.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-stride-lite-checklist-for-architects.py` | Enforce Stride Lite Checklist For Architects output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/`
- upstream playbook: `role-software-architect/Security review of a new dependency or service edge`
- pro/dev/role-software-architect
