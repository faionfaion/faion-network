<!-- purpose: Minimum viable filled-in plugin-adoption ADR -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=decision-record -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# ai-plugin-ecosystem smoke-test

Minimum viable filled-in decision-record artefact for the `ai-plugin-ecosystem` methodology.

Run: `python scripts/validate-ai-plugin-ecosystem.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "ai-plugin-ecosystem-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
