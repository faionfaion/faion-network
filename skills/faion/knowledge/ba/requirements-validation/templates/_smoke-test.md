<!-- purpose: Minimum filled-in sign-off pack. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum filled-in sign-off pack.

> Skeleton for `requirements-validation`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "pack_id": "VP-2026Q2",
  "scores": {
    "SR-0042": {
      "atomic": 5,
      "complete": 5,
      "consistent": 4,
      "correct": 5,
      "feasible": 4,
      "modifiable": 4,
      "prioritized": 5,
      "testable": 5,
      "traceable": 5,
      "unambiguous": 5
    }
  },
  "review_sessions": [
    {
      "session_id": "RS-0007",
      "scope": "Finance Ops",
      "technique": "inspection",
      "attendees": [
        "BA",
        "Sponsor",
        "QA Lead"
      ]
    }
  ],
  "sign_off": {
    "status": "approved",
    "signed_at": "2026-05-22",
    "signed_by": "Sponsor"
  },
  "dissent": []
}
```
