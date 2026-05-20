---
slug: ai-overview-presence-tracker
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e74d43f2b3b57a10"
summary: A recurring measurement of AI Overview presence per priority query so that AIO optimization tactics become testable rather than aspirational.
tags: [aio, tracker, seo, growth, marketing, pro]
---
# AI Overview Presence Tracker

## Summary

**One-sentence:** A recurring measurement of AI Overview (AIO) presence per priority query — does the panel surface, who gets cited, what snippet is selected — so AIO optimization tactics become testable rather than aspirational.

**One-paragraph:** Existing methodologies tell growth marketers to "optimize for AI Overviews", but no tracker exists in the pro tier to measure whether the optimization is working. This methodology defines a minimal but rigorous tracker: a query list (priority + watch + control), a per-query record (aio_present, aio_first_citation, our_domain_cited, our_snippet_selected, panel_position), a daily / weekly scrape cadence with a documented adapter, and a per-query 8-week trend view. Output: a `aio-presence/` folder that the team reads in the weekly Search Console + analytics review to decide where to invest more retrofit effort and where to deprioritize.

## Applies If (ALL must hold)

- Growth marketer has &gt;= 20 indexed pages targeting queries with measurable AIO presence in your geography.
- A weekly Search Console + analytics review is the team's existing cadence.
- An adapter for AIO scraping is available (Playwright + Google AI Overview SERP, third-party tool, or commercial tracker).
- Team can change publish strategy based on tracker signals.

## Skip If (ANY kills it)

- Niche has no AIO coverage in target geography — track manually, do not invest in scraper.
- Team uses the geek-tier `ai-overview-monitoring` methodology — that supersedes this one for AIO + Perplexity + ChatGPT.
- Priority list &lt; 10 queries — tracker overhead exceeds the signal.
- AIO is being de-emphasized by Google in your niche (announced rollback) — defer.

## Prerequisites

- `queries.yaml` with priority + watch + control lists.
- Playwright + headless Chrome installed in CI OR a commercial AIO tracking subscription.
- A control list of queries with stable behaviour (used to detect scraper drift).
- A weekly review meeting where the report is read.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/weekly-search-console-review` (or equivalent) | The tracker plugs into the weekly review cadence. |
| `geek/marketing/seo-manager/google-ai-overviews-optimization` | Strategic methodology this tracker measures. |
| `geek/marketing/growth-marketer/ai-overview-monitoring` | Geek-tier upgrade — extends to Perplexity / ChatGPT. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: control-list discipline, snapshot immutability, position-record, our-domain-cited as primary KPI, weekly cadence | ~1100 |
| `content/02-output-contract.xml` | essential | Snapshot schema, trend record, KPI definitions | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: scraper drift, geo bias, panel-personalisation | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scrape-aio-panel` | haiku | Mechanical: headless render + parse |
| `classify-citation` | sonnet | Bounded: was our domain cited? at what panel position? |
| `weekly-narrative` | sonnet | Bounded synthesis of deltas |

## Templates

| File | Purpose |
|------|---------|
| `templates/queries.yaml` | Priority + watch + control query lists |
| `templates/snapshot.json` | Per-query snapshot record |
| `templates/weekly-trend.md` | Markdown report format read in the weekly review |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scrape.py` | Run Playwright fetch; emit snapshots | Daily cron |
| `scripts/weekly-aggregate.py` | 7-day rollup; emit weekly-trend.md | Weekly |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodologies: `ai-overview-monitoring`, `ai-overview-content-template`, `ai-overview-risk-scoring`
- external: [Google Search Status Dashboard](https://status.search.google.com/) · [Playwright headless](https://playwright.dev/) · [SISTRIX AIO tracker](https://www.sistrix.com/)
