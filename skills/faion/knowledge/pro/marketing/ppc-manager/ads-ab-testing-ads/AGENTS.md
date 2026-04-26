# A/B Testing Ads

## Summary

Scientific method applied to ad creative: pre-register one hypothesis (one variable changed), calculate required sample size before launching, run control vs. variant on the same audience with equal budget, and only verdict once 95% confidence is reached. Test in priority order: offer → hook/headline → creative type → visual style → copy length → CTA. Document every result to build an institutional learning library.

## Why

Without controlled tests, every campaign iteration is a guess. You cannot learn whether your blue button beats red, or whether testimonials outperform product shots, if you change multiple things at once. Pre-registering hypothesis and sample size prevents peeking errors and p-hacking. A learning library compounds: each test narrows the hypothesis space for the next, accelerating improvement.

## When To Use

- Running a continuous testing cadence across hooks, creatives, and offers.
- Evaluating a specific creative hypothesis before scaling spend.
- Coordinating cross-platform tests (Meta + Google) on the same hypothesis.
- Maintaining a tests registry for team knowledge sharing.

## When NOT To Use

- Daily/weekly conversion volume below 100 per variant — tests will never reach significance; ship the better-reasoned option and move on.
- Brand-new accounts with under 30 days history — algorithmic variance dominates creative variance.
- Holiday peaks (BFCM, Q4 retail) — exogenous demand swamps treatment effect; run proven creatives.
- Tests where multiple variables changed — use multivariate or Bandit design instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-design.xml` | Testing priority order, variable isolation rules, sample-size requirements, significance thresholds. |
| `content/02-platform-execution.xml` | Meta Experiments setup, Google Ads Experiments setup, Bayesian verdict script, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-brief.md` | Test brief: hypothesis, variables, success metric, parameters, expected outcome. |
| `templates/test-results.md` | Results template: winner, confidence, lift, data table, learnings, next steps. |
| `templates/testing-roadmap.md` | Quarterly testing roadmap with monthly test schedule and backlog. |
| `templates/bayesian-ab.py` | Bayesian Beta-binomial verdict function (p_variant_better, expected lift, winner). |
