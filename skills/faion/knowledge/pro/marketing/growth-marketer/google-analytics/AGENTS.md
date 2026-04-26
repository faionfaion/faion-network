# Google Analytics 4 (GA4)

## Summary

GA4 setup, event taxonomy, custom dimensions, Data API reporting, and framework integrations (React/Gatsby, Django, Measurement Protocol). The rule: lock the event taxonomy in a repo file before deploying code; register all custom dimensions in GA4 Admin before data flows; always pass client_id from the cookie when sending Measurement Protocol events server-side.

## Why

GA4 is free and ubiquitous for web/app analytics, but its event-driven model requires upfront taxonomy design. Silent data loss is the most common failure: events with unregistered custom dimensions write nothing; Measurement Protocol calls with fresh UUIDs as client_id create ghost users; custom dimension names exceeding 40 characters are silently truncated. An agent that generates the taxonomy, code, and admin checklist in one pass prevents all three.

## When To Use

- Instrumenting a new site/app and needing a complete event taxonomy + gtag/Measurement Protocol code.
- Agent-driven daily or weekly reporting via the Data API.
- Auditing an existing GA4 property for misconfigurations (missing user_id, broken funnels, double-counted events).
- Server-side tracking via Measurement Protocol because client tracking is blocked by ad-blockers.

## When NOT To Use

- Privacy-strict EU-only audiences without server-side proxy + Consent Mode — GA4 in default mode breaks GDPR/Schrems II for many setups; use Plausible or Matomo instead.
- High-volume product analytics needing sub-second latency — GA4 data is sampled and delayed; use Mixpanel, Amplitude, or PostHog.
- BigQuery export not enabled — agent analytical depth is capped at the GA4 UI.
- B2B sales-led operations where revenue is closed in CRM, not on the site.

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Measurement ID install, data streams, enhanced measurement, user properties, event categories. |
| `content/02-tracking.xml` | Recommended events, custom events, Data API Python client, parameter limits, framework integrations. |
| `content/03-agent-rules.xml` | Agent gotchas: param limits, purchase dedup, Data API quotas, consent mode, cross-domain tracking. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gtag-snippet.html` | GA4 gtag.js installation snippet. |
| `templates/ga4_pull.py` | Python Data API helper for daily top-events report. |
| `templates/mp_track.py` | Measurement Protocol server-side event helper. |
