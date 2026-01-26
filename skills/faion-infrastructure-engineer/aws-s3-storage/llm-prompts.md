# AWS S3 LLM Prompts

## Bucket Setup

### Create Secure Bucket

```
Create an S3 bucket named "{bucket_name}" in {region} with:
- Default encryption using SSE-KMS with a new KMS key
- S3 Bucket Keys enabled for cost optimization
- Versioning enabled
- Block all public access
- Bucket policy enforcing HTTPS only
- Access logging to a separate logging bucket

Use Terraform/CloudFormation and follow AWS security best practices.
```

### Migrate Bucket to New Storage Class

```
Create a lifecycle policy for bucket "{bucket_name}" that:
- Transitions objects in "data/" to Standard-IA after 30 days
- Transitions to Glacier after 90 days
- Transitions to Deep Archive after 365 days
- Handles non-current versions (Glacier after 30 days, expire after 365)
- Aborts incomplete multipart uploads after 7 days
- Cleans up expired delete markers

Provide AWS CLI commands.
```

## Security

### Audit Bucket Security

```
Audit the security configuration of S3 bucket "{bucket_name}":
1. Check encryption settings (default encryption, bucket key)
2. Check public access settings (block public access)
3. Analyze bucket policy for overly permissive access
4. Check versioning and MFA delete status
5. Review access logging configuration
6. Check for VPC endpoint usage

Provide AWS CLI commands for the audit and recommendations.
```

### Harden Bucket Policy

```
Create a hardened bucket policy for "{bucket_name}" that:
- Denies all non-HTTPS requests
- Denies requests without encryption header
- Restricts access to specific IAM roles: {role_arns}
- Restricts access to VPC endpoint: {vpce_id}
- Allows CloudFront distribution: {distribution_arn}

Follow AWS security best practices and principle of least privilege.
```

### Enable MFA Delete

```
Enable MFA delete on versioned bucket "{bucket_name}":
1. Verify versioning is enabled
2. Create the MFA delete configuration
3. Document the process for deleting versions with MFA
4. Create IAM policy for users who can delete versions

Note: MFA delete must be enabled by root account credentials.
```

## Replication

### Setup Cross-Region Replication

```
Configure cross-region replication from "{source_bucket}" ({source_region}) to "{destination_bucket}" ({dest_region}):
- Replicate all objects
- Enable Replication Time Control (RTC) for 15-minute SLA
- Replicate delete markers
- Change storage class to Standard-IA at destination
- Handle KMS encrypted objects
- Create required IAM role and policies

Provide Terraform configuration.
```

### Setup Same-Region Replication for Compliance

```
Configure same-region replication for compliance:
- Source: "{source_bucket}"
- Destination: "{destination_bucket}" (different AWS account: {dest_account})
- Replicate only objects with tag "compliance=true"
- Enable replication metrics
- Configure destination bucket policy for cross-account access

Provide AWS CLI commands.
```

## Cost Optimization

### Analyze and Optimize Costs

```
Analyze storage costs for bucket "{bucket_name}" and create optimization plan:
1. Get current storage class distribution
2. Identify objects that could be transitioned
3. Find incomplete multipart uploads
4. Calculate potential savings with lifecycle policies
5. Evaluate Intelligent-Tiering for unknown access patterns

Provide S3 Storage Lens configuration and lifecycle recommendations.
```

### Enable Intelligent-Tiering

```
Configure S3 Intelligent-Tiering for bucket "{bucket_name}":
- Enable Archive Access tier (90 days)
- Enable Deep Archive Access tier (180 days)
- Set minimum object size to 128 KB
- Configure for specific prefix: "{prefix}"

Provide AWS CLI commands and cost comparison.
```

## Disaster Recovery

### Create DR Strategy

```
Design a disaster recovery strategy for bucket "{bucket_name}":
- Primary region: {primary_region}
- DR region: {dr_region}
- RPO: {rpo_hours} hours
- RTO: {rto_hours} hours

Include:
1. Replication configuration
2. Backup strategy using S3 Batch Operations
3. Failover procedure
4. Failback procedure
5. Testing plan
6. Monitoring and alerting

Provide Terraform configuration and runbook.
```

### Restore from Glacier

```
Create a restore procedure for objects in Glacier/Deep Archive:
- Bucket: "{bucket_name}"
- Prefix: "{prefix}"
- Restore type: {Expedited|Standard|Bulk}
- Restore duration: {days} days

Include:
1. List objects to restore
2. Initiate batch restore
3. Monitor restore progress
4. Access restored objects
5. Cleanup after restore

Provide AWS CLI commands and Python script.
```

## Access Patterns

### Static Website Hosting with CloudFront

```
Configure S3 bucket "{bucket_name}" for static website hosting with CloudFront:
- Block direct S3 access (OAC only)
- Enable HTTPS with custom domain: {domain}
- Configure caching headers
- Setup error pages
- Enable logging

Provide Terraform configuration for S3, CloudFront, and Route 53.
```

### Setup S3 Access Points

```
Create S3 Access Points for bucket "{bucket_name}" for different use cases:
1. "analytics-ap": Read-only access for data team (IAM role: {analytics_role})
2. "app-ap": Read/write for application (VPC: {vpc_id})
3. "backup-ap": Write-only for backup service

Configure network origin controls and access point policies.
```

## Monitoring and Compliance

### Setup Monitoring

```
Configure comprehensive monitoring for bucket "{bucket_name}":
1. S3 access logging to central logging bucket
2. CloudTrail data events for audit trail
3. CloudWatch metrics and alarms:
   - 4xx/5xx error rates
   - Request latency
   - Bytes uploaded/downloaded
4. S3 Storage Lens dashboard
5. EventBridge notifications for specific events

Provide Terraform configuration and CloudWatch dashboard JSON.
```

### Compliance Report

```
Generate a compliance report for bucket "{bucket_name}" covering:
1. Encryption status (at rest and in transit)
2. Access control (IAM policies, bucket policies, ACLs)
3. Public accessibility
4. Versioning and data protection
5. Logging and audit trail
6. Data residency and replication
7. Lifecycle management

Map findings to: {compliance_framework} (e.g., SOC 2, HIPAA, PCI-DSS)
```

## Troubleshooting

### Debug Access Issues

```
Debug access denied errors for bucket "{bucket_name}":
1. Identify the principal making requests
2. Check IAM policies attached to the principal
3. Analyze bucket policy
4. Check S3 Block Public Access settings
5. Verify VPC endpoint policies (if applicable)
6. Check KMS key policy (if encrypted)
7. Review SCPs at organizational level

Provide AWS CLI commands for each step and decision tree.
```

### Investigate Replication Issues

```
Troubleshoot replication failures for bucket "{bucket_name}":
1. Check replication configuration status
2. Verify IAM role permissions
3. Check source and destination bucket versioning
4. Verify KMS key permissions for encrypted objects
5. Review replication metrics in CloudWatch
6. Check for failed replication notifications

Provide diagnostic commands and resolution steps.
```

---

*AWS S3 LLM Prompts | faion-infrastructure-engineer*
