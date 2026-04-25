# Agent Integration — Churn Basics

## When to use
- Subscription / usage-based business with a clear "active customer" status and billing events; you need a baseline churn rate before any prevention work.
- Quarterly review or board prep where you must report customer churn, MRR churn, NRR (net revenue retention), and segment-level breakdowns.
- Diagnosing whether retention pain is acquisition-mix (low-quality leads), onboarding (new-cohort drop), or aging-cohort (long-term decay).
- Pre-cursor to `ops-churn-prevention` (interventions) and `cohort-basics` (retention curves) — `ops-churn-basics` is the measurement and segmentation layer.

## When NOT to use
- One-off transactional businesses without subscriptions — there is no "churn", measure repeat-purchase rate.
- Free B2C with no revenue — focus on retention curves directly.
- Pre-revenue products — measuring churn is meaningless until cohort sizes stabilize.
- Annual-only contracts in early-stage where you have <2 renewal cycles of data — your sample is too small for a stable rate.

## Where it fails / limitations
- Net Revenue Retention can mask logo churn in expansion-led businesses; report both side by side.
- "Customer churn" is ambiguous — define cancel-date vs end-of-paid-period vs failed-payment threshold once and stick to it.
- Annualized monthly churn (`1 - (1-m)^12`) overstates pain when monthly churn includes seasonal noise.
- Voluntary vs involuntary churn (failed payments) need separate tracking; lumping them hides a fixable revenue leak.
- Health scores derived from short windows (7–30 days) drift fast after product changes; recalibrate quarterly.

## Agentic workflow
Use Claude subagents to (1) compute the canonical churn metrics from raw billing + activity data, (2) segment churn by reason / cohort / plan / channel, (3) build and maintain a health-score model, and (4) produce a written narrative. The agent stays read-only against the warehouse and outputs into BI-friendly artifacts (SQL views, dbt models, dashboards). Never let it modify billing or downgrade users.

### Recommended subagents
- `data-analyst` (sonnet) — SQL for churn definitions, segment cuts, NRR.
- `growth-marketer` (sonnet) — interpret segments, propose follow-ups (link to `ops-churn-prevention`).
- `cs-ops` (sonnet) — define health-score thresholds, at-risk lists for CSMs.
- `bi-engineer` (sonnet) — promote queries into dbt models with tests.

