<!--
purpose: smoke-test fixture for manual-override-ledger
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-manual-override-ledger.py`
depends-on: templates/decision-record.md
token-budget-impact: ~250 tokens
-->

# Manual Override Ledger — manual-override-ledger-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | manual-override-ledger-smoke-test |
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
