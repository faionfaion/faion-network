<!-- purpose: Engagement Handover Playbook minimum viable filled-in playbook-step -->
<!-- consumes: same inputs as templates/engagement-handover-playbook.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/engagement-handover-playbook.md, scripts/validate-engagement-handover-playbook.py -->
<!-- token-budget-impact: ~400 tokens -->

# Engagement Handover Playbook — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `engagement-handover-playbook-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Engagement Handover Playbook to the smoke-test scope; serves as a fixture for `scripts/validate-engagement-handover-playbook.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
