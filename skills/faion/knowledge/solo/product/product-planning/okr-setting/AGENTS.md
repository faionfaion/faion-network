---
slug: okr-setting
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Set quarterly OKRs: 1-3 objectives, 3 key results each, leading not lagging where possible, with a confidence band and weekly check-in cadence.
content_id: "8f10305fbb41ca55"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["okr", "objectives", "key-results", "quarterly", "leading-indicators"]
---
# OKR Setting

## Summary

**One-sentence:** Set quarterly OKRs: 1-3 objectives, 3 key results each, leading not lagging where possible, with a confidence band and weekly check-in cadence.

**One-paragraph:** OKRs work when they're few, leading, and reviewed. The methodology forces choice — at most 3 objectives — and pairs each with leading-indicator KRs so the team can act on signals mid-quarter rather than reading a post-mortem.

**Ефективно для:**

- Solo founder running with vague 'goals for the quarter' — needs a 3-objective frame that survives 13 weeks without rewrite, plus a weekly check-in that doesn't take 2 hours.

## Applies If (ALL must hold)

- Quarterly planning cadence exists or is being established.
- Founder commits ≥30 min/week to OKR check-in.
- Outcomes can plausibly be measured within a quarter.

## Skip If (ANY kills it)

- Crisis / firefight mode — fix that first.
- Pre-product phase — use discovery cadence instead.
- Team prefers a different system (e.g. NSM-only) and is happy with it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic outcomes | markdown | Strategy doc |
| Metric history (3+ months) | csv | Analytics |
| Calendar slot for check-ins | calendar event | Calendar |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager/roadmap-design` | OKRs anchor roadmap horizons. |
| `solo/product/product-operations/product-analytics` | KR data source. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-okr-setting` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-okr-setting` | haiku | Schema check + threshold checks; deterministic. |
| `review-okr-setting` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/okr-setting.json` | JSON skeleton conforming to the output contract schema. |
| `templates/okr-setting.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-okr-setting.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[roadmap-design]]
- [[product-analytics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
