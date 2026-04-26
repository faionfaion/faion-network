# Ads Budget Optimization

## Summary

Data-driven framework for allocating and reallocating paid advertising budget across campaigns and channels: calculate target CPA/ROAS, rank campaigns by efficiency ratio, apply the 70-20-10 rule (proven/promising/testing), account for diminishing returns when scaling, and run weekly + monthly reallocation cycles. The core rule is: never scale a campaign more than 30% per week — larger jumps reset algorithm learning and spike CPA.

## Why

Evenly distributing budget ignores performance variance. Campaigns beating target CPA should absorb freed budget from under-performers — but over-scaling a single campaign triggers audience saturation and frequency-driven CPA increases. The efficiency ratio (Target CPA / Actual CPA) provides a single comparable metric across channels with different cost structures. Without a structured reallocation cadence, budget drifts to historical allocation rather than current performance.

## When To Use

- Monthly or weekly budget review across active campaigns
- Deciding whether to scale, hold, or cut a specific campaign
- Comparing efficiency across channels (Meta, Google, LinkedIn) on a common metric
- Planning initial budget split for a new multi-channel program
- Setting budget pacing rules for time-sensitive or month-end campaigns

## When NOT To Use

- Campaign creation or structure setup — use `ads-meta-campaign-setup` or `google-ads-optimization`
- Bid strategy configuration within a single platform — this covers cross-campaign allocation, not per-campaign bidding
- Attribution model selection — use `ads-conversion-tracking` for attribution window decisions
- Testing framework design — budget decisions here assume conversions are already tracking correctly

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Target CPA calculation, efficiency ratio formula, 70-20-10 allocation rule |
| `content/02-reallocation.xml` | Decision matrix by CPA vs target, scaling increments, diminishing-returns model |
| `content/03-cross-channel.xml` | Cross-channel comparison table, incrementality consideration, pacing formula |
| `content/04-antipatterns.xml` | Common budget mistakes: equal budgets, over-scaling, no testing reserve, premature cuts |

## Templates

| File | Purpose |
|------|---------|
| `templates/monthly-allocation.md` | Monthly budget allocation table by channel and campaign type |
| `templates/weekly-review.md` | Weekly reallocation review: performance summary, changes, next focus |
