<!-- purpose: Freelancer Handover Bundle Template minimum viable filled-in checklist -->
<!-- consumes: same inputs as templates/freelancer-handover-bundle-template.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/freelancer-handover-bundle-template.md, scripts/validate-freelancer-handover-bundle-template.py -->
<!-- token-budget-impact: ~400 tokens -->

# Freelancer Handover Bundle Template — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `freelancer-handover-bundle-template-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Freelancer Handover Bundle Template to the smoke-test scope; serves as a fixture for `scripts/validate-freelancer-handover-bundle-template.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
