<!-- purpose: Escalation Decision Template minimum viable filled-in decision-record -->
<!-- consumes: same inputs as templates/escalation-decision-template.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/escalation-decision-template.md, scripts/validate-escalation-decision-template.py -->
<!-- token-budget-impact: ~400 tokens -->

# Escalation Decision Template — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `escalation-decision-template-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Escalation Decision Template to the smoke-test scope; serves as a fixture for `scripts/validate-escalation-decision-template.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
