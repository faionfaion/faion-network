<!--
purpose: smoke-test fixture for opentelemetry-collector-architecture
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-opentelemetry-collector-architecture.py`
depends-on: templates/spec.md
token-budget-impact: ~250 tokens
-->

# OpenTelemetry Collector Architecture — opentelemetry-collector-architecture-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | opentelemetry-collector-architecture-smoke-test |
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
