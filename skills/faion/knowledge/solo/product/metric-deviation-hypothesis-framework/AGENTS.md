---
slug: metric-deviation-hypothesis-framework
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Metric Deviation Hypothesis Framework: codified product practice that turns the recurring 'role-product-manager/Weekly product metrics review' decision into a repeatable, auditable artefact.
content_id: "19b4375400bd2892"
tags: [metric-deviation-hypothesis-framework, product, solo]
---
# Metric Deviation Hypothesis Framework

## Summary

**One-sentence:** Metric Deviation Hypothesis Framework: codified product practice that turns the recurring 'role-product-manager/Weekly product metrics review' decision into a repeatable, auditable artefact.

**One-paragraph:** Metric Deviation Hypothesis Framework addresses the gap identified by the role-product-manager/Weekly product metrics review playbook: Product-analytics methodologies cover dashboard setup; they don't teach 'metric moved → hypothesis → action' triage. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-product-manager/Weekly product metrics review OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-product-manager/Weekly product metrics review task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
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
| `templates/metric-deviation-hypothesis-framework.json` | JSON schema for the Metric Deviation Hypothesis Framework output contract |
| `templates/metric-deviation-hypothesis-framework.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-metric-deviation-hypothesis-framework.py` | Enforce Metric Deviation Hypothesis Framework output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/product/product-planning/`
- upstream playbook: `role-product-manager/Weekly product metrics review`
