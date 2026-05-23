<!-- purpose: Minimum viable filled-in HITL spec -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=spec -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# human-in-the-loop-design smoke-test

Minimum viable filled-in spec artefact for the `human-in-the-loop-design` methodology.

Run: `python scripts/validate-human-in-the-loop-design.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "human-in-the-loop-design-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
