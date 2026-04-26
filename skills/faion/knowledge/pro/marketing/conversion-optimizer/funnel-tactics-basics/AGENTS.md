# Funnel Optimization Tactics — Basics

## Summary

A stage-indexed tactic catalog with quantified lift bands for improving conversion at each funnel stage (Top / Middle / Bottom of Funnel + Onboarding), plus four stage-specific checklists (landing page, signup form, checkout, onboarding) for pre-launch audits. Every tactic must be pinned to a measurable stage event and a current baseline before it enters the test backlog. ICE scoring is mandatory; never rank by team preference.

## Why

Funnel drop-off without a tactic catalog produces opinion-driven tests with low win rates. This methodology maps each leak type (headline clarity, form friction, page speed, social proof placement, checkout barriers) to concrete tactics with aggregate lift bands sourced from Formstack, ConversionXL, and Google. Paired with ICE scoring, it turns a funnel analysis into a prioritized sprint backlog within one session.

## When To Use

- Funnel analysis has surfaced a stage leak and you need a quick-win tactic matched to that stage.
- Producing a 30-day CRO sprint backlog: form-field reduction, button contrast, social proof placement, copy simplification.
- Pre-launch audit: running the four-stage checklist against landing page, signup form, checkout, and onboarding screens.
- Generating ICE-scored hypotheses for A/B tests where each hypothesis cites a quantified lift band.

## When NOT To Use

- Strategy or PLG model-selection work — route to `plg-basics`.
- Industry-specific or personalization tactics — route to `funnel-tactics-advanced`.
- Funnel mapping, diagnosis, or process work — route to `funnel-basics-framework`.
- Brand or positioning work — this methodology assumes positioning is fixed and only the conversion mechanism is being tuned.

## Content

| File | What's inside |
|------|---------------|
| `content/01-stage-tactics.xml` | Stage-indexed tactic tables (ToF, MoF, BoF) with typical lift bands; six quick-win tactics with specific benchmarks (form fields, progress bar, button contrast, social proof, page speed, copy simplification). |
| `content/02-checklists-and-rules.xml` | Four stage-specific optimization checklists; ICE ranking rule; mobile-vs-desktop segmentation rule; statistical significance enforcement; antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/form-audit.py` | Playwright-based signup form auditor: counts fields, detects social login, checks load time and CTA count against checklist pass criteria. |
