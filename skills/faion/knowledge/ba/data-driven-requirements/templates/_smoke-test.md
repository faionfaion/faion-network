<!-- purpose: Minimum viable filled-in record. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable filled-in record.

> Skeleton for `data-driven-requirements`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "req_id": "BR-0042",
  "business_question": "Will inline previews reduce abandoned uploads on the SMB plan?",
  "baseline": {
    "metric": "upload_abandon_rate",
    "value": 0.27,
    "source": "amplitude",
    "as_of": "2026-04-15"
  },
  "target": {
    "metric": "upload_abandon_rate",
    "value": 0.18,
    "direction": "decrease",
    "by_when": "2026-07-15"
  },
  "instrumentation": {
    "events": [
      "upload_started",
      "upload_completed",
      "upload_abandoned"
    ],
    "properties": [
      "plan",
      "file_type"
    ],
    "dashboard": "amplitude/abandon-funnel"
  },
  "post_launch_window": "P14D",
  "rice": {
    "reach": 1200,
    "impact": 2,
    "confidence": 0.7,
    "effort": 5
  }
}
```
