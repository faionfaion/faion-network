---
slug: ab-testing-implementation
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The implementation layer for A/B experiments: typed ExperimentEvent tracking (exposure + conversion), ExperimentTracker with in-request exposure deduplication, ExperimentAnalyzer using z-test for proportions with Wilson confidence intervals, and ExperimentReporter for dashboard summaries.
content_id: "4e7814564a65017a"
tags: [a-b-testing, experiment-tracking, statistical-analysis, event-analytics, experiment-reporting]
---
# A/B Testing Implementation

## Summary

**One-sentence:** The implementation layer for A/B experiments: typed ExperimentEvent tracking (exposure + conversion), ExperimentTracker with in-request exposure deduplication, ExperimentAnalyzer using z-test for proportions with Wilson confidence intervals, and ExperimentReporter for dashboard summaries.

**One-paragraph:** The implementation layer for A/B experiments: typed ExperimentEvent tracking (exposure + conversion), ExperimentTracker with in-request exposure deduplication, ExperimentAnalyzer using z-test for proportions with Wilson confidence intervals, and ExperimentReporter for dashboard summaries. Pair with ab-testing-basics for experiment design and sample-size calculation.

## Applies If (ALL must hold)

- Building experiment plumbing in code: deterministic assignment, exposure tracking, conversion events.
- Adding a typed analytics layer so events land cleanly in Mixpanel / Amplitude / PostHog / a warehouse.
- Implementing significance, lift, confidence interval, and power calculations for shipped experiments.
- Generating an experiment summary endpoint or daily-metrics report for a dashboard.

## Skip If (ANY kills it)

- For experiment design (hypothesis, MDE, sample size) — that belongs in ab-testing-basics.
- When a managed platform (Statsig, Optimizely, GrowthBook, LaunchDarkly Experiments, PostHog) already runs assignment and stats — wiring them in is far cheaper than reimplementing.
- For multi-armed bandit / contextual bandits — the methodology is fixed-allocation A/B. Bandits need a different stack (Vowpal Wabbit, Thompson sampling).
- For tests that require sequential analysis (always-valid p-values, mSPRT). Naive z-test peeking gives false positives.
- For tiny user volumes where you'll never reach significance — switch to qualitative or holdout testing instead.

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

- parent skill: `solo/dev/automation-tooling/`
