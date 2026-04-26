# Activation Framework & Path Optimization

## Summary

A 7-step framework for diagnosing and improving activation rate: define the activation event (behavior correlated with D30+ retention), measure baseline, map the funnel step by step, find the biggest drop-offs, reduce friction, increase motivation, and iterate with A/B tests. Correct activation event definition is the most critical and most commonly wrong step.

## Why

Most SaaS products lose 60-80% of signups before activation. The framework provides a systematic approach rather than guessing which tactic to apply first. The hardest part is defining the right activation event — it must be a behavior that predicts long-term retention, not a milestone that merely signals engagement (e.g. "completed onboarding" is less predictive than "shared a doc within 48h").

## When To Use

- Signups are coming in but week-1 retention is mediocre and the bottleneck is unknown.
- Choosing or validating an activation event ("aha moment") that should correlate with D30 retention.
- Mapping a funnel, instrumenting missing events, and prioritizing which drop-off to attack first.
- Building a weekly activation dashboard and experiment backlog.

## When NOT To Use

- Pre-launch: design activation into onboarding from day one; no remediation framework needed.
- Pre-PMF: low activation may signal wrong product or wrong audience — fix the product first, not the funnel.
- Sales-led B2B: activation happens in human-led implementation; CSM playbooks beat self-serve frameworks.
- Single-session utility tools where every visit is an activation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | 7-step framework, activation event definition rules, funnel mapping example. |
| `content/02-diagnosis.xml` | Diagnosis by symptom, common mistakes, ICE scoring for prioritization, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ice.py` | Python ICE scorer for ranking activation experiments. |
