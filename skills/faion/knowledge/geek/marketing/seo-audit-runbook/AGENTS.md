---
slug: seo-audit-runbook
tier: geek
group: marketing
domain: marketing
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Six-phase annual SEO audit runbook (crawl, on-page, content-decay, links, tech-SEO, reporting) emitting a ranked findings backlog keyed to GSC click data."
content_id: "b3bcc549ae31b13c"
complexity: deep
produces: report
est_tokens: 2900
tags: [seo, audit, runbook, content-decay, links, marketing, geek]
---

# SEO Audit Runbook

## Summary

**One-sentence:** Six-phase annual SEO audit runbook (crawl, on-page, content-decay, links, tech-SEO, reporting) emitting a ranked findings backlog keyed to GSC click data.

**One-paragraph:** Audit-level guidance is implicit across `seo-techniques`, `topical-authority`, and `on-page-seo-checklist-2026`, but no methodology orchestrates them into a single annual audit pass. This runbook fixes that with a six-phase sequence, the canonical tool list (GSC, Screaming Frog / Sitebulb / Lumar, Ahrefs OR SEMrush OR open-source alternatives), and a ranked-by-impact findings backlog template. Output is a markdown audit report with executive summary, ranked findings, and a 30/60-day sequencing plan.

**Ефективно для:** in-house SEOs running annual or post-migration audits; growth teams preparing executive briefings; agencies delivering quarterly audits.

## Applies If (ALL must hold)

- Site has ≥12 months of GSC data
- Team owns at least one of: Ahrefs / SEMrush / Sitebulb / Lumar / comparable crawler
- Audit window is bounded (annual refresh, post-migration, post-redesign)
- Stakeholder or finance review will receive the report

## Skip If (ANY kills it)

- Site has <50 indexed URLs — use `on-page-seo-checklist-2026` instead
- Recent audit (<6 months) exists and site has not materially changed
- Audit is for a single landing page — use `on-page-seo-checklist-2026`

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| GSC verified property with 12-month export rights | GSC export | Search Console |
| Crawler license OR open-source alternative installed | Tool path | ops |
| Backlink data source (Ahrefs / SEMrush / Majestic) | API or export | vendor |
| Write access to the audit report destination (Notion / repo) | Auth | team workspace |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/seo-manager` | parent role context |
| `solo/marketing/on-page-seo-checklist-2026` | drilldown for per-page issues |
| `solo/marketing/internal-linking-strategy-graph` | consumer of audit findings on internal links |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `crawl_diff_against_last` | haiku | Structured set-diff of URL inventory |
| `extract_decay_candidates` | sonnet | Per-URL impressions/clicks YoY analysis |
| `rank_findings_by_impact` | sonnet | Bounded scoring against traffic + intent value |
| `synthesize_executive_summary` | opus | Cross-phase narrative |

## Templates

| File | Purpose |
|------|---------|
| `templates/seo-audit-runbook.md` | Audit report skeleton with six-phase sections + executive summary |
| `templates/findings-backlog.csv` | CSV template for the ranked findings backlog |
| `templates/_smoke-test.md` | Minimum-viable filled audit report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-seo-audit-runbook.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- `geek/marketing/seo-manager`
- [[google-ai-overviews-optimization]]
- `solo/marketing/on-page-seo-checklist-2026`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether seo-audit-runbook applies: root question — "Is the site ≥12 months old with GSC export rights AND a bounded audit window?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-crawl-phase, r2-on-page-phase, r3-content-decay-phase, r4-links-phase, r5-tech-seo-phase, r6-report-phase.
