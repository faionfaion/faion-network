# Backup Basics

## Overview

Backup strategies ensure data protection, business continuity, and disaster recovery capabilities. This methodology covers backup fundamentals, types, core principles, and modern best practices for 2025-2026.

## When to Use

- Setting up data protection for applications
- Implementing disaster recovery (DR) plans
- Meeting compliance requirements (GDPR, HIPAA, SOC2)
- Protecting against ransomware and data loss
- Planning infrastructure migrations
- Configuring SaaS backup strategies

## Backup Types

| Type | Description | Pros | Cons | Frequency |
|------|-------------|------|------|-----------|
| Full | Complete copy of all data | Fast recovery, self-contained | Storage intensive, time consuming | Weekly/monthly |
| Incremental | Changes since last backup | Fast, storage efficient | Slower recovery, chain dependency | Daily/hourly |
| Differential | Changes since last full backup | Faster than full, easier recovery | Growing size over time | Daily |
| Snapshot | Point-in-time copy (COW) | Instant, space efficient | Same storage system risk | Hourly/on-demand |
| Continuous | Real-time data sync | Near-zero RPO | Complex, expensive | Continuous |

## The 3-2-1 Backup Rule

The foundational backup strategy:

```
3 copies of data
  1 primary (production)
  1 local backup
  1 offsite backup

2 different media types
  Disk storage
  Object storage / tape / cloud

1 offsite copy
  Different geographic location
```

## Modern Enhanced Strategies (2025-2026)

### 3-2-1-1-0 Strategy

Enhanced for ransomware protection:

| Component | Meaning |
|-----------|---------|
| 3 | Three copies of data |
| 2 | Two different media types |
| 1 | One offsite copy |
| 1 | One immutable or air-gapped copy |
| 0 | Zero errors after verification |

### 4-3-2 Strategy

For high-compliance, high-uptime environments:

| Component | Meaning |
|-----------|---------|
| 4 | Four copies of data |
| 3 | Three separate locations |
| 2 | Two offsite locations |

## Recovery Objectives

### RTO (Recovery Time Objective)

Time to restore operations after disaster:

| RTO Target | Backup Strategy | Cost |
|------------|-----------------|------|
| < 1 hour | Hot standby, continuous replication | High |
| 1-4 hours | Automated restore, frequent backups | Medium |
| 4-24 hours | Standard backup/restore process | Low |
| > 24 hours | Manual restore, tape backups | Very low |

### RPO (Recovery Point Objective)

Maximum acceptable data loss:

| RPO Target | Backup Frequency | Cost |
|------------|------------------|------|
| < 1 hour | Continuous replication, WAL | High |
| 1-4 hours | Hourly incremental backups | Medium |
| 4-24 hours | Daily backups | Low |
| > 24 hours | Weekly backups | Very low |

## Key Concepts

### Immutability

Immutable backups cannot be modified or deleted during retention periods:
- Object lock (S3, GCS, Azure Blob)
- WORM storage (Write Once Read Many)
- Air-gapped copies
- Critical for ransomware protection

### Retention Policies

Balance recoverability, storage costs, and compliance:

| Data Type | Minimum Retention | Recommended |
|-----------|-------------------|-------------|
| Critical systems | 90 days | 1 year |
| Standard data | 30 days | 90 days |
| Logs/audit trails | Per compliance | 7 years (financial) |
| Development/test | 7 days | 14 days |

### SaaS Backup Considerations

Most SaaS platforms lack robust native backup:
- Explicitly backup SaaS data (Google Workspace, M365, Salesforce)
- Native retention often insufficient
- Data may be unrecoverable without explicit backup

## Folder Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-implementation and operational checklists |
| [examples.md](examples.md) | Real-world backup configurations |
| [templates.md](templates.md) | Copy-paste templates for policies and configs |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI-assisted backup planning |

## Related Methodologies

- [backup-implementation](../backup-implementation/) - Detailed implementation guides
- [secrets-management](../secrets-management/) - Encryption key management
- [finops](../finops/) - Backup cost optimization

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Acronis 3-2-1 Backup Strategy Guide 2025](https://www.acronis.com/en/blog/posts/backup-rule/)
- [Backblaze 3-2-1 Strategy](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/)
- [Veeam 3-2-1 Backup Rule](https://www.veeam.com/blog/321-backup-rule.html)
- [HYCU 3-2-1 Rule Explained](https://www.hycu.com/blog/3-2-1-backup-rule-explained-how-it-works-why-it-matters)
- [TechTarget 3-2-1 Strategy](https://www.techtarget.com/searchdatabackup/definition/3-2-1-Backup-Strategy)
- [GitProtect 3-2-1 Complete Guide](https://gitprotect.io/blog/3-2-1-backup-rule-complete-guide/)
- [Datto 3-2-1 Backup Rule](https://www.datto.com/blog/3-2-1-backup-rule/)
- [PacGenesis Enterprise Data Protection](https://pacgenesis.com/the-3-2-1-backup-rule-enterprise-data-protection-strategy-that-actually-works/)

---

*Backup Basics Methodology | faion-cicd-engineer*
