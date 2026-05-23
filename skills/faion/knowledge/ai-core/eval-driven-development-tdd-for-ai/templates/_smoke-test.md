<!-- purpose: Minimum viable filled-in eval spec -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=playbook-step -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# eval-driven-development-tdd-for-ai smoke-test

Minimum viable filled-in playbook-step artefact for the `eval-driven-development-tdd-for-ai` methodology.

Run: `python scripts/validate-eval-driven-development-tdd-for-ai.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "eval-driven-development-tdd-for-ai-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
