---
slug: audience-segmentation
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A 5-step methodology for dividing a potential market into distinct, scored groups using 2-3 dimensions drawn from observed data (demographic, behavioral, psychographic, needs-based).
content_id: "1b17d1bfb969be65"
tags: [segmentation, marketing, positioning, icp, research]
---
# Audience Segmentation

## Summary

**One-sentence:** A 5-step methodology for dividing a potential market into distinct, scored groups using 2-3 dimensions drawn from observed data (demographic, behavioral, psychographic, needs-based).

**One-paragraph:** A 5-step methodology for dividing a potential market into distinct, scored groups using 2-3 dimensions drawn from observed data (demographic, behavioral, psychographic, needs-based). Produces a scored segment matrix and a target-strategy decision. Outputs audience-segmentation.md in .aidocs/product_docs/.

## Applies If (ALL must hold)

- Pre-launch: deciding which single segment gets the MVP.
- Post-launch with mixed signals (high churn in 30% of cohort, high NPS in 50%) — segment to find actual ICP.
- Repositioning a stalled product where "everyone" messaging tests failed.
- Pricing tier design when usage data shows two or more behavioral clusters.
- Channel allocation when paid spend is diffuse without a clear winner.
- B2B GTM when sales calls reveal distinct buyer types with different objections.

## Skip If (ANY kills it)

- TAM under ~5k addressable accounts — further segmentation starves each segment of evidence.
- First 10 paying customers — too few data points; run pain-points and problem-validation first.
- Pure infra/dev tools where the buyer is "any engineer with this stack" — use niche-evaluation.
- Dimensions chosen from gut alone with no interview/CRM/analytics data backing them.
- One-off campaigns where the segment is already given by the brief.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/research/researcher/`
