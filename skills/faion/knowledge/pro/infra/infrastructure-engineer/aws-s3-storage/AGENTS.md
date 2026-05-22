---
slug: aws-s3-storage
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: S3 bucket security, encryption, lifecycle policies, and cross-region replication best practices.
content_id: "44301306fddb235d"
tags: [s3, storage, aws, encryption, lifecycle]
---
# AWS S3 Storage: Security, Encryption, Lifecycle Policies, and Replication

## Summary

**One-sentence:** S3 bucket security, encryption, lifecycle policies, and cross-region replication best practices.

**One-paragraph:** S3 bucket security, encryption, lifecycle policies, and cross-region replication best practices. The concrete rule is: always block all public access at bucket AND account level; always enable default encryption (SSE-KMS for sensitive data, SSE-S3 for general); always configure lifecycle rules to abort incomplete multipart uploads within 7 days and transition objects to cheaper storage classes.

## Applies If (ALL must hold)

- Creating any S3 bucket (security defaults must be applied)
- Designing lifecycle rules for cost optimization (Standard → STANDARD-IA → Glacier)
- Setting up Cross-Region Replication (CRR) for disaster recovery
- Configuring bucket policies for cross-account access or HTTPS enforcement
- Choosing between SSE-S3, SSE-KMS, and DSSE-KMS encryption
- Integrating S3 with CloudFront (use OAC, not legacy OAI)

## Skip If (ANY kills it)

- CloudFront distribution configuration beyond S3 OAC — use aws-architecture-services
- Athena or Glue data pipeline patterns — those are analytics concerns, not storage concerns
- EBS or EFS storage decisions — different services for block/file storage
- GCP Cloud Storage — use gcp-storage methodology

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
