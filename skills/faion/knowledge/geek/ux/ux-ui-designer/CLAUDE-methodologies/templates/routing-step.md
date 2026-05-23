<!-- purpose: Playbook-step skeleton for the routing decision -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=playbook-step -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Routing Step

_Skeleton for the `CLAUDE-methodologies` methodology output. Fill each section; do not leave headings empty._

## Context

_Why this artefact exists. Link the upstream Applies-If conditions that triggered the methodology._

## Inputs

- Prerequisite artefact 1
- Prerequisite artefact 2

## Body

- Findings / decisions / steps (depending on produces type)

## Verdict

- Status: PASS / FAIL / WAIVED / APPROVE
- Rationale: prose, ≥20 words when verdict != APPROVE

## Provenance

- Author / reviewer / signers
- Timestamp
- Validator run: `python scripts/validate-CLAUDE-methodologies.py --file out.json`
