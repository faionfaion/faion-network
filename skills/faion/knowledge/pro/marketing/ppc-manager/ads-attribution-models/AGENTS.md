# Ads Attribution Models

## Summary

Attribution models define how conversion credit is distributed across ad touchpoints in a customer journey. Each platform (Meta, Google, LinkedIn) claims its own conversions using different windows and logic, causing totals to exceed actual sales. Use GA4 as a unified source of truth and compare platform-reported, GA4-modeled, and warehouse-deduped numbers per channel. Flag variances above 15% before making budget decisions.

## Why

Platform over-attribution leads to misallocated budgets: channels appear more efficient than they are, spending increases on the wrong channels, and ROAS targets are met on paper while revenue stagnates. A warehouse-deduped view with a documented lookback window matched to the sales cycle is the only defensible basis for reallocation. Data-driven attribution (GA4) outperforms last-click for most journeys but requires at least 50 conversions/month per channel to train reliably.

## When To Use

- Multi-channel paid programs (2+ platforms) where platform totals do not match the warehouse
- Setting up GA4 or BigQuery export pipelines that produce reconciled CPA and ROAS per channel
- Designing and scheduling quarterly geo-holdout (incrementality) tests
- Auto-generating weekly variance reports (platform vs. GA4 vs. warehouse) for human review
- Budget reallocation reviews requiring a defensible model

## When NOT To Use

- Single-channel programs — use the platform default model; cross-channel attribution adds no signal
- Pre-revenue or fewer than 50 conversions/month — data is too sparse for any model to be reliable
- Optimizing inside a single platform (bids, ad copy) — use native attribution; switching models mid-flight confuses the bidding algorithm
- Tactical creative decisions — attribution informs strategy and budget, not which thumbnail to ship

## Content

| File | What's inside |
|------|---------------|
| `content/01-models.xml` | Attribution model types, platform defaults, lookback window guidelines, overlap problem |
| `content/02-strategy.xml` | Choosing a source of truth, configuration steps, incrementality testing, common mistakes |
| `content/03-agent-rules.xml` | Agent-specific rules: variance thresholds, human-in-loop checkpoints, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/attribution-analysis.md` | Weekly variance report: platform vs. GA4 vs. warehouse per channel |
| `templates/variance-check.py` | Python helper flagging platform/GA4/warehouse drift above 15% |
