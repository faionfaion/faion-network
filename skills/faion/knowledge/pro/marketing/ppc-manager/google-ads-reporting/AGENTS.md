# Google Ads Reporting & Automation

## Summary

GAQL-based reporting, scheduled automation, and error handling patterns for Google Ads accounts. Use `search_stream` for large queries, always include `segments.date`, divide `cost_micros` by 1,000,000 before presenting, and pin the API version. Read-only reporting agents feed a warehouse; mutation agents (auto-pause, bid change) require strict guardrails and human approval before executing.

## Why

Google Ads generates more data than any human can review manually across multiple accounts. Automated reporting catches CPA spikes, CTR drops, and budget pacing issues within hours. Without this layer, problems compound for days before detection. The API's quirks — micros units, timezone mismatches, version deprecation every ~9 months — are a persistent source of silent bugs that only disciplined patterns prevent.

## When To Use

- Scheduled daily or weekly performance reports across multiple Google Ads accounts (MCC)
- Threshold-based alerting: high CPA, low CTR, paused-by-mistake, budget pacing exceptions
- Bulk read pipelines feeding a warehouse, Looker Studio, or Slack from raw GAQL
- Auto-pausing low performers with strict guardrails and a per-run paused-list log
- Change-history monitoring for compliance via `change_event`

## When NOT To Use

- A single dashboard the team already opens in Looker — agent overhead not justified
- Features requiring the UI only (some recommendations, brand-suitability controls)
- Smart Bidding interventions during the learning phase — threshold-based agents can sabotage learning
- Real-time intra-day decisions — conversion data lags 1-3 hours and stabilizes after ~3 days

## Content

| File | What's inside |
|------|---------------|
| `content/01-gaql.xml` | GAQL structure, common resources and metrics, cost_micros gotchas, search vs search_stream |
| `content/02-automation.xml` | Batch operations, scheduled scripts, change history monitoring patterns |
| `content/03-error-handling.xml` | Error codes, retry-with-backoff pattern, rate limiter implementation |
| `content/04-agent-rules.xml` | Agent-specific rules: micros, version pinning, auto-pause guardrails, AI gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/daily-runner.py` | Guarded daily report job with retry and dry-run flag |
| `templates/rate-limiter.py` | Per-day token bucket rate limiter for Google Ads API |
