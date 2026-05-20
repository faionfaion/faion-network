---
slug: rotation-evidence-template
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Rotation Evidence Template: defines the audit-grade record shape SOC-2 / ISO27001 require for each secret-rotation event so auditors get traceability, not screenshots.
content_id: "aca7a39cbefee452"
tags: [rotation-evidence-template, infra, pro]
---
# Rotation Evidence Template

## Summary

**One-sentence:** A typed, audit-grade record shape for every secret-rotation event (DB password, API key, signing key, cert) that SOC-2 / ISO27001 auditors can accept as evidence without follow-up questions.

**One-paragraph:** SOC-2 / ISO27001 demand evidence that secrets rotate on policy and that the rotation was both completed and verified. Most teams produce ad-hoc Slack threads or ticket comments that fail audit because they miss one of: cause (scheduled vs incident-triggered), prior-secret-decommission timestamp, dual-control attestation, or downstream-system reconciliation. This methodology defines the seven required fields, the allowed source-of-truth pointers (HashiCorp Vault audit log id, AWS KMS rotation event ARN, etc.), and the verification step that closes the record. Output is a single immutable rotation-evidence record per event, link-able from the rotation runbook and the audit response binder.

## Applies If (ALL must hold)

- a secret in scope for a compliance framework (SOC-2 CC6, ISO27001 A.10.1, PCI-DSS 3.6, etc.) is being rotated
- there is an authoritative system of record (Vault, KMS, secrets-manager) emitting an event id for the rotation
- the team performing the rotation has dual-control or named-approver capability
- tier == pro or higher

## Skip If (ANY kills it)

- the secret is out-of-scope for any compliance framework AND not customer-facing (use a lighter ops log instead)
- rotation is automated end-to-end and the system-of-record already emits a fully-typed audit event covering the seven fields — link it, do not duplicate
- the rotation is part of an active incident response — record minimally now, fill in evidence post-incident under r6

## Prerequisites

- rotation runbook reference (path + version)
- system-of-record event id for the rotation operation
- prior-secret identifier (last-4 or hash, never the plaintext)
- named approver(s) per dual-control policy
- list of downstream systems that consumed the prior secret

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/external-secrets-operator-recipe` | upstream rotation mechanism this evidence covers |
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: seven-required-fields, immutable-after-close, dual-control-attestation, downstream-reconciliation, prior-secret-decommission, incident-mode-flag | ~1200 |

## Related

- parent skill: `pro/infra/devops-engineer`
- upstream playbook: `role-devops-engineer/Secret rotation execution`
- sibling methodology: `pro/infra/cve-exception-template`
