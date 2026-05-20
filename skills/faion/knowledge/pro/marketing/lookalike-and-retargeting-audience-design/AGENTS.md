---
slug: lookalike-and-retargeting-audience-design
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Seed-audience selection, exclusion logic, lookalike degree, audience-overlap auditing, frequency-cap discipline — audience design IS the paid-ads moat post-iOS17.
content_id: "112cf4c85eed69d1"
tags: [lookalike-and-retargeting-audience-design, marketing, pro]
---

# Lookalike and Retargeting Audience Design

## Summary

**One-sentence:** Seed-audience selection, exclusion logic, lookalike degree, audience-overlap auditing, frequency-cap discipline — audience design IS the paid-ads moat post-iOS17.

**One-paragraph:** ads-retargeting exists as one entry; no methodology for the audience-design layer. After 2024 cookie deprecation + iOS17, audience design IS the moat. Output: seed policy + exclusion rules + lookalike degree + overlap audit.

## Applies If (ALL must hold)

- active paid-ads spend ≥$1k/month
- first-party data (CRM, purchases, events) available
- marketing owner with authority to design + audit audiences

## Skip If (ANY kills it)

- <$500/month spend — over-engineered
- purely organic / SEO-only — no paid layer
- single-channel only with no audience overlap risk

## Prerequisites

- CRM with customer segments
- ad platform pixels / server-side events deployed
- conversion event(s) defined + reliable

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent skill — provides operating context for this methodology |
| `pro/marketing/ppc-manager` | peer methodology — produces inputs or consumes outputs |
| `pro/marketing/ads-retargeting` | peer methodology — produces inputs or consumes outputs |

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
- peer methodology: `pro/marketing/ppc-manager`
- peer methodology: `pro/marketing/ads-retargeting`
- peer methodology: `geek/ai/ai-product-marketing-patterns`
- external: https://www.facebook.com/business/news/changes-to-audience-network; https://developers.facebook.com/docs/marketing-api/audiences; https://www.thinkwithgoogle.com/marketing-strategies/audiences/
