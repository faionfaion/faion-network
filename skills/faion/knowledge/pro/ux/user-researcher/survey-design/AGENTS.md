---
slug: survey-design
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A six-step process for designing surveys that produce valid quantitative data: define a single research objective, choose question types, write neutral non-hypothetical questions, structure the flow (screener → easy → core → demographics → open-end), pilot with 5-10 people, and pre-register the analysis plan before fielding.
content_id: "5f18f84108d2cf5e"
tags: [surveys, quantitative-research, survey-methodology, product-research, data-analysis]
---
# Survey Design

## Summary

**One-sentence:** A six-step process for designing surveys that produce valid quantitative data: define a single research objective, choose question types, write neutral non-hypothetical questions, structure the flow (screener → easy → core → demographics → open-end), pilot with 5-10 people, and pre-register the analysis plan before fielding.

**One-paragraph:** A six-step process for designing surveys that produce valid quantitative data: define a single research objective, choose question types, write neutral non-hypothetical questions, structure the flow (screener → easy → core → demographics → open-end), pilot with 5-10 people, and pre-register the analysis plan before fielding. Surveys quantify hypotheses already shaped by 10+ qualitative interviews — they do not discover new problems.

## Applies If (ALL must hold)

- Quantifying a hypothesis already shaped by 10+ qualitative interviews.
- Measuring satisfaction (CSAT, NPS, CES), feature priority (MaxDiff, Kano), or pricing (Van Westendorp, Gabor-Granger) over a defined population.
- Tracking a metric over time where comparability across waves matters more than depth.
- Screening a panel before booking interviews.

## Skip If (ANY kills it)

- Discovery of unknown problems — interviews and analytics outperform surveys here.
- Segment N below ~30 where you intend to report on that segment (confidence intervals explode).
- Predicting future behaviour ("would you buy?") — ask about past behaviour only.
- Audiences who cannot self-report accurately (children, expert tasks, sensitive topics).

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

- parent skill: `pro/ux/user-researcher/`
