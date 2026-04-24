# Backup Implementation Checklist

## Pre-Implementation

### Requirements Gathering

- [ ] Define RPO (Recovery Point Objective)
- [ ] Define RTO (Recovery Time Objective)
- [ ] Inventory all data sources (databases, files, configs)
- [ ] Classify data by criticality (tier 1/2/3)
- [ ] Document compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Estimate storage requirements
- [ ] Define retention policies

### Infrastructure Assessment

- [ ] Identify storage backends (S3, GCS, Azure Blob, local)
- [ ] Check network bandwidth for backup windows
- [ ] Verify IAM/RBAC permissions
- [ ] Plan encryption strategy (at rest, in transit)
- [ ] Document firewall/network requirements

## Database Backups

### PostgreSQL

- [ ] Configure `pg_hba.conf` for backup user
- [ ] Create dedicated backup role with minimal permissions
- [ ] Set up WAL archiving for PITR
- [ ] Configure `pg_dump` or `pg_basebackup` scripts
- [ ] Test parallel dump for large databases
- [ ] Verify backup file integrity
- [ ] Test restore procedure

### MySQL/MariaDB

- [ ] Configure backup user with `RELOAD`, `LOCK TABLES`, `REPLICATION CLIENT` privileges
- [ ] Choose tool: mysqldump vs XtraBackup
- [ ] Enable binary logging for PITR
- [ ] Configure `--single-transaction` for InnoDB
- [ ] Test incremental backups (XtraBackup)
- [ ] Verify backup consistency

### MongoDB

- [ ] Configure mongodump with oplog capture
- [ ] Set up replica set for consistent backups
- [ ] Test archive format vs directory format
- [ ] Verify BSON integrity

## File System Backups

### Restic Setup

- [ ] Initialize repository with encryption
- [ ] Configure exclude patterns (logs, caches, node_modules)
- [ ] Set up environment variables for credentials
- [ ] Configure bandwidth limits if needed
- [ ] Define retention policy (daily/weekly/monthly)
- [ ] Test snapshot creation
- [ ] Test restore (full and partial)
- [ ] Set up prune schedule

### BorgBackup Setup

- [ ] Initialize encrypted repository
- [ ] Configure compression level
- [ ] Set up SSH key authentication
- [ ] Define archive naming convention
- [ ] Test backup and restore
- [ ] Configure prune policy

## Kubernetes Backups (Velero)

### Installation

- [ ] Install Velero CLI
- [ ] Deploy Velero server to cluster
- [ ] Configure storage provider plugin
- [ ] Set up backup storage location
- [ ] Configure volume snapshot location
- [ ] Verify CSI driver compatibility

### Configuration

- [ ] Define namespace inclusion/exclusion
- [ ] Configure resource filters
- [ ] Set up label selectors
- [ ] Define TTL for backups
- [ ] Configure pre/post hooks for stateful apps
- [ ] Use Kopia (not Restic - deprecated in v1.15+)

### Scheduling

- [ ] Create daily backup schedule
- [ ] Create weekly backup schedule
- [ ] Set appropriate TTL values
- [ ] Test scheduled backup execution

## Cloud Backups

### AWS Backup

- [ ] Create backup vault
- [ ] Define backup plan with rules
- [ ] Configure lifecycle policies (warm to cold storage)
- [ ] Set up cross-region replication
- [ ] Apply resource tags for selection
- [ ] Test restore from vault

### S3 Configuration

- [ ] Enable versioning
- [ ] Configure lifecycle rules
- [ ] Set up cross-region replication
- [ ] Enable server-side encryption
- [ ] Configure bucket policies
- [ ] Enable MFA delete for critical buckets

## Automation

### Scheduling

- [ ] Create cron jobs or systemd timers
- [ ] Stagger backup times to avoid conflicts
- [ ] Configure appropriate timeouts
- [ ] Set up log rotation
- [ ] Handle credential refresh

### Monitoring

- [ ] Export backup metrics (success/failure, size, duration)
- [ ] Create Prometheus alerting rules
- [ ] Set up notification channels (email, Slack, PagerDuty)
- [ ] Create Grafana dashboard
- [ ] Alert on backup age > threshold
- [ ] Alert on backup size anomalies

## Security

### Encryption

- [ ] Encrypt backups at rest
- [ ] Use TLS for data in transit
- [ ] Secure encryption keys (HSM, KMS, Vault)
- [ ] Document key recovery procedure

### Access Control

- [ ] Apply least privilege principle
- [ ] Use dedicated service accounts
- [ ] Enable audit logging
- [ ] Restrict restore permissions
- [ ] Document access matrix

### Immutability

- [ ] Enable object lock (S3) or immutable storage
- [ ] Configure retention periods
- [ ] Test that locked objects cannot be deleted

## Verification

### Regular Testing

- [ ] Schedule weekly restore tests
- [ ] Document restore procedures
- [ ] Measure actual RTO
- [ ] Validate data integrity
- [ ] Test partial restores
- [ ] Test cross-region restores

### Verification Script

- [ ] Implement automated backup verification
- [ ] Check file/archive integrity
- [ ] Verify expected table/object counts
- [ ] Alert on verification failures

## Disaster Recovery

### Documentation

- [ ] Create DR runbook
- [ ] Document restore order (dependencies)
- [ ] List emergency contacts
- [ ] Define escalation procedures
- [ ] Map services to backup locations

### DR Drills

- [ ] Schedule quarterly DR drills
- [ ] Test full environment restore
- [ ] Measure actual RTO/RPO
- [ ] Document lessons learned
- [ ] Update runbooks based on findings

## Post-Implementation

### Documentation

- [ ] Document backup architecture
- [ ] Create operations runbook
- [ ] Update CLAUDE.md with backup details
- [ ] Train team on restore procedures

### Review

- [ ] Verify all critical data is covered
- [ ] Confirm retention meets compliance
- [ ] Review costs and optimize if needed
- [ ] Schedule periodic backup strategy review

---

*Last updated: 2026-01*
