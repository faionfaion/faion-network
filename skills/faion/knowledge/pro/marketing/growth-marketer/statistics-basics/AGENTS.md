---
slug: statistics-basics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Core statistical concepts for growth marketers running A/B tests: null hypothesis, p-value, significance level (alpha), statistical power, confidence intervals, and Type I/II errors.
content_id: "62fd6dfef97e856b"
tags: [statistics, ab-testing, hypothesis, p-value, power]
---
# Statistical Significance: Basics

## Summary

**One-sentence:** Core statistical concepts for growth marketers running A/B tests: null hypothesis, p-value, significance level (alpha), statistical power, confidence intervals, and Type I/II errors.

**One-paragraph:** Core statistical concepts for growth marketers running A/B tests: null hypothesis, p-value, significance level (alpha), statistical power, confidence intervals, and Type I/II errors. The rule: set alpha=0.05 and required sample size BEFORE the test; never peek early and never stop based on direction alone.

## Applies If (ALL must hold)

- Designing an A/B test: you need sample size, duration, and a primary metric before launch.
- Interpreting finished experiment results: deciding whether to ship, kill, or extend.
- Evaluating whether a result is practically meaningful (lift is real but too small to matter).
- Comparing frequentist vs Bayesian approaches for your team's reporting needs.

## Skip If (ANY kills it)

- Exploratory analysis of observational data with no random assignment — p-values over-claim causality.
- Fewer than ~30 events per variant — use Fisher's exact test instead.
- Continuous metrics like revenue per user — proportions z-test does not apply; use bootstrapping.
- Sequential/bandit experiments — standard z-tests inflate false positives; use SPRT or Bayesian.

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
