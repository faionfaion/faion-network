<!--
purpose: smoke-test fixture for opentelemetry-rollout-runbook
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-opentelemetry-rollout-runbook.py`
depends-on: templates/playbook-step.md
token-budget-impact: ~250 tokens
-->

# OpenTelemetry Rollout Runbook — opentelemetry-rollout-runbook-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | opentelemetry-rollout-runbook-smoke-test |
| produces | playbook-step |
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
