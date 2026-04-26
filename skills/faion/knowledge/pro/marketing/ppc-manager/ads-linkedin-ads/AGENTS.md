# LinkedIn Ads

## Summary

B2B advertising on LinkedIn using job title, seniority, company size, and ABM targeting. CPCs run $5-15; minimum $50/day budget is required for the optimizer to exit the learning phase. Use Lead Gen Forms in parallel with Website Conversions — LGF has higher volume but lower intent. Refresh creative every 14-21 days. Never increase budget more than 25% in one step without human approval.

## Why

LinkedIn is the only ad platform with reliable professional identity targeting (title, seniority, company). This precision makes it the correct channel for reaching narrow B2B ICPs — VPs at fintech, Directors at mid-market SaaS — that are unreachable at equivalent cost on Meta or Google. The tradeoff is cost: CPM of $30-80 and CPC of $5-15 require AOV or LTV above ~$1k to be viable.

## When To Use

- B2B campaigns where the buyer is identifiable by job title, seniority, or company (ABM)
- Lead-gen forms with LinkedIn-prefilled fields (email, company, title) for high-quality MQLs
- Reaching narrow ICPs unreachable on Meta or Google at acceptable CPL
- Retargeting site visitors with the LinkedIn Insight Tag for warm-funnel B2B nurture

## When NOT To Use

- B2C, low-AOV products, or impulse purchases — CPC of $5-15 destroys unit economics below ~$1k LTV
- Daily budgets under $50 — LinkedIn's optimizer cannot exit learning phase
- Audiences under 20k — costs spike, learning never converges, frequency fatigue triggers early
- Pure brand awareness on a tight budget — Meta/YouTube cost-per-impression is 5-10x cheaper

## Content

| File | What's inside |
|------|---------------|
| `content/01-campaign-setup.xml` | Objectives, targeting options and strategies, ad formats, audience sizing |
| `content/02-creative-bidding.xml` | Copy formula, budget expectations, bidding options, optimization metrics |
| `content/03-agent-rules.xml` | API gotchas: token rotation, versioning, rate limits, cost units, Lead Gen Form schema drift |

## Templates

| File | Purpose |
|------|---------|
| `templates/campaign-checklist.md` | Pre-launch checklist: targeting, creative, budget, lead gen form |
| `templates/ad-copy.md` | B2B ad copy template: intro, headline, description, CTA |
| `templates/pacing-audit.py` | Daily spend pacing check against daily budget cap |
