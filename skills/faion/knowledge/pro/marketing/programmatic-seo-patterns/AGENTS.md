---
slug: programmatic-seo-patterns
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Template-driven pages backed by structured data: comparison pages, tool listings, location pages — the dominant SaaS growth lever Faion has zero coverage of.
content_id: "369698d7b2d9665d"
tags: [programmatic-seo-patterns, marketing, pro]
---

# Programmatic SEO Patterns

## Summary

**One-sentence:** Template-driven pages backed by structured data: comparison pages, tool listings, location pages — the dominant SaaS growth lever Faion has zero coverage of.

**One-paragraph:** Programmatic SEO is the dominant growth lever for SaaS in 2026 (Webflow, Tinybird, Levels.fyi, Clay, Apollo). Faion has zero coverage. Output: data source plan + template + indexability rules + thin-content guards + intent-coverage matrix.

## Applies If (ALL must hold)

- SaaS / product with broad audience + structured data domain
- marketing capacity to build templates + maintain data pipeline
- competitive SEO landscape where long-tail wins

## Skip If (ANY kills it)

- narrow B2B with no template-able pages
- regulated content (medical, financial) where each page needs review
- no structured data source (cannot template)

## Prerequisites

- data source (DB, API, third-party feed) for the corpus
- CMS or static-site builder capable of templated generation
- Google Search Console + analytics access

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/topic-cluster-architecture-with-eeat` | peer methodology — produces inputs or consumes outputs |
| `solo/marketing/seo-manager` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- peer methodology: `pro/marketing/topic-cluster-architecture-with-eeat`
- peer methodology: `solo/marketing/seo-manager`
- peer methodology: `pro/marketing/growth-marketer`
- external: https://www.searchengineland.com/programmatic-seo-guide-411111; https://www.tinybird.co/blog/programmatic-seo (Tinybird case study)
