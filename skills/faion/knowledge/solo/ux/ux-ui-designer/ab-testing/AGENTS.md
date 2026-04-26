# A/B Testing

## Summary

A/B testing is a controlled experiment that compares two versions of a UI element (control A vs. variant B) on a live user population to determine which produces a better outcome on a defined metric. The hypothesis must be pre-registered; statistical significance (typically 95%) and practical significance must both be checked before shipping.

## Why

Design decisions based on opinions create unresolvable debates. A/B testing replaces opinion with behavioral evidence from real users at scale. It answers "which version performs better" but not "why" — that requires qualitative methods.

## When To Use

- A design change has a clear, measurable primary metric (conversion rate, click-through, completion)
- Traffic is sufficient for the required sample size (typically 1,000+ conversions/month)
- The change is isolated — one variable at a time to enable attribution
- Iterative optimization of an existing flow, not early-stage discovery

## When NOT To Use

- Traffic under ~1,000 conversions/month — sample size makes results meaningless
- Major redesigns with multiple simultaneous changes — too many confounds
- When you need to understand *why* users behave differently — use user interviews
- Early-stage product where the primary metric itself is unclear
- Regulatory or safety-critical features where split exposure carries risk

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Seven-step process, hypothesis format, sample size factors, decision matrix |
| `content/02-rules.xml` | Statistical and practical significance rules, agent gotchas, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/test-plan.md` | A/B test plan: hypothesis, metrics, sample size, timeline, risks |
| `templates/results-report.md` | Results template: metrics table, statistical details, segment analysis, decision |
| `templates/ab_stats.py` | Python script for sample size calculation and chi-squared significance test |
