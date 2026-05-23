<!-- purpose: minimal API Gateway Patterns artefact skeleton conforming to content/02-output-contract.xml -->
<!-- consumes: input brief + source-of-truth refs declared in AGENTS.md prerequisites -->
<!-- produces: config artefact validated by scripts/validate-api-gateway-patterns.py -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500-1500 tokens when filled -->

# API Gateway Patterns — Artefact

| Field | Value |
|-------|-------|
| artefact_id | api-gateway-patterns-YYYY-MM-DD |
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
| gateway_id | ingress name (kong-prod, nginx-edge) |
| engine | kong|nginx|envoy|traefik|cloud-managed |
| routes | list of {path, upstream, timeout_ms, plugins[]} entries |
| auth_strategy | jwt|api-key|oauth-introspect|mtls |
| rate_limit_backend | redis|local-memory|cloud-managed |
| cors_policy | {allowed_origins, allowed_methods, allowed_headers, expose_headers, max_age_seconds} |
| observability | {access_log_format, metrics_exporter, trace_propagation} |
| evidence | list of {source, citation} pairs anchoring engine + plugin choices |
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
- [ ] `scripts/validate-api-gateway-patterns.py --file artefact.json` exits 0
