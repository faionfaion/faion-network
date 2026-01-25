---
id: backup-basics
name: "Backup Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Backup Basics

## Overview

Backup strategies ensure data protection, business continuity, and disaster recovery capabilities. This section covers backup fundamentals, types, and core principles.

## When to Use

- Setting up data protection for applications
- Implementing disaster recovery (DR) plans
- Meeting compliance requirements (GDPR, HIPAA)
- Protecting against ransomware and data loss
- Planning infrastructure migrations

## Backup Fundamentals

### Backup Types

```yaml
backup_types:
  full_backup:
    description: "Complete copy of all data"
    pros: ["Fast recovery", "Self-contained"]
    cons: ["Storage intensive", "Time consuming"]
    frequency: "Weekly or monthly"

  incremental_backup:
    description: "Only changes since last backup"
    pros: ["Fast", "Storage efficient"]
    cons: ["Slower recovery", "Chain dependency"]
    frequency: "Daily or hourly"

  differential_backup:
    description: "Changes since last full backup"
    pros: ["Faster than full", "Easier recovery than incremental"]
    cons: ["Growing size over time"]
    frequency: "Daily"

  snapshot:
    description: "Point-in-time copy"
    pros: ["Instant", "Space efficient (COW)"]
    cons: ["Same storage system risk"]
    frequency: "Hourly or on-demand"

  continuous_replication:
    description: "Real-time data sync"
    pros: ["Near-zero RPO"]
    cons: ["Complex", "Expensive"]
    frequency: "Continuous"
```

### 3-2-1 Backup Rule

```
3 copies of data
├── 1 primary (production)
├── 1 local backup
└── 1 offsite backup

2 different media types
├── Disk storage
└── Object storage / tape

1 offsite copy
└── Different geographic location
```

## Best Practices

### Planning

1. **Define RTO/RPO** - Know your requirements
2. **Document everything** - Runbooks, procedures
3. **Test regularly** - Untested backups are not backups
4. **Automate** - Reduce human error

### Storage

1. **3-2-1 rule** - Multiple copies, locations
2. **Encryption** - Encrypt backups at rest
3. **Immutable backups** - Protect against ransomware
4. **Retention policies** - Balance cost and compliance

### Operations

1. **Monitor backup jobs** - Alert on failures
2. **Verify integrity** - Regular restore tests
3. **Version backups** - Keep multiple generations
4. **Log everything** - Audit trail

### Security

1. **Encrypt in transit** - TLS for transfers
2. **Access control** - Least privilege
3. **Separate credentials** - Backup-specific access
4. **Air-gapped copies** - For critical data

## Recovery Objectives

### RTO (Recovery Time Objective)

Time to restore operations after disaster:

| RTO Target | Backup Strategy | Cost |
|------------|----------------|------|
| < 1 hour | Hot standby, continuous replication | High |
| 1-4 hours | Automated restore, frequent backups | Medium |
| 4-24 hours | Standard backup/restore process | Low |
| > 24 hours | Manual restore, tape backups | Very low |

### RPO (Recovery Point Objective)

Maximum acceptable data loss:

| RPO Target | Backup Frequency | Cost |
|------------|-----------------|------|
| < 1 hour | Continuous replication, WAL | High |
| 1-4 hours | Hourly incremental backups | Medium |
| 4-24 hours | Daily backups | Low |
| > 24 hours | Weekly backups | Very low |

## Disaster Recovery Scenarios

```yaml
disaster_recovery:
  rto: 4_hours  # Recovery Time Objective
  rpo: 1_hour   # Recovery Point Objective

  scenarios:
    database_corruption:
      detection: "Automated monitoring alert"
      steps:
        - stop_application_writes
        - identify_corruption_time
        - restore_from_point_in_time
        - verify_data_integrity
        - resume_operations
      estimated_time: 2_hours

    region_outage:
      detection: "AWS Health Dashboard + monitoring"
      steps:
        - activate_dns_failover
        - verify_dr_region_databases
        - scale_dr_region_compute
        - update_configuration
        - resume_operations
      estimated_time: 4_hours

    ransomware:
      detection: "Security alert + file integrity monitoring"
      steps:
        - isolate_affected_systems
        - identify_attack_vector
        - restore_from_air_gapped_backup
        - security_hardening
        - resume_operations
      estimated_time: 8_hours

  testing_schedule:
    full_dr_test: quarterly
    backup_restore_test: monthly
    runbook_review: quarterly
```

## Backup Policy Template

```markdown
# Backup Policy

## Scope
This policy covers all production systems and databases.

## Backup Schedule
| System | Type | Frequency | Retention |
|--------|------|-----------|-----------|
| PostgreSQL | Full | Daily 02:00 UTC | 30 days |
| PostgreSQL | WAL | Continuous | 7 days |
| MongoDB | Full | Daily 03:00 UTC | 30 days |
| Application Files | Incremental | Hourly | 7 days |
| Application Files | Full | Weekly Sunday | 90 days |

## Storage Locations
- Primary: AWS S3 us-east-1
- Secondary: AWS S3 eu-west-1 (cross-region replication)
- Archive: AWS Glacier (after 90 days)

## Recovery Objectives
- RTO: 4 hours
- RPO: 1 hour

## Testing Schedule
- Monthly: Automated restore test
- Quarterly: Full DR test
- Annually: DR documentation review

## Responsibilities
- DevOps Team: Backup configuration and monitoring
- Security Team: Encryption key management
- Management: Policy approval and compliance
```

## References

- [Restic Documentation](https://restic.readthedocs.io/)
- [BorgBackup Documentation](https://borgbackup.readthedocs.io/)
- [Velero Documentation](https://velero.io/docs/)
- [AWS Backup](https://docs.aws.amazon.com/aws-backup/)
- [PostgreSQL Backup and Recovery](https://www.postgresql.org/docs/current/backup.html)

## Sources

- [Backup and Recovery Best Practices](https://www.veeam.com/blog/how-to-follow-the-3-2-1-backup-rule.html)
- [AWS Backup Documentation](https://docs.aws.amazon.com/aws-backup/)
- [Disaster Recovery Planning](https://www.ready.gov/business/implementation/IT)
- [Restic Backup Tool](https://restic.net/)
- [Borg Backup](https://www.borgbackup.org/)
