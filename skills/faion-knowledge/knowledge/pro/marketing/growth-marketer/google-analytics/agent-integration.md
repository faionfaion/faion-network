# Agent Integration — Google Analytics 4 (GA4)

## When to use
- You need agent-driven reporting on web/app traffic, conversions, and event funnels using a free, ubiquitous tool.
- You're instrumenting a new site/app and need an agent to generate a complete event taxonomy + gtag/MP code.
- You want server-side tracking via Measurement Protocol because client tracking is being blocked by ad-blockers.
- You're auditing an existing GA4 property for misconfigurations (missing user_id, broken funnels, double-counted events).

## When NOT to use
- Privacy-strict EU-only audiences without server-side proxy + consent mode — GA4 in default mode breaks GDPR/Schrems II for many setups; use Plausible/Matomo.
- High-volume product analytics with sub-second latency needs — GA4's data model is sampled and delayed; use Mixpanel/Amplitude/PostHog.
- BigQuery export not enabled — agent's analytical depth will be capped at the GA4 UI; serious analysis needs the BQ connector.
- B2B sales-led ops where revenue is closed in CRM, not on the site; CRM analytics are more useful.

## Where it fails / limitations
- Sampling kicks in on high-cardinality reports; agents may report numbers that change between runs.
- Thresholding hides small-segment data ("(other)" rows); agent reports look incomplete.
- Event/parameter name limits (40 chars name, 100 chars value, 25 params) — agents that auto-name long parameters silently lose data.
- Custom dimensions must be registered in admin BEFORE data flows; agent-generated events with new params do nothing until a human registers them.
- Consent Mode v2 changes data dramatically; an agent comparing pre/post consent-mode periods will misread declines as performance regressions.
- Measurement Protocol requires a `client_id` that matches the cookie; agent server-side calls without it create a separate ghost user.

## Agentic workflow
A `sonnet` instrumentation agent generates a full event taxonomy (recommended events, custom events, params, user properties) from a product spec, plus the gtag and Measurement Protocol code. A `haiku` reporting agent runs daily Data API queries and writes a markdown digest (top events, top sources, conversion deltas). An `opus` audit agent inspects the property for missing key events, broken funnels, BigQuery export status, and consent-mode coverage.

### Recommended subagents
- `faion-growth-agent` (opus for audits, sonnet for taxonomy design).
- Generic data/haiku subagent — daily Data API pulls into markdown.
- DevTools/sonnet subagent — write/refactor gtag, GTM tags, server-side MP calls.

### Prompt pattern
```
Given product = {description} with key flows {flow_list}, generate a GA4
event taxonomy: recommended events (login/sign_up/purchase) and custom
events. For each, list params (≤25, ≤40 chars), user_properties, and
admin steps to register custom dimensions. Output as markdown table.
```

```
Pull last 7d from property {id}: top 10 events by count, top 5 sources,
conversion count by event_name. Use Data API with date_ranges
[7daysAgo, today]. Return markdown + flag any event with day-over-day
delta >30%.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-analytics-data` Python SDK | Query Data API (reports) | `pip install google-analytics-data` |
| `google-analytics-admin` Python SDK | Manage properties, custom dimensions | `pip install google-analytics-admin` |
| `gcloud` CLI | Auth, service account keys for API access | https://cloud.google.com/sdk |
| GTM Server-Side container | Server-side tagging proxy | https://developers.google.com/tag-platform/tag-manager/server-side |
| `bq` CLI | Query GA4 BigQuery export tables | https://cloud.google.com/bigquery/docs/bq-command-line-tool |
| `dbt` | Model GA4 BigQuery export into clean tables | `pip install dbt-bigquery` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| GA4 Data API | SaaS | Yes (REST + SDKs) | Read-only reporting |
| GA4 Admin API | SaaS | Yes (REST) | Manage events, audiences, custom dims |
| GA4 Measurement Protocol | SaaS | Yes (REST) | Server-side event ingest |
| BigQuery (GA4 export) | SaaS | Yes (SQL + bq) | Raw event-level data, no sampling |
| Looker Studio | SaaS | Partial | Dashboards; APIs limited, agent can build via gas |
| GTM (web + server) | SaaS | Partial | Container management API exists but heavy |
| Stape, Addingwell | SaaS | Yes | Managed server-side GTM hosting |
| Consent platforms (CookieYes, OneTrust, Cookiebot) | SaaS | Yes (REST) | Required for GA4 + EU compliance |

## Templates & scripts
See `templates.md` for gtag and MP snippets. Inline Data API helper:

```python
# ga4_pull.py — agent's daily report
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Dimension, Metric, RunReportRequest)

def top_events(property_id: str, days: int = 7):
    client = BetaAnalyticsDataClient()
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="today")],
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount"), Metric(name="totalUsers")],
        limit=10,
    )
    resp = client.run_report(req)
    return [
        {"event": r.dimension_values[0].value,
         "count": int(r.metric_values[0].value),
         "users": int(r.metric_values[1].value)}
        for r in resp.rows
    ]
```

## Best practices
- Lock the event taxonomy in a `events.md` file in the repo and have agents diff against it before code changes.
- Always pass `client_id` from cookie when sending Measurement Protocol events; never let the agent generate fresh UUIDs server-side.
- Enable BigQuery export from day 1 — it's free for most volumes and bypasses sampling/thresholding.
- Use GTM Server-Side for resilience against ad-blockers and to keep secrets server-side.
- Register all custom dimensions in admin before deploying code that sends them; agents should generate the admin checklist alongside the code.
- Tie consent-mode signals to the event flow; without it, post-2024 EU traffic is severely under-reported.

## AI-agent gotchas
- Agents may exceed the 25-parameter or 40-char-name limits silently; build a validator into the codegen step.
- `purchase` event fires must include `transaction_id` for de-duplication; agent often forgets and you double-count revenue.
- The Data API has quotas (50 concurrent, 250k tokens/day per property); a haiku agent in a tight loop can exhaust them.
- DebugView only shows real-time, not historical; agents asking "why isn't my event in standard reports?" must remember the 24-48h lag.
- Service account JSON keys leak into prompts — use Workload Identity Federation or short-lived OAuth tokens.
- Cross-domain tracking requires the `linker` config; agent-generated single-domain code breaks attribution on multi-domain sites.
- "Conversions" in GA4 = events you marked as conversions in admin; an agent reporting "conversions" without that mapping reports zero.

## References
- GA4 Data API docs — https://developers.google.com/analytics/devguides/reporting/data/v1
- Measurement Protocol GA4 — https://developers.google.com/analytics/devguides/collection/protocol/ga4
- Simo Ahava's blog — https://www.simoahava.com/ (de facto practitioner reference)
- GA4 BigQuery export schema — https://support.google.com/analytics/answer/7029846
- Google's GA4 migration guide — https://support.google.com/analytics/topic/14088998
