---
slug: growth-referral-programs
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured programs that turn satisfied customers into acquisition channels via the TRIGGER-ACTION-REWARD model.
content_id: "c84c5b2ba4e89705"
tags: [referral, growth, acquisition, word-of-mouth, viral]
---
# Growth Referral Programs

## Summary

**One-sentence:** Structured programs that turn satisfied customers into acquisition channels via the TRIGGER-ACTION-REWARD model.

**One-paragraph:** Structured programs that turn satisfied customers into acquisition channels via the TRIGGER-ACTION-REWARD model. Referred users have 4x LTV vs paid-acquisition users and cost 50-80% less to acquire. Referral programs fail when incentives are too weak, the sharing flow is hidden, or fraud is not prevented. Key design decisions: double-sided vs single-sided reward, reward sizing at 20-50% of CAC, trigger placement at win moments (not first visit), and idempotent reward fulfillment to prevent double-crediting.

## Applies If (ALL must hold)

- Product has PMF and at least a few hundred happy customers (NPS positive, D30 retention > 30%).
- CAC via paid channels is rising and unit economics allow a 20-50% CAC reward to referrers.
- LTV is high enough (> 3x CAC) that double-sided incentives are sustainable.
- An agent loop can own design → tracking → email/in-app promotion → fraud review → KPI reporting.

## Skip If (ANY kills it)

- Pre-PMF or NPS still negative — referrals propagate churn, not growth.
- Low-margin commodities where a $10 give/$10 get reward is not sustainable.
- B2B with long enterprise sales cycles where sales-assisted introductions outperform self-serve referrals.
- Compliance-heavy verticals (regulated finance, health) where incentivized referrals trigger jurisdiction-specific disclosure rules.

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
