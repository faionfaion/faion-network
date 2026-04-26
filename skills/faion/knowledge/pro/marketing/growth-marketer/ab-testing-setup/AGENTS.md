# A/B Testing Setup

## Summary

A/B testing setup covers the technical and analytical groundwork for a valid experiment: accurate sample-size calculation (statsmodels NormalIndPower, not the simplified 16×p(1-p)/MDE² teaching formula), traffic-split configuration with deterministic-hash bucketing, SRM monitoring from day 1, and a plan-and-results template that an analyst agent fills in deterministically.

## Why

The single biggest experiment-program failure mode is not low K-factor or poor hypothesis quality — it is underpowered tests that produce noise mistaken for signal. Using statsmodels gives honest sample-size math; the simplified formula under- or over-estimates by 25–50% for non-50/50 splits, one-sided tests, or asymmetric baselines. Pre-committing to end dates and wiring SRM day 1 prevents the two most common invalidation patterns.

## When To Use

- Pre-launch sample-size and duration calculation for any planned experiment.
- Configuring traffic split, randomization, and SRM monitoring in Statsig, GrowthBook, LaunchDarkly, or equivalent.
- Auditing a draft test plan against the pre-launch checklist before traffic flows.
- Generating plan and results templates that analysts fill in consistently across the team.

## When NOT To Use

- Network-effect surfaces (chat, marketplace, multiplayer) — independent randomization is invalid; use cluster or switchback designs.
- Heavy personalization where every user already sees a unique variant — plain A/B math doesn't apply.
- Single-shot critical decisions (pricing model, brand direction) — blast radius too large.
- Pre-instrumentation: if the primary metric is not tracked end-to-end yet, instrument first; computing sample size is meaningless otherwise.
- Continuous heavy-tailed outcome metrics (revenue per user) without log-transform or bootstrap — proportion math misleads.

## Content

| File | What's inside |
|------|---------------|
| `content/01-sample-size.xml` | Sample-size calculation rules, formula comparison (statsmodels vs simplified), duration formula, quick reference table |
| `content/02-experiment-config.xml` | Randomization rules, SRM monitoring, sequential testing, A/A test, holdout bucket |
| `content/03-checklist.xml` | Setup checklist: technical platform, analytics, team training, success metrics, governance |

## Templates

| File | Purpose |
|------|---------|
| `templates/sample-size.py` | Python: accurate n_per_variant and duration_days using statsmodels |
| `templates/test-plan.md` | A/B test planning card template |
| `templates/test-results.md` | A/B test results template |
