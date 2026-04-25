# Agent Integration — Google Ads Reporting & Automation

## When to use
- Scheduled performance reports (daily/weekly) across multiple Google Ads accounts where the agent assembles, validates, and ships the output.
- Threshold-based alerting: high CPA, low CTR, paused-by-mistake, budget-pacing exceptions.
- Bulk read pipelines feeding a warehouse / Looker Studio / Slack from raw GAQL.
- Auto-pausing low performers (with a strict guardrail) and producing a "what was paused yesterday and why" log.
- Change-history monitoring for compliance — agent watches `change_event` and flags unexpected human edits.

## When NOT to use
- A single dashboard the team already opens in Looker — the agent is overhead.
- Anything requiring a UI-only feature (e.g. some recommendations, brand-suitability controls) — these aren't in the API.
- Smart Bidding interventions during the learning phase — even threshold-based agents can sabotage learning.
- Real-time intra-day decisions; Google Ads conversion data lags 1–3 hours and stabilizes ~3 days later. Agents that act intra-day act on noisy data.

## Where it fails / limitations
- API quotas: Basic Access = 15,000 ops/day; reporting agents that re-pull "yesterday" hourly burn through it.
- `cost_micros` divisions: agents that forget to divide by 1,000,000 silently report values 1M× too large.
- `cost_per_conversion` is ALSO in micros — easy to forget.
- API versions deprecate every ~9 months; reporting jobs that hardcode v17 break on rollover.
- `search` (unary) caps at the response size limit; >10k rows requires `search_stream`.
- `change_event` only retains 30 days — agents missing a daily run lose audit history.
- Date segmentation: omitting `segments.date` returns lifetime totals; agents that sum lifetime daily clobber dashboards.
- `segments.date` semantics use the customer's timezone; multi-account agents normalize to UTC manually.

## Agentic workflow
Reporting agent runs daily: load credentials, list MCC children, run a small set of pre-canned GAQL queries via `search_stream`, write to BigQuery / parquet. A separate alerting agent reads the warehouse table (not the API) and posts to Slack/email when thresholds trip. A third "auto-pause" agent runs nightly with strict guardrails (impression floor, account allow-list, dry-run preview output to a log) before mutating. Always pin API version in client config and roll forward deliberately. Use a rate limiter with per-day token bucket per account.

### Recommended subagents
- `faion-ads-agent` — owns Google Ads credentials and GAQL queries.
- `faion-feature-executor` — for wiring the warehouse / dbt build pipeline as feature work.
- `password-scrubber-agent` — pre-commit redaction of any logged tokens / customer IDs in PRs.

### Prompt pattern
```
System: You are the reporting agent. Use search_stream for any query that
        could exceed 10k rows. Always include segments.date in WHERE.
        Convert micros → currency before presenting. Never SELECT *.
        Refuse to mutate from this agent — read-only.
User:   Pull last 7 days of campaign performance for accounts [A,B,C].
        Aggregate to daily, output CSV with cost / clicks / conversions /
        ctr / cpa columns. Currency in account currency.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | API client with `search_stream` | `pip install google-ads` |
| `bq` (BigQuery CLI) | Schedule queries, load data | https://cloud.google.com/bigquery/docs/bq-command-line-tool |
| BigQuery Data Transfer Service | Native daily Google Ads → BQ schema sync | https://cloud.google.com/bigquery/docs/google-ads-transfer |
| `dbt` | Transform raw Google Ads tables into reporting marts | https://docs.getdbt.com |
| Google Ads Scripts | In-product JS automation when you cannot host code | https://developers.google.com/google-ads/scripts |
| `schedule` (Python) | Lightweight cron substitute inside an agent loop | `pip install schedule` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads API | SaaS | Yes | Source of truth for the live account state. |
| BigQuery + Data Transfer | SaaS | Yes (SQL) | Skip GAQL entirely for most reporting. |
| Looker Studio | SaaS | Partial (UI) | Native Google Ads connector for ad-hoc charts. |
| Supermetrics / Funnel.io | SaaS | Yes | Off-the-shelf connectors → Sheets/BQ/Snowflake. |
| Optmyzr / Adalysis | SaaS | Yes (API) | Pre-built audits and rules — sometimes cheaper than rolling your own. |
| Slack / Email (SMTP) | service | Yes | Agent alert sinks. |
| Sentry / OpsGenie | SaaS | Yes | Pipe agent failures into incident tooling. |

## Templates & scripts
See `templates.md` and the GAQL examples in `README.md`. Inline rate-limited daily-runner pattern (drop-in for an agent loop):

```python
# daily_runner.py — guarded daily report job with retry + dry-run flag
import logging, time
from google.ads.googleads.errors import GoogleAdsException

