---
slug: freelance-saas-billing-decision
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Seed-stage SaaS billing-shape decision — subscription vs usage vs hybrid — scored on 4 signals (predictability, primary-value driver, expansion surface, customer size).
content_id: "66db14aa6dbc86f1"
complexity: medium
produces: decision-record
est_tokens: 3200
tags: [saas, billing, pricing-model, subscription, usage-based]
---
# Freelance SaaS Billing Decision

## Summary

**One-sentence:** Seed-stage SaaS billing-shape decision — subscription vs usage vs hybrid — scored on 4 signals (predictability, primary-value driver, expansion surface, customer size).

**One-paragraph:** Current subscription-models content is single-axis. Seed-stage SaaS founders need a decision tree across subscription / usage / hybrid. This methodology scores 4 signals: value predictability (high = subscription, low = usage), primary-value driver (per-seat = subscription, per-action = usage), expansion surface (seat-growth = subscription, usage-spike = usage), customer size (SMB = subscription, enterprise = hybrid). Core rules: every signal scored; decision recorded with kill-criteria + reassessment at 100 customers or 6 months; pricing-page math published; no on-the-fly billing changes.

**Ефективно для:**

- Seed-stage SaaS — initial billing-shape decision.
- Pivot to new value driver — re-evaluate billing.
- Bootstrapped SaaS — defensible math behind the choice.
- Indie hacker — alignment between value + billing.

## Applies If (ALL must hold)

- Seed-stage SaaS pre-100 paying customers.
- Authority to set billing model.
- Stripe / billing infrastructure capable of the chosen model.
- Cost-of-delivery model with at least rough COGS per unit.

## Skip If (ANY kills it)

- Mature SaaS &gt;100 paying customers — switching cost high.
- Pre-revenue with no first paying customer.
- Strict procurement context (enterprise-only).
- Cost-of-delivery unknown.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Value-delivery model | spec | founder |
| Cost-per-unit estimate | spreadsheet | founder |
| Competitor billing models (3 examples) | research | growth team |
| Stripe / Paddle capability check | config | billing team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[fixed-vs-hourly-decision-framework]] | Same signal-scoring pattern. |
| [[freelance-pilot-pricing]] | Pilot pricing is upstream. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: four-signal-score, decision-with-kill-criteria, reassessment-100-or-6m, pricing-page-math, no-on-the-fly-changes | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision-record + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-signals` | sonnet | Bounded judgment per signal. |
| `draft-math` | sonnet | Transparent unit-math copy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.json` | JSON example of billing decision record |
| `templates/pricing-page-math.md` | Pricing-page math template (unit breakdown) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelance-saas-billing-decision.py` | Validate one decision-record JSON against the schema | After draft, before publish |

## Related

- [[fixed-vs-hourly-decision-framework]]
- [[freelance-pilot-pricing]]
- [[experiment-hypothesis-scoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
