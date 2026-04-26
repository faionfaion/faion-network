# Product Development Trends (Market-Side Brief)

## Summary

A market-side trend brief that produces TAM/pricing/positioning implications from a scored signal set — distinct from the product-side sibling at researcher/product-development-trends. A three-stage pipeline (wide signal collection → scored synthesis → human checkpoint) writes a dated trend-report.md and a signals.jsonl audit trail so next-quarter runs diff rather than re-scrape.

## Why

"Trend" articles are written for SEO, not signal. LLM training data lags real markets by 6-18 months, so any unsourced trend claim is likely stale. A recency × evidence × applicability scoring rubric (0-3 each, threshold ≥5) filters noise before paying for Opus synthesis, and forces the deliverable to carry market implications (TAM shift, pricing power, positioning) rather than duplicating product-roadmap advice.

## When To Use

- Quarterly market-trend refresh feeding GTM positioning, pricing tier design, or category framing.
- Pre-investment decision: separating hype from durable adoption before budget is committed.
- When competitive intel uncovers a methodology shift and you need to decide whether to follow or counter-position.
- Annual board memo where the market lens (TAM expansion, sub-segment emergence, pricing-power shifts) is the deliverable.
- Inside faion-research-agent mode=market when the team explicitly asks for a "what's changing" overlay.

## When NOT To Use

- Product roadmap or sprint planning — use researcher/product-development-trends or pm-agile.
- Pure pricing benchmark — use market-researcher/pricing-research.
- Single-feature validation — use user-researcher/problem-validation or continuous-discovery.
- Competitive tear-down of one named rival — use competitor-analysis and competitive-intelligence.
- Less than 90 days since the last trends pass with no triggering event (funding round, regulatory shift, major launch).

## Content

| File | What's inside |
|------|---------------|
| `content/01-pipeline-and-scoring.xml` | Three-stage pipeline, signal JSONL schema, recency/evidence/applicability scoring rubric, market-implication output format |
| `content/02-rules-and-gotchas.xml` | Source-freshness rule, US-bias guard, kill-list requirement, consumer vs platform trend separation, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/signal-scorer.py` | Score signals.jsonl on recency/evidence/applicability, drop below threshold, render markdown table |
| `templates/trend-report.md` | Trend report skeleton with market implications per bucket, kill-list, sourced consumer vs platform separation |
