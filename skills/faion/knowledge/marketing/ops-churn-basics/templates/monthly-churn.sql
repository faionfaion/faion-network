-- purpose: ops-churn-basics — monthly churn
-- consumes: see content/02-output-contract.xml inputs
-- produces: artefact aligned with content/02-output-contract.xml
-- depends-on: content/01-core-rules.xml
-- token-budget-impact: ~200-1000 tokens when loaded as context

-- monthly_churn.sql — voluntary vs involuntary customer + MRR churn
-- Input: subscription_state_daily(status, customer_id, mrr, d)
--        subscriptions(canceled_at, customer_id, mrr, cancel_reason)
-- Output: per-month churn rates split by voluntary/involuntary

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
         COUNT(DISTINCT a.customer_id)                                          AS start_customers,
         SUM(a.mrr)                                                             AS start_mrr,
         COUNT(DISTINCT e.customer_id) FILTER (WHERE e.kind = 'voluntary')      AS lost_vol_cust,
         COUNT(DISTINCT e.customer_id) FILTER (WHERE e.kind = 'involuntary')    AS lost_inv_cust,
         SUM(e.mrr)                    FILTER (WHERE e.kind = 'voluntary')      AS lost_vol_mrr,
         SUM(e.mrr)                    FILTER (WHERE e.kind = 'involuntary')    AS lost_inv_mrr
    FROM active_at_start a
    LEFT JOIN ended_in_month e USING (m)
   GROUP BY a.m
)
SELECT m,
       start_customers,
       start_mrr,
       ROUND(100.0 * lost_vol_cust  / NULLIF(start_customers, 0), 2) AS vol_cust_churn_pct,
       ROUND(100.0 * lost_inv_cust  / NULLIF(start_customers, 0), 2) AS inv_cust_churn_pct,
       ROUND(100.0 * lost_vol_mrr   / NULLIF(start_mrr, 0), 2)       AS vol_mrr_churn_pct,
       ROUND(100.0 * lost_inv_mrr   / NULLIF(start_mrr, 0), 2)       AS inv_mrr_churn_pct
  FROM agg
 ORDER BY m;
