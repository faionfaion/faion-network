<!-- purpose: Minimum viable data dictionary. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable data dictionary.

> Skeleton for `data-analysis`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "name": "active_customer",
  "type": "boolean",
  "source": {
    "system": "billing",
    "table": "customer",
    "column": "is_active"
  },
  "scope": "billing",
  "quality": {
    "accuracy": 0.99,
    "completeness": 1.0,
    "consistency": 0.98,
    "timeliness": 0.95,
    "validity": 1.0,
    "uniqueness": 1.0
  },
  "owner": "Finance Ops",
  "rules": [
    {
      "rule_type": "validation",
      "expression": "is_active IN (true,false)"
    }
  ]
}
```
