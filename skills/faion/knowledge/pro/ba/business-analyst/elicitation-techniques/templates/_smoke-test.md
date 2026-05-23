<!-- purpose: Minimum viable session artifact + REQ stub. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable session artifact + REQ stub.

> Skeleton for `elicitation-techniques`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "session_id": "ES-0014",
  "technique": "interview",
  "stakeholders": [
    {
      "name": "S. Operator",
      "role": "frontline"
    }
  ],
  "consent_signed": true,
  "pii_redacted": true,
  "notes": "Captured operator workaround on invoice exception path.",
  "req_stubs": [
    {
      "req_id": "BR-0019",
      "summary": "System must support partial-invoice exception path",
      "supporting_sessions": [
        "ES-0014",
        "ES-0017"
      ]
    }
  ]
}
```
