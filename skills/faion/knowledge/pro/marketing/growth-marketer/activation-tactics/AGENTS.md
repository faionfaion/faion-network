# Activation Tactics & Experiments

## Summary

Concrete techniques for increasing the percentage of new signups that reach the Aha moment: progressive onboarding, templates/presets, activation checklists, empty state redesign, time-to-value reduction, activation emails, and in-app guidance. Each tactic is paired with an experiment template for A/B testing.

## Why

Activation is the conversion from signup to experienced value. Most SaaS products lose 60-70% of signups before they activate. Each tactic targets a specific friction or motivation gap in the signup-to-Aha funnel. Users who use templates activate at 65% vs 35% for blank-start users — a measurable, reproducible pattern across multiple products.

## When To Use

- Activation rate below target (typically below 30-40% for D7).
- Session recordings show users landing on empty states or quitting during onboarding.
- Time-to-first-value exceeds 5 minutes for a simple use case.
- Email open rates for Day 0 welcome email are high but click-through is low.
- You have an A/B testing framework and want a prioritized experiment backlog.

## When NOT To Use

- Pre-PMF: low activation may signal wrong product/audience, not friction — fix the product first.
- Sales-led B2B with human-guided implementations — self-serve activation tactics do not apply.
- When you do not yet track the activation event — instrument first, optimize second.
- Single-session utility tools where "activation" equals "usage" — no onboarding funnel exists.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tactics.xml` | Seven activation tactics with mechanism, example, and expected impact range. |
| `content/02-experiments.xml` | Experiment backlog table, hypothesis template, and rules for running activation A/B tests. |

## Templates

| File | Purpose |
|------|---------|
| `templates/activation-checklist.yaml` | YAML config for in-product onboarding checklist with activation event flag. |
| `templates/email-sequence.md` | 4-email activation sequence: Day 0, Day 1, Day 3, Day 7. |
