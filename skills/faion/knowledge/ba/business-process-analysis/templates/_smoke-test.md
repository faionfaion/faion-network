<!-- purpose: Minimum viable filled-in process analysis. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable filled-in process analysis.

> Skeleton for `business-process-analysis`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "process_id": "P-0042",
  "name": "Order to Cash",
  "owner": "Finance Ops",
  "tier": "deep",
  "va_pct": 0.55,
  "bn_pct": 0.2,
  "nva_pct": 0.25,
  "baseline_metrics": {
    "volume_per_year": 120000,
    "cycle_time_minutes": 38,
    "cost_per_transaction": 4.2
  },
  "diff_table": [
    {
      "step": "Credit check",
      "current_actor": "AR clerk",
      "future_actor": "S/4 automated rule",
      "change_type": "automate",
      "risk": "model drift",
      "dependency": "S/4 credit module"
    }
  ],
  "framework_anchor": "APQC PCF 9.1.1",
  "deviation_log": [],
  "ownership_decision": "hybrid"
}
```
