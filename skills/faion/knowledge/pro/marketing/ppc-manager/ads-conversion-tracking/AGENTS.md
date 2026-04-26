# Ads Conversion Tracking

## Summary

Multi-platform conversion tracking setup: define macro and micro conversion events with dollar values, install browser-side pixels (Meta Pixel, Google Tag, LinkedIn Insight Tag), implement server-side APIs (Meta CAPI, Google Ads offline upload), verify all events fire correctly, and configure attribution windows. The core rule is: always implement server-side (CAPI/Conversions API) in addition to browser pixels — browser tracking degrades by 20-40% due to ad blockers and iOS privacy restrictions, causing smart bidding to optimize on incomplete data.

## Why

Ad platform algorithms (Meta, Google) optimize bidding toward the conversion signal you provide. If browser tracking is the only source and 30% of events are blocked, the algorithm sees inflated CPA and under-delivers on good audiences. Server-side events pass directly from your server, bypassing browser restrictions, and can include offline CRM data. Accurate conversion data is the single highest-leverage optimization lever in paid advertising.

## When To Use

- Setting up conversion tracking on a new site, app, or ad account
- Auditing tracking accuracy when reported conversions don't match CRM data
- Implementing Meta Conversions API (CAPI) for server-side event deduplication
- Uploading offline conversions from CRM systems to Meta or Google
- Configuring attribution windows to match the product's sales cycle length

## When NOT To Use

- Attribution model comparison and selection — use `ads-attribution-models`
- Analytics property setup (GA4 events, Mixpanel) — this covers ad-platform pixels only
- Campaign creation — tracking must be in place first; see `ads-meta-campaign-setup`
- Bid strategy configuration — tracking is a prerequisite, not the bidding logic itself

## Content

| File | What's inside |
|------|---------------|
| `content/01-conversion-definition.xml` | Macro vs micro conversions, value assignment, event mapping across Meta/Google/LinkedIn |
| `content/02-pixel-installation.xml` | Meta Pixel and Google Ads tag installation code, standard event JS calls |
| `content/03-server-side.xml` | Meta CAPI Node.js implementation, Google offline upload flow, deduplication |
| `content/04-verification.xml` | Verification tools per platform, testing process, attribution window settings |

## Templates

| File | Purpose |
|------|---------|
| `templates/tracking-plan.md` | Conversion tracking plan: macro/micro events, values, platforms, implementation checklist |
| `templates/meta-pixel.html` | Meta Pixel base code snippet with PageView |
| `templates/google-tag.html` | Google Ads conversion tag snippet |
