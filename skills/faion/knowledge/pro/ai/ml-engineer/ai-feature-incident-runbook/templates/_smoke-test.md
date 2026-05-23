<!-- purpose: Minimum viable filled-in incident record -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=playbook-step -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# ai-feature-incident-runbook smoke-test

Minimum viable filled-in playbook-step artefact for the `ai-feature-incident-runbook` methodology.

Run: `python scripts/validate-ai-feature-incident-runbook.py --self-test` to exercise the validator against the built-in OK / BAD fixtures. This file is the human-readable counterpart.

## Example output (JSON)

```json
{
  "artefact_id": "ai-feature-incident-runbook-smoke-001",
  "produced_at": "2026-05-23T10:00:00Z",
  "validator_passed": true
}
```
