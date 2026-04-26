# AWS S3 Storage

## Summary

S3 bucket security, encryption, lifecycle policies, and cross-region replication best practices. The concrete rule is: always block all public access at bucket AND account level; always enable default encryption (SSE-KMS for sensitive data, SSE-S3 for general); always configure lifecycle rules to abort incomplete multipart uploads within 7 days and transition objects to cheaper storage classes.

## Why

S3 misconfiguration (public access, missing encryption) is among the top causes of cloud data breaches. Lifecycle policies eliminate unbounded storage growth — unmanaged buckets accumulate incomplete multipart uploads and orphaned versions that cost money without delivering value. As of April 2026, SSE-C is disabled by default for new buckets.

## When To Use

- Creating any S3 bucket (security defaults must be applied)
- Designing lifecycle rules for cost optimization (Standard → STANDARD-IA → Glacier)
- Setting up Cross-Region Replication (CRR) for disaster recovery
- Configuring bucket policies for cross-account access or HTTPS enforcement
- Choosing between SSE-S3, SSE-KMS, and DSSE-KMS encryption
- Integrating S3 with CloudFront (use OAC, not legacy OAI)

## When NOT To Use

- CloudFront distribution configuration beyond S3 OAC — use `aws-architecture-services`
- Athena or Glue data pipeline patterns — those are analytics concerns, not storage concerns
- EBS or EFS storage decisions — different services for block/file storage
- GCP Cloud Storage — use `gcp-storage` methodology

## Content

| File | What's inside |
|------|---------------|
| `content/01-security.xml` | Block public access rule, encryption options (SSE-S3/KMS/DSSE-KMS, Apr 2026 SSE-C change), bucket policy HTTPS enforcement |
| `content/02-lifecycle-replication.xml` | Storage class transitions, multipart upload cleanup, versioning, CRR/SRR setup rules |
| `content/03-checklist.xml` | Pre-deployment security, data management, access pattern, and cost optimization checklists |

## Templates

none
