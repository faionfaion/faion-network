# Agent Integration — Plausible Analytics

## When to use
- Setting up privacy-first web analytics on a Gatsby, React, or static site without GDPR consent banners
- Replacing Google Analytics on a site where cookie consent overhead is undesirable
- Querying site metrics programmatically to feed reports, dashboards, or agent decision-making
- Tracking custom conversion events (signups, purchases, CTA clicks) via the Stats API
- Self-hosting analytics on a controlled server for full data ownership

## When NOT to use
- You need user-level session replay or heatmaps — Plausible is aggregate-only by design; use PostHog or Hotjar for session-level data
- You need funnel analysis across authenticated user sessions — Plausible does not track logged-in user journeys; use Mixpanel or PostHog
- You require advanced cohort analysis, retention curves, or A/B test results — Plausible lacks these; use a product analytics tool alongside it
- You need advertising attribution with click IDs (gclid, fbclid) mapped to conversions — Plausible's attribution model is source-based, not click-level

## Where it fails / limitations
- No user-level data by design — you cannot identify which specific user visited a page
- Custom properties are limited in the free/self-hosted plan; revenue tracking requires the paid hosted plan
- API rate limits apply to the Stats API; bulk data extraction for large sites requires pagination
- Adblockers and privacy browsers block Plausible's default script — proxy setup via Nginx is required to maximize data accuracy
- The Data Export API (for raw event data) is only available in the Business/Enterprise plan; v1 Stats API covers aggregate and breakdown queries

## Agentic workflow
Claude agents can interact with Plausible primarily through its Stats API to pull aggregate metrics, timeseries data, top-page breakdowns, and goal/conversion counts. Haiku is appropriate for data extraction and formatting; Sonnet for interpreting analytics data and generating recommendations. Agents can also generate integration code (script tags, React components, custom event calls) and FAQ/howto content for Plausible setup. The Stats API does not require browser interaction — it is fully headless and agent-compatible. Writing to Plausible (sending events) uses the `/api/event` endpoint and can be done from server-side code agents generate.

### Recommended subagents
- `faion-sdd-executor-agent` — for managing analytics implementation as an SDD task with acceptance criteria
- General Claude Haiku subagent — for pulling data from Stats API, formatting reports, generating event tracking code
- General Claude Sonnet subagent — for interpreting analytics trends, generating optimization recommendations

### Prompt pattern
```
Query the Plausible Stats API for [site_id] and produce a weekly summary report.
Metrics: visitors, pageviews, bounce_rate, visit_duration.
Period: last 7 days vs previous 7 days (manual calculation from two API calls).
Output: markdown table with metric, this week, last week, % change.
API key: [from env PLAUSIBLE_API_KEY].
```

```
Generate Plausible custom event tracking code for the following conversion events
on a React/Gatsby site. Use the tagged-events script variant.
Events:
- Newsletter signup (form submit button)
- Pricing page CTA click
- Free trial start
Output: script tag, CSS class for each button, and JS fallback for programmatic firing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | Direct Stats API queries | Standard |
| `plausible-api` (Python) | Unofficial wrapper for Stats API | `pip install plausible-tracker` (community) |
| `gatsby-plugin-plausible` | Gatsby integration | `npm install gatsby-plugin-plausible` |
| `next-plausible` | Next.js integration with event helpers | `npm install next-plausible` |
| `plausible-tracker` (npm) | TypeScript event tracking library | `npm install plausible-tracker` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Plausible Cloud | SaaS | Yes — Stats API v1 | Hosted; GDPR compliant; easy setup; EU servers optional |
| Plausible CE (Community Edition) | OSS | Yes — Stats API v1 | Self-hosted; Docker; full data ownership; same API |
| Nginx | OSS | Partial | Proxy config for script + event endpoint (blocks adblockers) |
| Grafana | OSS | Yes | Dashboard layer on top of Plausible API data |
| n8n | OSS/SaaS | Yes | Automate Plausible API pulls into reports or alerts |
| Netlify / Vercel | SaaS | Partial | Edge function proxy for Plausible to bypass adblockers |

## Templates & scripts
The README.md contains a complete Python client (PlausibleClient) with `aggregate()`, `timeseries()`, `breakdown()`, and `realtime_visitors()` methods. Use that as the primary reference.

Minimal bash script for a quick daily stats pull:
```bash
#!/bin/bash
# Pull yesterday's Plausible stats
SITE_ID="${PLAUSIBLE_SITE_ID:-yourdomain.com}"
API_KEY="${PLAUSIBLE_API_KEY}"
PERIOD="day"

curl -s \
  "https://plausible.io/api/v1/stats/aggregate?site_id=${SITE_ID}&period=${PERIOD}&metrics=visitors,pageviews,bounce_rate" \
  -H "Authorization: Bearer ${API_KEY}" \
  | python3 -m json.tool
```

Nginx proxy config for adblocker bypass (copy from README.md — already documented there; see section "Custom Domain (Proxy)").

## Best practices
- Deploy the Nginx proxy configuration before launch — without it, adblocker and privacy browser users (often 20-40% of technical audiences) are invisible
- Use tagged events (`class="plausible-event-name=..."`) for CTA click tracking instead of JavaScript events when possible — no code changes needed for new buttons
- Define custom goals in the Plausible dashboard before firing events from code — goals that don't exist in the dashboard will be silently ignored
- Track revenue events for purchases immediately — the `revenue` field in `plausible()` calls is the only way to get revenue attribution in Plausible without a separate BI tool
- For Gatsby: use `gatsby-plugin-plausible` with a `customDomain` pointing to your proxy — this ensures the plugin uses your proxied endpoint
- Set up a weekly automated Stats API pull (via n8n or a cron job) into a Slack or Telegram message for passive monitoring without opening a dashboard
- Use `localStorage.setItem('plausible_ignore', 'true')` in your browser console during development to exclude your own visits from data

## AI-agent gotchas
- Stats API v1 does not support user-level or session-level queries — agents that attempt to query individual user paths will receive errors or meaningless aggregate data
- Period parameter formatting differs from common conventions: use `day`, `7d`, `30d`, `month`, `6mo`, `12mo`, or custom `YYYY-MM-DD,YYYY-MM-DD` — agents may use incorrect formats
- The `property` parameter in breakdown queries uses specific values (`event:page`, `visit:source`, `visit:device`, `visit:country`) — agents hallucinate property names; always validate against Plausible API docs
- Revenue tracking data is only available in the hosted Business plan; self-hosted CE does not support it by default — verify before implementing
- Agents producing Nginx proxy configs must be tested in a staging environment; misconfigured proxy blocks all analytics silently
- `plausible()` function calls fire in the browser only after the script loads; server-side rendering (SSR) in Next.js/Gatsby requires the `typeof window !== 'undefined'` guard

## References
- https://plausible.io/docs
- https://plausible.io/docs/stats-api
- https://plausible.io/docs/custom-event-goals
- https://plausible.io/docs/proxy/guides/nginx
- https://github.com/plausible/analytics
