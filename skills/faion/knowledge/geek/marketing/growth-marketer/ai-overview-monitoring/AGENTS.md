---
slug: ai-overview-monitoring
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3946b3f6b9dc3779"
summary: A documented monitoring approach for AI Overview presence, Perplexity citation, and ChatGPT-Search visibility — weekly cadence, citation counts per query, and an action ladder when presence drops.
tags: [aio, monitoring, seo, perplexity, chatgpt-search, marketing, geek]
---
# AI Overview Monitoring

## Summary

**One-sentence:** A weekly monitoring cadence for AI Overview (Google AIO), Perplexity, and ChatGPT-Search citation presence across the marketer's priority query list — with a documented action ladder when presence drops.

**One-paragraph:** Optimization without monitoring is theatre. This methodology defines the monitoring stack: a query list (priority + watch), three citation sources (AIO, Perplexity, ChatGPT-Search), a weekly cadence, a per-query record (cited / not_cited / partial), and an action ladder that fires when a query falls off citation. Output: a `aio-monitoring/` folder with weekly snapshots, a trends report, and a per-query investigation log that feeds back into content edits via the sibling `ai-overview-content-template`. This is the "is our optimization working" feedback loop for 2026 search reality.

## Applies If (ALL must hold)

- Marketer has 10+ priority queries with measurable AIO / Perplexity presence.
- Content cluster has been retrofit per `ai-overview-content-template` for at least 30 days.
- A monitoring stack (manual, BrightEdge, sistrix, custom Playwright scraper, or commercial AIO tracker) is reachable.
- Team can act on monitoring findings (rewrite sections, re-publish, update citations).

## Skip If (ANY kills it)

- Priority list has &lt; 5 queries — monitoring overhead exceeds the signal.
- Niche has zero AIO / Perplexity coverage in your geography — monitor coverage, not presence.
- Monitoring stack is unreliable (results vary &gt; 50% week-over-week without content changes) — fix the stack first.
- Team cannot act on findings — monitor is wasted; defer.

## Prerequisites

- Priority + watch query lists in `aio-monitoring/queries.yaml`.
- Citation-source adapters: `google-aio-fetch.py`, `perplexity-fetch.py`, `chatgpt-search-fetch.py` (or commercial-tool integration).
- Storage of weekly snapshots (Git or DB) for trend analysis.
- A defined action ladder (which findings trigger what action).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/growth-marketer/ai-overview-presence-tracker` | Sibling — operational tracker; this methodology covers cadence and decision-making. |
| `geek/marketing/growth-marketer/ai-overview-content-template` | Sibling — content retrofit feeds the monitor. |
| `geek/marketing/growth-marketer/ai-overview-risk-scoring` | Sibling — risk scoring informs which queries to monitor closely vs hedge. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: weekly cadence, three sources required, snapshot immutability, action-ladder discipline, human review | ~1100 |
| `content/02-output-contract.xml` | essential | Weekly snapshot schema, trend report, action-log shape | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: scraper drift, source-coverage gap, action-fatigue | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scrape-aio-perplexity-chatgpt` | haiku | Mechanical: HTTP + parse |
| `classify-citation-status` | sonnet | Bounded judgement: cited / partial / not_cited |
| `trend-narrative` | sonnet | Bounded synthesis: week-over-week changes |
| `action-ladder-decide` | sonnet | Bounded: map drop to action (rewrite, citation update, abandon) |

## Templates

| File | Purpose |
|------|---------|
| `templates/queries.yaml` | Priority + watch query lists |
| `templates/weekly-snapshot.json` | Per-query citation status across the three sources |
| `templates/action-ladder.md` | Documented action mapping for each finding type |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/run-monitor.sh` | Run all three source fetches; write weekly-snapshot.json | Weekly cron |
| `scripts/trend-report.py` | 4-week trend report; emit per-query deltas | Weekly post-snapshot |
| `scripts/action-router.py` | Read trend report; emit suggested actions from the ladder | Weekly post-trend |

## Related

- parent skill: `geek/marketing/growth-marketer/`
- peer methodologies: `ai-overview-presence-tracker`, `ai-overview-content-template`, `ai-overview-risk-scoring`, `google-ai-overviews-optimization`
- external: [SISTRIX AIO data](https://www.sistrix.com/) · [Sparktoro 2025 AIO study](https://sparktoro.com/) · [Perplexity citation guidelines](https://www.perplexity.ai/hub)
