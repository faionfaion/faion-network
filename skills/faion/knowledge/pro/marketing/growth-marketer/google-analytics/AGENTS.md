---
slug: google-analytics
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GA4 setup, event taxonomy, custom dimensions, Data API reporting, and framework integrations (React/Gatsby, Django, Measurement Protocol).
content_id: "bfddc5dd2218205b"
tags: [google-analytics, ga4, analytics, data-api, event-tracking]
---
# Google Analytics 4 (GA4)

## Summary

**One-sentence:** GA4 setup, event taxonomy, custom dimensions, Data API reporting, and framework integrations (React/Gatsby, Django, Measurement Protocol).

**One-paragraph:** GA4 setup, event taxonomy, custom dimensions, Data API reporting, and framework integrations (React/Gatsby, Django, Measurement Protocol). The rule: lock the event taxonomy in a repo file before deploying code; register all custom dimensions in GA4 Admin before data flows; always pass client_id from the cookie when sending Measurement Protocol events server-side.

## Applies If (ALL must hold)

- Instrumenting a new site/app and needing a complete event taxonomy + gtag/Measurement Protocol code.
- Agent-driven daily or weekly reporting via the Data API.
- Auditing an existing GA4 property for misconfigurations (missing user_id, broken funnels, double-counted events).
- Server-side tracking via Measurement Protocol because client tracking is blocked by ad-blockers.

## Skip If (ANY kills it)

- Privacy-strict EU-only audiences without server-side proxy + Consent Mode — GA4 in default mode breaks GDPR/Schrems II for many setups; use Plausible or Matomo instead.
- High-volume product analytics needing sub-second latency — GA4 data is sampled and delayed; use Mixpanel, Amplitude, or PostHog.
- BigQuery export not enabled — agent analytical depth is capped at the GA4 UI.
- B2B sales-led operations where revenue is closed in CRM, not on the site.

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
