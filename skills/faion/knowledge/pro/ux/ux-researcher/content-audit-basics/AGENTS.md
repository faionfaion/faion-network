---
slug: content-audit-basics
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A content audit is a systematic inventory and quality review of all content on a site or application.
content_id: "56a5fc1502da8898"
tags: [content, audit, inventory, quality, scoring]
---
# Content Audit Basics

## Summary

**One-sentence:** A content audit is a systematic inventory and quality review of all content on a site or application.

**One-paragraph:** A content audit is a systematic inventory and quality review of all content on a site or application. It catalogs what exists (URL, type, owner, date, analytics), evaluates each item against rubric criteria (accuracy, relevance, quality scored 1-5), and produces a keep/update/consolidate/remove action column. The basics methodology covers audit types, spreadsheet schema, evaluation criteria, and tooling.

## Applies If (ALL must hold)

- Pre-redesign or migration: build a complete URL inventory with quality scores before scope decisions.
- SEO/content strategy reset: combine crawl data + analytics + LLM quality scoring.
- Quarterly content governance: rolling audits of high-traffic clusters with freshness checks.
- Site consolidation (M&A, multi-brand merge): de-duplicate near-identical pages across domains.

## Skip If (ANY kills it)

- Site under ~50 pages — a manual spreadsheet review is faster than tooling setup.
- Greenfield (content does not yet exist) — use content modeling, not auditing.
- Analytics performance only — GA4/GSC views suffice; no inventory needed.
- Pre-launch QA of a single page batch — use editorial review instead.

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

- parent skill: `pro/ux/ux-researcher/`
