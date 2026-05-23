<!-- purpose: Founder-as-PM Survival Kit minimum viable filled-in checklist -->
<!-- consumes: same inputs as templates/founder-as-pm-survival-kit.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/founder-as-pm-survival-kit.md, scripts/validate-founder-as-pm-survival-kit.py -->
<!-- token-budget-impact: ~400 tokens -->

# Founder-as-PM Survival Kit — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `founder-as-pm-survival-kit-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Founder-as-PM Survival Kit to the smoke-test scope; serves as a fixture for `scripts/validate-founder-as-pm-survival-kit.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
