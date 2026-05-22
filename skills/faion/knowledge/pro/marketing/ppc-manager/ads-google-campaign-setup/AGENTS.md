---
slug: ads-google-campaign-setup
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured process for creating Google Ads Search campaigns via the API: conversion tracking first, then campaign with PAUSED status, ad groups by theme, Responsive Search Ads (RSA), and extensions.
content_id: "eade5f4484c75a19"
tags: [campaign-setup, google-ads-api, search-campaigns, responsive-search-ads, api-automation]
---
# Google Ads Campaign Setup

## Summary

**One-sentence:** Structured process for creating Google Ads Search campaigns via the API: conversion tracking first, then campaign with PAUSED status, ad groups by theme, Responsive Search Ads (RSA), and extensions.

**One-paragraph:** Structured process for creating Google Ads Search campaigns via the API: conversion tracking first, then campaign with PAUSED status, ad groups by theme, Responsive Search Ads (RSA), and extensions. Default network settings must explicitly disable Display and Search Partners — the API does not match the UI defaults. Never flip status to ENABLED without verified conversion tracking firing in the last 24 hours and at least one RSA per ad group.

## Applies If (ALL must hold)

- Templating new Google Ads accounts: agent provisions a Search campaign with conversion tracking, RSAs, extensions, and naming convention enforced
- Onboarding agency or multi-tenant clients where the same campaign skeleton repeats across many accounts
- Pre-launch QA: agent walks the launch checklist and refuses to enable until every item passes
- Migrating manual campaigns to Smart Bidding by templating fresh campaigns with historical conversions

## Skip If (ANY kills it)

- One-off campaigns launched in the UI in under 20 minutes — API setup overhead does not pay back
- Campaigns using UI-only features (some recommendations, brand-suitability tweaks, certain PMax settings)
- Heavily creative-led campaigns where asset variation is the primary work
- Already-running accounts with established Smart Bidding — re-templating restarts learning

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
