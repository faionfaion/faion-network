<!-- purpose: Minimum filled-in BR/SH/SR triple. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1500 tokens when loaded as context -->

# Minimum filled-in BR/SH/SR triple.

> Skeleton for `requirements-documentation`. Replace placeholders with real engagement data; commit alongside the parent record.

## Smoke-test record

```json
{
  "req_id": "SR-0042",
  "type": "SR",
  "title": "Partial-invoice exception path",
  "description": "System must support partial-invoice exception path with auditor-visible justification field.",
  "acceptance_criteria": [
    "Given an invoice with partial payment, the system records the operator's justification.",
    "Given missing justification, the system blocks the operation."
  ],
  "source_citations": [
    "ES-0014",
    "ES-0017"
  ],
  "status": "approved",
  "owner": "Finance Ops",
  "parent": "BR-0019"
}
```
