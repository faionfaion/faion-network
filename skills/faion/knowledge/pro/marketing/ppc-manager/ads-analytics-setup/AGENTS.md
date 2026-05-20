---
slug: ads-analytics-setup
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three-layer analytics implementation — Collect, Analyze, Attribute — covering GA4 property creation, event tracking plan, conversion designation, UTM naming conventions, and dashboard setup.
content_id: "901d45e5c073b6e7"
tags: [analytics, ga4, tracking, conversion, utm]
---
# Analytics Setup

## Summary

**One-sentence:** Three-layer analytics implementation — Collect, Analyze, Attribute — covering GA4 property creation, event tracking plan, conversion designation, UTM naming conventions, and dashboard setup.

**One-paragraph:** Three-layer analytics implementation — Collect, Analyze, Attribute — covering GA4 property creation, event tracking plan, conversion designation, UTM naming conventions, and dashboard setup. Define the event spec before writing any tracking code. Implement Consent Mode v2 from day one. Link GA4 to Google Ads, BigQuery, and Search Console immediately after property creation to unlock features without future migration work.

## Applies If (ALL must hold)

- New site or app launch needing GA4 and ad-platform pixels installed correctly from day one
- Migration from Universal Analytics to GA4 (UA sunset 2023; validate event mapping)
- Multi-channel attribution rebuild: UTM standards, dataLayer schema, conversion definitions
- E-commerce or SaaS rolling out enhanced ecommerce or product analytics
- Compliance refit (Consent Mode v2, GDPR/CCPA banners, server-side tagging migration)

## Skip If (ANY kills it)

- Sites with a working analytics stack and consistent UTM data — focus on optimization, not reinstall
- Pure backend or API-only products with no front-end — use server-side analytics (PostHog Backend)
- Privacy-first or low-traffic projects where Plausible or Fathom suffices
- One-page marketing sites — Plausible/Fathom plus UTM macros is sufficient

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
