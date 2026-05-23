<!-- purpose: Fixed-Price Three-Point Estimation minimum viable filled-in spec -->
<!-- consumes: same inputs as templates/fixed-price-three-point-estimation.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/fixed-price-three-point-estimation.md, scripts/validate-fixed-price-three-point-estimation.py -->
<!-- token-budget-impact: ~400 tokens -->

# Fixed-Price Three-Point Estimation — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `fixed-price-three-point-estimation-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Fixed-Price Three-Point Estimation to the smoke-test scope; serves as a fixture for `scripts/validate-fixed-price-three-point-estimation.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
