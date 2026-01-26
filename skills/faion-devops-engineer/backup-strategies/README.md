# Backup Strategies

Comprehensive backup implementation guide covering databases, filesystems, Kubernetes, and cloud environments with modern best practices including the 3-2-1-1-0 rule, immutable backups, and disaster recovery.

## Overview

Modern backup strategies have evolved beyond the traditional 3-2-1 rule to address ransomware threats and ensure zero-error recovery. This guide covers practical implementation patterns.

## Backup Strategy Evolution

| Strategy | Components | Use Case |
|----------|------------|----------|
| **3-2-1** | 3 copies, 2 media types, 1 offsite | Basic protection |
| **3-2-1-1** | + 1 immutable/air-gapped copy | Ransomware protection |
| **3-2-1-1-0** | + 0 recovery errors | Enterprise-grade |
| **4-3-2** | 4 copies, 3 locations (2 offsite) | High availability |
| **3-2-2** | 3 copies, 2 media, 2 offsite | Geographic redundancy |

## The 3-2-1-1-0 Rule

The gold standard for modern backup strategies:

| Component | Requirement | Implementation |
|-----------|-------------|----------------|
| **3** | Three copies of data | Production + 2 backups |
| **2** | Two different media types | Disk + Cloud/Tape |
| **1** | One copy offsite | Cloud storage or remote DC |
| **1** | One immutable/air-gapped | S3 Object Lock, WORM storage |
| **0** | Zero recovery errors | Automated verification |

## Immutable Backups

Backups that cannot be modified or deleted after creation.

**Implementation Options:**

| Technology | Provider | Method |
|------------|----------|--------|
| S3 Object Lock | AWS | Compliance/Governance mode |
| Immutable Blob | Azure | WORM policy |
| Bucket Lock | GCP | Retention policy |
| WORM Storage | On-prem | Hardware-enforced |

**Benefits:**
- Ransomware-proof (cannot encrypt/delete)
- Compliance (regulatory requirements)
- Integrity guarantee (tamper-evident)

## Air-Gapped Backups

Physically or logically isolated from production networks.

**Methods:**

| Type | Implementation | Security Level |
|------|----------------|----------------|
| Physical | Tape/disk offline storage | Highest |
| Logical | Network segmentation | High |
| Cloud | Separate account/region | Medium-High |

## Backup Types by Target

### Databases

| Database | Tool | Best Practice |
|----------|------|---------------|
| PostgreSQL | pg_dump, pg_basebackup | PITR with WAL archiving |
| MySQL | mysqldump, XtraBackup | Incremental with binlogs |
| MongoDB | mongodump | Oplog for PITR |
| Redis | RDB + AOF | Point-in-time snapshots |

### File Systems

| Tool | Strengths | Use Case |
|------|-----------|----------|
| Restic | Deduplication, encryption | General purpose |
| BorgBackup | Compression, space-efficient | Archive storage |
| rsync | Simple, proven | Basic file sync |
| rclone | Multi-cloud | Cloud storage |

### Kubernetes

| Tool | Scope | Features |
|------|-------|----------|
| Velero | Full cluster | Snapshots, migration |
| Kasten K10 | Enterprise | App-aware backups |
| Stash | Workloads | CRD-based |

### Cloud Native

| Provider | Service | Integration |
|----------|---------|-------------|
| AWS | AWS Backup | Cross-service, cross-region |
| Azure | Azure Backup | VM, SQL, files |
| GCP | Cloud Backup | Compute, SQL |

## RPO and RTO Guidelines

| Data Criticality | RPO | RTO | Strategy |
|------------------|-----|-----|----------|
| Critical | < 1 hour | < 1 hour | Continuous replication |
| Important | < 4 hours | < 4 hours | Frequent snapshots |
| Standard | < 24 hours | < 24 hours | Daily backups |
| Archive | < 1 week | < 1 week | Weekly full |

## Files in This Directory

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-implementation and verification checklists |
| [examples.md](examples.md) | Working scripts and configurations |
| [templates.md](templates.md) | Reusable templates for common scenarios |
| [llm-prompts.md](llm-prompts.md) | AI prompts for backup planning |

## Quick Decision Tree

```
What to backup?
├─ Database → Use native tools (pg_dump, mysqldump)
├─ Files → Use Restic or BorgBackup
├─ Kubernetes → Use Velero
└─ Cloud resources → Use provider backup service

Where to store?
├─ Same region → Fast recovery, disaster risk
├─ Cross-region → DR protection, higher cost
├─ Multi-cloud → Vendor independence, complex
└─ Air-gapped → Maximum security, slower recovery
```

## Key Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Backup success rate | 100% | < 99% |
| Backup age | < 24 hours | > 36 hours |
| Size variance | < 20% | > 50% drop |
| Recovery test | Monthly | Failed test |

## References

- [Restic Documentation](https://restic.readthedocs.io/)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/)
- [Velero Documentation](https://velero.io/docs/)
- [AWS Backup](https://docs.aws.amazon.com/aws-backup/)
- [PostgreSQL Backup and Recovery](https://www.postgresql.org/docs/current/backup.html)

## Sources

- [Acronis 3-2-1 Backup Strategy Guide 2025](https://www.acronis.com/en/blog/posts/backup-rule/)
- [Backblaze 3-2-1 Backup Strategy](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/)
- [Veeam 3-2-1-1-0 Rule](https://www.veeam.com/blog/321-backup-rule.html)
- [Keepit Air-Gapped Immutable Backups](https://www.keepit.com/blog/understanding-the-new-backup-rules/)
- [Impossible Cloud Golden Rules](https://www.impossiblecloud.com/blog/the-golden-rules-of-backup-strategy-from-3-2-1-to-3-2-1-1-0)
- [NAKIVO 3-2-1 Guide](https://www.nakivo.com/blog/3-2-1-backup-rule-efficient-data-protection-strategy/)
