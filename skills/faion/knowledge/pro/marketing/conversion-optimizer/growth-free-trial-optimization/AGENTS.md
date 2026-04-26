# Free Trial Optimization

## Summary

A value-first framework for converting time-limited trials (7-30 days) to paid. The core rule: anchor the entire optimization on one activation metric derived from cohort data (not intuition), reduce time to that activation, build a behavior-triggered email sequence with a hard stop-on-activation rule, add in-app countdown and rescue mechanics for inactive trials, and make the trial-to-paid transition seamless (same data, same login).

## Why

Most trials end in silence — no conversion, no feedback — because users never reach the activation event. A clear activation metric anchors all optimization: onboarding shortens the path to it, emails reference it, and rescue triggers fire when users deviate from it. Trial-to-paid conversion benchmarks: 15% is baseline, 25%+ is strong. Activated users convert at 55%+, unactivated at under 10%.

## When To Use

- SaaS with a time-limited trial whose trial-to-paid conversion is below ~15%.
- Clear activation metric is defined; optimization target is reducing time-to-activation.
- Building or refactoring the trial email sequence (welcome → quick start → mid-trial → ending → win-back).
- Designing trial extension and rescue mechanics for inactive trials.
- Comparing trial models (opt-in, opt-out, reverse trial, freemium-to-trial) for a product.

## When NOT To Use

- No trial yet exists and self-serve signup is not validated — prove freemium first.
- Sales-led product where the "trial" is a POC managed by an account team.
- Pre-activation friction (signup conversion) is the dominant problem — fix that first.
- Compliance or contract-required custom trials per customer (enterprise legal).

## Content

| File | What's inside |
|------|---------------|
| `content/01-activation-and-sequence.xml` | Activation metric definition, email sequence structure and timing, in-app engagement tactics, conversion mechanics. |
| `content/02-rescue-and-rules.xml` | At-risk signals, rescue interventions, trial extension policy, hard rules (stop-on-activation, holdback, measurement window). Antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/email-sequence.md` | Welcome, mid-trial check-in, and trial-ending email templates. |
| `templates/at-risk-flagger.py` | Python function: flags trials at risk by login recency, onboarding completion, feature breadth, and team invite status. |
