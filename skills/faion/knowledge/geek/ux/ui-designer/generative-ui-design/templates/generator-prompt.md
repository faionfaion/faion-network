<!-- purpose: Prompt skeleton with brand-token + must-not-have injection slots. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Generative UI Design — generator-prompt.md

Skeleton for the spec artefact this methodology produces.

Fill the fields below per task; the validator at `scripts/validate-generative-ui-design.py` enforces the schema in `content/02-output-contract.xml`.

## Required fields

- `brief_id` — fill from task context.
- `variants_generated` — fill from task context.
- `selected_variant_id` — fill from task context.
- `selection_rationale` — fill from task context.
- `labelled_not_production` — fill from task context.
- `generators_used` — fill from task context.
