<!-- purpose: minimal API Testing artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-testing.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Testing — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-testing-YYYY-MM-DD |
| owner | named human (no group terms) |
| last_touched | ISO-8601 timestamp |
| template_version | 1.1.0 |
| status | draft \| ready_for_review \| approved \| archived |

## Inputs

- Triggering activity: [from AGENTS.md Applies If list]
- Source-of-truth refs: [list URLs / design-file ids / dashboard snapshots]

## Methodology fields

| Field | Purpose |
|-------|---------|
| api_id | service id or repo slug |
| pyramid | {unit, integration, contract, e2e} counts/percentages |
| frameworks | list of test frameworks per layer (pytest, schemathesis, pact, playwright) |
| negative_coverage | {4xx_required, 5xx_required, alg_none_required} booleans |
| contract_tests | {provider, consumers[], broker_url} |
| spec_conformance_tool | schemathesis|dredd|portman |
| ci_jobs | list of CI job names per layer |
| evidence | list of {source, citation} pairs anchoring layer counts and tool choices |
| status | draft|ready_for_review|approved|archived |

## Evidence

| Source | Citation |
|--------|----------|
| https://example.com/source-1 | verbatim quote |

## Self-check

- [ ] template_version pinned to 1.1.0
- [ ] owner is single named human (no team/us/tbd)
- [ ] every non-trivial field has ≥1 evidence row
- [ ] status is not approved unless a named reviewer signed off
- [ ] `scripts/validate-api-testing.py --file artefact.json` exits 0
