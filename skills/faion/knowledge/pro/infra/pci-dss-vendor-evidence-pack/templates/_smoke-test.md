<!--
purpose: smoke-test fixture for pci-dss-vendor-evidence-pack
consumes: nothing; self-contained fixture
produces: minimum-viable filled instance; passes `scripts/validate-pci-dss-vendor-evidence-pack.py`
depends-on: templates/report.md
token-budget-impact: ~250 tokens
-->

# PCI-DSS Vendor Evidence Pack — pci-dss-vendor-evidence-pack-smoke-test

| Field | Value |
|-------|-------|
| artefact_id | pci-dss-vendor-evidence-pack-smoke-test |
| produces | report |
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
