# Growth Referral Programs

## Summary

Structured programs that turn satisfied customers into acquisition channels via the TRIGGER-ACTION-REWARD model. Key design decisions: double-sided vs single-sided reward, reward sizing at 20-50% of CAC, trigger placement at win moments (not first visit), and idempotent reward fulfillment to prevent double-crediting.

## Why

Word-of-mouth is the highest-converting acquisition channel but is left to chance without a program. Referred users have 4x LTV vs paid-acquisition users (they arrived with social proof) and cost 50-80% less to acquire. Referral programs fail when incentives are too weak, the sharing flow is hidden, or fraud is not prevented.

## When To Use

- Product has PMF and at least a few hundred happy customers (NPS positive, D30 retention > 30%).
- CAC via paid channels is rising and unit economics allow a 20-50% CAC reward to referrers.
- LTV is high enough (> 3x CAC) that double-sided incentives are sustainable.
- An agent loop can own design → tracking → email/in-app promotion → fraud review → KPI reporting.

## When NOT To Use

- Pre-PMF or NPS still negative — referrals propagate churn, not growth.
- Low-margin commodities where a $10 give/$10 get reward is not sustainable.
- B2B with long enterprise sales cycles where sales-assisted introductions outperform self-serve referrals.
- Compliance-heavy verticals (regulated finance, health) where incentivized referrals trigger jurisdiction-specific disclosure rules.

## Content

| File | What's inside |
|------|---------------|
| `content/01-design.xml` | Reward types, sizing formula, trigger points, sharing friction reduction. |
| `content/02-operations.xml` | Promotion channels, fraud prevention, key metrics, agent workflow and gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/landing-page.md` | Referral program landing page copy with stats block and FAQ. |
| `templates/emails.md` | Announcement and reminder email copy. |
| `templates/k_factor.py` | Python helper to compute K from API/event data. |
