---
slug: privacy-compliance
tier: pro
group: marketing
domain: growth-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Privacy-compliant analytics means implementing a consent management platform (CMP) with default-deny analytics, GA4 Consent Mode v2 wiring, CCPA Global Privacy Control (GPC) signal handling, and IP anonymization — so tracking only activates after explicit user consent.
content_id: "22bdb6180308b231"
tags: [privacy, gdpr, analytics, compliance, consent]
---
# Privacy-Compliant Analytics

## Summary

**One-sentence:** Privacy-compliant analytics means implementing a consent management platform (CMP) with default-deny analytics, GA4 Consent Mode v2 wiring, CCPA Global Privacy Control (GPC) signal handling, and IP anonymization — so tracking only activates after explicit user consent.

**One-paragraph:** Privacy-compliant analytics means implementing a consent management platform (CMP) with default-deny analytics, GA4 Consent Mode v2 wiring, CCPA Global Privacy Control (GPC) signal handling, and IP anonymization — so tracking only activates after explicit user consent. Every new tag or pixel must pass through the consent gate before firing.

## Applies If (ALL must hold)

- Any web or app property tracked by GA4, Plausible, Mixpanel, Amplitude, or PostHog under GDPR, CCPA, or LGPD scope.
- Adding a new analytics or marketing tag — must pass through the consent gate before firing.
- Migrating to GA4 Consent Mode v2 or upgrading a CMP to IAB TCF 2.2.
- Implementing or auditing a CMP: OneTrust, Cookiebot, Iubenda, Osano, CookieYes, Klaro.
- DPIA or vendor review for a new tracker, pixel, or session-replay tool.

## Skip If (ANY kills it)

- Internal-only tools behind SSO with no third-party analytics — no public consent surface.
- Server-side-only telemetry tied to authenticated user IDs processed under contract (legitimate interest / contract basis) — still needs Records of Processing, but not a cookie banner.
- Static brochure sites with zero cookies and zero analytics — a banner here is legal theater.

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
