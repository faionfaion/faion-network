---
slug: secrets-rotation-end-to-end
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Rotation lifecycle (cadence, dual-secret window, app-side reload, audit trail) — what secrets-management covers storage of but not rotation of.
content_id: "063dc8efd3f2ff6a"
tags: [secrets-rotation-end-to-end, infra, pro]
---

# Secrets Rotation End-to-End

## Summary

**One-sentence:** Rotation lifecycle (cadence, dual-secret window, app-side reload, audit trail) — what secrets-management covers storage of but not rotation of.

**One-paragraph:** secrets-management methodologies cover storage but not rotation lifecycle. Only cicd-cert-rotation-pipeline exists and that's TLS-only. Output: rotation calendar + dual-secret window + app-side reload spec + audit.

## Applies If (ALL must hold)

- production system with managed secrets (API keys, DB passwords, signing keys)
- compliance requirement OR explicit security policy mandates rotation
- team can enforce code-level secret-reload

## Skip If (ANY kills it)

- static config never accessed externally
- secrets stored in deprecated systems with no rotation plan — fix storage first
- regulated context requiring HSM + dedicated rotation tooling (defer to those)

## Prerequisites

- current secrets inventory with last-rotated dates
- secrets manager (Vault, AWS Secrets Manager, Doppler, 1Password)
- app-side secret-reload capability

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent skill — provides operating context for this methodology |
| `pro/sec/secrets-management` | peer methodology — produces inputs or consumes outputs |
| `pro/infra/cicd-cert-rotation-pipeline` | peer methodology — produces inputs or consumes outputs |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodology: `pro/sec/secrets-management`
- peer methodology: `pro/infra/cicd-cert-rotation-pipeline`
- peer methodology: `pro/infra/incident-response-blameless-playbook`
- external: https://owasp.org/www-community/vulnerabilities/Use_of_Hard-coded_Cryptographic_Key; https://www.vaultproject.io/docs/secrets
