<!-- purpose: minimal API Documentation artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-documentation.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Documentation — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-documentation-YYYY-MM-DD |
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
| publisher | docs platform (redocly, mintlify, scalar, mkdocs) |
| sections | ordered list of section ids: [quick-start, auth, endpoints, errors, sdks, changelog, support] |
| examples_per_endpoint | minimum 2 examples per endpoint (happy + at least one error) |
| error_catalogue_ref | path or URL to the canonical error catalogue |
| changelog_url | URL of the API changelog |
| freshness_check | CI doc-test name + cadence |
| evidence | list of {source, citation} pairs anchoring tool choices and section content |
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
- [ ] `scripts/validate-api-documentation.py --file artefact.json` exits 0
