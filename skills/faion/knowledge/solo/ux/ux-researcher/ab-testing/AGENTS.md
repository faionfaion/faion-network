---
slug: ab-testing
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design decisions based on opinions create debates without resolution.
content_id: "b7f4b22564934e1d"
tags: [ab-testing, quantitative-research, experimentation, statistics, conversion-optimization]
---
# A/B Testing

## Summary

**One-sentence:** Design decisions based on opinions create debates without resolution.

**One-paragraph:** Design decisions based on opinions create debates without resolution. A/B testing (controlled experimentation) compares a control version against a variant by randomly assigning users to each, measuring conversion or engagement impact, and determining statistical significance. Use when you have a specific metric to measure, enough traffic to reach significance within a reasonable timeframe, and need to validate that a change does not harm secondary or guardrail metrics.

## Applies If (ALL must hold)

- You have a specific, measurable conversion metric (sign-ups, click-through, checkout completion) and want to validate a design change improves it.
- A design debate cannot be resolved by expert judgment and a quantitative answer is needed.
- You have enough traffic to reach statistical significance within a reasonable run time (typically 1-2 weeks).
- You are iterating on a proven flow to optimize incrementally—not when redesigning from scratch.
- You want to validate that a change helps the primary metric without harming secondary or guardrail metrics.

## Skip If (ANY kills it)

- On low-traffic pages where reaching statistical significance would take months or years—qualitative research is faster.
- During major product redesigns where user mental models differ—test user understanding first with qualitative research (interviews, usability testing).
- When you need to understand why users behave differently, not just whether they do—use session recordings and interviews instead.
- For complex multi-step flows where the winning variant on step 1 may harm completion on step 5—funnel analysis with holdout groups is needed.
- On pages with high seasonal variance without adjusting for the cycle.

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

- parent skill: `solo/ux/ux-researcher/`
