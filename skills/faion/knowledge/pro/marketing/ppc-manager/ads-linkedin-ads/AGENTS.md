---
slug: ads-linkedin-ads
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: B2B advertising on LinkedIn using job title, seniority, company size, and ABM targeting.
content_id: "e35780f421ff1183"
tags: [linkedin, b2b, ads, abm, lead-generation]
---
# LinkedIn Ads

## Summary

**One-sentence:** B2B advertising on LinkedIn using job title, seniority, company size, and ABM targeting.

**One-paragraph:** B2B advertising on LinkedIn using job title, seniority, company size, and ABM targeting. CPCs run $5-15; minimum $50/day budget is required for the optimizer to exit the learning phase. Use Lead Gen Forms in parallel with Website Conversions — LGF has higher volume but lower intent. Refresh creative every 14-21 days. Never increase budget more than 25% in one step without human approval.

## Applies If (ALL must hold)

- B2B campaigns where the buyer is identifiable by job title, seniority, or company (ABM)
- Lead-gen forms with LinkedIn-prefilled fields (email, company, title) for high-quality MQLs
- Reaching narrow ICPs unreachable on Meta or Google at acceptable CPL
- Retargeting site visitors with the LinkedIn Insight Tag for warm-funnel B2B nurture

## Skip If (ANY kills it)

- B2C, low-AOV products, or impulse purchases — CPC of $5-15 destroys unit economics below ~$1k LTV
- Daily budgets under $50 — LinkedIn's optimizer cannot exit learning phase
- Audiences under 20k — costs spike, learning never converges, frequency fatigue triggers early
- Pure brand awareness on a tight budget — Meta/YouTube cost-per-impression is 5-10x cheaper

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

- parent skill: `pro/marketing/ppc-manager/`
