---
slug: audience-driven-pivot-decision
tier: solo
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: When MRR stalls and the product fails, pivot the product while keeping the audience — a scoped decision distinct from zero-to-one repivots.
content_id: "41912af86f2c2f99"
tags: [audience-driven-pivot-decision, product, solo]
---

# Audience-Driven Pivot Decision

## Summary

**One-sentence:** When MRR stalls and the product fails, pivot the product while keeping the audience — a scoped decision distinct from zero-to-one repivots.

**One-paragraph:** No methodology covers this scoped decision for audience-first builders. Mechanism: confirm audience health, isolate product/feature failure, brainstorm 3-5 adjacent products the same audience would buy, run a paid validation test, decide. Output: pivot decision artefact with audience-retention plan.

## Applies If (ALL must hold)

- MRR has been flat or declining ≥90 days
- founder has an active audience (newsletter/Twitter/community) ≥1,000 engaged
- product can be sunset within 30 days without contractual issues

## Skip If (ANY kills it)

- audience also stalled — full repivot needed, not audience-keeping pivot
- B2B with annual contracts — pivot timeline incompatible
- single enterprise customer dependency — pivot needs different governance

## Prerequisites

- newsletter open / engagement metrics for last 6 months
- MRR and churn data for last 6 months
- list of 5+ adjacent problems the audience has raised

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning` | parent skill — provides operating context for this methodology |
| `solo/product/sunset-failed-product-playbook` | peer methodology — produces inputs or consumes outputs |
| `solo/research/problem-validation` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `solo/product/product-planning/`
- peer methodology: `solo/product/sunset-failed-product-playbook`
- peer methodology: `solo/research/problem-validation`
- external: https://www.indiehackers.com/post/the-audience-first-pivot (indie hackers community)
