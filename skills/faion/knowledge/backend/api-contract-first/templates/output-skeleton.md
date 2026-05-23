<!-- purpose: minimal API Contract-First Workflow artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-contract-first.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Contract-First Workflow — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-contract-first-YYYY-MM-DD |
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
| spec_path | path to the OpenAPI 3.1 document (root + sharded refs) |
| generator | tool used to produce server stubs + SDKs (openapi-generator, oats, oazapfts) |
| ci_gates | list of CI jobs (spectral-lint, oasdiff-breaking-changes, contract-test) |
| runtime_validator | library used to validate responses against the spec (pydantic, jsonschema, openapi-core) |
| consumer_sdks | list of {language, generator-output-path} |
| evidence | list of {source, citation} pairs anchoring tool choices and CI gates |
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
- [ ] `scripts/validate-api-contract-first.py --file artefact.json` exits 0
