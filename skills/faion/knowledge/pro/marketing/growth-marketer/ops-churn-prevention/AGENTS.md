---
slug: ops-churn-prevention
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Churn prevention is an operational playbook for reducing involuntary and voluntary cancellations through three phases: early intervention (re-engagement before the user decides to leave), save offers (at the cancellation flow), and win-back campaigns (after churn).
content_id: "1b4e918e8d16b451"
tags: [churn, retention, lifecycle-marketing, saas, customer-retention]
---
# Churn Prevention

## Summary

**One-sentence:** Churn prevention is an operational playbook for reducing involuntary and voluntary cancellations through three phases: early intervention (re-engagement before the user decides to leave), save offers (at the cancellation flow), and win-back campaigns (after churn).

**One-paragraph:** Churn prevention is an operational playbook for reducing involuntary and voluntary cancellations through three phases: early intervention (re-engagement before the user decides to leave), save offers (at the cancellation flow), and win-back campaigns (after churn). Each phase uses tiered actions matched to churn-reason segment, not a generic discount. Agent role: score health, draft segmented copy, stage campaigns — humans approve send.

## Applies If (ALL must hold)

- Monthly churn is at or above 3% on a paid SaaS or subscription product.
- Churn analysis (ops-churn-basics) is done: root causes segmented by reason (price / value / feature gap / involuntary).
- Engagement events (login, feature use) and payment events are tracked and accessible.
- A lifecycle email tool (Customer.io, Intercom, Braze) is owned and writable.
- Cancellation flow is in your product (you can ship a save-offer page, dunning UI).

## Skip If (ANY kills it)

- B2C apps with no recurring revenue and no contact channel — there is nobody to save.
- Pre-product-market-fit: churn is a symptom of weak value, not weak retention ops.
- Enterprise contracts with manual renewal — handled by AE/CS humans, not this playbook.
- Free tier with zero LTV — saving free users wastes intervention budget.

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
