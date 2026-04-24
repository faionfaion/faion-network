# Backup Strategies LLM Prompts

AI prompts for backup planning, implementation, and troubleshooting.

## Backup Strategy Planning

### Prompt: Design Backup Strategy

```
Design a comprehensive backup strategy for the following system:

System Overview:
- Type: [e.g., E-commerce platform, SaaS application]
- Databases: [e.g., PostgreSQL 15, Redis, MongoDB]
- File Storage: [e.g., User uploads, static assets]
- Infrastructure: [e.g., Kubernetes on AWS, VMs on GCP]
- Data Volume: [e.g., 500GB database, 2TB files]
- Growth Rate: [e.g., 10% monthly]

Business Requirements:
- RPO Target: [e.g., 1 hour]
- RTO Target: [e.g., 4 hours]
- Compliance: [e.g., GDPR, HIPAA, SOC2]
- Budget: [e.g., $500/month]

Provide:
1. Recommended backup strategy (3-2-1, 3-2-1-1-0, etc.)
2. Specific tools for each component
3. Backup schedule (full, incremental, transaction logs)
4. Storage locations (local, cloud, immutable)
5. Retention policy
6. Estimated costs
7. Monitoring and alerting approach
8. Recovery testing schedule
```

### Prompt: Evaluate Existing Backup

```
Evaluate the following backup configuration against best practices:

Current Setup:
[Paste current backup configuration, scripts, or description]

Environment:
- Production/Staging/Dev
- Criticality: [Critical/Important/Standard]
- Compliance requirements: [List any]

Analyze:
1. Compliance with 3-2-1-1-0 rule
2. RPO/RTO achievability
3. Security gaps (encryption, access control)
4. Monitoring coverage
5. Recovery testing adequacy
6. Cost efficiency
7. Specific improvement recommendations
```

## Implementation Prompts

### Prompt: Generate Backup Script

```
Generate a production-ready backup script for:

Database: [e.g., PostgreSQL 15]
Environment: [e.g., Linux/Ubuntu 22.04]
Storage Targets:
- Local: [path]
- Cloud: [e.g., S3, GCS, Azure Blob]
- Immutable: [e.g., S3 Object Lock]

Requirements:
- Compression: [yes/no, algorithm]
- Encryption: [at rest, in transit]
- Retention: [X days local, Y days cloud]
- Parallelism: [number of threads]
- Bandwidth limit: [if any]
- Notification: [email, Slack, PagerDuty]

Include:
1. Error handling and retry logic
2. Logging with rotation
3. Metrics for Prometheus
4. Verification after backup
5. Cleanup of old backups
6. Idempotent execution (can run multiple times safely)
```

### Prompt: Kubernetes Backup Configuration

```
Generate Velero configuration for:

Cluster: [e.g., EKS, GKE, AKS, self-managed]
Namespaces to backup: [list]
Exclude namespaces: [list]

Storage Backend: [e.g., S3, GCS, Azure, MinIO]
Credentials: [how provided - secret, IRSA, workload identity]

Requirements:
- PVC backups: [yes/no, method - snapshots/restic]
- Schedule: [daily, weekly]
- Retention: [X days]
- Cross-cluster restore capability: [yes/no]
- Resource filters: [specific resources to include/exclude]

Provide:
1. Velero installation command/manifest
2. BackupStorageLocation configuration
3. VolumeSnapshotLocation configuration
4. Schedule manifests
5. RBAC configuration
6. Testing commands
```

### Prompt: Terraform Backup Infrastructure

```
Generate Terraform configuration for AWS Backup:

Resources to protect:
- RDS instances: [list or pattern]
- EBS volumes: [list or pattern]
- DynamoDB tables: [list or pattern]
- EFS filesystems: [list or pattern]
- S3 buckets: [list or pattern]

Requirements:
- Backup frequency: [daily, hourly, etc.]
- Retention: [X days warm, Y days cold, Z days delete]
- Cross-region copy: [yes/no, target region]
- Vault lock: [yes/no, retention period]
- Tagging strategy: [how resources are identified]

Include:
1. Backup vault with KMS encryption
2. Backup plan with multiple rules
3. Resource selection (tag-based and explicit)
4. IAM roles and policies
5. Cross-region vault (if needed)
6. Outputs for integration
```

## Disaster Recovery Prompts

### Prompt: DR Runbook Generation

```
Generate a disaster recovery runbook for:

Scenario: [e.g., Complete data center failure, Ransomware attack, Database corruption]

System Components:
- [List all components: databases, applications, storage]

Backup Sources:
- [List all backup locations and types]

Recovery Environment:
- Primary: [location/region]
- DR: [location/region]

Include:
1. Pre-requisites and assumptions
2. Step-by-step recovery procedure
3. Verification steps after each phase
4. Rollback procedures
5. Communication templates
6. Escalation path
7. Post-recovery validation checklist
8. Lessons learned template
```

### Prompt: Recovery Time Estimation

