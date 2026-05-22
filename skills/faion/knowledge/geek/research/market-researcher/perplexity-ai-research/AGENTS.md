---
slug: perplexity-ai-research
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Decompose a research question into 3-5 targeted Perplexity sub-queries, dispatch each via the Perplexity REST API with explicit search_recency_filter, collect cited results, de-duplicate sources, and consolidate into a markdown synthesis with a source registry.
content_id: "dc8d19cecf63327c"
tags: [perplexity, research, api, market-sizing, citations]
---
# Perplexity AI for Research

## Summary

**One-sentence:** Decompose a research question into 3-5 targeted Perplexity sub-queries, dispatch each via the Perplexity REST API with explicit search_recency_filter, collect cited results, de-duplicate sources, and consolidate into a markdown synthesis with a source registry.

**One-paragraph:** Decompose a research question into 3-5 targeted Perplexity sub-queries, dispatch each via the Perplexity REST API with explicit search_recency_filter, collect cited results, de-duplicate sources, and consolidate into a markdown synthesis with a source registry. Never query the full question at once — narrow sub-queries produce better coverage and citation quality.

## Applies If (ALL must hold)

- Fast, cited multi-source synthesis where manual source collection would take hours
- Market sizing queries needing recent (under 6 months) data with traceable URLs
- Competitive landscape sweeps producing a first-pass list of players and funding events
- Trend research where breadth matters more than depth in the first pass
- Validating or cross-checking a specific claim with multiple independent sources

## Skip If (ANY kills it)

- Deep primary-source research — Perplexity aggregates web content, not proprietary data
- When citations must be peer-reviewed or from specific databases (PubMed, SSRN, SEC EDGAR)
- Real-time streaming data (stock prices, live social signals) — Perplexity crawls on delay
- Tasks where context must persist across multiple sessions — Perplexity has no persistent memory
- When the research question is too ambiguous — vague queries produce authoritative-sounding but unreliable results

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

- parent skill: `geek/research/market-researcher/`
