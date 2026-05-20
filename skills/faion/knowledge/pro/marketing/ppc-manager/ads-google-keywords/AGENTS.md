---
slug: ads-google-keywords
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Targeting the right keywords is critical for profitable campaigns.
content_id: "81972e835246aebd"
tags: [google-ads, ppc, keywords, search, intent]
---
# Google Ads Keyword Strategy

## Summary

**One-sentence:** Targeting the right keywords is critical for profitable campaigns.

**One-paragraph:** Targeting the right keywords is critical for profitable campaigns. Broad keywords waste budget on irrelevant clicks; too narrow and you miss opportunities. The right strategy balances reach with relevance through intent-first keyword research, match type selection, ad group organization, negative list management, and continuous optimization.

## Applies If (ALL must hold)

- Building a new search campaign from scratch requiring seed keywords, expansion, clustering, and match type assignment.
- Weekly Search Terms Report mining to extract new negatives and identify new keyword themes.
- Migrating existing spend from broad-only to a phrase + exact + tight-negatives structure.
- Reorganizing overgrown accounts where single ad groups have 100+ mixed-intent keywords.
- Harvesting SEO keyword data and converting it to paid keyword plans.

## Skip If (ANY kills it)

- Performance Max campaigns—PMax does not expose individual keywords; use audience signals and asset groups instead.
- Smart campaigns—Google automatically selects keywords based on themes you provide.
- Display or YouTube campaigns—keyword hints on display are weak signals; topics and audiences dominate.
- Brand-only campaigns with a tight, converged keyword list—agent optimization loops add noise.

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

- parent skill: `pro/marketing/ppc-manager/`
