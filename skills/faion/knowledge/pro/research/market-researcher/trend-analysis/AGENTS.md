# Trend Analysis (Market-Researcher Lens)

## Summary

Trend analysis at the market-researcher level identifies emerging patterns from industry analyst reports, macroeconomic indicators, regulatory pipelines, and incumbent 10-K filings — not just consumer signals. The core rule: every numeric market-size or CAGR row must carry a source URL, publication year, and page number; reject any row that an agent produces from training data without a live citation. This is the macro-and-regulatory variant; the generalist signal-collection pipeline (Hacker News, Product Hunt, GitHub) lives in the researcher counterpart.

## Why

Analyst reports lag real inflection by 12-24 months but still provide the confirming evidence investors require. Regulatory pipeline shifts (EU AI Act, MiCA, DSA) reshape market structure before any revenue KPI moves. 10-K risk-factor diffs signal incumbent fear before earnings. Without a structured citation-enforcement rule, LLMs fabricate CAGR numbers with high confidence — the highest-confidence/lowest-grounding sentence pattern in research automation.

## When To Use

- Pre-investment or vertical-selection for regulated categories (fintech, health, crypto, AI infra) where the policy clock dominates the product clock
- Annual strategic planning: mapping CAGR + concentration + regulatory pipeline against a 3-year revenue plan
- M&A or partnership scan: spotting that an incumbent's moat is eroding because a rule is opening the market
- Re-pricing an existing offer after a macro shift (rates, FX, labour cost) moves customer willingness-to-pay
- Investor or board memo: produces the "market context" slide with cited analyst rows, not vibes

## When NOT To Use

- Pure dev-tool or open-source category trends — the researcher variant (HN/PH/GitHub signals) is faster and cheaper
- Day-to-day content topic ranking — analyst-report cadence is quarterly, not weekly
- Pre-revenue idea screening — at idea stage, customer interviews beat IDC reports
- Narrow local-language B2B niches — Gartner/Forrester rarely cover segments below $500M outside US/EU
- When the goal is "find the next viral product" — analyst reports are explicitly lagging signals

## Content

| File | What's inside |
|------|---------------|
| `content/01-trend-lifecycle.xml` | Trend categories (fad/trend/megatrend/shift), adoption curve stages, STEEP analysis framework |
| `content/02-macro-regulatory.xml` | Macro-collector sources (FRED, World Bank, Eurostat), regulatory pipeline tracking (EUR-Lex, Federal Register), incumbent momentum via 10-K diffs |
| `content/03-scoring-and-antipatterns.xml` | Trend strength scoring criteria, opportunity matrix, AI-agent gotchas (numeric hallucination, stale data, regulatory-stage confusion) |

## Templates

| File | Purpose |
|------|---------|
| `templates/trend-analysis-report.md` | Full trend analysis report with STEEP analysis, competitive landscape, and opportunity assessment |
| `templates/trend-monitoring-dashboard.md` | Monthly trend watch dashboard for tracking multiple trends and logging new signals |
| `templates/market-trend-signals.py` | Python collector for macro series (FRED), US regulatory filings (Federal Register), and EU law (EUR-Lex) |
