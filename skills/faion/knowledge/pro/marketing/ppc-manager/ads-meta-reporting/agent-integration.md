# Agent Integration — Meta Ads Reporting & Analysis

## When to use
- Daily / weekly automated performance reports for stakeholders (executive summary, campaign trends, creative analysis).
- Diagnosing CPA spikes — running the symptom→cause flow (CTR, CVR, CPM, frequency) at scale.
- Multi-account agencies needing consolidated reports across many ad accounts.
- Building a single source of truth that reconciles Meta-reported numbers with GA4 and server-side revenue.
- Triggering automation rules: pause/scale/refresh when metrics cross thresholds.

## When NOT to use
- Single-account, single-stakeholder, < $50/day spend — Meta Ads Manager UI is enough; automation overhead exceeds benefit.
- Account in active learning phase (< 14 days) — daily reports tempt premature action; monitor only.
- Attribution-sensitive cases (e-com with long sales cycles) — platform-only reporting will mislead; use a proper MMM/MTA tool.

## Where it fails / limitations
- Meta Insights API has rate limits per ad account (~25 calls/hr for high-volume async); naive agent loops hit them on minute one.
- iOS 14.5+ cuts Meta-reported conversions by 15-40% vs server-side — reports comparing Meta to GA4 will look wrong even when both are correct.
- Default attribution window is now 7-day click + 1-day view; older reports use 28-day click which inflates everything 1.5-2x. Don't compare across windows.
- Breakdowns can't be combined freely — `placement` + `age` + `gender` together is forbidden, agent must split into multiple calls.
- Async insights jobs (>50 rows) take minutes; agents that timeout at 30s will silently lose data.
- Modeled conversions in Aggregated Event Measurement look real in reports but aren't deterministic — reconciliation will never be 100%.

## Agentic workflow
A reporting agent runs on a cron (daily/weekly): pulls Insights via API → joins with server-side conversion log → writes a structured report → posts to Slack/email. A diagnosis agent runs on-demand: receives a campaign ID + date range, walks the symptom tree (CPA up → CTR/CVR/CPM/frequency → root cause), proposes 2-3 actions. An action agent applies bounded changes (pause ads with CTR < 0.5% and spend > $X) inside guardrails, never raw-edits live campaigns without approval above $Y/day spend.

### Recommended subagents
- `faion-ads-agent` — Insights API pulls, breakdown queries, report formatting.
- `improver` — closes the loop: symptom → diagnosis → action plan.
- `faion-sdd-executor-agent` — gates auto-actions behind plan/approve/apply when spend > threshold.

### Prompt pattern
```
Pull last 14 days for ad account {id}, level=ad. Fields: spend, impressions,
clicks, ctr, cpc, cpm, actions:purchase, action_values:purchase, frequency.
Compute CVR = purchases / clicks. Output ranked CSV: best-CTR, worst-CPA,
high-frequency (>3). Then diagnose: which need creative refresh, audience
expansion, or pause.
```

```
Diagnose campaign {id}: CPA went from ${old} to ${new} over the last
{days} days. Walk the metrics tree (CTR, CVR, CPM, frequency, placement
breakdown). For each metric, state direction and magnitude. Conclude with
root cause (creative / landing / audience / fatigue) and 3 ranked actions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `facebook-business` Python SDK | Insights API + async jobs | `pip install facebook-business` |
| `facebook-nodejs-business-sdk` | Node Insights client | `npm i facebook-nodejs-business-sdk` |
| Supermetrics | SaaS connector → Sheets / BigQuery | https://supermetrics.com |
| Funnel.io | Multi-channel ETL | https://funnel.io |
| Looker Studio | Dashboarding on top of Insights | Free |
| Meta Ads MCP | Lets Claude/agents query Insights directly | https://github.com/pipeboard-co/meta-ads-mcp |
| `dlt` (data load tool) | OSS Python ETL with Meta source | `pip install dlt` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Meta Insights API | SaaS API | Yes | Sync for small queries, async (`AdReportRun`) for large breakdowns |
| Triple Whale | SaaS | Partial | E-com attribution, has API for top metrics |
| Northbeam | SaaS | Partial | MMM-style attribution; good ground truth for paid |
| Madgicx | SaaS | Limited | Rules engine; can conflict with agent actions |
| Polar Analytics | SaaS | Yes | Shopify-native, good API for joining ad spend with revenue |
| Supermetrics for Sheets | SaaS | Yes | Cheapest Meta-to-Sheets pipe for SMB |
| BigQuery + Meta connector | SaaS | Yes | Best for cross-account reporting at scale |

## Templates & scripts
See `templates.md` for weekly-report and creative-analysis layouts. Inline async-insights helper — required for multi-account or breakdown-heavy pulls:

```python
import time
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

def async_insights(account_id, params, token, poll=10, max_wait=600):
    """Run an async Insights job and poll until ready (avoids 30s timeouts)."""
    FacebookAdsApi.init(access_token=token)
    job = AdAccount(account_id).get_insights(params=params, is_async=True)
    job.api_get()
    waited = 0
    while job["async_status"] not in ("Job Completed", "Job Failed"):
        if waited >= max_wait:
            raise TimeoutError(f"Insights job stuck at {job['async_percent_completion']}%")
        time.sleep(poll); waited += poll; job.api_get()
    if job["async_status"] == "Job Failed":
        raise RuntimeError("Meta Insights job failed")
    return list(job.get_result())
```

## Best practices
- Always state the attribution window in every report (`7d_click + 1d_view`); a report with no window is uninterpretable.
- Reconcile against server-side ground truth weekly; if Meta-reported revenue is > 25% off Stripe, fix tracking before optimizing creative.
- Walk the diagnostic flow in order: CTR → CVR → CPM → frequency. Skipping steps leads to fixing the wrong thing.
- Cache Insights pulls for the same `(account, date_range, fields, breakdown)` key — agents that re-fetch the same data hit rate limits fast.
- Keep one "north-star" metric per campaign objective (CPA for Sales, CPL for Leads, ROAS for catalog) and grade everything against it. Vanity metrics distract.
- Send weekly reports on Monday morning local time, not the moment data closes — late Sunday data is often re-stated by Tuesday.

## AI-agent gotchas
- Insights API silently truncates results above row limits in sync mode — always use async for `level=ad` queries on large accounts.
- LLMs love to say "CTR is up" without checking statistical significance — a $20 ad with 3% CTR is noise. Require minimum spend / impressions per row.
- Modeled conversions inflate Meta-reported numbers; agents reporting "Meta says 100, GA4 says 65" without flagging modeled-vs-deterministic produce false alarms.
- Don't let an agent auto-pause based on 24h data — Meta's reporting is not final for 72h. Use rolling 7-day windows for action triggers.
- Human-in-loop checkpoint: any auto-action that pauses spend > $50/day, any rule that scales budget > 25% in one step.
- Watch for `Spending Limit Reached` errors — they look like "no spend" in reports, agents misdiagnose as audience fatigue.

## References
- https://developers.facebook.com/docs/marketing-api/insights/
- https://developers.facebook.com/docs/marketing-api/insights/best-practices
- https://www.facebook.com/business/help/458681590974355 (attribution settings)
- https://developers.facebook.com/docs/marketing-api/insights/breakdowns
- https://github.com/pipeboard-co/meta-ads-mcp
