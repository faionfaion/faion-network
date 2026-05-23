<!-- purpose: minimal API REST Design artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-rest-design.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API REST Design — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-rest-design-YYYY-MM-DD |
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
| base_url | https://api.example.com/v1 |
| resources | list of {name, collection_url, item_url, allowed_verbs} |
| verb_semantics | map verb → semantics (idempotent, safe, body-required) |
| status_code_map | map outcome → status code (created→201, validation-error→422, conflict→409) |
| idempotency_header | header name; conventionally Idempotency-Key on POST/DELETE |
| hateoas | true when responses include rel-link objects |
| evidence | list of {source, citation} pairs anchoring choices |
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
- [ ] `scripts/validate-api-rest-design.py --file artefact.json` exits 0
