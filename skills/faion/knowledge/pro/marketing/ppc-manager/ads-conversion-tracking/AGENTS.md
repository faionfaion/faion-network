---
slug: ads-conversion-tracking
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Multi-platform conversion tracking setup: define macro and micro conversion events with dollar values, install browser-side pixels (Meta Pixel, Google Tag, LinkedIn Insight Tag), implement server-side APIs (Meta CAPI, Google Ads offline upload), verify all events fire correctly, and configure attribution windows.
content_id: "146d8c830568701f"
tags: [conversion-tracking, pixel-implementation, event-setup, platform-pixels, capi]
---
# Ads Conversion Tracking

## Summary

**One-sentence:** Multi-platform conversion tracking setup: define macro and micro conversion events with dollar values, install browser-side pixels (Meta Pixel, Google Tag, LinkedIn Insight Tag), implement server-side APIs (Meta CAPI, Google Ads offline upload), verify all events fire correctly, and configure attribution windows.

**One-paragraph:** Multi-platform conversion tracking setup: define macro and micro conversion events with dollar values, install browser-side pixels (Meta Pixel, Google Tag, LinkedIn Insight Tag), implement server-side APIs (Meta CAPI, Google Ads offline upload), verify all events fire correctly, and configure attribution windows. The core rule is: always implement server-side (CAPI/Conversions API) in addition to browser pixels — browser tracking degrades by 20-40% due to ad blockers and iOS privacy restrictions, causing smart bidding to optimize on incomplete data.

## Applies If (ALL must hold)

- Setting up conversion tracking on a new site, app, or ad account
- Auditing tracking accuracy when reported conversions don't match CRM data
- Implementing Meta Conversions API (CAPI) for server-side event deduplication
- Uploading offline conversions from CRM systems to Meta or Google
- Configuring attribution windows to match the product's sales cycle length

## Skip If (ANY kills it)

- Attribution model comparison and selection — use ads-attribution-models
- Analytics property setup (GA4 events, Mixpanel) — this covers ad-platform pixels only
- Campaign creation — tracking must be in place first; see ads-meta-campaign-setup
- Bid strategy configuration — tracking is a prerequisite, not the bidding logic itself

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
