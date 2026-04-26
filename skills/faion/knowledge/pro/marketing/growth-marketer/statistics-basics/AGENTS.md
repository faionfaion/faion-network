# Statistical Significance: Basics

## Summary

Core statistical concepts for growth marketers running A/B tests: null hypothesis, p-value, significance level (alpha), statistical power, confidence intervals, and Type I/II errors. The rule: set alpha=0.05 and required sample size BEFORE the test; never peek early and never stop based on direction alone.

## Why

Without statistical rigor, growth teams ship changes that do not work (Type I error) or kill changes that would have worked (Type II error). P-values quantify the probability that an observed difference is random noise. Confidence intervals reveal practical significance beyond the binary yes/no. Pre-calculated sample sizes prevent underpowered tests that are essentially useless (6% power = 94% chance of missing real effects).

## When To Use

- Designing an A/B test: you need sample size, duration, and a primary metric before launch.
- Interpreting finished experiment results: deciding whether to ship, kill, or extend.
- Evaluating whether a result is practically meaningful (lift is real but too small to matter).
- Comparing frequentist vs Bayesian approaches for your team's reporting needs.

## When NOT To Use

- Exploratory analysis of observational data with no random assignment — p-values over-claim causality.
- Fewer than ~30 events per variant — use Fisher's exact test instead.
- Continuous metrics like revenue per user — proportions z-test does not apply; use bootstrapping.
- Sequential/bandit experiments — standard z-tests inflate false positives; use SPRT or Bayesian.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Null hypothesis, p-value, alpha, power, confidence intervals, Type I/II error table. |
| `content/02-formulas.xml` | Two-proportion z-test formula, sample size calculation, worked example with numbers. |
| `content/03-antipatterns.xml` | Peeking, one-tailed tests, multiple comparisons, conflating statistical with practical significance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sample-size-table.md` | Pre-computed sample sizes by baseline rate and MDE for quick planning. |
