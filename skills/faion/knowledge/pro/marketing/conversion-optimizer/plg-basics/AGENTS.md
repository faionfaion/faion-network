# PLG Basics and Models

## Summary

Product-Led Growth (PLG) is a go-to-market strategy where the product is the primary vehicle for acquiring, activating, and retaining customers — no sales team required for self-serve tiers. Four models: freemium (forever-free tier with limits), free trial (full access for 7-30 days), open core (free OSS + paid cloud/enterprise), usage-based (pay per consumption unit). Select the model using the 6-factor fit matrix (complexity, decision-maker, price, TTV, trial feasibility, market size); score ≥ 5/6 = pure PLG, 3-4 = hybrid PLG + sales.

## Why

Traditional SaaS sales-led GTM requires linear headcount scaling: more revenue = more sales reps. PLG makes the product the seller for sub-$50K ACV deals: users discover, try, and upgrade without talking to sales. CAC drops from $500-5,000 (sales-led) to $10-100 (PLG). Scale becomes exponential rather than linear. The PLG flywheel — acquisition → activation → engagement → monetization → expansion → referral — compounds with product improvement.

## When To Use

- Choosing a PLG model for a new product or new pricing tier.
- Auditing whether a sales-led or marketing-led GTM should adopt or hybridize with PLG.
- Onboarding team members who need shared vocabulary (Aha moment, TTV, PLG flywheel, PQL) before deeper PLG work.
- Writing strategic memos or pricing-model RFCs that need a defensible model classification with examples.

## When NOT To Use

- Tactical optimization (which form fields, which copy) — route to `plg-optimization-tactics`.
- Implementation steps (Aha definition, PQL scoring, playbooks) — route to `plg-implementation-guide`.
- Metric definitions and tracking — route to `plg-metrics`.
- Deep enterprise procurement, six-figure sales-cycle products — methodology explicitly flags ACV &gt; $50K as poor PLG fit.

## Content

| File | What's inside |
|------|---------------|
| `content/01-models.xml` | Four PLG models (freemium, free trial, open core, usage-based) with best-fit conditions, conversion triggers, and canonical examples (Slack, Zoom, Notion, Calendly). |
| `content/02-fit-and-flywheel.xml` | PLG vs sales-led vs marketing-led comparison, 6-factor fit matrix, hybrid PLG+sales motion, fit scorer, common LLM mistakes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plg-fit-scorer.py` | Dataclass scoring product against the 6-factor fit matrix; returns fit score and pure_plg / hybrid / sales_led recommendation. |