```
Estimate recovery time for the following scenario:

Data to Recover:
- Database size: [X GB]
- File storage size: [X GB]
- Number of services: [X]

Backup Locations:
- Local: [latency, bandwidth]
- Cloud: [region, storage class]
- Cross-region: [if applicable]

Infrastructure:
- Target environment: [specs]
- Network bandwidth: [Mbps]
- Parallelism capability: [concurrent restores]

Provide:
1. Estimated time for each recovery phase
2. Bottlenecks and how to address them
3. Optimization recommendations
4. Realistic RTO based on analysis
5. Parallel vs sequential recovery strategy
```

## Troubleshooting Prompts

### Prompt: Backup Failure Analysis

```
Analyze the following backup failure:

Error Message:
[Paste error message/log]

Context:
- Backup tool: [e.g., pg_dump, restic, velero]
- Target: [database/filesystem/kubernetes]
- Schedule: [when it runs]
- Last successful backup: [date/time]
- Recent changes: [any infrastructure/config changes]

Provide:
1. Root cause analysis
2. Immediate fix
3. Prevention measures
4. Monitoring improvements to catch earlier
5. Alternative approaches if issue is recurring
```

### Prompt: Backup Performance Optimization

```
Optimize backup performance for:

Current State:
- Backup duration: [X hours]
- Data size: [X GB]
- Tool: [backup tool]
- Target duration: [X hours]

Infrastructure:
- Source system: [specs]
- Network: [bandwidth]
- Storage: [type, performance]

Current Configuration:
[Paste current backup configuration]

Analyze and provide:
1. Bottleneck identification
2. Parallelization opportunities
3. Compression optimization
4. Network optimization
5. Scheduling optimization (backup windows)
6. Incremental/differential strategy improvements
7. Expected improvement percentages
```

## Compliance Prompts

### Prompt: Compliance Audit Preparation

```
Prepare backup documentation for compliance audit:

Compliance Framework: [e.g., SOC2, HIPAA, GDPR, PCI-DSS]

Current Backup Setup:
[Describe or paste configuration]

Required Documentation:
1. Backup policy document
2. Retention schedule justification
3. Encryption evidence
4. Access control documentation
5. Recovery test evidence
6. Monitoring and alerting proof

Generate:
1. Policy document template filled with details
2. Evidence collection checklist
3. Gap analysis against compliance requirements
4. Remediation recommendations
5. Audit response templates
```

### Prompt: Data Retention Policy

```
Design a data retention policy for:

Data Types:
- [Type 1]: [sensitivity, regulatory requirements]
- [Type 2]: [sensitivity, regulatory requirements]
- [Type 3]: [sensitivity, regulatory requirements]

Regulations:
- [List applicable: GDPR, HIPAA, SOX, etc.]

Business Requirements:
- [Legal hold requirements]
- [E-discovery needs]
- [Historical analysis needs]

Provide:
1. Retention periods for each data type
2. Justification for each period
3. Deletion procedures
4. Exception handling process
5. Documentation requirements
6. Implementation guidelines
```

## Cost Optimization Prompts

### Prompt: Backup Cost Analysis

```
Analyze and optimize backup costs:

Current Spending:
- Storage: $X/month
- Compute: $X/month (for backup jobs)
- Network: $X/month (egress)
- Tools/Licenses: $X/month

Data Profile:
- Total data: [X TB]
- Daily change rate: [X%]
- Retention: [X days]

Current Strategy:
[Describe backup frequency, retention, storage tiers]

Provide:
1. Cost breakdown by component
2. Storage tier optimization (hot/warm/cold/archive)
3. Deduplication potential
4. Compression improvements
5. Retention policy adjustments
6. Alternative tool/service recommendations
7. Projected savings
```

### Prompt: Multi-Cloud Backup Strategy

```
Design a multi-cloud backup strategy for:

Primary Cloud: [AWS/GCP/Azure]
Secondary Cloud: [AWS/GCP/Azure]

Requirements:
- Vendor lock-in avoidance
- Geographic redundancy
- Cost optimization
- Consistent tooling

Data Types:
- [List data types and locations]

Provide:
1. Tool selection (cloud-agnostic)
2. Storage mapping across clouds
3. Replication strategy
4. Cost comparison
5. Recovery procedures for each cloud
6. Monitoring across clouds
```

## Migration Prompts

### Prompt: Backup Migration Plan

```
Plan migration from current to new backup system:

Current System:
- Tool: [e.g., legacy backup tool]
- Storage: [location]
- Retention: [X backups]
- Total data: [X TB]

Target System:
- Tool: [e.g., modern backup tool]
- Storage: [location]
- Requirements: [list new requirements]

Constraints:
- Migration window: [X days/weeks]
- Budget: $X
- Downtime tolerance: [none/minimal/flexible]

Provide:
1. Migration phases
2. Parallel running strategy
3. Data migration approach
4. Validation procedures
5. Rollback plan
6. Cutover criteria
7. Post-migration verification
```
