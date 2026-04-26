# Viral Metrics & K-factor

## Summary

The viral coefficient K = i × c, where i is average invites sent per user and c is the conversion rate of those invites. K > 1 produces exponential growth; K = 0.5-1.0 amplifies other channels. Measure i, c, and viral cycle time weekly; optimize both independently.

## Why

Paid acquisition costs compound; viral growth does not. K-factor quantifies self-sustaining growth: each user with K=1.2 brings 1.2 more users, doubling the cohort every cycle. Most products target K=0.3-0.7 as a meaningful supplement to paid channels — K > 1 is rare and reserved for inherently collaborative or content-based products.

## When To Use

- Designing or auditing a referral/sharing mechanism for an existing product.
- Building a weekly viral dashboard to track i, c, and K by loop type and channel.
- Projecting growth to determine whether viral alone can hit a user target within N cycles.
- Identifying which factor (i or c) has the most improvement headroom.

## When NOT To Use

- Pre-retention: if D30 retention is below 20%, increasing K just cycles more users through a leaky bucket.
- B2B enterprise with 6-month sales cycles — K compounds too slowly to matter for pipeline.
- When invite event tracking is not yet in place — computing K from incomplete data is misleading.
- Regulated products where incentivized referrals trigger disclosure requirements.

## Content

| File | What's inside |
|------|---------------|
| `content/01-k-factor.xml` | K formula, interpretation thresholds, growth projection table, viral cycle time. |
| `content/02-optimization.xml` | How to increase i and c independently; benchmarks by product type; common mistakes. |

## Templates

none
