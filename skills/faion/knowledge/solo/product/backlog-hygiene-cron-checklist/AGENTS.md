---
slug: backlog-hygiene-cron-checklist
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Backlog Hygiene Cron Checklist: codified product-management practice that turns the recurring 'role-product-manager/Backlog grooming + prioritization session' decision into a repeatable, auditable artefact.
content_id: "12061425ab7d1c60"
tags: [backlog-hygiene-cron-checklist, product, solo]
---
# Backlog Hygiene Cron Checklist

## Summary

**One-sentence:** Backlog Hygiene Cron Checklist: codified product-management practice that turns the recurring 'role-product-manager/Backlog grooming + prioritization session' decision into a repeatable, auditable artefact.

**One-paragraph:** Backlog Hygiene Cron Checklist addresses the gap identified by the role-product-manager/Backlog grooming + prioritization session playbook: backlog-management methodology is conceptual; PMs need a stale-item / duplicate / missing-owner cron checklist they can run in 30 min. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Backlog grooming + prioritization session OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Backlog grooming + prioritization session task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/backlog-hygiene-cron-checklist.json` | JSON schema for the Backlog Hygiene Cron Checklist output contract |
| `templates/backlog-hygiene-cron-checklist.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backlog-hygiene-cron-checklist.py` | Enforce Backlog Hygiene Cron Checklist output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `role-product-manager/Backlog grooming + prioritization session`
