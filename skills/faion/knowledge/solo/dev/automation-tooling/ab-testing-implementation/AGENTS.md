# A/B Testing Implementation

## Summary

The implementation layer for A/B experiments: typed `ExperimentEvent` tracking (exposure + conversion), `ExperimentTracker` with in-request exposure deduplication, `ExperimentAnalyzer` using z-test for proportions with Wilson confidence intervals, and `ExperimentReporter` for dashboard summaries. Pair with `ab-testing-basics` for experiment design and sample-size calculation.

## Why

Unstructured event tracking leads to data that cannot support analysis: missing variant labels, duplicate exposures inflating sample size, or conversions logged without checking whether the user was actually exposed. Typed dataclasses + a single analytics call pattern make the event schema a code-reviewable contract; the analyzer runs only on closed datasets to prevent peeking.

## When To Use

- Building experiment plumbing in code: deterministic assignment, exposure tracking, conversion events.
- Adding a typed analytics layer so events land cleanly in Mixpanel / Amplitude / PostHog / a warehouse.
- Implementing significance, lift, confidence interval, and power calculations for shipped experiments.
- Generating an experiment summary endpoint or daily-metrics report for a dashboard.

## When NOT To Use

- Experiment design (hypothesis, MDE, sample size) — that belongs in `ab-testing-basics`.
- When a managed platform (Statsig, Optimizely, GrowthBook, PostHog) already handles assignment and stats.
- Multi-armed bandit / contextual bandits — this is fixed-allocation A/B only.
- Sequential analysis (always-valid p-values, mSPRT) — the naive z-test here inflates Type I error if used for peeking.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tracking.xml` | `ExperimentEvent` schema, `ExperimentTracker` with deduplication, exposure vs conversion call sites. |
| `content/02-analysis.xml` | `ExperimentAnalyzer`: z-test for proportions, Wilson CI, power calc, sample-size solver. SRM guard. |
| `content/03-reporting.xml` | `ExperimentReporter`: per-variant summary, daily-metrics trend, structured JSON output contract. |

## Templates

| File | Purpose |
|------|---------|
| `templates/srm-check.py` | Chi-square SRM guard — fail the analysis if traffic split deviates from configured allocation. |
