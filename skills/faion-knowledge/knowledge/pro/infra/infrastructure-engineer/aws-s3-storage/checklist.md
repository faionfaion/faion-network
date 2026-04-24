# AWS S3 Checklist

## Pre-Deployment Checklist

### Bucket Configuration

- [ ] Bucket name follows naming convention (lowercase, no underscores)
- [ ] Region selected based on latency and compliance requirements
- [ ] Object Ownership set to "Bucket owner enforced" (ACLs disabled)
- [ ] Block Public Access enabled at bucket level
- [ ] Versioning enabled for critical data

### Encryption

- [ ] Default encryption configured (SSE-S3 or SSE-KMS)
- [ ] S3 Bucket Keys enabled for SSE-KMS to reduce costs
- [ ] KMS key policy allows S3 service principal
- [ ] DSSE-KMS considered for highly sensitive data
- [ ] SSE-C explicitly enabled if required (disabled by default Apr 2026)

### Access Control

- [ ] Bucket policy enforces HTTPS (aws:SecureTransport)
- [ ] IAM policies follow least privilege principle
- [ ] VPC endpoint configured for private access
- [ ] Cross-account access uses resource-based policies
- [ ] Presigned URLs have appropriate expiration

### Logging and Monitoring

- [ ] S3 access logging enabled (target bucket configured)
- [ ] CloudTrail data events enabled for audit
- [ ] CloudWatch metrics configured for bucket
- [ ] S3 Storage Lens enabled for analytics
- [ ] EventBridge notifications configured

## Security Checklist

### Bucket-Level Security

- [ ] Public access blocked at account level (S3 Block Public Access)
- [ ] Public access blocked at bucket level
- [ ] Bucket policy denies non-HTTPS requests
- [ ] No wildcard principals in bucket policy
- [ ] MFA Delete enabled for versioned critical buckets

### Object-Level Security

- [ ] Default encryption enforced
- [ ] Object Lock configured for WORM compliance (if required)
- [ ] Legal holds configured for litigation (if required)
- [ ] Presigned URL expiration under 1 hour for sensitive data

### Network Security

- [ ] VPC endpoint (Gateway or Interface) configured
- [ ] Endpoint policy restricts access to specific buckets
- [ ] Security groups configured for Interface endpoints
- [ ] S3 Access Points used for granular access patterns

### Compliance

- [ ] AWS Config rules enabled:
  - [ ] s3-bucket-server-side-encryption-enabled
  - [ ] s3-bucket-ssl-requests-only
  - [ ] s3-bucket-public-read-prohibited
  - [ ] s3-bucket-public-write-prohibited
  - [ ] s3-bucket-logging-enabled
  - [ ] s3-bucket-versioning-enabled
- [ ] Security Hub controls enabled for S3
- [ ] Trusted Advisor checks reviewed

## Lifecycle Policy Checklist

### Transitions

- [ ] Transition rules match access patterns
- [ ] Minimum object size for transitions considered (128 KB)
- [ ] Transition costs calculated (retrieval + request fees)
- [ ] Days between transitions respect minimums:
  - [ ] Standard to Standard-IA: 30 days minimum
  - [ ] Standard-IA to Glacier: 30 days after previous transition

### Expiration

- [ ] Expiration rules for temporary data (logs, temp files)
- [ ] Non-current version expiration configured
- [ ] Expired delete markers cleanup enabled
- [ ] Incomplete multipart upload abort rule (7 days recommended)

### Versioning Considerations

- [ ] Separate rules for current vs non-current versions
- [ ] Non-current versions transition to cheaper storage
- [ ] Maximum non-current versions limit set
- [ ] Non-current version expiration after transition period

## Replication Checklist

### Prerequisites

- [ ] Versioning enabled on source bucket
- [ ] Versioning enabled on destination bucket
- [ ] IAM role created with replication permissions
- [ ] KMS key policy allows replication (if encrypted)

### Configuration

- [ ] Replication rule scope defined (prefix/tags or entire bucket)
- [ ] Destination storage class selected
- [ ] Replica ownership configured (same or different account)
- [ ] Delete marker replication configured (if needed)
- [ ] Replication Time Control (RTC) enabled for compliance

### Cross-Account Replication

- [ ] Destination bucket policy allows source account
- [ ] Replica modification sync configured
- [ ] KMS key shared or replicated across accounts

### Monitoring

- [ ] S3 Replication metrics enabled
- [ ] CloudWatch alarms for replication latency
- [ ] Failed replication notifications configured

## Cost Optimization Checklist

- [ ] S3 Intelligent-Tiering for unpredictable access patterns
- [ ] Lifecycle policies for known access patterns
- [ ] S3 Bucket Keys enabled for SSE-KMS buckets
- [ ] Incomplete multipart uploads aborted after 7 days
- [ ] S3 Storage Lens for cost analysis
- [ ] Requester Pays enabled for shared datasets
- [ ] Transfer Acceleration evaluated for global uploads

## Disaster Recovery Checklist

- [ ] CRR configured to DR region
- [ ] RTO/RPO requirements documented
- [ ] Replication lag acceptable for RPO
- [ ] DR bucket tested for failover
- [ ] Restore procedures documented and tested
- [ ] Glacier retrieval times acceptable for RTO

---

*AWS S3 Checklist | faion-infrastructure-engineer*
