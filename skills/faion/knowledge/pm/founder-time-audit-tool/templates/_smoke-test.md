<!-- purpose: Founder Time Audit Tool minimum viable filled-in report -->
<!-- consumes: same inputs as templates/founder-time-audit-tool.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/founder-time-audit-tool.md, scripts/validate-founder-time-audit-tool.py -->
<!-- token-budget-impact: ~400 tokens -->

# Founder Time Audit Tool — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `founder-time-audit-tool-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Founder Time Audit Tool to the smoke-test scope; serves as a fixture for `scripts/validate-founder-time-audit-tool.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
