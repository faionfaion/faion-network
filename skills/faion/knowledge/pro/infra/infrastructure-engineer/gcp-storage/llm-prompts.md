# GCP Cloud Storage LLM Prompts

## Bucket Design

### Prompt: Design Storage Architecture

```
Design a GCP Cloud Storage architecture for the following requirements:

Application: [describe application]
Data types: [files, logs, backups, media, etc.]
Access patterns: [frequency, read/write ratio]
Retention requirements: [compliance, legal holds]
Geographic requirements: [regions, latency needs]
Security requirements: [encryption, access control]
Budget constraints: [monthly budget]

Provide:
1. Bucket structure (separate buckets by purpose)
2. Storage class recommendations
3. Lifecycle rules
4. IAM strategy
5. Encryption approach (GMEK vs CMEK)
6. CDN integration (if applicable)
7. Cost estimate
```

### Prompt: Optimize Storage Costs

```
Analyze and optimize costs for the following GCP Cloud Storage setup:

Current buckets:
- [bucket1]: [size], [storage class], [access frequency]
- [bucket2]: [size], [storage class], [access frequency]

Current monthly cost: [amount]
Egress patterns: [internal, cross-region, internet]
Compliance requirements: [retention periods]

Provide:
1. Storage class optimization opportunities
2. Lifecycle rule recommendations
3. Estimated savings
4. Implementation plan
5. Monitoring approach for ongoing optimization
```

## Security Configuration

### Prompt: Security Audit

```
Perform a security audit for GCP Cloud Storage bucket:

Bucket name: [name]
Current configuration:
- Public access: [yes/no]
- IAM bindings: [list principals and roles]
- Encryption: [GMEK/CMEK/CSEK]
- Versioning: [enabled/disabled]
- Logging: [enabled/disabled]
- VPC Service Controls: [yes/no]

Compliance requirements: [SOC2, HIPAA, PCI-DSS, etc.]

Provide:
1. Security issues found
2. Risk severity for each issue
3. Remediation steps
4. Recommended security hardening
5. Monitoring recommendations
```

### Prompt: Design CMEK Strategy

```
Design a CMEK encryption strategy for GCP Cloud Storage:

Project: [project-id]
Buckets: [list buckets and their purposes]
Compliance requirements: [regulatory requirements]
Key rotation requirements: [frequency]
Geographic constraints: [regions]

Provide:
1. KMS keyring structure
2. Key naming convention
3. Key rotation schedule
4. IAM bindings for service agents
5. Terraform code
6. Key management procedures
7. Disaster recovery for keys
```

### Prompt: IAM Strategy

```
Design an IAM strategy for GCP Cloud Storage:

Buckets:
- [bucket1]: [purpose, sensitivity level]
- [bucket2]: [purpose, sensitivity level]

Access requirements:
- Application services: [list services and their needs]
- Human users: [roles/teams and their needs]
- External integrations: [third-party services]

Security requirements:
- Least privilege: [strict/moderate]
- Audit requirements: [logging needs]
- Conditional access: [IP restrictions, etc.]

Provide:
1. Custom IAM roles (if needed)
2. IAM bindings per bucket
3. Service account design
4. Workload Identity Federation (if applicable)
5. Access review process
```

## Lifecycle Management

### Prompt: Design Lifecycle Rules

```
Design lifecycle rules for GCP Cloud Storage bucket:

Bucket purpose: [describe use case]
Data types: [file types and sizes]
Access patterns:
- Hot data: [0-X days, frequency]
- Warm data: [X-Y days, frequency]
- Cold data: [Y-Z days, frequency]
- Archive: [>Z days]

Retention requirements: [legal/compliance]
Deletion policy: [when data can be deleted]
Versioning needs: [version retention]

Provide:
1. Lifecycle configuration JSON
2. Storage class transitions with timing
3. Version retention rules
4. Deletion rules
5. Cost impact analysis
6. Testing approach
```

### Prompt: Migrate Storage Classes

```
Plan a storage class migration for GCP Cloud Storage:

Current state:
- Bucket: [name]
- Storage class: [current class]
- Size: [total size]
- Object count: [number]
- Access patterns: [describe]

Target state:
- Storage class strategy: [describe desired state]
- Timeline: [migration window]
- Budget for migration: [if applicable]

Constraints:
- Downtime tolerance: [acceptable downtime]
- Access during migration: [requirements]

Provide:
1. Migration approach (lifecycle vs rewrite)
2. Step-by-step plan
3. Cost analysis (migration vs savings)
4. Rollback plan
5. Verification steps
```

