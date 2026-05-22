---
slug: survey-design
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Survey design is the methodology for creating quantitative research instruments that yield valid, actionable data.
content_id: "5f18f84108d2cf5e"
tags: [survey, quantitative-research, questionnaire-design, user-research, data-collection]
---
# Survey Design

## Summary

**One-sentence:** Survey design is the methodology for creating quantitative research instruments that yield valid, actionable data.

**One-paragraph:** Survey design is the methodology for creating quantitative research instruments that yield valid, actionable data. The core rule: conduct at least 10 interviews before building a survey — surveys quantify known patterns, they cannot discover unknown problems. Every question must be specific, single-concept, and neutrally worded; surveys fail when they ask hypotheticals instead of facts or exceed 7 minutes in length.

## Applies If (ALL must hold)

- After 10+ qualitative interviews have surfaced patterns worth quantifying
- Pricing sensitivity studies (Van Westendorp, Gabor-Granger) where N >= 100 is realistic
- Feature prioritization across an installed user base (MaxDiff, Kano, importance/satisfaction matrix)
- Periodic NPS/CSAT tracking against a stable cohort
- Screener-driven recruitment funnels for follow-up interviews

## Skip If (ANY kills it)

- Discovery of unknown problems — interviews and observation reveal what surveys cannot ask about
- Sample sizes below ~30 — stick to interviews; quantitative claims are not defensible
- Predicting future behavior ("would you pay X?") — use price-anchored conjoint or pre-orders
- B2B segments where the named buyer is gated — 1:1 outreach beats panel surveys
- Internal stakeholder alignment — use a workshop, not a survey

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
