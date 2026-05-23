<!-- purpose: Follow-The-Sun Handoff Protocol minimum viable filled-in playbook-step -->
<!-- consumes: same inputs as templates/follow-the-sun-handoff-protocol.md -->
<!-- produces: smoke-test artefact for validator -->
<!-- depends-on: templates/follow-the-sun-handoff-protocol.md, scripts/validate-follow-the-sun-handoff-protocol.py -->
<!-- token-budget-impact: ~400 tokens -->

# Follow-The-Sun Handoff Protocol — smoke test

| Field | Value |
|-------|-------|
| artefact_id | `follow-the-sun-handoff-protocol-smoke-2026q2` |
| owner | `ops@example.com` |
| version | `1.0.0` |
| last_reviewed | `2026-05-23` |
| status | `active` |

## Decision

Apply Follow-The-Sun Handoff Protocol to the smoke-test scope; serves as a fixture for `scripts/validate-follow-the-sun-handoff-protocol.py --self-test`.

## Rationale

Smoke-test fixture references `inputs_used[0].name`. The artefact is a minimum-viable filled-in record so that the validator can exercise required-field + format + forbidden-pattern checks.

## Inputs used

- `smoke-input` — `repo://fixtures/smoke-input.yaml`

## Notes

Not a real engagement; do not link from production runbooks.
