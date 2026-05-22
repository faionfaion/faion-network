---
slug: competitor-tracker-template
tier: solo
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Lightweight monthly competitor-matrix tooling plus a stable weekly scan schema (channels watched, last delta, action queued) so competitor signal does not devolve into noise.
content_id: "f1a84647b4450db5"
tags: [research, competitor-analysis, market-monitoring, solo, serp, productivity]
---

# Competitor Tracker Template (Solo)

## Summary

**One-sentence:** A lightweight monthly competitor matrix (5-7 competitors, 6-8 attributes) plus a weekly 45-min scan with a stable schema (channels watched, last delta, action queued) that keeps solo competitor research signal-rich without becoming noise.

**One-paragraph:** Solo SaaS builders need awareness of competitive moves but cannot run enterprise-grade analyst processes. Mechanism: pick 5-7 competitors max, define 6-8 attribute columns once (positioning, pricing, target ICP, primary channel, last-shipped-feature, recent-content-themes, customer-evidence), build the matrix once, then run a 45-min weekly scan with a fixed channel checklist that produces a delta-list and action-queue. Primary output: a versioned competitor matrix + a weekly delta journal that feeds product / marketing decisions without becoming busywork.

## Applies If (ALL must hold)

- founder operates in a market with >= 3 identifiable direct competitors (same ICP + same job-to-be-done)
- founder is the constraint on competitor research time (solo or 2-person team)
- competitor moves have influenced at least one product / pricing / positioning decision in the last 6 months
- founder is willing to commit 45 min/week to the scan (anything more is too much for solo)

## Skip If (ANY kills it)

- pre-launch product with no defined ICP — competitor research is premature; do JTBD / problem validation first
- pure infrastructure / API tool with no consumer-facing competitive landscape
- founder treats competitor research as procrastination (low-value-but-feels-productive) — break the habit with a hard time-box, not better tooling
- market is so niche that competitors are non-comparable (custom enterprise) — use win/loss interviews instead

## Prerequisites

- ICP defined enough to identify "competitors of the SAME ICP" (not generic "everyone with similar product")
- list of 5-7 named competitors with primary URL + ICP statement per competitor
- weekly 45-min calendar block agreed (the time itself is the budget)
- one persistent file location (Notion DB, Airtable, repo /research/competitors) where the matrix lives

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/niche-evaluation` | ICP definition feeds competitor-set scope; competitors must share ICP |
| `solo/marketing/seo-manager/serp-monitoring` | Weekly scan reuses SERP-monitoring patterns at a lower frequency / scope |
| `pro/research/market-researcher/competitive-positioning-map` | Pro-tier deep-dive; this methodology is the solo-cadenced subset |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 5-7-competitor-cap, stable-schema, 45-min-time-box, delta-with-action-or-explicit-noop, monthly-prune | ~900 |
| `content/02-output-contract.xml` | essential | Matrix schema + weekly delta journal contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (matrix-bloat, scan-skip, delta-without-action, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `weekly_scan_collation` | sonnet | Aggregate channel signals (changelog, blog, pricing page, social, hiring) per competitor |
| `delta_categorization` | sonnet | Classify changes (feature shipped, price moved, content theme, ICP shift) |
| `action_queue_proposal` | sonnet | For each delta, propose a concrete action OR explicit no-op with reason |
| `monthly_matrix_refresh` | opus | Cross-competitor synthesis; matrix attributes may shift over time |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-matrix.csv` | 5-7 competitors x 6-8 attributes matrix |
| `templates/weekly-delta-journal.md` | Per-week journal entry template |
| `templates/channel-checklist.md` | Channels to scan per competitor (changelog / blog / pricing / social / hiring / G2 reviews) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/fetch-competitor-pages.py` | Pulls public pages (changelog, pricing, blog) with last-modified headers | Weekly scan input |
| `scripts/audit-action-queue.py` | Counts delta entries with action-queued vs explicit-no-op; flags chronic gap | Monthly |

## Related

- parent skill: `solo/research/researcher/`
- peer methodologies: `niche-evaluation`, `customer-evidence-collection`, `pricing-research`
- external: [Crayon Competitive Intelligence](https://www.crayon.co/playbook) · [Klue CI Methodology](https://klue.com/blog/) · [April Dunford — Obviously Awesome (positioning)](https://www.aprildunford.com/)
