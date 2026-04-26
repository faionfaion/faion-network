# Cohort Analysis Basics

## Summary

Cohort analysis groups users who share a common characteristic (typically signup period) and tracks their behavior over time. The primary output is a cohort retention table (rows = cohort, columns = D1/D7/D30/D90, cells = retention rate). Three cohort types exist: acquisition (when they joined), behavioral (what action they took), and feature (which feature they used). Aggregate metrics hide trends that cohort tables reveal.

## Why

Overall "D30 = 15%" is not actionable — it mixes users from different acquisition periods, channels, and product states. Cohort tables reveal whether retention is improving across cohorts, which acquisition channels produce quality users, and which behaviors or features predict better outcomes. Behavioral cohorts ("users who completed onboarding have 3x D30 retention") drive product prioritization better than aggregate averages.

## When To Use

- Aggregate retention numbers feel meaningless because the product, traffic mix, or pricing has changed over time.
- You need to attribute a retention shift to a specific product or acquisition change.
- Pre-A/B-test power planning — knowing baseline cohort variance is required to size experiments.
- Identifying "magic features" (high-retention predictors) to double down on in onboarding.

## When NOT To Use

- Pre-launch or fewer than 100 users per cohort — noise dominates signal.
- One-off transactional products where retention is not the goal — measure repeat-purchase or NPS instead.
- Long-cycle B2B with quarterly usage — daily/weekly cohort tables produce noise; switch to monthly or feature-event cohorts.
- As proof of causation — behavioral cohort correlation ("feature X users retain 3x better") is not evidence the feature caused it; requires A/B test or propensity matching.

## Content

| File | What's inside |
|------|---------------|
| `content/01-cohort-types.xml` | Acquisition, behavioral, and feature cohort types with reading guide for cohort tables |
| `content/02-analysis-rules.xml` | Cohort minimum size rule, diagonal effect, survivorship bias, magic-feature fallacy |
| `content/03-benchmarks.xml` | SaaS and consumer app retention benchmarks by cohort day with quality tiers |

## Templates

| File | Purpose |
|------|---------|
| `templates/basic-cohort.py` | Quick acquisition cohort table from CSV using pandas |
| `templates/retention-cohort-table.md` | Cohort retention analysis reporting template |
| `templates/behavioral-cohort.md` | Behavioral cohort hypothesis and results template |
