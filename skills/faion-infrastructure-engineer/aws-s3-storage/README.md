# AWS S3 Storage

> **Entry Point:** Invoked via [faion-infrastructure-engineer](../CLAUDE.md)

## Overview

Amazon S3 (Simple Storage Service) best practices for secure, cost-optimized, and resilient object storage. Covers bucket policies, encryption, lifecycle management, and cross-region replication.

## Quick Reference

| Topic | Description |
|-------|-------------|
| Bucket Policies | IAM-based access control, HTTPS enforcement |
| Encryption | SSE-S3, SSE-KMS, DSSE-KMS, S3 Bucket Keys |
| Lifecycle | Storage class transitions, expiration rules |
| Replication | CRR, SRR, multi-destination replication |

## Key Concepts

### Storage Classes

| Class | Use Case | Retrieval |
|-------|----------|-----------|
| S3 Standard | Frequent access | Immediate |
| S3 Intelligent-Tiering | Unknown patterns | Automatic |
| S3 Standard-IA | Infrequent access | Immediate |
| S3 One Zone-IA | Non-critical infrequent | Immediate |
| S3 Glacier Instant | Archive with instant access | Milliseconds |
| S3 Glacier Flexible | Archive | Minutes to hours |
| S3 Glacier Deep Archive | Long-term archive | 12-48 hours |

### Encryption Options (2025/2026)

| Type | Key Management | Cost |
|------|----------------|------|
| SSE-S3 | AWS managed (default) | Free |
| SSE-KMS | Customer managed via KMS | KMS charges |
| DSSE-KMS | Dual-layer KMS | Higher KMS charges |
| SSE-C | Customer provided | Free (deprecated for new buckets Apr 2026) |

**Important:** Starting April 2026, SSE-C is disabled by default for new buckets. Must explicitly enable via `PutBucketEncryption` API.

### Replication Types

| Type | Description |
|------|-------------|
| SRR | Same-Region Replication |
| CRR | Cross-Region Replication |
| Multi-destination | Replicate to multiple buckets |

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-deployment and security checklists |
| [examples.md](examples.md) | CLI commands and code examples |
| [templates.md](templates.md) | CloudFormation, Terraform, bucket policies |
| [llm-prompts.md](llm-prompts.md) | Prompts for S3 tasks |

## Best Practices Summary

### Security

1. Enable default encryption (SSE-KMS for sensitive data)
2. Block public access at account and bucket level
3. Require HTTPS in bucket policies
4. Enable versioning with MFA delete for critical buckets
5. Use VPC endpoints for private access
6. Enable S3 access logging and CloudTrail

### Cost Optimization

1. Use lifecycle policies to transition objects
2. Enable S3 Intelligent-Tiering for unpredictable access
3. Abort incomplete multipart uploads (7-day rule)
4. Delete non-current versions and expired delete markers
5. Use S3 Bucket Keys to reduce KMS costs

### Resilience

1. Enable versioning for data protection
2. Use CRR for disaster recovery
3. Configure replication time control (RTC) for compliance
4. Test restore procedures regularly

## Related AWS Services

| Service | Integration |
|---------|-------------|
| CloudFront | CDN distribution |
| Lambda | Event-driven processing |
| Athena | SQL queries on S3 data |
| Glue | ETL and data catalog |
| EventBridge | Event notifications |

## Sources

- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [S3 Encryption Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/encryption-best-practices/s3.html)
- [S3 Lifecycle Policies](https://www.cloudoptimo.com/blog/s3-lifecycle-policies-optimizing-cloud-storage-in-aws/)
- [S3 Bucket Encryption Update (Nov 2025)](https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-s3-bucket-level-standardize-encryption-types/)
- [Wiz S3 Security Guide](https://www.wiz.io/academy/cloud-security/amazon-s3-security-best-practices)

---

*AWS S3 Storage Reference | faion-infrastructure-engineer*
