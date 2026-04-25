# Agent Integration — Budget Optimization

## When to use
- Multi-channel paid programs (Google, Meta, LinkedIn, TikTok) needing systematic monthly reallocation.
- Scaling phase: efficient campaigns warrant 20-30% step-ups; you need a process, not gut.
- Cutting waste: tightening losers without killing learning.
- Quarterly planning: setting budget envelopes by channel, campaign type (prospecting/retargeting/brand), and testing reserve.
- Cross-channel attribution-aware reallocation (LTV-based, not last-click CPA).

## When NOT to use
- Single-channel single-campaign accounts — overkill; let platform CBO/Advantage+ Budget handle it.
- Accounts with <30 conversions/month per channel — too noisy to allocate by efficiency.
- Pure brand-awareness budgets where reach/frequency matter more than CPA — different framework needed.
- Pre-launch testing where every channel is new — keep equal split until 14d data exists.

## Where it fails / limitations
- Last-click CPA over-credits bottom-funnel channels (branded search, retargeting); without multi-touch attribution, agents systematically defund top-funnel.
- Diminishing-returns curves are channel-specific — 20% Meta scale ≠ 20% LinkedIn scale.
- Platform learning resets when daily budget changes >20% — aggressive reallocation breaks the optimizer.
- Cross-channel incrementality is real: cutting Meta brand-awareness can drop Google branded search 10-15% (proven by holdout tests).
- Seasonal effects mask trends; comparing September to October without YoY is misleading.
- Conversion-tracking gaps (iOS, ad-blockers, server-side delays) make CPA look 20-40% worse than reality.

## Agentic workflow
A monthly subagent run: ingest performance data from all channels via API → normalize to common metrics (CPA, ROAS, blended CAC) → cluster campaigns by intent (prospecting/retargeting/brand) → score each by efficiency vs. target → propose budget moves with caps (max ±25% step) → human approves → push budget changes via platform APIs. Weekly cadence is too aggressive; daily is destructive. Human-in-loop required for: changes above 25% step size, cuts to channels with <14d data, reallocations between platforms (one platform's loss may be another's gain).

### Recommended subagents
- A `multi-channel-budget-allocator` — pulls all channels into one normalized table, runs the 70-20-10 reallocation framework.
- A `diminishing-returns-curve-fitter` — fits log-curve (`CPA = a + b*log(spend)`) per campaign over last 90d to predict outcomes of scale steps.
- A `pacing-monitor` — daily: detects under/over-pacing, flags campaigns that will miss month-end budget by >10%.
- `faion-ads-agent` — applies budget changes via Google Ads API + Meta Marketing API + LinkedIn API.
- `faion-sdd-executor-agent` (existing) — runs monthly reallocation as SDD task with QA gates ("zero regressions on top-3 campaigns by spend").

### Prompt pattern
```
You are a budget reallocator. Inputs: 
- channel_perf: [{channel, campaign_id, spend, conv, cpa, roas, last_30d}]
- target_cpa, total_budget
Output JSON: {moves: [{campaign_id, current_budget, new_budget, delta_pct, rationale}],
              testing_reserve, hold_recommendations, risks}
Hard rules:
- No single change >25% step (preserve learning)
- Maintain ≥10% testing reserve
- Don't cut campaigns with <14d data unless CPA >2x target
- Flag any cross-channel rebalance for human approval
```

```
Diagnose pacing variance for account <id>.
Pull MTD spend, expected daily run rate, end-of-month projection.
For each campaign with variance >15%, output: {campaign, variance_pct, cause: 
  "creative_fatigue" | "audience_saturation" | "auction_pressure" | "tracking_drop" | "unclear",
  recommended_action}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `google-ads-python` | Read perf, mutate campaign budgets | `pip install google-ads` |
| `facebook_business` | Read insights, mutate ad-set/campaign daily_budget | `pip install facebook_business` |
| `linkedin-api` (official OAuth) | Read perf, update campaign daily budget | learn.microsoft.com/linkedin/marketing |
| `bq` CLI | Query unified BigQuery export across channels | cloud.google.com/bigquery |
| `dbt` | Cross-channel transformation (CPA, CAC, ROAS unified) | docs.getdbt.com |
| `pandas` / `polars` | Reallocation math, curve fitting | `pip install pandas polars` |
| `prophet` (Meta) | Forecasting spend pacing trends | `pip install prophet` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Funnel.io | SaaS | Yes — API | Multi-channel data warehouse |
| Supermetrics | SaaS | Yes — connectors | Sheets/BQ/Snowflake aggregation |
| Adriel | SaaS | Yes | Cross-channel dashboards + alerts |
| Triple Whale | SaaS | Yes | E-comm-focused MTA + budget recs |
| Northbeam | SaaS | Yes | DTC attribution + reallocation |
| Optmyzr | SaaS | Yes | Google Ads-focused budget rules |
| Google Sheets + Apps Script | SaaS | Yes — connectors | DIY allocation dashboards |
| Looker Studio | SaaS | Yes — Google connectors | Pacing dashboards |

## Templates & scripts
See `templates.md` and the README's "Monthly Budget Allocation" + "Weekly Reallocation Review" templates.

Inline reallocation calculator (pandas):

```python
# reallocate.py
import pandas as pd

