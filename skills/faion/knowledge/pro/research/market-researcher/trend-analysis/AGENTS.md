---
slug: trend-analysis
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Trend analysis at the market-researcher level identifies emerging patterns from industry analyst reports, macroeconomic indicators, regulatory pipelines, and incumbent 10-K filings.
content_id: "bf474c5624667233"
tags: [trend-analysis, market-trends, macro-indicators, regulatory-analysis, competitor-signals]
---
# Trend Analysis (Market-Researcher Lens)

## Summary

**One-sentence:** Trend analysis at the market-researcher level identifies emerging patterns from industry analyst reports, macroeconomic indicators, regulatory pipelines, and incumbent 10-K filings.

**One-paragraph:** Trend analysis at the market-researcher level identifies emerging patterns from industry analyst reports, macroeconomic indicators, regulatory pipelines, and incumbent 10-K filings. Every numeric market-size or CAGR row must carry a source URL, publication year, and page number; reject any row that an agent produces from training data without a live citation.

## Applies If (ALL must hold)

- Pre-investment or vertical-selection for regulated categories (fintech, health, crypto, AI infra) where the policy clock dominates the product clock
- Annual strategic planning: mapping CAGR + concentration + regulatory pipeline against a 3-year revenue plan
- M&A or partnership scan: spotting that an incumbent's moat is eroding because a rule is opening the market
- Re-pricing an existing offer after a macro shift (rates, FX, labour cost) moves customer willingness-to-pay
- Investor or board memo: produces the "market context" slide with cited analyst rows, not vibes

## Skip If (ANY kills it)

- Pure dev-tool or open-source category trends - the researcher variant (HN/PH/GitHub signals) is faster and cheaper
- Day-to-day content topic ranking - analyst-report cadence is quarterly, not weekly
- Pre-revenue idea screening - at idea stage, customer interviews beat IDC reports
- Narrow local-language B2B niches - Gartner/Forrester rarely cover segments below $500M outside US/EU
- When the goal is "find the next viral product" - analyst reports are explicitly lagging signals

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

- parent skill: `pro/research/market-researcher/`
