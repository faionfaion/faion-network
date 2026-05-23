<!-- purpose: Minimum viable filled-in interface spec. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable filled-in interface spec.

> Skeleton for `interface-analysis`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "interface_id": "IF-0012",
  "name": "Order events to billing",
  "type": "system",
  "data_elements": [
    {
      "name": "order_id",
      "type": "string",
      "direction": "out"
    }
  ],
  "protocol": {
    "name": "kafka",
    "version": "3.6"
  },
  "frequency": "continuous",
  "volume": {
    "records_per_day": 250000,
    "peak_per_minute": 600
  },
  "security": {
    "authn": "mTLS",
    "authz": "RBAC",
    "encryption_in_transit": "TLS1.3",
    "encryption_at_rest": "AES-256",
    "data_classification": "PII"
  },
  "error_handling": {
    "retry": "exp-backoff",
    "dlq": "kafka:billing.dlq",
    "alerting": "pagerduty:billing-on-call"
  },
  "owner": "Order Platform"
}
```
