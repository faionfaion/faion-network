# Plausible Analytics

## Summary

Privacy-first, cookie-free web analytics for Gatsby, React, and static sites.
Covers script installation, Nginx proxy setup for adblocker bypass, custom event
tracking, and the Stats API for programmatic data access. The core rule: deploy
the Nginx proxy before launch — without it, adblocker users (20-40% of technical
audiences) are invisible.

## Why

Google Analytics requires GDPR cookie consent, adds ~45KB to page weight, and
sends user data to Google. Plausible is GDPR-compliant by design (no cookies, no
personal data), lightweight (< 1KB script), and exposes a REST Stats API that
agents can query programmatically for reports, dashboards, and automated alerts.

## When To Use

- Setting up privacy-first analytics on a Gatsby/React/static site without consent banners
- Replacing Google Analytics where cookie consent overhead is undesirable
- Querying site metrics programmatically to feed reports or agent decisions
- Tracking custom conversion events (signups, purchases, CTA clicks) via Stats API
- Self-hosting analytics for full data ownership

## When NOT To Use

- You need user-level session replay or heatmaps — Plausible is aggregate-only; use PostHog
- You need funnel analysis across authenticated user sessions — use Mixpanel or PostHog
- You require advanced cohort analysis or A/B test results — Plausible lacks these
- You need advertising attribution with click IDs (gclid, fbclid) mapped to conversions

## Content

| File | What's inside |
|------|---------------|
| `content/01-setup.xml` | Script variants, Nginx proxy config, Gatsby and React integration patterns |
| `content/02-event-tracking.xml` | Custom events, goal tracking, CSS class tagged events, revenue tracking |
| `content/03-stats-api.xml` | Aggregate, timeseries, breakdown, realtime endpoints; Python client; gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/plausible-client.py` | Python client: aggregate(), timeseries(), breakdown(), realtime_visitors() |
| `templates/nginx-proxy.conf` | Nginx proxy config for adblocker bypass |
| `templates/gatsby-config.js` | gatsby-plugin-plausible configuration snippet |
| `templates/prompt-weekly-report.txt` | LLM prompt to generate a weekly stats summary from API data |
| `templates/prompt-event-tracking.txt` | LLM prompt to generate custom event tracking code for a site |
