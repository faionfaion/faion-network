---
slug: aws-iam-security-foundations
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AWS security foundations span identity (IAM Identity Center, IRSA, least privilege), encryption (KMS at rest, TLS in transit, Secrets Manager), network controls (security groups, NACLs, PrivateLink, WAF), and detection (GuardDuty, Security Hub, Config).
content_id: "5a253f55108f3692"
tags: [aws, iam, security, encryption, secrets]
---
# AWS IAM and Security Foundations

## Summary

**One-sentence:** AWS security foundations span identity (IAM Identity Center, IRSA, least privilege), encryption (KMS at rest, TLS in transit, Secrets Manager), network controls (security groups, NACLs, PrivateLink, WAF), and detection (GuardDuty, Security Hub, Config).

**One-paragraph:** AWS security foundations span identity (IAM Identity Center, IRSA, least privilege), encryption (KMS at rest, TLS in transit, Secrets Manager), network controls (security groups, NACLs, PrivateLink, WAF), and detection (GuardDuty, Security Hub, Config). All layers must be active in production — each addresses a distinct failure mode that the others cannot compensate for.

## Applies If (ALL must hold)

- Designing the IAM layer for any new workload or environment baseline.
- Auditing an existing account for credential exposure, wildcard policies, or missing encryption.
- Setting up EKS clusters where pods need AWS service access (S3, Secrets Manager, DynamoDB).
- Compliance reviews that require encryption at rest and in transit evidence (KMS key IDs, ACM cert ARNs).

## Skip If (ANY kills it)

- Day-2 incident response — use incident response runbooks; this methodology is for design and baseline setup.
- Non-AWS clouds — GCP uses Workload Identity Federation; use gcp-security-iam instead.

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

- parent skill: `pro/infra/infrastructure-engineer/`
