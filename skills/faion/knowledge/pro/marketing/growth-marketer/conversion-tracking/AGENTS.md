# Conversion Tracking

## Summary

Implementation patterns for tracking conversion events across the full user lifecycle — GA4 goal setup, funnel step instrumentation, A/B test exposure and conversion events, SaaS user-lifecycle events (signup, activation, retention, purchase, referral), content engagement, and video tracking. Includes a reusable `FunnelTracker` class and an event-registry validator.

## Why

Client-side tracking loses 20-40% of events to ad-blockers, ITP, and consent gating. A versioned event registry with typed wrappers and server-side purchase reconciliation is the only reliable source of truth for funnel analysis, paid-channel ROAS, and A/B test results.

## When To Use

- Pre-launch: setting up GA4 + privacy-friendly analytics and a server-side event log before first users.
- Implementing a SaaS funnel (signup → activation → trial → paid → expansion) with consistent naming.
- Replatforming or migrating analytics — codifying schema prevents lossy reinstrumentation.
- Need a single source-of-truth for conversion events backing A/B tests and exec dashboards.

## When NOT To Use

- Pure 1:1 sales with fewer than 100 prospects/month — CRM tracking is simpler and sufficient.
- Pre-launch landing-page test where a sign-up form already gives the answer.
- Highly regulated environments (healthcare PHI, COPPA) without a prior privacy/legal review of payloads.
- Cannot commit to maintaining the schema; broken events are worse than no events.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ga4-conversion-setup.xml` | GA4 conversion goal setup, key conversion events with monetary value, funnel definition. |
| `content/02-tracking-patterns.xml` | A/B test tracking, SaaS lifecycle events, feature usage, content engagement, video tracking. |
| `content/03-rules-and-antipatterns.xml` | Event-registry discipline, PII rules, currency unit consistency, consent gating, server-side reconciliation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/funnel-tracker.js` | FunnelTracker class: trackStep, trackCompletion, trackAbandonment with GA4 + Plausible. |
| `templates/validate-events.py` | CI script to fail if any tracking call uses an unregistered event name. |
