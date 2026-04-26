# Perplexity AI for Research

## Summary

Decompose a research question into 3-5 targeted Perplexity sub-queries, dispatch
each via the Perplexity REST API with explicit search_recency_filter, collect cited
results, de-duplicate sources, and consolidate into a markdown synthesis with a
source registry. Never query the full question at once — narrow sub-queries produce
better coverage and citation quality.

## Why

Perplexity returns citations inline alongside synthesized answers, saving a separate
synthesis step needed when using general-purpose LLMs. With 780 million search
queries/month (May 2025) and 45 million active users, the API is production-ready.
The key gotcha is that Pro Search (web UI) does not exist in the API; use
sonar-large with search_recency_filter as the equivalent.

## When To Use

- Fast, cited multi-source synthesis where manual source collection would take hours
- Market sizing queries needing recent (under 6 months) data with traceable URLs
- Competitive landscape sweeps producing a first-pass list of players and funding events
- Trend research where breadth matters more than depth in the first pass
- Validating or cross-checking a specific claim with multiple independent sources

## When NOT To Use

- Deep primary-source research — Perplexity aggregates web content, not proprietary data
- When citations must be peer-reviewed or from specific databases (PubMed, SSRN, SEC EDGAR)
- Real-time streaming data (stock prices, live social signals) — Perplexity crawls on delay
- Tasks where context must persist across multiple sessions — Perplexity has no persistent memory
- When the research question is too ambiguous — vague queries produce authoritative-sounding but unreliable results

## Content

| File | What's inside |
|------|---------------|
| `content/01-query-strategy.xml` | Sub-query decomposition rules, recency filter, source validation |
| `content/02-agentic-patterns.xml` | API dispatcher, parallel sub-queries, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/perplexity-dispatcher.py` | Sync and async Perplexity API dispatchers |
| `templates/perplexity-prompt.txt` | XML prompt template for query decomposition |
