<!-- purpose: minimal API Error Handling artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-error-handling.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Error Handling — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-error-handling-YYYY-MM-DD |
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
| envelope_standard | rfc7807|json-api|other (must be named explicitly) |
| type_uri_base | base URI for error type identifiers (https://api.example.com/errors/) |
| trace_header | request header name carrying the traceId (e.g. X-Request-Id, traceparent) |
| error_catalogue | list of {code, type_uri, title, status} entries — closed list |
| field_level_validation | true when validation errors include the `errors[]` field-level array |
| raw_exception_banned | must be true; raw stack traces in responses are forbidden |
| evidence | list of {source, citation} pairs anchoring catalogue entries |
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
- [ ] `scripts/validate-api-error-handling.py --file artefact.json` exits 0
