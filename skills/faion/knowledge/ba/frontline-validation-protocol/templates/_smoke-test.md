<!-- purpose: Minimum viable filled-in report. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (report) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum viable filled-in report.

> Skeleton for `frontline-validation-protocol`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "validation_matrix": [
    {
      "variant_id": "V1",
      "operator_ids": [
        "op-1",
        "op-2"
      ],
      "methods_used": [
        "shadowing",
        "listening_session"
      ],
      "completed_date": "2026-05-12",
      "coverage_status": "complete"
    }
  ],
  "observation_log": [
    {
      "observation_id": "O-1",
      "operator_id": "op-1",
      "process_step": "approve-credit",
      "taxonomy_tag": "workaround",
      "note": "Operator bypasses system 2 via spreadsheet to meet SLA.",
      "timestamp": "2026-05-10T10:23:00Z"
    }
  ],
  "listening_session_log": [
    {
      "operator_id": "op-1",
      "session_date": "2026-05-11",
      "sequenced_after_observation": true
    }
  ],
  "reconciled_as_is": {
    "documented_version_ref": "as-is-v1.bpmn",
    "observed_divergences": [
      {
        "documented_step": "system-2 approval",
        "observed_step": "spreadsheet override",
        "operator_evidence_ids": [
          "O-1"
        ],
        "divergence_type": "workaround"
      }
    ],
    "evidence_links": [
      "O-1"
    ]
  },
  "signed_access_agreement": true
}
```
