<!-- purpose: Per-customer invoice line skeleton with evidence + reason. -->
<!-- consumes: see content/02-output-contract.xml inputs for monthly-billing-batch-routine -->
<!-- produces: playbook-step -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Invoice Row

Filled-in skeleton for **Monthly Billing Batch Routine**. See `AGENTS.md` and `content/02-output-contract.xml` for the contract this artefact must satisfy.

## Section A

Replace this section with the required structured content per the schema.

## Section B — Evidence

Cite source per non-trivial field; un-anchored values are rejected by the validator.

## Section C — Status

`status: draft | ready_for_review | approved | sent | archived`
