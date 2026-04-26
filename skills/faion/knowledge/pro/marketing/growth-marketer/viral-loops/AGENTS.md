# Viral Loops & Types

## Summary

Five viral loop archetypes — Word of Mouth, Inherent, Incentivized, Content, and Outbreak — each with distinct K-factor ranges, share mechanics, and product fit conditions. Pick the loop type that matches the product's natural use, then layer one secondary loop. Never run 4 loops simultaneously.

## Why

Loop type selection determines the ceiling of achievable K. Inherent virality (Slack, Zoom) can reach K=2+ because collaboration requires inviting others. Content virality (TikTok) has K=0.3-0.8 because conversion from viewer to signup is low. Choosing the wrong loop type (forcing "inherent" onto a non-collaborative product) kills NPS without raising K.

## When To Use

- Choosing between viral loop types for a new product or vertical.
- Modeling growth plans: need realistic K, i, c benchmarks before committing to a target.
- Trying to raise K by 0.1-0.3 and needing a structured experiment plan.
- Instrumenting share-moment events for weekly K reporting by loop type.

## When NOT To Use

- Pre-retention: virality on a leaky bucket just speeds churn. Prove D30 retention first.
- B2B enterprise with 6-month sales cycles — loops do not compound on that timescale.
- Heavily regulated products (medical, financial) where outbound viral mechanics breach compliance.
- When you have fewer than 500 invite events — K is noise at small samples.

## Content

| File | What's inside |
|------|---------------|
| `content/01-loop-types.xml` | Five loop types with K ranges, share mechanics, product fit, and real examples. |
| `content/02-selection.xml` | Loop selection by product type, share moments per loop, instrumentation requirements, agent gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/viral_sim.py` | Python simulator comparing loop choices over N days. |
