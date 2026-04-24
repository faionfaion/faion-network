# LLM Prompts for Backup Implementation

## Analysis Prompts

### Backup Strategy Assessment

```
Analyze the backup requirements for this infrastructure:

**Context:**
- Databases: [PostgreSQL/MySQL/MongoDB]
- File storage: [Local/NFS/S3]
- Kubernetes: [Yes/No, number of clusters]
- Cloud provider: [AWS/GCP/Azure/On-prem]
- Data classification: [PII, financial, general]
- Compliance: [GDPR/HIPAA/SOC2/None]

**Questions to answer:**
1. What backup tools are most appropriate?
2. What RPO/RTO should be targeted?
3. What retention policy makes sense?
4. How should backups be tested?
5. What monitoring is needed?

Provide a backup strategy document with:
- Tool recommendations with rationale
- Backup schedule (hourly/daily/weekly/monthly)
- Retention policy
- Storage tier strategy (hot/warm/cold)
- DR considerations
- Cost estimate
```

### Backup Gap Analysis

```
Review this existing backup configuration and identify gaps:

**Current state:**
[Paste existing backup scripts/configs]

**Analyze for:**
1. Missing critical data sources
2. Inadequate retention
3. Missing encryption
4. No verification/testing
5. Single point of failure
6. Missing monitoring/alerting
7. Non-compliance with 3-2-1 rule
8. Performance issues

Provide:
- List of gaps with severity (critical/high/medium/low)
- Remediation recommendations
- Priority order for fixes
```

## Implementation Prompts

### Database Backup Script Generation

```
Generate a production-ready backup script for [PostgreSQL/MySQL/MongoDB]:

**Requirements:**
- Database name: [name]
- Backup location: [local path and/or S3 bucket]
- Retention: [X days local, Y days remote]
- PITR support: [Yes/No]
- Compression: [Yes/No]
- Encryption: [Yes/No, method]
- Notification: [email/slack/none]

**Include:**
1. Error handling with proper exit codes
2. Logging with timestamps
3. Metrics export for Prometheus
4. Cleanup of old backups
5. Verification step
6. Cloud upload (if applicable)

**Output:** Complete bash script with inline comments
```

### Velero Configuration

```
Generate Velero backup configuration for Kubernetes:

**Cluster details:**
- Kubernetes version: [version]
- Cloud provider: [AWS/GCP/Azure/on-prem]
- Storage class: [name]
- CSI driver: [Yes/No, which one]

**Backup requirements:**
- Namespaces: [list]
- Excluded namespaces: [list]
- Schedule: [cron expression]
- Retention: [days]
- Cross-region: [Yes/No]

**Generate:**
1. velero install command
2. BackupStorageLocation YAML
3. VolumeSnapshotLocation YAML
4. Schedule YAML for daily/weekly backups
5. Pre/post backup hooks for stateful apps
```

### Restic Setup

```
Create complete Restic backup setup:

**Environment:**
- Source paths: [list of directories]
- Exclude patterns: [list]
- Backend: [S3/B2/local/SFTP]
- Encryption: [Yes with password/No]

**Schedule:**
- Frequency: [hourly/daily]
- Retention: [daily/weekly/monthly counts]
- Verification: [frequency]

**Generate:**
1. Repository initialization script
2. Backup script with exclusions
3. Prune/forget script
4. Verification script
5. Systemd timer and service files
6. Environment file template
7. Prometheus metrics export
```

### Terraform AWS Backup

```
Generate Terraform configuration for AWS Backup:

**Resources to backup:**
- RDS instances: [list or tag-based]
- DynamoDB tables: [list or tag-based]
- EBS volumes: [list or tag-based]
- EFS filesystems: [list or tag-based]

**Policy:**
- Daily backup at: [time UTC]
- Weekly backup on: [day]
- Monthly backup on: [day]
- Cross-region copy to: [region]
- Lifecycle: [days to cold storage, days to delete]

**Generate:**
1. Backup vault with KMS encryption
2. DR region vault
3. Backup plan with all rules
4. Resource selection by tags
5. IAM roles and policies
6. SNS notifications
```