def run_daily(client, customer_ids, query_fn, sink_fn, dry_run=False):
    ga = client.get_service("GoogleAdsService")
    log = logging.getLogger("ads-report")
    for cid in customer_ids:
        for attempt in range(3):
            try:
                rows = []
                for batch in ga.search_stream(customer_id=cid, query=query_fn(cid)):
                    rows.extend(batch.results)
                log.info("%s: %d rows", cid, len(rows))
                if not dry_run:
                    sink_fn(cid, rows)
                break
            except GoogleAdsException as ex:
                if any(e.error_code.quota_error for e in ex.failure.errors):
                    sleep = 2 ** attempt * 30
                    log.warning("quota; sleep %ss", sleep); time.sleep(sleep)
                else:
                    log.error("non-retryable: %s", ex.request_id); break
```

## Best practices
- Pin `api_version` and bump on a calendar (≤9 months); subscribe to the API release-notes feed.
- Do reporting via BigQuery Data Transfer Service when possible — it handles the API quirks (versioning, retries, schema drift) for free.
- One agent run = one query batch = one sink write; don't multiplex tasks in a single API session.
- Always include account-level filters (`customer.status = 'ENABLED'`) when iterating MCC trees; cancelled accounts return weird shapes.
- Build a `change_event` archive job day 1 — when something blows up, you'll need to know who changed what 28 days ago.
- Auto-pause guardrails: minimum impression threshold (≥5,000), minimum spend threshold ($X), allow-list of accounts, output a paused-list log per run.
- Convert `cost_micros / 1_000_000` and `cost_per_conversion / 1_000_000` close to the source (ETL); downstream consumers shouldn't see micros.

## AI-agent gotchas
- LLMs hallucinate GAQL fields that don't exist (e.g., `metrics.spend`). Validate against `googleads_v18.services.types` before running.
- Agents conflate `metrics.conversions` (counted per attribution rules) with `metrics.all_conversions` (every conversion action) — the second number is bigger and "wronger" for ROAS.
- `cost_micros` divisor confusion: model writes `cost_micros / 1_000` instead of `1_000_000` and ships off-by-1000 numbers.
- Auto-pause agents that trip on day-1 of a fresh campaign kill momentum — enforce a minimum-age (≥7 days) before pausing.
- Date math: agents using "yesterday" in local code but the account is in another timezone produce gappy reports.
- Human-in-loop checkpoint: any auto-mutation (pause, budget change, status flip) — even with thresholds — should drop a notification to a human.
- Quota thrash: agents retrying on quota errors with no backoff just delay the inevitable; require exponential backoff + max-attempts.
- Models writing GAQL forget that `LIMIT` is supported but `OFFSET` is NOT — paginate via `search_stream` instead.

## References
- Google Ads API docs — https://developers.google.com/google-ads/api
- GAQL field reference — https://developers.google.com/google-ads/api/fields/v18/overview
- BigQuery Data Transfer (Google Ads) — https://cloud.google.com/bigquery/docs/google-ads-transfer
- API release notes / version policy — https://developers.google.com/google-ads/api/docs/release-notes
- Reporting best practices — https://developers.google.com/google-ads/api/docs/reporting/best-practices
