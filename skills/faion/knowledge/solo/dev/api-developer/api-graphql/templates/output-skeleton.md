<!-- purpose: minimal API GraphQL Design artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-graphql.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API GraphQL Design — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-graphql-YYYY-MM-DD |
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
| schema_path | path to the SDL document (.graphql) — schema-first |
| dataloader_required | must be true; every relation field uses a loader |
| pagination_style | relay-cursor|offset|none (must be cursor for >100 items) |
| depth_limit | max query depth on public endpoint, conventionally 10 |
| complexity_limit | max query complexity (cost-weighted) |
| persisted_queries | true for production clients; ad-hoc allowed only in dev |
| introspection_in_prod | false on public endpoints |
| evidence | list of {source, citation} pairs anchoring decisions |
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
- [ ] `scripts/validate-api-graphql.py --file artefact.json` exits 0
