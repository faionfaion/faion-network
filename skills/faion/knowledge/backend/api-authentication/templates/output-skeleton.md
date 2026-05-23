<!-- purpose: minimal API Authentication artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: spec artefact validated by scripts/validate-api-authentication.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Authentication — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-authentication-YYYY-MM-DD |
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
| mechanism | api-key|jwt-bearer|oauth2-code-pkce|mtls|hybrid |
| token_ttl_minutes | access token TTL; conventionally 5-15 for JWT |
| refresh_rotation | true when refresh tokens rotate on every use |
| allowed_algorithms | explicit allowlist (no alg:none); e.g. [RS256, EdDSA] |
| claims_validated | subset of [iss, aud, exp, nbf, kid] — all five required in production |
| storage | cookie-httponly|authorization-header|other (mobile) |
| negative_tests | list of test ids covering expired, wrong-aud, missing-scope, alg-none |
| rotation_plan | two-key window policy + cadence |
| evidence | list of {source, citation} pairs anchoring each non-trivial field |
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
- [ ] `scripts/validate-api-authentication.py --file artefact.json` exits 0
