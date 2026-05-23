<!--
purpose: smoke-test fixture for observability-stack-decision-matrix
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-observability-stack-decision-matrix.py`
depends-on: templates/decision-record.md
token-budget-impact: ~250 tokens
-->

# Observability Stack Decision Matrix — observability-stack-decision-matrix-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | observability-stack-decision-matrix-smoke-test |
| produces | decision-record |
| owner | ruslan@faion.net |
| version | 1.0.0 |
| last_reviewed | 2026-05-23 |
| status | draft |

## Inputs used

- smoke-input — file://./smoke-input.json

## Decision

Smoke-test fixture; produced to exercise the validator end-to-end.

## Rationale

Fixture exercises the methodology shape: typed inputs, named owner, traceable decision. Cites smoke-input.

## Trace refs

- smoke-input.json
