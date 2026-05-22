---
slug: activation-metrics
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A methodology for defining, measuring, and improving the activation rate — the percentage of signups who reach their first value moment (the "Aha moment").
content_id: "70985e50393475c1"
tags: [activation, metrics, retention, funnel, onboarding]
---
# Activation Metrics

## Summary

**One-sentence:** A methodology for defining, measuring, and improving the activation rate — the percentage of signups who reach their first value moment (the "Aha moment").

**One-paragraph:** A methodology for defining, measuring, and improving the activation rate — the percentage of signups who reach their first value moment (the "Aha moment"). Covers how to identify the right activation event by correlating candidate actions with D30 retention, how to measure time-bounded activation rates, benchmark ranges by product type, and a worked optimization funnel template.

## Applies If (ALL must hold)

- Users sign up but don't return after the first session.
- Onboarding completion is high but D30 retention is low — possible activation misdefinition.
- Pre-scaling acquisition: fix activation before spending more on top-of-funnel.
- Redesigning onboarding flow and need a metric to validate the change.

## Skip If (ANY kills it)

- Pre-PMF: if core value is undefined, activation measurement is premature.
- Enterprise SaaS with multi-month sales cycles — activation happens over weeks, not sessions.
- Products with no analytics infrastructure — defining the metric without tracking it produces no signal.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/marketing/growth-marketer/`
