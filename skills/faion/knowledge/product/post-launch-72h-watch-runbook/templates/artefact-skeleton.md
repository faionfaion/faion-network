<!-- purpose: Post-Launch 72h Watch Runbook artefact skeleton -->
<!-- consumes: Prerequisites bundle (see AGENTS.md) -->
<!-- produces: artefact conforming to content/02-output-contract.xml (playbook-step) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Post-Launch 72h Watch Runbook — artefact skeleton

Fill every `<PLACEHOLDER>` per artefact; remove placeholders before commit.

## Required fields

- **runbook_id**: `<FILL>`
- **owner**: `<FILL>`
- **last_touched**: `<FILL>`
- **launch**: `<FILL>`
- **signals**: `<FILL>`
- **thresholds**: `<FILL>`
- **on_call_schedule**: `<FILL>`
- **rollback_path**: `<FILL>`

## Owner + cycle

- `owner`: `<email-or-handle>`
- `last_touched`: `<ISO-8601>`
- `template_version`: `1.1.0`
- `status`: `draft | ready_for_review | approved | archived`
