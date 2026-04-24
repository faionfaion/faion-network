# Backup Strategies Checklist

## Pre-Implementation Checklist

### Data Classification

- [ ] Identify all data sources requiring backup
- [ ] Classify data by criticality (critical, important, standard, archive)
- [ ] Document data owners and stakeholders
- [ ] Determine compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Calculate data volumes and growth rates

### RPO/RTO Requirements

- [ ] Define Recovery Point Objective for each data class
- [ ] Define Recovery Time Objective for each data class
- [ ] Document maximum acceptable data loss
- [ ] Document maximum acceptable downtime
- [ ] Get stakeholder sign-off on RPO/RTO targets

### Infrastructure Assessment

- [ ] Inventory existing backup infrastructure
- [ ] Assess network bandwidth for backup windows
- [ ] Evaluate storage capacity requirements
- [ ] Plan for backup storage growth (minimum 2 years)
- [ ] Identify air-gapped/immutable storage options

## 3-2-1-1-0 Implementation Checklist

### Three Copies

- [ ] Production data (copy 1)
- [ ] Primary backup (copy 2)
- [ ] Secondary backup (copy 3)
- [ ] Verify all copies are independent

### Two Media Types

- [ ] Primary storage medium selected
- [ ] Secondary storage medium selected
- [ ] Media types are truly different (not just different vendors)

### One Offsite

- [ ] Offsite location identified
- [ ] Network connectivity verified
- [ ] Encryption in transit configured
- [ ] Access controls implemented

### One Immutable/Air-Gapped

- [ ] Immutable storage configured (S3 Object Lock, Azure Immutable Blob)
- [ ] OR air-gapped backup implemented
- [ ] Retention policies defined
- [ ] Cannot be deleted even by admins verified

### Zero Errors

- [ ] Automated verification enabled
- [ ] Backup integrity checks scheduled
- [ ] Recovery testing automated
- [ ] Alerting configured for failures

## Database Backup Checklist

### PostgreSQL

- [ ] pg_dump or pg_basebackup configured
- [ ] WAL archiving enabled for PITR
- [ ] Archive storage configured
- [ ] Retention policy defined
- [ ] Restore procedure documented
- [ ] Restore tested successfully

### MySQL/MariaDB

- [ ] mysqldump or XtraBackup configured
- [ ] Binary log retention set
- [ ] Full backup schedule defined
- [ ] Incremental backup schedule defined
- [ ] Restore procedure documented
- [ ] Restore tested successfully

### MongoDB

- [ ] mongodump configured
- [ ] Oplog backup enabled (if replica set)
- [ ] Compression enabled
- [ ] Restore procedure documented
- [ ] Restore tested successfully

## Kubernetes Backup Checklist

### Velero Setup

- [ ] Velero installed in cluster
- [ ] Backup storage location configured
- [ ] Volume snapshot location configured
- [ ] Service account permissions verified
- [ ] Namespace inclusion/exclusion defined
- [ ] Resource filters configured

### Scheduled Backups

- [ ] Daily backup schedule created
- [ ] TTL (retention) configured
- [ ] PVC snapshots enabled
- [ ] etcd backup included (if self-managed)
- [ ] Secrets encryption verified

### Disaster Recovery

- [ ] Cross-cluster restore tested
- [ ] Namespace mapping documented
- [ ] PV restore procedure documented
- [ ] Full cluster recovery runbook created

## Cloud Backup Checklist

### AWS

- [ ] AWS Backup vault created
- [ ] Backup plan configured
- [ ] Resource selection defined
- [ ] Cross-region copy configured
- [ ] Lifecycle rules set
- [ ] IAM roles configured

### Azure

- [ ] Recovery Services vault created
- [ ] Backup policy defined
- [ ] Retention configured
- [ ] Geo-redundant storage enabled
- [ ] RBAC permissions set

### GCP

- [ ] Backup plan created
- [ ] Backup vault configured
- [ ] Resource targeting defined
- [ ] Cross-region configured
- [ ] IAM bindings set

## Monitoring Checklist

### Alerts

- [ ] Backup failure alert configured
- [ ] Backup age alert configured (> 24h)
- [ ] Backup size anomaly alert configured
- [ ] Storage capacity alert configured
- [ ] Recovery test failure alert configured

### Metrics

- [ ] Backup duration tracked
- [ ] Backup size tracked
- [ ] Backup success/failure rate tracked
- [ ] Storage utilization tracked
- [ ] Recovery time tracked (during tests)

### Reporting

- [ ] Weekly backup status report
- [ ] Monthly recovery test report
- [ ] Quarterly capacity planning report
- [ ] Annual DR test report

## Recovery Testing Checklist

### Monthly Tests

- [ ] Select random backup for testing
- [ ] Restore to isolated environment
- [ ] Verify data integrity
- [ ] Document recovery time
- [ ] Report findings

### Quarterly Tests

- [ ] Full database recovery test
- [ ] Application functionality verification
- [ ] Document deviations from expected RTO
- [ ] Update procedures if needed

### Annual Tests

- [ ] Full disaster recovery drill
- [ ] Cross-region failover test
- [ ] All stakeholders involved
- [ ] Lessons learned documented
- [ ] Procedures updated

## Security Checklist

### Encryption

- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Key management documented
- [ ] Key rotation schedule defined
- [ ] Key backup procedure documented

### Access Control

- [ ] Backup admin roles defined
- [ ] Least privilege principle applied
- [ ] MFA required for backup access
- [ ] Audit logging enabled
- [ ] Access reviews scheduled

### Immutability

- [ ] WORM storage configured
- [ ] Retention lock enabled
- [ ] Admin delete prevention verified
- [ ] Compliance mode vs governance mode decided

## Documentation Checklist

### Runbooks

- [ ] Backup procedure documented
- [ ] Restore procedure documented
- [ ] Troubleshooting guide created
- [ ] Escalation path defined
- [ ] Contact list maintained

### Architecture

- [ ] Backup architecture diagram
- [ ] Data flow diagram
- [ ] Network topology documented
- [ ] Storage layout documented

### Compliance

- [ ] Retention requirements documented
- [ ] Audit trail maintained
- [ ] Compliance certifications listed
- [ ] Data residency requirements documented
