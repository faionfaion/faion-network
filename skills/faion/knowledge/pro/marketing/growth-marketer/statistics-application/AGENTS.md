# Statistical Significance: Application

## Summary

Practical tools for applying significance testing: a significance calculation template, pre-test power analysis template, three worked examples (significant result, insufficient data, underpowered test), and a Python helper for automated analysis. Requires raw counts (n1, x1, n2, x2) — never run from headline percentages alone.

## Why

Growth teams waste traffic by running underpowered tests and make wrong decisions by analyzing results before the pre-registered sample size is reached. Standardized templates force pre-registration of hypothesis, primary metric, and sample size before launch — preventing post-hoc metric selection and peeking.

## When To Use

- Analyzing a finished A/B test and needing a defensible significance + CI verdict.
- Sizing an experiment up-front (power analysis) so you do not waste traffic.
- Suspecting an "underpowered win" and needing to compute actual achieved power.
- Standardizing stat reporting across many small tests so results are comparable over time.

## When NOT To Use

- Causal inference from observational data (no random assignment) — significance tests over-claim.
- Multi-armed / sequential / bandit experiments — z-tests inflate false positives; use SPRT, group sequential, or Bayesian.
- Fewer than 30 events per variant — use Fisher's exact test.
- Highly skewed continuous metrics (revenue, session length) — use bootstrapping or t-test on log-transformed data.

## Content

| File | What's inside |
|------|---------------|
| `content/01-worked-examples.xml` | Three examples: significant result, not significant (need more data), underpowered test. |
| `content/02-agent-rules.xml` | Agent-specific rules: forcing raw counts, binary significance, Bonferroni, common LLM gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/significance-check.md` | Template for recording raw data, z-test, CI, and decision. |
| `templates/power-analysis.md` | Template for pre-test sample size calculation with MDE notation. |
| `templates/stat_check.py` | Python helper using statsmodels for z-test + power analysis. |
