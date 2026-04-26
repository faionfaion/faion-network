# Product-Led Growth (PLG)

## Summary

PLG is a go-to-market strategy where the product itself drives acquisition, activation, and expansion — users sign up, reach value without sales intervention, and upgrade through usage. The PM owns the activation metric definition, the PQL-to-sales hand-off contract, and the weekly metric-review loop.

## Why

Sales-led CAC payback >18 months is unsustainable for SaaS. PLG companies achieve higher revenue per employee by making the product the growth engine. Ahrefs reached $40M ARR with 40 employees via pure PLG. The key mechanism: freeze an activation definition tied to D30 retention, instrument it, and run a weekly review loop with growth.

## When To Use

- New SaaS/API/dev-tool where the buyer is also the user (founder, dev, designer).
- Existing sales-led product losing on CAC — convert top-of-funnel to self-serve.
- Bottom-up enterprise wedge: individual signs up free, expansion to org is the business model.
- Product has a measurable "aha moment" reachable in under 10 minutes.
- API/developer product where first successful call is the activation event.

## When NOT To Use

- True top-down enterprise (procurement, RFPs, 6+ month sales cycles) — PLG instrumentation is fine, PLG-as-strategy will starve.
- Highly regulated B2B where self-serve onboarding is legally blocked.
- One-time-purchase/transactional products with no retention curve to optimize.
- Marketplaces with cold-start liquidity problems — fix supply/demand first.
- Products requiring a human implementation (data migration, custom modeling).

## Content

| File | What's inside |
|------|---------------|
| `content/01-plg-principles.xml` | Core PLG principles, key metrics (Activation Rate, TTV, PQL, NRR), onboarding best practices |
| `content/02-plg-agentic-workflow.xml` | Weekly PM loop, PQL hand-off contract, agent gotchas, failure modes |

## Templates

| File | Purpose |
|------|---------|
| `templates/plg-definitions.yml` | Frozen activation/PQL spec — the PM-to-growth contract |
| `templates/plg-snapshot.sh` | Weekly PLG metric snapshot script (PostHog/HogQL) |
