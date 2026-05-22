---
slug: growth-viral-loops
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Viral loops are self-reinforcing growth cycles where a user action creates an artifact that is shared or exposed, motivating new users to join and repeat the action.
content_id: "06a0e566319fd7f6"
tags: [viral, growth, k-factor, loops, acquisition]
---
# Viral Loops and Growth Mechanics

## Summary

**One-sentence:** Viral loops are self-reinforcing growth cycles where a user action creates an artifact that is shared or exposed, motivating new users to join and repeat the action.

**One-paragraph:** Viral loops are self-reinforcing growth cycles where a user action creates an artifact that is shared or exposed, motivating new users to join and repeat the action. The K-factor (K = i * c, invites-per-user times conversion rate) quantifies loop strength. Seven loop types exist: inherent, word-of-mouth, incentivized, social, collaborative, content, and embedded. Select one primary loop type matched to your product before engineering, then instrument it and iterate via viral-optimization.

## Applies If (ALL must hold)

- Designing a growth loop for a new product or vertical (strategic design layer).
- Choosing among loop types: which fits product DNA, ICP, and current PMF stage?
- Planning measurement infrastructure (events, K-funnel, cycle-time tracker) before engineering.
- Companion to viral-optimization (the iterating layer) and ops-churn-prevention (retention side).
- Designing or auditing a growth loop where user output (content, invites, embedded artifacts) creates distribution that brings new users.
- Strategic-level work: matching loop to product type, sizing the realistic K for the category, planning measurement infrastructure.

## Skip If (ANY kills it)

- Pre-PMF: weak product value means weak inviter motivation and the loop fizzles regardless of mechanics. Fix value, then design loops.
- Pure sales-led businesses where unit economics already work — adding viral complexity gives marginal lift.
- Regulated categories (finance, health, gambling) where unsolicited referrals violate FTC/MiFID II/HIPAA or CASL/GDPR compliance rules.
- Products where sharing imposes social cost on the inviter (sensitive niches) — virality is anti-loyalty.

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
