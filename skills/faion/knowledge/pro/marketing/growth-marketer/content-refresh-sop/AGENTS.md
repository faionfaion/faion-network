---
slug: content-refresh-sop
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Refresh-or-kill decision flow + execution checklist for evergreen content that has decayed in traffic, rank, or conversion.
content_id: "4f6866cd3ee67f91"
tags: [marketing, seo, content-refresh, evergreen, decay, e-e-a-t]
---

# Content Refresh SOP

## Summary

**One-sentence:** Standard operating procedure that scores each evergreen URL on a refresh-vs-kill-vs-leave matrix and runs the refresh through a fixed 9-step execution checklist.

**One-paragraph:** Replaces ad-hoc "refresh that old post" growth work with a repeatable decision flow. Mechanism: pull GSC + GA4 + rank-tracker data for URLs older than 12 months, classify each into refresh / consolidate / kill / leave based on impressions trend, top-position decay, intent shift, and conversion contribution, then execute the chosen path through a fixed checklist (title, intro, primary claim, evidence, schema, internal links, image alt, last-updated, redirect-or-noindex). Primary output: refreshed URL with documented before/after metrics + a 90-day re-evaluation date.

## Applies If (ALL must hold)

- url_age_months >= 12
- primary keyword has clicks_last_90d > 0 OR rank_position_last_90d <= 30
- domain has Google Search Console + GA4 access
- content is evergreen (not news, not event-tied)

## Skip If (ANY kills it)

- url is news / time-bound — refresh wastes effort; archive or noindex instead
- url_age_months < 6 — too young to refresh; wait for at least one stable ranking cycle
- the SERP intent shifted to a different format (video, tool, map) — refresh will not win; build a new asset
- the URL targets a keyword you no longer rank for at all AND have zero topical authority — kill, do not refresh

## Prerequisites

- 90-day GSC export (page-level: impressions, clicks, CTR, avg position)
- 90-day GA4 export (sessions, engaged sessions, conversions per URL)
- rank tracker history (12 months minimum) for the URL's target keyword cluster
- original publish date + last-substantive-update date per URL

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/seo-audit-quarterly` | Refresh SOP consumes URL inventory + decay flags from the audit, not from scratch crawl |
| `pro/marketing/growth-marketer/topical-authority-cluster` | Refresh decisions consider whether URL is pillar / cluster / orphan; signal comes from this methodology |
| `free/marketing/marketing-manager/e-e-a-t-signals` | Refresh must restore E-E-A-T evidence (author, citations, dates); base rules come from this |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: decay-evidence threshold, intent-shift kill, last-updated honesty, evidence-replacement before prose-rewrite, redirect-vs-noindex disambiguation | ~900 |
| `content/02-output-contract.xml` | essential | Refresh-decision schema + 9-step checklist contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 LLM-specific failure modes (date lying, cosmetic rewrite, citation hallucination, cannibalization, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decay_signal_collation` | haiku | Mechanical join of GSC + GA4 + rank data per URL |
| `refresh_vs_kill_decision` | sonnet | Bounded judgment per URL against the matrix |
| `checklist_execution_per_url` | sonnet | Fill 9 fixed checklist items, requires evidence checking |
| `cluster_cannibalization_check` | opus | Cross-URL synthesis — needs full topical cluster context |

## Templates

| File | Purpose |
|------|---------|
| `templates/refresh-decision.json` | JSON Schema for the per-URL decision record |
| `templates/refresh-checklist.md` | 9-step execution checklist with evidence fields |
| `templates/refresh-log.csv` | Before/after metrics log (one row per refreshed URL) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-decay.py` | Joins GSC + GA4 + rank exports, returns decay-score per URL | Before the refresh-vs-kill decision |
| `scripts/validate-refresh-output.py` | Validates that refreshed URL meets output-contract (last-updated honest, citations resolved, no cannibal anchors) | Before publishing the refreshed URL |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodologies: `seo-audit-quarterly`, `topical-authority-cluster`, `internal-linking-strategy`
- external: [Google Search Central — Freshness](https://developers.google.com/search/blog/2011/11/giving-you-fresher-more-recent-search) · [Ahrefs Content Decay](https://ahrefs.com/blog/content-decay/) · [Animalz Content Decay Study](https://www.animalz.co/blog/content-decay/)
