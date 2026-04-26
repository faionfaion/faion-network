# Agent Integration — Google Ads Optimization

## When to use
- Migrating a manual-CPC account to Smart Bidding (Target CPA / Target ROAS / Maximize Conversion Value).
- Programmatic creation of portfolio bidding strategies across many campaigns via Google Ads API.
- Bulk uploading offline conversions (CRM-closed deals, store visits) back into Google Ads to feed Smart Bidding.
- Auditing or rebuilding conversion actions and attribution windows after a tracking incident.
- Wiring GA4 event imports into Google Ads as conversion sources.

## When NOT to use
- Account spends < $20/day or has < 30 conversions/month — Smart Bidding lacks data, manual CPC is fine.
- You don't yet have working conversion tracking — Smart Bidding without conversions is just expensive Maximize Clicks.
- Brand-only accounts where impression share / cost-cap matters more than CPA.
- One-off bid adjustments — do them in the UI, don't write API code for a 5-minute job.

## Where it fails / limitations
- Smart Bidding learning phase resets when you change tCPA/tROAS by > ~20% in one go — staircase changes instead.
- Offline conversion uploads require a `gclid` and a timestamp ≤ 90 days old; older conversions are silently dropped (`partial_failure=True`).
- `customer_manager_link` query does not return GA4 links; GA4 linkage lives in the GA4 Admin API, not Google Ads API.
- `cpc_bid_ceiling_micros` on Target CPA can starve a campaign if set too low — the bidder simply stops serving.
- Data-driven attribution needs ≥ 300 conversions and ≥ 3000 ad interactions in 30 days; below that, Google falls back to last-click silently.

## Agentic workflow
The marketing agent owns strategy (which bidding strategy, what tCPA, which conversions count), and a code agent translates the decision into google-ads API mutations. Keep the agent loop short: fetch current state with GAQL → diff against desired state → emit `mutate_*` operations → log diffs for human approval before push when spend > $X/day. Never let an agent silently change `bidding_strategy` on a live campaign with > 7 days of learning data.

### Recommended subagents
- `faion-ads-agent` — owns Google Ads API client, bidding mutations, conversion tracking config.
- `faion-marketing-manager` — picks the strategy (tCPA vs tROAS vs MaxConv) based on funnel stage and data volume.
- `faion-sdd-executor-agent` — wraps risky mutations behind a plan/approve/apply gate.

### Prompt pattern
```
You are managing Google Ads account {customer_id}. Current strategy: {current}.
Goal: switch campaign {cid} to Target CPA at ${tcpa} with bid ceiling 2x.
Steps: (1) GAQL fetch current bidding_strategy_type and 30d conversions,
(2) if conversions < 30, ABORT and report, (3) else build BiddingStrategyOperation
and CampaignOperation, (4) print the JSON of operations, wait for "APPLY".
```

```
Reconcile offline conversions from CRM dump {csv}. For each row:
hash email (sha256), find matching gclid in CRM table, if conversion_date_time
is older than 89 days SKIP and log. Build ClickConversion list, upload with
partial_failure=True, return per-row status.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` SDK | Official Google Ads API client (v17+) | `pip install google-ads` · https://developers.google.com/google-ads/api/docs/client-libs/python |
| `gads` CLI (community) | GAQL queries, mutations from shell | https://github.com/gtech-grace/google-ads-cli |
| `gaarf` (Google Ads API Report Fetcher) | Templated GAQL → BigQuery/CSV | `pip install google-ads-api-report-fetcher` · https://github.com/google/ads-api-report-fetcher |
| `gtag` debugger / Tag Assistant | Verify conversion firing | Chrome extension |
| `googleapis/google-ads-mcc-tools` | Manager-account scripts | https://github.com/googleads |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Google Ads API | SaaS API | Yes | Requires developer token + OAuth refresh token, dev token needs production approval for non-test accts |
| Google Analytics 4 Admin API | SaaS API | Yes | Required for programmatic GA4↔Ads linking |
| Hyros / TripleWhale | SaaS | Partial | Better for offline conversion ingestion than building yourself for e-com |
| Optmyzr | SaaS | Limited | UI-first; agents fight against its rule engine |
| Adalysis | SaaS | Limited | Audit-style; export reports, parse with agent |
| Google Sheets + Apps Script | OSS | Yes | Cheap automation for SMB accts: GAQL → sheet → email |

