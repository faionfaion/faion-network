<!-- purpose: Minimum filled-in decision record + one deliverable. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (decision-record) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum filled-in decision record + one deliverable.

> Skeleton for `methodologies-detail`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "record_id": "FRS-0003",
  "ka": "KA-4",
  "frameworks": [
    "current-state",
    "future-state",
    "risk-analysis"
  ],
  "deliverables": [
    {
      "framework": "current-state",
      "template": "templates/current-state.md",
      "owner": "BA Lead"
    }
  ]
}
```
