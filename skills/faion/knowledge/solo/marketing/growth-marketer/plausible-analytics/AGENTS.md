---
slug: plausible-analytics
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Privacy-first, cookie-free web analytics for Gatsby, React, and static sites.
content_id: "2dace3871fd48c93"
tags: [analytics, privacy, plausible, tracking, gdpr]
---
# Plausible Analytics

## Summary

**One-sentence:** Privacy-first, cookie-free web analytics for Gatsby, React, and static sites.

**One-paragraph:** Privacy-first, cookie-free web analytics for Gatsby, React, and static sites. Covers script installation, Nginx proxy setup for adblocker bypass, custom event tracking, and the Stats API for programmatic data access. The core rule: deploy the Nginx proxy before launch — without it, adblocker users (20-40% of technical audiences) are invisible.

## Applies If (ALL must hold)

- Setting up privacy-first analytics on a Gatsby, React, or static site without consent banners
- Replacing Google Analytics where cookie consent overhead is undesirable
- Querying site metrics programmatically to feed reports or agent decisions
- Tracking custom conversion events (signups, purchases, CTA clicks) via Stats API
- Self-hosting analytics for full data ownership

## Skip If (ANY kills it)

- You need user-level session replay or heatmaps — Plausible is aggregate-only; use PostHog
- You need funnel analysis across authenticated user sessions — use Mixpanel or PostHog
- You require advanced cohort analysis or A/B test results — Plausible lacks these
- You need advertising attribution with click IDs (gclid, fbclid) mapped to conversions

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

- parent skill: `solo/marketing/growth-marketer/`
