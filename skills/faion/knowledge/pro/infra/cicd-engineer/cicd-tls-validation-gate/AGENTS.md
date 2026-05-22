---
slug: cicd-tls-validation-gate
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Enforce TLS quality as a pipeline gate: run testssl.
content_id: "31e7af2246a37603"
tags: [tls, ci-gate, security-scanning, testssl, ssl-labs]
---
# TLS Validation Gate in CI/CD

## Summary

**One-sentence:** Enforce TLS quality as a pipeline gate: run testssl.

**One-paragraph:** Enforce TLS quality as a pipeline gate: run testssl.sh --severity HIGH and SSL Labs or sslyze against staging before every production promotion. Catch cipher regressions, broken chains, weak protocols, and HSTS misconfigurations before they reach users. Monitor Certificate Transparency logs for rogue issuance.

## Applies If (ALL must hold)

- Any deploy pipeline that provisions or modifies TLS configuration — run the gate on every change.
- Post-cert-rotation validation before declaring a rotation complete.
- Quarterly TLS hygiene review to catch protocol or cipher drift.
- New domain onboarding: verify the full chain, HSTS headers, and OCSP stapling before public launch.
- Post-nginx/HAProxy/Envoy upgrade to confirm TLS config survived the upgrade.

## Skip If (ANY kills it)

- Internal-only endpoints not reachable from the scanner — use local openssl s_client checks instead.
- Development environments where self-signed certs are intentional — the gate will always fail by design.
- Pre-commit hooks — TLS scanning requires a live running server; it is a post-deploy check, not a pre-commit check.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
