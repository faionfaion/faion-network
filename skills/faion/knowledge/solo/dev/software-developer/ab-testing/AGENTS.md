# A/B Testing Implementation

## Summary

A/B testing runtime implementation covering deterministic variant assignment, exposure and conversion event tracking, statistical analysis (z-test for proportions, Wilson CI), and Sample Ratio Mismatch detection. Core rule: assignment must use deterministic hashing (`hash(user_id || experiment_id) mod 100`) — never `random.choice` — to ensure sticky bucketing across sessions, devices, and processes.

## Why

Non-deterministic assignment produces different variants for the same user on repeat visits, contaminating results. Tracking conversions without exposures removes the denominator, making results meaningless. Peeking at p-values before the precomputed end date inflates false-positive rate from 5% to 20–30%. SRM (skewed traffic split) invalidates all results and is almost always caused by bucketing bugs or redirect asymmetries.

## When To Use

- Experiment design is complete (hypothesis, primary metric, MDE, sample size) and runtime is needed
- Multi-platform consistency: same user must get same variant on web, iOS, app, and email
- Building an event pipeline joining exposure → conversion in a stats engine (Snowflake, ClickHouse)
- Wiring a feature flag into a real experiment with stratified randomization

## When NOT To Use

- Traffic too low to reach statistical power (under ~1k weekly users on the surface) — use qualitative methods
- Changes affecting every user equally and irreversibly (DB schema migrations)
- Cosmetic tweaks where test cost exceeds shipping cost
- Multi-armed scenarios with strong network effects (marketplace pricing) — A/B is biased; use switchback or geo splits
- Compliance-bound flows (KYC, payments) where variant differences create audit problems

## Content

| File | What's inside |
|------|---------------|
| `content/01-assignment.xml` | Deterministic hash-based assignment, sticky bucketing, experiment configuration |
| `content/02-tracking.xml` | ExperimentEvent dataclass, ExperimentTracker with exposure deduplication and conversion logging |
| `content/03-analysis.xml` | ExperimentAnalyzer: z-test for proportions, Wilson CI, power calculation, sample size formula |
| `content/04-antipatterns.xml` | random.choice, missing exposures, peeking, wrong statistical test for binary metrics |

## Templates

| File | Purpose |
|------|---------|
| `templates/analyzer.py` | ExperimentAnalyzer with full statistical analysis and ExperimentResults dataclass |
| `templates/sample-size.py` | Sample size calculator per arm using NormalIndPower |
