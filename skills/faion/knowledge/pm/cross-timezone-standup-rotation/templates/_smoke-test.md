<!-- purpose: Cross Timezone Standup Rotation minimum viable filled-in spec -->
<!-- consumes: same inputs as templates/cross-timezone-standup-rotation.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/cross-timezone-standup-rotation.md, scripts/validate-cross-timezone-standup-rotation.py -->
<!-- token-budget-impact: ~400 tokens -->

# Cross Timezone Standup Rotation — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `cross-timezone-standup-rotation-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Cross Timezone Standup Rotation to the smoke-test scope; serves as a fixture for `scripts/validate-cross-timezone-standup-rotation.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