### Prompt pattern
```
Input: schema (subscriptions, invoices, events) + window (last 12 full months)
Goal: compute monthly customer-churn, MRR-churn, expansion-MRR, NRR
      segmented by (plan, signup_channel, signup_cohort_quarter)
Output: 1) read-only SQL (no DDL), 2) results table,
        3) 3 hypotheses ranked by ICE (impact, confidence, ease)
Constraint: voluntary and involuntary churn reported separately
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe` CLI | Pull subscription + invoice events for churn defs | `brew install stripe/stripe-cli/stripe` |
| `recurly` / `chargebee` API | Subscription state + cancel reasons | https://docs.recurly.com / https://apidocs.chargebee.com |
| `dbt-core` | Build canonical churn / NRR models | `pip install dbt-core` |
| `metabase` / `mode` API | Embed/auto-refresh churn dashboards | https://www.metabase.com/docs/latest/api-documentation |
| `posthog` CLI | Activity events feeding health score | `npm i -g posthog-node` |
| `bq` (BigQuery) | Run + schedule churn jobs | `gcloud components install bq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe Billing | SaaS | Yes — full API | Source of truth for subscription state |
| Chargebee | SaaS | Yes — REST | Subscription lifecycle, cancel reasons |
| Recurly | SaaS | Yes — REST | Mid-market subscription billing |
| ProfitWell / Paddle Retain | SaaS | Yes — REST | Free tier for retention metrics, recovery tooling |
| Vitally / Totango / Gainsight | SaaS | Yes — REST | Health scoring, CS playbooks |
| ChartMogul | SaaS | Yes — REST | Subscription analytics; canonical churn / NRR |
| Baremetrics | SaaS | Yes — REST | Churn dashboards, recovery |
| Mixpanel / Amplitude | SaaS | Yes — REST | Behavioral signals into health score |

## Templates & scripts
See `README.md` for the Churn Analysis Dashboard template and the Health Score formula. For a warehouse-native canonical churn calc:

```sql
-- monthly_churn.sql — voluntary vs involuntary, customer + MRR
WITH active_at_start AS (
  SELECT DATE_TRUNC('month', d) AS m, customer_id, mrr
    FROM subscription_state_daily
   WHERE status = 'active'
     AND d = DATE_TRUNC('month', d)
),
ended_in_month AS (
  SELECT DATE_TRUNC('month', canceled_at) AS m, customer_id, mrr,
         CASE WHEN cancel_reason = 'payment_failed' THEN 'involuntary'
              ELSE 'voluntary' END AS kind
    FROM subscriptions
   WHERE canceled_at IS NOT NULL
),
agg AS (
  SELECT a.m,
         COUNT(DISTINCT a.customer_id)            AS start_customers,
         SUM(a.mrr)                               AS start_mrr,
         COUNT(DISTINCT e.customer_id) FILTER (WHERE e.kind = 'voluntary')   AS lost_vol_cust,
         COUNT(DISTINCT e.customer_id) FILTER (WHERE e.kind = 'involuntary') AS lost_inv_cust,
         SUM(e.mrr)                    FILTER (WHERE e.kind = 'voluntary')   AS lost_vol_mrr,
         SUM(e.mrr)                    FILTER (WHERE e.kind = 'involuntary') AS lost_inv_mrr
    FROM active_at_start a
    LEFT JOIN ended_in_month e USING (m)
   GROUP BY a.m
)
SELECT m,
       start_customers, start_mrr,
       ROUND(100.0 * lost_vol_cust / NULLIF(start_customers,0), 2) AS vol_cust_churn_pct,
       ROUND(100.0 * lost_inv_cust / NULLIF(start_customers,0), 2) AS inv_cust_churn_pct,
       ROUND(100.0 * lost_vol_mrr  / NULLIF(start_mrr,0), 2)       AS vol_mrr_churn_pct,
       ROUND(100.0 * lost_inv_mrr  / NULLIF(start_mrr,0), 2)       AS inv_mrr_churn_pct
  FROM agg
 ORDER BY m;
```

## Best practices
- Define churn once, in writing, with cancel-date semantics and grace-period rules — and pin that definition in every dashboard description.
- Always report voluntary and involuntary churn separately; involuntary is recoverable with dunning + smart-retries.
- Pair customer churn with NRR; SaaS investors look at NRR ≥ 110% (good) and ≥ 120% (great) for product-led growth.
- Cohort-segment every reported number (signup quarter, plan, channel) — global numbers hide stage-specific problems.
- Run an exit survey on every cancel event with ≤6 reasons; free-text only as supplemental.
- Health-score thresholds should be backtested: retro-fit against last 90 days of actual churn before trusting the alerts.

## AI-agent gotchas
- Free-text "cancel reason" classification with LLMs hallucinates categories; force a fixed taxonomy in the prompt and require N/A when unclear.
- Agents will mix MRR churn and customer churn in the same sentence. Demand explicit metric names per number.
- Health-score "model" suggestions from LLMs are usually unweighted sums; do not adopt without backtesting against actual churn.
- "Reduce churn by X%" projections in agent output should be flagged as hypotheses, not forecasts — require an A/B-test plan before stating expected lift.
- Date-window bugs: the agent must pin `as_of` and "month boundary in customer timezone vs UTC" — small shifts produce large reported deltas.
- Annualized churn formulas are non-linear; agents that linearly extrapolate quarterly to annual will be wrong.

## References
- David Skok, "SaaS Metrics 2.0" — https://www.forentrepreneurs.com/saas-metrics-2/
- Lincoln Murphy, "Churn Rate Calculation" — https://sixteenventures.com
- ProfitWell, "Net Revenue Retention" guide — https://www.profitwell.com/recur/all/nrr
- Baremetrics, "Churn vs Retention" — https://baremetrics.com/blog
- Tomasz Tunguz, "The right way to measure churn" — https://tomtunguz.com
- ChartMogul, "Churn metrics for SaaS" — https://chartmogul.com/blog
