# A/B Testing Basics

## Summary

A/B testing compares two or more variants of a feature using deterministic hash-based assignment to measure which performs better on a pre-registered primary metric. Define an `Experiment` (hypothesis, variants, metrics, target sample size) before writing any code; bucket users with `hash(experiment_id + user_id) % 10000` for stable, reproducible assignments.

## Why

Gut-feel product decisions produce unpredictable outcomes. Randomized controlled experiments give a causal estimate of variant impact. The key reliability constraint is that everything — allocation, primary metric, MDE, sample size — must be locked before launch; post-hoc changes invalidate the statistical guarantees.

## When To Use

- Testing UI/UX changes (button text, layout, checkout flow) before full rollout.
- Evaluating algorithm improvements (search ranking, recommendation) with a defined success metric.
- Pricing or copy experiments where conversion delta is the primary signal.
- Any change where you need a causal (not correlational) lift estimate.

## When NOT To Use

- Rollouts where randomization is impossible (e.g., infrastructure changes) — use quasi-experimental methods.
- Multi-armed bandit / adaptive allocation — this methodology is fixed-split only.
- High-throughput platforms with thousands of concurrent experiments — use a managed platform (Statsig, Optimizely, GrowthBook) instead of the code snippets here.
- When you cannot reach the required sample size — switch to qualitative research.

## Content

| File | What's inside |
|------|---------------|
| `content/01-design.xml` | Experiment dataclass, variant/metric schema, validation rules, sample-size formula. |
| `content/02-assignment.xml` | Hash-based bucketing, deterministic assignment, override hooks for QA, gotchas. |
| `content/03-antipatterns.xml` | Peeking, multiple testing, mid-run changes, no hypothesis, ignored segments. |

## Templates

| File | Purpose |
|------|---------|
| `templates/experiment.py` | `Experiment`, `Variant`, `Metric` dataclasses + `ExperimentAssigner`. |
| `templates/sample-size.py` | `sample_size_per_variant()` using `statsmodels` z-test for two proportions. |
| `templates/exposure-event.json` | Canonical exposure event schema (experiment_id, variant, user_id, ts, context). |
