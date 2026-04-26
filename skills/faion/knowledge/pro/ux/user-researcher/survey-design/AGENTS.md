# Survey Design

## Summary

A six-step process for designing surveys that produce valid quantitative data: define a single research objective, choose question types, write neutral non-hypothetical questions, structure the flow (screener → easy → core → demographics → open-end), pilot with 5-10 people, and pre-register the analysis plan before fielding. Surveys quantify hypotheses already shaped by 10+ qualitative interviews — they do not discover new problems.

## Why

Surveys without methodology training produce misleading data: leading questions bias responses, double-barreled items are uninterpretable, hypothetical questions ("would you pay $X?") predict nothing, and small-N segments reported as findings create false confidence. A bias-auditor agent pass over every instrument catches issues the drafting agent introduces. Pre-registering the analysis plan prevents fishing expeditions after data arrives.

## When To Use

- Quantifying a hypothesis already shaped by 10+ qualitative interviews.
- Measuring satisfaction (CSAT, NPS, CES), feature priority (MaxDiff, Kano), or pricing (Van Westendorp, Gabor-Granger) over a defined population.
- Tracking a metric over time where comparability across waves matters more than depth.
- Screening a panel before booking interviews.

## When NOT To Use

- Discovery of unknown problems — interviews and analytics outperform surveys here.
- Segment N below ~30 where you intend to report on that segment (confidence intervals explode).
- Predicting future behaviour ("would you buy?") — ask about past behaviour only.
- Audiences who cannot self-report accurately (children, expert tasks, sensitive topics).

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-process.xml` | Six-step process, question types, bias patterns, structure and length guidelines |
| `content/02-examples.xml` | Two worked examples (SaaS pricing, feature prioritization) with antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/survey-design-doc.md` | Survey design document with objective, screener, core questions, analysis plan |
| `templates/question-bank.md` | Reusable questions for pricing (Van Westendorp), satisfaction (NPS), feature priority (MaxDiff) |
| `templates/vw-pricing.py` | Van Westendorp price-sensitivity analysis from CSV export |
