---
slug: google-ads-optimization
tier: pro
group: marketing
domain: ppc-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Google Ads API patterns for bidding strategy management, conversion action setup, offline conversion upload, and GA4 integration: create portfolio bidding strategies (Target CPA, Target ROAS), apply them to campaigns, set device bid adjustments, define conversion actions with counting and attribution, upload offline conversions via gclid, and query imported GA4 conversion data.
content_id: "e763268ab06ba55a"
tags: [google-ads, bidding, conversions, ga4, api]
---
# Google Ads Optimization — Bidding, Conversions, GA4

## Summary

**One-sentence:** Google Ads API patterns for bidding strategy management, conversion action setup, offline conversion upload, and GA4 integration: create portfolio bidding strategies (Target CPA, Target ROAS), apply them to campaigns, set device bid adjustments, define conversion actions with counting and attribution, upload offline conversions via gclid, and query imported GA4 conversion data.

**One-paragraph:** Google Ads API patterns for bidding strategy management, conversion action setup, offline conversion upload, and GA4 integration: create portfolio bidding strategies (Target CPA, Target ROAS), apply them to campaigns, set device bid adjustments, define conversion actions with counting and attribution, upload offline conversions via gclid, and query imported GA4 conversion data. The core rule is: let automated bidding accumulate at least 30 conversions per campaign before switching from Maximize Conversions to Target CPA — insufficient conversion data causes erratic bidding.

## Applies If (ALL must hold)

- Configuring bidding strategies for existing Google Ads campaigns via Python client
- Creating or updating conversion actions (WEBSITE, APP, UPLOAD types)
- Uploading offline conversions from CRM data matched by gclid
- Querying per-campaign conversion volume and value split by conversion action
- Setting device-level bid adjustments on campaigns

## Skip If (ANY kills it)

- Initial campaign/ad group/keyword creation — use google-ads-campaign-setup methodology instead
- Ad copy and responsive search ad authoring — use google-ads-creative methodology
- Cross-channel budget allocation — use budget-optimization methodology
- GA4 property administration or event schema design — this covers only the Ads API side

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
