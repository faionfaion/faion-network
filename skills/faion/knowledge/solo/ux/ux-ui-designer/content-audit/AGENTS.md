---
slug: content-audit
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A content audit is a systematic review of all content on a website or application — cataloging what exists, evaluating quality (accuracy, relevance, quality on a 1-5 scale), and deciding Keep / Update / Rewrite / Remove per item.
content_id: "1d856a6ef6da43a8"
tags: [content-strategy, audit, inventory, seo, governance]
---
# Content Audit

## Summary

**One-sentence:** A content audit is a systematic review of all content on a website or application — cataloging what exists, evaluating quality (accuracy, relevance, quality on a 1-5 scale), and deciding Keep / Update / Rewrite / Remove per item.

**One-paragraph:** A content audit is a systematic review of all content on a website or application — cataloging what exists, evaluating quality (accuracy, relevance, quality on a 1-5 scale), and deciding Keep / Update / Rewrite / Remove per item. Average score >= 4.0 → Keep; 3.0-3.9 → Update; 2.0-2.9 → Rewrite; < 2.0 → Remove.

## Applies If (ALL must hold)

- Before a website redesign — establish full inventory before structural changes
- Before a CMS migration — map old URLs to keep/redirect/remove decisions
- SEO improvement sprints — combine crawl data with analytics to prune low-value pages
- Rolling content governance — quarterly review of core pages, bi-annual for blog
- Scoring content quality at scale when 50+ pages need evaluation

## Skip If (ANY kills it)

- New sites with under 50 pages — a spreadsheet and manual review is faster
- When the primary goal is IA redesign — audit catalogs content, not structure (use card sorting)
- Highly regulated content (medical, legal) where agent quality judgments must not replace subject-matter expert review
- When analytics access is unavailable — remove/keep decisions without traffic data produce low-value output

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

- parent skill: `solo/ux/ux-ui-designer/`
