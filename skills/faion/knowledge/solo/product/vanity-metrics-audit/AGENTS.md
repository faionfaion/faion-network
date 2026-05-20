---
slug: vanity-metrics-audit
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1954945716760d83"
summary: "Vanity Metrics Audit: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR'."
tags: [vanity-metrics-audit, product, solo]
---
# Vanity Metrics Audit

## Summary

**One-sentence:** Vanity Metrics Audit: produces a versioned, owner-signed artefact that closes the gap 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR'.

**One-paragraph:** Addresses the gap surfaced by 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR': Product-analytics methodology covers tooling and event design but not the political act of killing vanity metrics that exec dashboards depend on. PMs need a checklist + stakeholder script. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vanity metrics audit artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vanity metrics audit artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-product-manager/Build a defensible KPI tree from a fuzzy company OKR' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product` | parent domain group — provides operating context for Vanity Metrics Audit |

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
| `templates/vanity-metrics-audit.json` | JSON schema for the Vanity Metrics Audit output contract |
| `templates/vanity-metrics-audit.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vanity-metrics-audit.py` | Enforce Vanity Metrics Audit output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `role-product-manager/Build a defensible KPI tree from a fuzzy company OKR`
- solo/product/role-product-manager
