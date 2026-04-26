# Funnel Optimization Framework

## Summary

A 7-phase process for systematically improving conversion at each step of a user journey: map steps, measure rates, find the biggest drop, diagnose the cause, generate testable hypotheses, run A/B tests, and repeat on the next biggest drop. The rule: always fix the biggest absolute loss first, not the easiest step.

## Why

Every product funnel leaks. Without a structured process, teams guess which step to fix and waste effort on small gains. The framework ensures effort is directed at the highest-leverage drop-off and that changes are validated with data before being declared wins.

## When To Use

- A product has measurable steps from entry to goal (signup, purchase, activation)
- Overall conversion is below industry benchmarks or declining
- You need to prioritize which step to optimize next
- You have at least 7 days of tracking data per step

## When NOT To Use

- Fewer than 100 users per funnel step — sample size too small for meaningful diagnosis
- No analytics instrumentation in place — map and measure steps first before optimizing
- Product has not yet reached product-market fit — optimize retention before acquisition funnel

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 7-phase optimization process with decision rules per phase |
| `content/02-checklist.xml` | Per-phase checklist: measurement, diagnosis, hypothesis, testing |

## Templates

| File | Purpose |
|------|---------|
| `templates/funnel-analysis.md` | Funnel definition + performance + leak analysis + hypothesis table |
| `templates/prompt-funnel-analysis.txt` | LLM prompt for analyzing funnel drop-off and prioritizing fixes |
