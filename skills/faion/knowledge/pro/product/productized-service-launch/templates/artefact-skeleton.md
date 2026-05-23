<!-- purpose: Productized Service Launch artefact skeleton -->
<!-- consumes: Prerequisites bundle (see AGENTS.md) -->
<!-- produces: artefact conforming to content/02-output-contract.xml (playbook-step) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Productized Service Launch — artefact skeleton

Fill every `<PLACEHOLDER>` per artefact; remove placeholders before commit.

## Required fields

- **launch_id**: `<FILL>`
- **owner**: `<FILL>`
- **last_touched**: `<FILL>`
- **design_ref**: `<FILL>`
- **pricing_page**: `<FILL>`
- **outbound_list**: `<FILL>`
- **beta_cohort**: `<FILL>`
- **ship_gates**: `<FILL>`
- **metrics_targets**: `<FILL>`

## Owner + cycle

- `owner`: `<email-or-handle>`
- `last_touched`: `<ISO-8601>`
- `template_version`: `1.1.0`
- `status`: `draft | ready_for_review | approved | archived`
