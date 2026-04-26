# Financial Planning

## Summary

Forward-looking financial methodology for solopreneurs: project cash flow (3-month and
12-month), calculate runway (cash / monthly burn), allocate profits using the reinvestment
framework (reserve 20% first, then split reinvestment vs. owner pay by profit tier), and
run quarterly scenario reviews with a base case and 20%-revenue-drop stress case.

## Why

Solopreneurs conflate owner draw with operating profit, causing invisible cash drain.
Building the 12-month forecast bottom-up from known customer count and ARPU — not top-down
from desired revenue — produces a grounded plan. The reinvestment framework (50/30/20 at
under $5K profit, shifting to 30/50/20 above $15K) prevents both under-paying the owner and
over-investing before the business is stable. A minimum 3-month runway protects against a
single bad month becoming a crisis.

## When To Use

- Solopreneur has initial revenue and needs sustainable growth planning
- Product reaches breakeven; deciding how to allocate the first profits
- Runway drops below 6 months; need scenario modeling to prioritize cuts
- Quarterly review is due and projections need updating from real data
- Planning a pricing change or major spend decision (ads, contractor)

## When NOT To Use

- Pre-revenue stage with no real data — use financial-basics methodology instead
- GAAP accounting or investor-grade reporting — requires a CPA, not an agent
- Complex equity or cap-table planning — use Carta or legal counsel
- Multi-entity corporate structures — agent assumptions do not hold
- Any automated payment or transfer decision — human approval required before execution

## Content

| File | What's inside |
|------|---------------|
| `content/01-cash-flow-and-runway.xml` | Cash flow projection tables, runway formula, safety targets by stage |
| `content/02-reinvestment-framework.xml` | Profit allocation tiers, investment priority order, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/monthly-review.md` | Monthly P&L review: revenue, expenses, profitability, cash position, next focus |
| `templates/annual-budget.md` | Annual revenue forecast + expense budget by category and quarter |
| `templates/stripe-runway.py` | Pull MRR from Stripe API and calculate runway with warning threshold |