## Templates & scripts
See `templates.md` for bidding-strategy YAML and conversion-action JSON. Inline helper for the most common agent action — bulk-pause underperformers:

```python
def pause_underperformers(client, customer_id, days=30, max_cost_per_conv=0):
    """Pause campaigns spending money with zero or expensive conversions."""
    ga = client.get_service("GoogleAdsService")
    cs = client.get_service("CampaignService")
    q = f"""
        SELECT campaign.id, campaign.status, metrics.cost_micros,
               metrics.conversions, metrics.cost_per_conversion
        FROM campaign
        WHERE segments.date DURING LAST_{days}_DAYS
          AND campaign.status = 'ENABLED'
          AND metrics.cost_micros > 50000000
    """
    ops = []
    for row in ga.search(customer_id=customer_id, query=q):
        cpa = row.metrics.cost_per_conversion / 1_000_000 if row.metrics.conversions else 9e9
        if row.metrics.conversions == 0 or (max_cost_per_conv and cpa > max_cost_per_conv):
            op = client.get_type("CampaignOperation")
            op.update.resource_name = f"customers/{customer_id}/campaigns/{row.campaign.id}"
            op.update.status = client.enums.CampaignStatusEnum.PAUSED
            client.copy_from(op.update_mask, {"paths": ["status"]})
            ops.append(op)
    if ops:
        cs.mutate_campaigns(customer_id=customer_id, operations=ops)
    return len(ops)
```

## Best practices
- Always set `partial_failure=True` on bulk mutations — one bad row shouldn't kill the batch; inspect `partial_failure_error` afterwards.
- Use `validate_only=True` for the first run of any new mutation flow; promote to real run only after a clean dry-run.
- Pin Smart Bidding tCPA changes to ≤ 15-20% per step and wait 7 days between changes; bigger jumps reset learning.
- Always send `currency_code` on offline conversions even if account currency is the same — saves silent rejects on multi-currency MCCs.
- Keep one "shadow" campaign on Manual CPC as a control when running tROAS — useful for diagnosing whether a downturn is bidding or market.
- Set `click_through_lookback_window_days` to match your actual sales cycle, not the 30-day default — too long inflates DDA-fed Smart Bidding.

## AI-agent gotchas
- Agents love to "optimize" by setting tCPA = current CPA; that's the floor, not a target — drop 10-15% below current to push, or volume craters.
- Don't let an agent flip a campaign from MaxConv to tCPA mid-week without checking conversion volume — if < 30 conv/30d, it'll throttle hard.
- `change_status` events are the canonical audit trail — log every agent-driven mutation as a separate annotation, otherwise root-cause analysis becomes guesswork.
- Watch for `RESOURCE_TEMPORARILY_UNAVAILABLE` on `mutate_*` — Google Ads API is eventually consistent; retry with jitter, don't loop tight.
- Human-in-loop checkpoint: any change to `bidding_strategy_type` on a campaign with > $X/day spend OR > 7 days of learning. Cheap mutations (negatives, bid adjustments, copy) can run unattended.
- An agent uploading offline conversions can double-count if it doesn't dedupe by `(gclid, conversion_action, conversion_date_time)` — Google does NOT dedupe for you across uploads.

## References
- https://developers.google.com/google-ads/api/docs/start (API overview)
- https://developers.google.com/google-ads/api/docs/conversions/upload-clicks
- https://developers.google.com/google-ads/api/docs/migration/best-practices
- https://support.google.com/google-ads/answer/7065882 (Smart Bidding strategy guide)
- https://github.com/google/ads-api-report-fetcher
