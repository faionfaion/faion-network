<!-- purpose: Minimum viable filled-in unit-economics report -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=report -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# inference-cost-unit-economics smoke-test

Minimum viable filled-in report artefact for the `inference-cost-unit-economics` methodology.

Run: `python scripts/validate-inference-cost-unit-economics.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "inference-cost-unit-economics-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
