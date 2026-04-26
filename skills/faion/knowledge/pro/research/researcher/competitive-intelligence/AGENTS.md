# Competitive Intelligence

## Summary

Continuous monitoring of competitor signals — pricing, features, hiring, funding, reviews, content — collected and synthesized into digests, threat assessments, and auto-generated battlecards. Replaces point-in-time snapshots with a live delta pipeline driven by specialized subagents.

## Why

Point-in-time competitor snapshots go stale within weeks. Continuous CI pipelines that separate mechanical collection (Haiku) from strategic synthesis (Opus) achieve 85-95% time reduction and measurably improve sales win rates. Battlecards older than 14 days with confident tone are worse than no battlecard.

## When To Use

- Live B2B/SaaS market where competitors ship weekly and pricing changes often.
- Sales team needs current battlecards (deal cycle > 30 days exposes stale data fast).
- Product roadmap decisions blocked on feature parity or differentiation gaps.
- Funding round, M&A, or executive hire signals need to surface within 24h.
- You have 3+ named direct competitors with stable public URLs.

## When NOT To Use

- Pre-PMF or category-creation phase — customer interviews beat CI here.
- Fewer than 5 known competitors — manual quarterly snapshot beats pipeline overhead.
- Highly regulated/closed markets (defense, sealed bids) where public signals are noise.
- When the team will not act on alerts — CI without a sales/product action loop is theater.

## Content

| File | What's inside |
|------|---------------|
| `content/01-monitoring-framework.xml` | Signal sources, frequencies, platform comparison, CI evolution 2025-2026. |
| `content/02-agentic-pipeline.xml` | Subagent roles, prompt patterns, fact-checker pass, gotchas. |
| `content/03-tools-and-services.xml` | CLI tools table, services table, best practices, limitations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-collector.py` | Minimal collector loop: fetches watchlist URLs via Jina reader, emits delta events to NDJSON. |
| `templates/watchlist.yaml` | Input config for ci-collector: competitor name, URLs, signal type. |

## Scripts

none
