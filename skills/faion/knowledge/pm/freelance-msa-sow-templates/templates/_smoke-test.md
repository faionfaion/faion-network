<!-- purpose: Freelance MSA + SOW Templates minimum viable filled-in spec -->
<!-- consumes: same inputs as templates/freelance-msa-sow-templates.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/freelance-msa-sow-templates.md, scripts/validate-freelance-msa-sow-templates.py -->
<!-- token-budget-impact: ~400 tokens -->

# Freelance MSA + SOW Templates — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `freelance-msa-sow-templates-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Freelance MSA + SOW Templates to the smoke-test scope; serves as a fixture for `scripts/validate-freelance-msa-sow-templates.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
