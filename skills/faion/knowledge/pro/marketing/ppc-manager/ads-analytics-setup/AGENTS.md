# Analytics Setup

## Summary

Three-layer analytics implementation — Collect, Analyze, Attribute — covering GA4 property creation, event tracking plan, conversion designation, UTM naming conventions, and dashboard setup. Define the event spec before writing any tracking code. Implement Consent Mode v2 from day one. Link GA4 to Google Ads, BigQuery, and Search Console immediately after property creation to unlock features without future migration work.

## Why

Without a properly structured analytics stack, ad platforms receive incomplete or inconsistent conversion signals, bidding algorithms optimize for the wrong goals, and channel attribution is unreliable. A documented event spec with consistent UTM conventions is the foundation all downstream reporting, attribution, and optimization depends on. Missing it means silent data loss that only surfaces weeks later when campaigns underperform.

## When To Use

- New site or app launch needing GA4 and ad-platform pixels installed correctly from day one
- Migration from Universal Analytics to GA4 (UA sunset 2023; validate event mapping)
- Multi-channel attribution rebuild: UTM standards, dataLayer schema, conversion definitions
- E-commerce or SaaS rolling out enhanced ecommerce or product analytics
- Compliance refit (Consent Mode v2, GDPR/CCPA banners, server-side tagging migration)

## When NOT To Use

- Sites with a working analytics stack and consistent UTM data — focus on optimization, not reinstall
- Pure backend or API-only products with no front-end — use server-side analytics (PostHog Backend)
- Privacy-first or low-traffic projects where Plausible or Fathom suffices
- One-page marketing sites — Plausible/Fathom plus UTM macros is sufficient

## Content

| File | What's inside |
|------|---------------|
| `content/01-ga4-setup.xml` | GA4 property creation, tag installation, enhanced measurement, event configuration |
| `content/02-conversions-utm.xml` | Conversion designation by business type, UTM parameter schema and naming rules |
| `content/03-agent-rules.xml` | GA4 gotchas: reserved events, custom dimension limits, cardinality, Consent Mode v2, iframe contexts |

## Templates

| File | Purpose |
|------|---------|
| `templates/event-tracking-plan.md` | Event spec template: page events, user events, engagement events, conversion flags |
| `templates/utm-conventions.md` | UTM naming conventions: source, medium, campaign, content format |
| `templates/validate-events.js` | Playwright script to verify event firing on staging via dataLayer interception |
