# Agent Integration — Google Ads Reporting & Optimization

## When to use
- Recurring weekly/monthly performance reports across multiple Google Ads accounts (MCC).
- Search-terms triage: identify expensive non-converting queries → add as negatives at scale.
- Cross-segment diagnosis: device, daypart, location, audience performance breakdowns.
- Post-campaign attribution and budget reallocation reviews.
- KPI threshold monitoring (CPA exceeded, impression share dropped, QS drop) with alerts.

## When NOT to use
- Real-time bid management — Google Ads' own automated bidding is faster and has more signal access.
- Pure attribution across non-Google channels — use a multi-touch attribution tool (GA4 + Looker, Dreamdata, Triple Whale).
- Creative-quality scoring — needs design judgment, not data.
- Strategic budget allocation across channels (use `ads-budget-optimization` instead).

## Where it fails / limitations
- GAQL (Google Ads Query Language) can only join entities Google exposes; some segment combinations are blocked (e.g., search_term + device on some campaign types).
- Performance Max and Demand Gen hide query-level data — reporting is asset-group level.
- API has 24h hardening lag for some metrics (conversions, conversion value); intra-day numbers are estimates.
- Quality Score is reported per-keyword but can be `null` for insufficient impressions; agents must handle this.
- Search-terms report has a privacy threshold — terms with low volume aggregate to `(other)`, often 30-40% of cost.
- Auction Insights is not in the standard query API — must hit `auction_insight_view` and only works for selected campaign types.

## Agentic workflow
The reporting subagent runs a scheduled cycle: pull GAQL → diff vs. prior period → tag anomalies → propose actions (negatives to add, bids to adjust, ad groups to pause) → human approves → execute via mutate API. Use `google-ads-python`'s streaming reports for accounts >1M rows/day. Human-in-loop for: pausing campaigns, adding/removing keywords with >$X spend impact, altering bidding strategies.

### Recommended subagents
- `faion-ads-agent` — owns query construction and report fetch.
- A purpose-built `search-terms-triager` — daily: pull Search Terms report, classify query (relevant-converter / relevant-non-converter / irrelevant) via LLM, queue negatives for one-click human approval.
- A `ppc-anomaly-detector` — Z-score + EWMA on CPA/CPC/CTR per campaign; raises Slack alert when |z| > 2 over 3 consecutive days.
- `faion-sdd-executor-agent` (existing) — runs scheduled report generation as an SDD task with QA gates.

### Prompt pattern
```
You are a Search Terms triager.
Input: CSV with [search_term, campaign, ad_group, clicks, cost, conversions].
For each row, output: {action: "negative_exact" | "negative_phrase" | "promote_to_keyword" | "monitor", rationale}.
Rules:
- cost > $20 AND conversions == 0 → negative_exact
- conversions ≥ 2 AND CTR > 5% → promote_to_keyword
- ambiguous brand terms → escalate to human
```

```
Generate weekly performance report for account <id>.
Pull GAQL: campaign-level metrics last 7d vs. prior 7d.
Flag campaigns with: CPA up >20%, impression share down >15%, conv volume down >25%.
Output Markdown with tables, then bulleted recommendations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | GAQL queries, report streaming | `pip install google-ads` |
| `google-ads-toolkit` (community) | GAQL builder, report templates | github.com/google/google-ads-python |
| Google Ads Scripts | In-account JS automation, scheduled reports | developers.google.com/google-ads/scripts |
| BigQuery Data Transfer Service | Daily backfill of all Google Ads data into BQ | cloud.google.com/bigquery-transfer/docs/google-ads-transfer |
| `dbt` | Transformation layer over BQ Ads data | docs.getdbt.com |
| Looker Studio | Free dashboards, native connector | datastudio.google.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optmyzr | SaaS | Yes — API + scripts | Pre-built optimization recipes |
| Adalysis | SaaS | Yes — API | A/B testing + alerts |
| Supermetrics | SaaS | Yes — connectors | Pull Ads data into Sheets/BQ/Snowflake |
| Funnel.io | SaaS | Yes — API | Multi-channel data warehouse |
| Owox BI | SaaS | Yes | GA4 + Ads attribution layer |
| Looker (paid) | SaaS | Yes — LookML | Enterprise dashboards |

## Templates & scripts
See `templates.md` and the README's "Weekly Optimization Checklist" + "Performance Report" templates — ready to plug into a markdown generator.

Inline GAQL helpers an agent can run unchanged:

```python
# weekly_report.py
from google.ads.googleads.client import GoogleAdsClient