def reallocate(df, target_cpa, total_budget, max_step_pct=0.25):
    """
    df columns: campaign_id, spend, conv, cpa, current_daily
    Returns suggested new daily budgets.
    """
    df = df.copy()
    df["efficiency"] = target_cpa / df["cpa"].replace(0, 1e9)
    # Tier classification
    def tier(e): return "scale" if e > 1.4 else ("hold" if e > 0.7 else ("trim" if e > 0.5 else "cut"))
    df["tier"] = df["efficiency"].apply(tier)
    # Step changes capped at max_step_pct
    step = {"scale": 1 + max_step_pct, "hold": 1.0, "trim": 1 - max_step_pct, "cut": 0.5}
    df["proposed"] = df["current_daily"] * df["tier"].map(step)
    # Rescale to total
    factor = total_budget / df["proposed"].sum()
    df["new_daily"] = (df["proposed"] * factor).round(2)
    df["delta_pct"] = ((df["new_daily"] - df["current_daily"]) / df["current_daily"] * 100).round(1)
    return df[["campaign_id", "tier", "current_daily", "new_daily", "delta_pct", "efficiency"]]
```

## Best practices
- Set targets BEFORE optimizing: target CPA = LTV / payback-period-multiple. Without a number, "optimization" is opinion.
- Compare campaigns by ROAS or CPA against target, not against each other — comparing two losers picks the less-bad one.
- Always reserve 10-15% for testing — without it, the program ossifies and cannot find new winners.
- Step size 20-30% max per change; preserve platform learning. Aggressive moves of 50-100% reset optimizer and waste 5-7 days.
- Holdout tests quarterly: pause 10% of channel for 2 weeks, measure incrementality. Last-click attribution overstates true contribution by 20-50% on average.
- Track CAC payback (months to recoup CAC), not just CPA. Two campaigns with same CPA but different LTV behave differently.
- Document every reallocation decision (commit message in a budget-tracking repo, or a Notion log) — pattern recognition over months requires memory.
- Coordinate with finance — if total monthly cap is hard, agents must respect it; auto-pause campaigns when 90% spent in MTD with 30% of month remaining.
- For seasonal businesses, build allocation curve from prior-year data, not flat MoM.

## AI-agent gotchas
- Each platform uses different units: Google Ads = micros (× 1M), Meta = cents (× 100), LinkedIn = local-currency floats. Mixing them in one calculation creates 4-6 orders of magnitude bugs.
- `daily_budget` vs `lifetime_budget` on Meta: setting one zeros the other; agents must preserve which mode the campaign is in.
- Google Ads campaign budgets can be `shared` across campaigns; mutating one campaign's "budget" actually mutates the shared budget — affects siblings.
- Account-level lifetime budget caps in Meta: agents pushing daily budgets that sum past the cap silently fail to deliver.
- Time zone effects: end-of-month spending varies depending on whether budgets cycle on UTC or account TZ; can be ±24h off.
- Currency conversion lag: cross-channel agents normalizing to USD must use a stable FX source (don't pull rates from random APIs); platform-reported metrics already use account currency.
- "Pacing" varies by platform: Meta uses standard/accelerated, Google has campaign-level + ad-group; agents conflating them break delivery.
- Diminishing-returns curves only apply within a channel-account; copying constants across accounts gives wrong forecasts.
- Conversion lag: 7-30 day attribution windows mean MTD CPA looks worse than reality early in month; agents reallocating Day-3 data over-cut healthy campaigns.
- Holdout tests cannot be fully agent-driven — selecting test cells, holding integrity, and reading results requires human judgment.
- Some platforms (TikTok, Reddit) have minimum daily budgets that floor reallocation — agents proposing $5/day on a platform with $20 floor get rejected.
- Setting `daily_budget=0` does not pause; it errors. Use status `PAUSED` to truly stop a campaign.

## References
- Google Ads budget reference: https://developers.google.com/google-ads/api/docs/campaigns/budgets
- Meta Campaign Budget Optimization: https://www.facebook.com/business/help/153514848493595
- LinkedIn budget management: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/manage-campaigns
- Diminishing returns in paid media (Nielsen MMM): https://www.nielsen.com/insights/2023/marketing-mix-modeling/
- Incrementality testing: https://www.thinkwithgoogle.com/marketing-strategies/measurement/incrementality-testing/
- LTV:CAC framework: https://www.klipfolio.com/resources/kpi-examples/saas/ltv-to-cac
