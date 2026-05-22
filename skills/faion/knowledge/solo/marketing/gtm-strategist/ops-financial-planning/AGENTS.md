---
slug: ops-financial-planning
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Forward-looking financial methodology for solopreneurs: project cash flow (3-month and 12-month), calculate runway (cash / monthly burn), allocate profits using the reinvestment framework (reserve 20% first, then split reinvestment vs.
content_id: "bf47f5ebf94bba7d"
tags: [financial-planning, cash-flow, runway, reinvestment, solopreneur]
---
# Financial Planning

## Summary

**One-sentence:** Forward-looking financial methodology for solopreneurs: project cash flow (3-month and 12-month), calculate runway (cash / monthly burn), allocate profits using the reinvestment framework (reserve 20% first, then split reinvestment vs.

**One-paragraph:** Forward-looking financial methodology for solopreneurs: project cash flow (3-month and 12-month), calculate runway (cash / monthly burn), allocate profits using the reinvestment framework (reserve 20% first, then split reinvestment vs. owner pay by profit tier), and run quarterly scenario reviews with a base case and 20%-revenue-drop stress case.

## Applies If (ALL must hold)

- Solopreneur has initial revenue and needs sustainable growth planning
- Product reaches breakeven; deciding how to allocate the first profits
- Runway drops below 6 months; need scenario modeling to prioritize cuts
- Quarterly review is due and projections need updating from real data
- Planning a pricing change or major spend decision (ads, contractor)

## Skip If (ANY kills it)

- Pre-revenue stage with no real data — use financial-basics methodology instead
- GAAP accounting or investor-grade reporting — requires a CPA, not an agent
- Complex equity or cap-table planning — use Carta or legal counsel
- Multi-entity corporate structures — agent assumptions do not hold
- Any automated payment or transfer decision — human approval required before execution

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

- parent skill: `solo/marketing/gtm-strategist/`