def weekly_campaign_report(client, customer_id, days=7):
    ga = client.get_service("GoogleAdsService")
    q = f"""
      SELECT campaign.name, campaign.status,
             metrics.cost_micros, metrics.clicks, metrics.impressions,
             metrics.ctr, metrics.average_cpc, metrics.conversions,
             metrics.cost_per_conversion, metrics.search_impression_share
      FROM campaign
      WHERE segments.date DURING LAST_{days}_DAYS
        AND campaign.status != 'REMOVED'
      ORDER BY metrics.cost_micros DESC
    """
    rows = []
    for r in ga.search(customer_id=customer_id, query=q):
        rows.append({
            "campaign": r.campaign.name,
            "cost": r.metrics.cost_micros / 1_000_000,
            "conv": r.metrics.conversions,
            "cpa": (r.metrics.cost_micros / 1_000_000) / max(r.metrics.conversions, 0.01),
            "is_share": r.metrics.search_impression_share,
        })
    return rows
```

```python
def search_terms_for_negatives(client, customer_id, min_cost=20):
    ga = client.get_service("GoogleAdsService")
    q = f"""
      SELECT search_term_view.search_term, campaign.id, ad_group.id,
             metrics.cost_micros, metrics.conversions, metrics.clicks
      FROM search_term_view
      WHERE segments.date DURING LAST_7_DAYS
        AND metrics.cost_micros >= {min_cost * 1_000_000}
        AND metrics.conversions = 0
      ORDER BY metrics.cost_micros DESC LIMIT 200
    """
    return list(ga.search(customer_id=customer_id, query=q))
```

## Best practices
- Always compare period-over-period AND year-over-year — seasonal effects mask real changes.
- Segment by device + network before any campaign-level conclusion; mobile/Search-Partners often skew the average.
- Tag every action: in commit messages, change history, or a structured log. Ad accounts without an audit trail are unmanageable for agents.
- Set up automated rules for the boring stuff (pause keywords with >$X cost and 0 conv in 14d) — frees agents for diagnosis.
- Track Quality Score weekly per keyword; QS drift predicts CPA spikes 1-2 weeks ahead.
- Use streaming reports (`search_stream`) for >100k rows; the regular `search` endpoint paginates and times out.
- Always store raw GAQL output to BQ/disk before transformation — Google occasionally backfills metrics, and you want to reproduce reports.

## AI-agent gotchas
- All cost fields are micros (1 unit = $0.000001) — wrong scaling leads to 6-orders-of-magnitude bugs in alerts.
- Conversion floats: stored as `double`, not int — `metrics.conversions` can be `0.5` for fractional attribution.
- Impression share is a fraction, NOT a percentage; multiply by 100 for human display.
- `ALL_CONVERSIONS` vs `CONVERSIONS` — first includes all conv actions, second only counts those marked "include in Conversions"; agents must pick deliberately.
- API version pinning: every quarterly version deprecates fields without warning; pin `api_version` in the config file.
- Time zone: account time zone differs from server; `segments.date` is in account TZ, easy to misalign with GA4/server logs.
- Privacy thresholds: `search_term_view` only returns terms above a volume floor — never assume coverage = 100% of spend.
- Reports for `customer_search_term_insight` (PMax) have additional access requirements; default service accounts may get empty results.
- Quota: 15,000 operations/day for basic access tier; report fetches count toward this. Large dashboards can starve mutation calls.

## References
- GAQL reference: https://developers.google.com/google-ads/api/docs/query/overview
- Reports list: https://developers.google.com/google-ads/api/fields/v17/overview
- Account quotas: https://developers.google.com/google-ads/api/docs/best-practices/quotas
- Streaming reports: https://developers.google.com/google-ads/api/docs/reporting/streaming
- Google Ads Scripts: https://developers.google.com/google-ads/scripts
