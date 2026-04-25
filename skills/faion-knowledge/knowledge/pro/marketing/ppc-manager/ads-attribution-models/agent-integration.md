# Agent Integration — Ads Attribution Models

## When to use
- Multi-channel paid programs (≥2 platforms) where platform totals don't match the warehouse and budget reallocation depends on a defensible model.
- Setting up GA4 / BigQuery export pipelines that an agent queries to produce reconciled "true" CPA / ROAS per channel.
- Designing and running incrementality (geo-holdout) tests as a recurring quarterly job.
- Auto-generating weekly attribution variance reports (platform-reported vs. GA4 vs. warehouse) so humans can spot drift fast.

## When NOT to use
- Single-channel programs — pick the platform's default model and move on; cross-channel models add no signal.
- Pre-revenue or <50 conversions/month — the data isn't dense enough for any model (least of all data-driven) to be reliable.
- When you're optimizing inside a single platform (changing bids, ad copy) — use that platform's native attribution; switching models mid-flight just confuses the bidding algorithm.
- Tactical creative decisions — attribution informs strategy and budget, not which thumbnail to ship today.

## Where it fails / limitations
- Walled-garden attribution (Meta CAPI, Google's modeled conversions) cannot be deduplicated perfectly — every model has irreducible error.
- Data-driven attribution requires enough conversions per channel to train; GA4 falls back to last-click silently below the threshold.
- Cross-device journeys are weak without a logged-in user or hashed-email join key — most "true" attribution is approximate.
- iOS ATT, ITP, and consent-mode "denied" hits leave attribution holes that no model fills; agents over-confidently report numbers that hide ~10–30% missing data.
- Geo-holdout tests need clean geo separation and sufficient runtime (4+ weeks) — short tests produce noise, not signal.
- "Last-click" inside a single platform is incomparable to "data-driven" across platforms; agents that present them side-by-side mislead.

## Agentic workflow
Stand up a daily ETL agent: pull raw cost + conversion rows from Google Ads, Meta Ads (Insights API), and GA4 (Data API) into a warehouse, then materialize three views — platform-reported, GA4-unified, warehouse-deduped. A reporting agent compares the three weekly and flags variances >15%. Once a quarter, an experiment agent designs a geo-holdout (paired-region selection, sample-size calc), schedules budget changes via the platform-specific agent, and reads results back. Treat any conclusion as a "decision proposal" needing human sign-off before budget shifts.

### Recommended subagents
- `faion-ads-agent` — pulls raw Google + Meta Ads data, executes geo-holdout config changes.
- `faion-feature-executor` — wraps the warehouse / dbt build pipeline as feature work.
- `faion-sdd-execution` — quality gates around SQL views feeding the attribution dashboard.
- `faion-brainstorm` — divergent thinking when "the data doesn't make sense and we need new hypotheses".

### Prompt pattern
```
System: You are the attribution agent. Always present THREE numbers per
        channel (platform-reported, GA4 modeled, warehouse-deduped) and
        flag if they diverge >15%. Refuse to recommend budget reallocation
        without min 4 weeks of data and conversion volume ≥ statistical
        threshold provided in context.
User:   Reconcile last 30 days for Meta + Google. Highlight where platform
        over-reports vs warehouse. Recommend geo-holdout candidates.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-analytics-data` (GA4 Data API) | Read GA4 modeled attribution | `pip install google-analytics-data` |
| `google-ads-python` | Google Ads conversions + offline import | `pip install google-ads` |
| `facebook-business` | Meta Insights + CAPI | `pip install facebook-business` |
| `dbt` | Materialize attribution views over warehouse data | https://docs.getdbt.com |
| `GeoLift` (R / Python) | Open-source geo-holdout test design | https://github.com/facebookincubator/GeoLift |
| `bigquery` CLI / `bq` | Run SQL views, schedule queries | https://cloud.google.com/bigquery/docs/bq-command-line-tool |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GA4 (web + Data API) | SaaS | Yes | Default unified-view source for most teams. |
| BigQuery (GA4 export) | SaaS | Yes (SQL) | Required for >10M event/month or >14-month windows. |
| Snowplow / Rudderstack | OSS / SaaS | Yes | Server-side tracking for first-party event capture. |
| Triple Whale | SaaS (e-com) | Yes | Pixel + first-party post-purchase survey + MTA model. |
| Northbeam, Rockerbox | SaaS | Yes | Multi-touch attribution with platform integrations. |
| Funnel.io / Supermetrics | SaaS | Yes | Connector layer to dump platform data into warehouse. |
| Meta Conversion Lift / Google Conversion Lift | SaaS | Yes | Native incrementality studies; pair with own geo-holdout. |
| Recast / Robyn (OSS MMM) | OSS / SaaS | Yes | Marketing mix modelling for top-down validation. |

## Templates & scripts
See `templates.md` for the attribution-analysis report template. Inline weekly variance helper that an agent runs as the first step:

```python
# variance_check.py — flag platform vs warehouse drift per channel
def variance(rows: list[dict]) -> list[dict]:
    """rows: [{channel, platform_conv, ga4_conv, warehouse_conv, spend}]"""
    out = []
    for r in rows:
        pc, gc, wc = r["platform_conv"], r["ga4_conv"], r["warehouse_conv"]
        base = wc or 1
        out.append({
            "channel": r["channel"],
            "platform_vs_warehouse_pct": round((pc - wc) / base * 100, 1),
            "ga4_vs_warehouse_pct": round((gc - wc) / base * 100, 1),
            "warehouse_cpa": round(r["spend"] / base, 2) if wc else None,
            "alert": abs((pc - wc) / base) > 0.15 or abs((gc - wc) / base) > 0.15,
        })
    return out
```

## Best practices
- Pick ONE source of truth (usually warehouse on top of GA4 export) and use platform data only for in-platform optimization.
- Document the attribution model + lookback window in a constitution-style doc; surprise model changes invalidate historical comparisons.
- Match the lookback window to the sales cycle (1-day click for impulse, 30-day for SaaS, 90-day for B2B enterprise).
- Validate yearly with an incrementality test even if data-driven attribution looks fine; modeled attribution drifts.
- Always send the same `event_id` from pixel and CAPI for the same conversion — dedup happens server-side via that field.
- Keep raw, untransformed cost + conversion data in the warehouse; resist the urge to only store the model output.
- Never let an agent retroactively re-attribute historical conversions without snapshotting the previous numbers; you'll lose audit trail.

## AI-agent gotchas
- Models love to "explain" small variances with elaborate stories; force a minimum-variance threshold (e.g., 15%) before producing narrative.
- LLMs treat platform-reported and GA4 modeled numbers as comparable; they're not — they use different lookback windows and dedup logic.
- Currency / timezone mismatches: GA4 uses property timezone, Google Ads uses account timezone; agent computing a single "today" number can off-by-one.
- Data-driven model "drift": the same query last week and this week can return different historical values — agent diff jobs need to handle that, not flag as bug.
- Incrementality test contamination: agents shifting budget mid-test invalidate the experiment. Lock controls during runs.
- Human-in-loop checkpoint: any reallocation >10% of total spend, any change of the canonical model, any retroactive re-attribution.
- Confidence-interval blindness: LLMs report point estimates with bravado. Force them to include CIs (or at least sample size) in every recommendation.
- Hashing email for offline conversion uploads requires SHA-256 on lowercase-trimmed email; agents that skip normalization see 0% match rate.

## References
- GA4 attribution docs — https://support.google.com/analytics/answer/10596866
- Google Ads attribution models — https://support.google.com/google-ads/answer/6259715
- Meta attribution settings — https://www.facebook.com/business/help/370704083280490
- Meta Conversions API + dedup — https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
- GeoLift methodology — https://research.facebook.com/blog/2022/9/geolift-an-open-source-tool-for-incremental-measurement
- Robyn MMM — https://github.com/facebookexperimental/Robyn
