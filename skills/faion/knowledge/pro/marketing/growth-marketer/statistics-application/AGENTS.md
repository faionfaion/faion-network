---
slug: statistics-application
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Practical tools for applying significance testing: raw-count templates, power analysis template, three worked examples (significant result, insufficient data, underpowered test), and Python helpers.
content_id: "4aa88eb0b67b952e"
tags: [statistics, significance, a-b-testing, power-analysis, experiments]
---
# Statistical Significance: Application

## Summary

**One-sentence:** Practical tools for applying significance testing: raw-count templates, power analysis template, three worked examples (significant result, insufficient data, underpowered test), and Python helpers.

**One-paragraph:** Practical tools for applying significance testing: raw-count templates, power analysis template, three worked examples (significant result, insufficient data, underpowered test), and Python helpers. Requires raw counts (n1, x1, n2, x2) — never run from headline percentages alone.

## Applies If (ALL must hold)

- Analyzing a finished A/B test and needing a defensible significance and CI verdict.
- Sizing an experiment up-front (power analysis) so you do not waste traffic.
- Suspecting an "underpowered win" and needing to compute actual achieved power.
- Standardizing stat reporting across many small tests so results are comparable over time.

## Skip If (ANY kills it)

- Causal inference from observational data (no random assignment) — significance tests over-claim.
- Multi-armed or sequential or bandit experiments — z-tests inflate false positives; use SPRT, group sequential, or Bayesian.
- Fewer than 30 events per variant — use Fisher's exact test.
- Highly skewed continuous metrics (revenue, session length) — use bootstrapping or t-test on log-transformed data.

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

- parent skill: `pro/marketing/growth-marketer/`
