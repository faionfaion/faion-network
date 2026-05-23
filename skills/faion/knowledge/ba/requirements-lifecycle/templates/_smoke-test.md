<!-- purpose: Minimum filled-in lifecycle record. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum filled-in lifecycle record.

> Skeleton for `requirements-lifecycle`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "req_id": "SR-0042",
  "current_state": "verified",
  "transitions": [
    {
      "from": "draft",
      "to": "reviewed",
      "by": "BA Lead",
      "at": "2026-05-12",
      "evidence": "review-pack-v1"
    },
    {
      "from": "reviewed",
      "to": "approved",
      "by": "Sponsor",
      "at": "2026-05-14",
      "evidence": "signed-ac-form"
    }
  ],
  "change_log": []
}
```
