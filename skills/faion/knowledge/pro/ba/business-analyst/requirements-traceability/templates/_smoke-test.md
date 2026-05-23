<!-- purpose: Minimum filled-in RTM. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum filled-in RTM.

> Skeleton for `requirements-traceability`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "rtm_id": "RTM-2026Q2",
  "role_vocabulary_version": "v1.2",
  "edges": [
    {
      "from": "BR-0019",
      "to": "SR-0042",
      "from_role": "business_requirement",
      "to_role": "solution_requirement"
    },
    {
      "from": "SR-0042",
      "to": "TC-0103",
      "from_role": "solution_requirement",
      "to_role": "test_case"
    }
  ],
  "coverage": {
    "needs_with_tests_pct": 0.98,
    "tests_with_needs_pct": 0.95
  },
  "orphans": {
    "needs_without_tests": [
      "NFR-0007"
    ],
    "tests_without_needs": [
      "TC-0210"
    ]
  }
}
```
