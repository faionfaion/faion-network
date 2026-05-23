-- purpose: Daily aggregator producing daily_attribution from raw_attribution.
-- consumes: raw_attribution(request_id, ts, tenant_id, feature, route, model, prompt_cache_hit, input_tokens, output_tokens, latency_ms, cost_usd, pricing_snapshot_id)
-- produces: daily_attribution(date, tenant_id, feature, model, calls, input_tokens, output_tokens, cache_hits, cost_usd)
-- depends-on: content/04-procedure.xml step 5
-- token-budget-impact: SQL-only; not loaded by agent

INSERT INTO daily_attribution (date, tenant_id, feature, model, calls, input_tokens, output_tokens, cache_hits, cost_usd)
SELECT
  CAST(ts AS DATE) AS date,
  tenant_id,
  feature,
  model,
  COUNT(*) AS calls,
  SUM(input_tokens) AS input_tokens,
  SUM(output_tokens) AS output_tokens,
  SUM(CASE WHEN prompt_cache_hit THEN 1 ELSE 0 END) AS cache_hits,
  ROUND(SUM(cost_usd), 4) AS cost_usd
FROM raw_attribution
WHERE ts >= CURRENT_DATE - INTERVAL '1' DAY
  AND ts <  CURRENT_DATE
GROUP BY 1, 2, 3, 4
ON CONFLICT (date, tenant_id, feature, model) DO UPDATE
SET calls = EXCLUDED.calls,
    input_tokens = EXCLUDED.input_tokens,
    output_tokens = EXCLUDED.output_tokens,
    cache_hits = EXCLUDED.cache_hits,
    cost_usd = EXCLUDED.cost_usd;
