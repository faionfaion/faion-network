<!--
purpose: Per-model rollback procedure with named approver
consumes: Inputs declared in `AGENTS.md` Prerequisites.
produces: Filled artefact for `model-onboarding-checklist` matching `content/02-output-contract.xml`.
depends-on: `content/01-core-rules.xml`, `scripts/validate-model-onboarding-checklist.py`.
token-budget-impact: small (template fill ~300-600 tokens).
-->

# Rollback Plan

## Context

- slug: model-onboarding-checklist
- version: <semver>
- owner: <role:person>
- approver: <role:person>
- produced_at: <YYYY-MM-DDTHH:MM:SSZ>

## Body

<Fill the body following the procedure in `content/04-procedure.xml`. Cite at least one rule id from `content/01-core-rules.xml` per substantive paragraph.>

## Review

- cadence: monthly | quarterly
- next_review_at: <YYYY-MM-DD>
- outcome: <filled at next review>
