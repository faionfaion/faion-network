---
slug: weekly-pm-async-broadcast-template
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c7f6063ad3d8efe9"
summary: "Weekly Pm Async Broadcast Template: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Monday roadmap pulse review'."
tags: [weekly-pm-async-broadcast-template, product, solo]
---
# Weekly Pm Async Broadcast Template

## Summary

**One-sentence:** Weekly Pm Async Broadcast Template: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Monday roadmap pulse review'.

**One-paragraph:** Addresses the gap surfaced by 'role-product-manager/Monday roadmap pulse review': Solo + small-team PMs need a repeatable async-update format (problem/decision/next-step) — current product-planning playbooks stop at roadmap-design and don't cover the broadcast ritual. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly pm async broadcast template artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-product-manager/Monday roadmap pulse review' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly pm async broadcast template artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-product-manager/Monday roadmap pulse review' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product` | parent domain group — provides operating context for Weekly Pm Async Broadcast Template |

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
| `templates/weekly-pm-async-broadcast-template.json` | JSON schema for the Weekly Pm Async Broadcast Template output contract |
| `templates/weekly-pm-async-broadcast-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-pm-async-broadcast-template.py` | Enforce Weekly Pm Async Broadcast Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `role-product-manager/Monday roadmap pulse review`
- solo/product/role-product-manager
