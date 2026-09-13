<!-- purpose: Minimum viable filled-in unit-economics report -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=report -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# inference-cost-unit-economics smoke-test

Minimum viable filled-in report artefact for the `inference-cost-unit-economics` methodology: the valid example from `content/02-output-contract.xml`, trimmed to one feature.

Run: `python scripts/validate-inference-cost-unit-economics.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "report_id": "support-agent-unit-economics-2026q2",
  "as_of": "2026-06-30",
  "author": "ml-finance@acme.example",
  "window": {
    "start": "2026-06-01",
    "end": "2026-06-28",
    "days": 28
  },
  "token_source": "provider_usage",
  "headline_metric": "cost_per_successful_outcome",
  "price_sheet": [
    {
      "provider": "anthropic",
      "model_id": "claude-sonnet-4-20250514",
      "sheet_date": "2026-06-01",
      "sheet_url": "https://www.anthropic.com/pricing",
      "input_price_per_1m": 3.0,
      "output_price_per_1m": 15.0,
      "cached_input_price_per_1m": 0.3,
      "discount_pct": 10,
      "discount_kind": "committed_use"
    }
  ],
  "features": [
    {
      "feature_id": "support-agent",
      "success_definition": "ticket marked resolved by the customer within 24h of the last bot turn, no reopen within 7 days",
      "successful_outcomes": 41280,
      "cost_lines": {
        "input_tokens": 0.19,
        "output_tokens": 0.12,
        "cached_input_tokens": 0.02,
        "retrieval": 0.06,
        "tools": 0.05
      },
      "cost_per_call": 0.04,
      "cost_per_outcome": {
        "p50": 0.31,
        "p95": 0.97,
        "mean": 0.44
      },
      "retry_share_pct": 12,
      "first_action": "prompt",
      "revenue_basis": {
        "kind": "value_proxy",
        "derivation": "blended human-agent cost per resolved ticket from the Q1 support P&L, $4.10, used as value delivered"
      },
      "revenue_per_outcome": 4.1,
      "gross_margin_pct": 89.3,
      "target_gross_margin_pct": 85,
      "cost_ceiling_per_outcome": 0.62,
      "tail_dominated": false,
      "daily_spend_alert": {
        "threshold_kind": "pct_over_trailing_7d",
        "threshold": 30,
        "wired_to": "grafana:alerts/llm-spend-support-agent"
      }
    }
  ],
  "over_ceiling": []
}
```