## Troubleshooting Prompts

### Backup Failure Analysis

```
Analyze this backup failure:

**Error log:**
[Paste error log]

**Context:**
- Backup tool: [tool name]
- Backup target: [description]
- Last successful backup: [date/time]
- Recent changes: [if any]

**Provide:**
1. Root cause analysis
2. Immediate fix steps
3. Prevention measures
4. Monitoring improvements to detect earlier
```

### Performance Optimization

```
Optimize backup performance for this scenario:

**Current state:**
- Backup duration: [X hours]
- Data size: [X GB/TB]
- Network bandwidth: [X Mbps]
- Backup window: [available hours]

**Tool configuration:**
[Paste current config]

**Analyze and suggest:**
1. Parallelization options
2. Compression tuning
3. Bandwidth optimization
4. Incremental/differential strategies
5. Schedule adjustments
6. Tool-specific optimizations
```

## Documentation Prompts

### Backup Runbook Generation

```
Generate a backup operations runbook for:

**System:** [description]
**Tools:** [list of backup tools]
**Stakeholders:** [who needs to be notified]

**Include sections:**
1. Daily operations checklist
2. Backup verification procedures
3. Restore procedures (step-by-step)
4. Failure response procedures
5. Escalation matrix
6. Contact information
7. Common issues and solutions
8. DR drill procedures
```

### Compliance Documentation

```
Generate backup compliance documentation for [GDPR/HIPAA/SOC2]:

**Current backup setup:**
[Describe or paste config]

**Document:**
1. Data classification and backup coverage
2. Encryption implementation (at rest and in transit)
3. Access control and audit logging
4. Retention policy compliance
5. Cross-border data transfer considerations
6. Incident response procedures
7. Regular testing evidence requirements
8. Vendor risk assessment (if using cloud)
```

## Migration Prompts

### Backup Tool Migration

```
Plan migration from [old tool] to [new tool]:

**Current state:**
- Tool: [old tool]
- Data volume: [size]
- Current retention: [policy]
- Existing backups: [number of snapshots]

**Target state:**
- Tool: [new tool]
- New retention: [policy]
- Migration window: [available time]

**Provide:**
1. Pre-migration checklist
2. Migration steps with rollback points
3. Parallel running period plan
4. Validation procedures
5. Cutover checklist
6. Post-migration cleanup
```

## Monitoring Prompts

### Prometheus Alerting Setup

```
Generate Prometheus alerting rules for backup monitoring:

**Backup jobs:**
[List of backup jobs with expected frequency]

**Alert requirements:**
- Backup age threshold: [hours]
- Size change threshold: [percentage]
- Duration threshold: [multiplier of average]

**Generate:**
1. PrometheusRule CRD YAML
2. Alert definitions with proper labels and annotations
3. Grafana dashboard JSON
4. Runbook links for each alert
```

## Cost Optimization Prompts

### Backup Cost Analysis

```
Analyze and optimize backup storage costs:

**Current usage:**
- Storage backend: [S3/GCS/Azure Blob]
- Current size: [TB]
- Monthly growth: [%]
- Current cost: [$]
- Retention: [policy]

**Analyze:**
1. Current cost breakdown by tier
2. Lifecycle optimization opportunities
3. Deduplication potential
4. Compression improvements
5. Retention policy review
6. Alternative storage classes
7. Projected costs with recommendations
```

---

## Usage Guidelines

1. **Be specific** - Include actual values, not placeholders
2. **Provide context** - More context = better recommendations
3. **Iterate** - Start broad, then refine with follow-up prompts
4. **Validate** - Always test generated scripts in non-production first
5. **Security** - Never include actual passwords or secrets in prompts

---

*LLM Prompts last updated: 2026-01*