## CDN Integration

### Prompt: Design CDN Architecture

```
Design Cloud CDN integration for GCP Cloud Storage:

Use case: [static assets, media streaming, downloads]
Content types: [file types and sizes]
Geographic distribution: [target regions/countries]
Traffic patterns: [requests/day, bandwidth]
Origin bucket: [bucket name and location]

Requirements:
- Latency requirements: [target latency]
- Cache hit ratio target: [percentage]
- Content updates frequency: [how often content changes]
- Security: [signed URLs, Cloud Armor]

Provide:
1. Architecture diagram (text-based)
2. Cache configuration recommendations
3. TTL strategy by content type
4. Cache invalidation strategy
5. Load balancer configuration
6. Cloud Armor rules (if needed)
7. Terraform code
8. Cost estimate
```

### Prompt: Optimize CDN Performance

```
Optimize Cloud CDN configuration for GCP Cloud Storage:

Current setup:
- Backend bucket: [name]
- Cache mode: [current mode]
- Current TTLs: [values]
- Cache hit ratio: [current percentage]

Performance issues:
- [describe observed issues]

Traffic analysis:
- Top requested paths: [paths]
- Cache miss patterns: [describe]

Provide:
1. Root cause analysis
2. TTL optimization recommendations
3. Cache key configuration
4. Content versioning strategy
5. Monitoring dashboard design
6. Performance benchmarks to track
```

## Troubleshooting

### Prompt: Debug Access Issues

```
Debug GCP Cloud Storage access issues:

Error message: [exact error message]
Operation: [upload/download/list/delete]
Bucket: [bucket name]
Object path: [if applicable]
Principal: [user/service account]
Method: [console/gcloud/API/client library]

Current configuration:
- IAM bindings: [relevant bindings]
- Bucket settings: [relevant settings]
- VPC Service Controls: [yes/no, perimeter details]

Provide:
1. Likely root causes
2. Diagnostic commands to run
3. Resolution steps for each cause
4. Prevention recommendations
```

### Prompt: Debug Performance Issues

```
Debug GCP Cloud Storage performance issues:

Symptoms:
- Operation: [upload/download/list]
- Latency observed: [value]
- Expected latency: [value]
- Throughput observed: [value]
- Expected throughput: [value]

Configuration:
- Bucket location: [region]
- Client location: [region/on-prem]
- Object sizes: [typical sizes]
- Concurrency: [parallel operations]
- Network path: [VPC, internet, interconnect]

Provide:
1. Diagnostic approach
2. Commands to gather metrics
3. Potential bottlenecks
4. Optimization recommendations
5. Performance testing approach
```

## Migration

### Prompt: Plan Data Migration

```
Plan data migration to GCP Cloud Storage:

Source:
- Platform: [AWS S3/Azure Blob/on-prem/other]
- Size: [total data size]
- Object count: [number of objects]
- Largest objects: [max sizes]
- Access during migration: [requirements]

Target:
- Bucket: [name or to be created]
- Region: [target region]
- Storage class: [target class]
- Encryption: [requirements]

Constraints:
- Migration window: [available time]
- Bandwidth: [available bandwidth]
- Downtime tolerance: [acceptable downtime]
- Budget: [migration budget]

Provide:
1. Migration approach (Transfer Service/gsutil/custom)
2. Pre-migration checklist
3. Step-by-step migration plan
4. Parallel vs sequential strategy
5. Verification approach
6. Cutover plan
7. Rollback plan
```

## Terraform Generation

### Prompt: Generate Terraform

```
Generate Terraform code for GCP Cloud Storage:

Requirements:
- Bucket name: [name]
- Region: [region]
- Storage class: [class]
- Versioning: [yes/no]
- Lifecycle rules: [describe rules]
- Encryption: [GMEK/CMEK]
- IAM bindings: [list principals and roles]
- CDN integration: [yes/no]
- Labels: [key-value pairs]

Standards:
- Module structure: [yes/no]
- Variable naming: [convention]
- Output requirements: [what to expose]

Provide:
1. Complete Terraform code
2. Variables file
3. Outputs file
4. Example tfvars
5. README with usage instructions
```

---

*GCP Cloud Storage LLM Prompts v2.0*
