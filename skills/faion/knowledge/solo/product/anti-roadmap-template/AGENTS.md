---
slug: anti-roadmap-template
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Anti Roadmap Template: codified product-management practice that turns the recurring 'role-product-manager/Quarter planning + OKR cascade' decision into a repeatable, auditable artefact.
content_id: "06795c229e5a4444"
tags: [anti-roadmap-template, product, solo]
---
# Anti Roadmap Template

## Summary

**One-sentence:** Anti Roadmap Template: codified product-management practice that turns the recurring 'role-product-manager/Quarter planning + OKR cascade' decision into a repeatable, auditable artefact.

**One-paragraph:** Anti Roadmap Template addresses the gap identified by the role-product-manager/Quarter planning + OKR cascade playbook: Roadmap methodologies focus on what we WILL ship; the costly skill is publishing what we explicitly will NOT ship. PMs ask for this every quarter. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Quarter planning + OKR cascade OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Quarter planning + OKR cascade task (last 30 days)
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
| `templates/anti-roadmap-template.json` | JSON schema for the Anti Roadmap Template output contract |
| `templates/anti-roadmap-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-roadmap-template.py` | Enforce Anti Roadmap Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/`
- upstream playbook: `role-product-manager/Quarter planning + OKR cascade`
