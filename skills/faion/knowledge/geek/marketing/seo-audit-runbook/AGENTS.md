---
slug: seo-audit-runbook
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "Step-by-step annual SEO audit runbook covering crawl, on-page, off-page, content decay, and tech-SEO with the tool inventory (GSC + Screaming Frog + Ahrefs alternatives)."
content_id: "b3bcc549ae31b13c"
tags: [seo-audit-runbook, marketing, geek]
---
# SEO Audit Runbook

## Summary

**One-sentence:** A step-by-step audit runbook a single operator can execute over a defined window using a fixed tool inventory, producing a ranked findings backlog.

**One-paragraph:** Audit-level guidance is implicit across `seo-techniques`, `topical-authority`, and `on-page-seo-checklist-2026`, but no methodology orchestrates them into an audit pass. A new operator has to assemble the workflow from scratch every year. This runbook fixes that with a six-phase sequence (crawl → on-page → content-decay → links → tech-SEO → reporting), the canonical tool list (Google Search Console, Screaming Frog, Ahrefs OR SEMrush OR open-source alternatives like Sitebulb / Lumar), and a ranked-by-impact findings backlog template. Output is a Notion/markdown audit report keyed to GSC click data so the team can prioritize fix work.

## Applies If (ALL must hold)

- the site has ≥ 12 months of GSC data
- you (or the team) own at least one of: Ahrefs / SEMrush / Sitebulb / Lumar / a comparable crawler
- the audit window is bounded (annual refresh, post-migration, post-redesign)
- tier == geek

## Skip If (ANY kills it)

- the site has fewer than 50 indexed URLs (use `on-page-seo-checklist-2026` instead)
- a recent audit (< 6 months) already exists and the site has not materially changed
- the audit is for a single landing page (use `on-page-seo-checklist-2026`)

## Prerequisites

- GSC verified property with 12-month export rights
- crawler license OR open-source alternative installed
- backlink data source (Ahrefs / SEMrush / Majestic)
- write access to the audit report destination

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/seo-manager` | parent role context |
| `solo/marketing/internal-linking-strategy-graph` | consumer of audit findings on internal links |
| `solo/marketing/on-page-seo-checklist-2026` | drilldown for per-page issues |
| `solo/marketing/search-intent-to-brief` | drilldown for content-gap findings |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable audit-phase rules + tool inventory + 1 worked finding example | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `crawl_diff_against_last` | haiku | structured set-diff of URL inventory |
| `extract_decay_candidates` | sonnet | per-URL impressions/clicks YoY analysis |
| `rank_findings_by_impact` | sonnet | bounded scoring against traffic + intent value |
| `synthesize_executive_summary` | opus | cross-phase narrative |

## Related

- parent skill: `geek/marketing/`
- `geek/marketing/seo-manager`
- `solo/marketing/on-page-seo-checklist-2026`
- upstream playbook: `role-growth-marketing/Annual SEO Audit & Refresh (6 weeks)`
