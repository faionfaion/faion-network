<!-- purpose: minimal API Rate Limiting artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: config artefact validated by scripts/validate-api-rate-limiting.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Rate Limiting — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-rate-limiting-YYYY-MM-DD |
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
| algorithm | sliding-window|token-bucket|fixed-window|leaky-bucket |
| tiers | list of {tier, requests_per_minute, burst} |
| per_endpoint_multipliers | map of endpoint pattern → multiplier |
| backend | redis|memcached|in-memory|cloud-managed |
| headers | list of response header names emitted (Retry-After, RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset) |
| over_limit_response | {status, body_template} for 429 response |
| evidence | list of {source, citation} pairs anchoring quotas and algorithm choice |
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
- [ ] `scripts/validate-api-rate-limiting.py --file artefact.json` exits 0
