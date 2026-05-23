<!-- purpose: Minimum viable filled-in post-mortem -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=report -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# ai-post-mortem-template smoke-test

Minimum viable filled-in report artefact for the `ai-post-mortem-template` methodology.

Run: `python scripts/validate-ai-post-mortem-template.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "ai-post-mortem-template-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
