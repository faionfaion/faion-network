---
slug: conversion-tracking
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Implementation patterns for tracking conversion events across the full user lifecycle — GA4 goal setup, funnel step instrumentation, A/B test exposure and conversion events, SaaS user-lifecycle events (signup, activation, retention, purchase, referral), content engagement, and video tracking.
content_id: "189b8e353730756a"
tags: [conversion-tracking, ga4, funnel, event-tracking, analytics]
---
# Conversion Tracking

## Summary

**One-sentence:** Implementation patterns for tracking conversion events across the full user lifecycle — GA4 goal setup, funnel step instrumentation, A/B test exposure and conversion events, SaaS user-lifecycle events (signup, activation, retention, purchase, referral), content engagement, and video tracking.

**One-paragraph:** Implementation patterns for tracking conversion events across the full user lifecycle — GA4 goal setup, funnel step instrumentation, A/B test exposure and conversion events, SaaS user-lifecycle events (signup, activation, retention, purchase, referral), content engagement, and video tracking. Includes a reusable FunnelTracker class and an event-registry validator.

## Applies If (ALL must hold)

- Pre-launch: setting up GA4 + privacy-friendly analytics and a server-side event log before first users.
- Implementing a SaaS funnel (signup → activation → trial → paid → expansion) with consistent naming.
- Replatforming or migrating analytics — codifying schema prevents lossy reinstrumentation.
- Need a single source-of-truth for conversion events backing A/B tests and exec dashboards.

## Skip If (ANY kills it)

- Pure 1:1 sales with fewer than 100 prospects/month — CRM tracking is simpler and sufficient.
- Pre-launch landing-page test where a sign-up form already gives the answer.
- Highly regulated environments (healthcare PHI, COPPA) without a prior privacy/legal review of payloads.
- Cannot commit to maintaining the schema; broken events are worse than no events.

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

- parent skill: `pro/marketing/growth-marketer/`
