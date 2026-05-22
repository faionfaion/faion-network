---
slug: gha-security-hardening
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Pin every action reference to a 40-char SHA, not a tag.
content_id: "33e6ebe3a6959840"
tags: [github-actions, security, oidc, supply-chain, permissions]
---
# GitHub Actions Security Hardening

## Summary

**One-sentence:** Pin every action reference to a 40-char SHA, not a tag.

**One-paragraph:** Pin every action reference to a 40-char SHA, not a tag. Set permissions: explicitly at the job level with minimum required scope. Use OIDC (id-token: write) for all cloud authentication — no long-lived AWS_ACCESS_KEY, GCP_SERVICE_ACCOUNT_KEY, or AZURE_CREDENTIALS secrets. Never use pull_request_target without a protected environment gate. Run actionlint and gha-audit.py on every PR touching .github/.

## Applies If (ALL must hold)

- Any workflow that runs on a PR or push to a shared branch — SHA pinning is non-negotiable.
- Any workflow that deploys to a cloud provider — replace long-lived credentials with OIDC.
- Any workflow that uses third-party Marketplace actions — audit before use, pin by SHA.
- Repos with required status checks — add actionlint as a required check.

## Skip If (ANY kills it)

- Throwaway local-only repos with no secrets — overhead is not worth it, but still good practice.
- Disabling OIDC for a provider that does not support it — use short-lived API tokens from a secrets manager instead.

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
