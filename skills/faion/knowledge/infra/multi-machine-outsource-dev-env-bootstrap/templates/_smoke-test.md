<!--
purpose: smoke-test fixture for multi-machine-outsource-dev-env-bootstrap
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-multi-machine-outsource-dev-env-bootstrap.py`
depends-on: templates/spec.md
token-budget-impact: ~250 tokens
-->

# Multi-Machine Outsource Dev Env Bootstrap — multi-machine-outsource-dev-env-bootstrap-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | multi-machine-outsource-dev-env-bootstrap-smoke-test |
| produces | spec |
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
