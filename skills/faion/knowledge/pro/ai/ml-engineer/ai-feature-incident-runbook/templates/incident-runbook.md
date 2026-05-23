<!-- purpose: Runbook playbook-step skeleton -->
<!-- consumes: See content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=playbook-step -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200-1000 tokens when loaded as context -->

# Incident Runbook

_Skeleton for the `ai-feature-incident-runbook` methodology output. Fill each section; do not leave headings empty._

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
- Validator run: `python scripts/validate-ai-feature-incident-runbook.py --file out.json`
