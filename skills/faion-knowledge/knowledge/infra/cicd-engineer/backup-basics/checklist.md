# Backup Basics Checklists

## Pre-Implementation Checklist

### Requirements Gathering

- [ ] Define RTO for each system (max downtime)
- [ ] Define RPO for each system (max data loss)
- [ ] Identify critical vs non-critical systems
- [ ] Document data classification (PII, financial, etc.)
- [ ] List compliance requirements (GDPR, HIPAA, SOC2, PCI-DSS)
- [ ] Calculate total data volume to backup
- [ ] Estimate data growth rate (monthly/yearly)

### Infrastructure Assessment

- [ ] Inventory all production databases
- [ ] Inventory all application servers
- [ ] Identify SaaS applications requiring backup
- [ ] Document existing backup solutions
- [ ] Assess network bandwidth for backup windows
- [ ] Identify backup storage locations (on-prem, cloud, hybrid)

### Security Requirements

- [ ] Define encryption requirements (at-rest, in-transit)
- [ ] Plan key management strategy
- [ ] Identify immutability requirements
- [ ] Document access control policies
- [ ] Plan for air-gapped copy (if required)

## 3-2-1 Rule Compliance Checklist

### Three Copies

- [ ] Primary production data identified
- [ ] First backup copy location defined
- [ ] Second backup copy location defined (offsite)

### Two Media Types

- [ ] Primary media type selected (SSD/HDD/NVMe)
- [ ] Secondary media type selected (Object storage/Tape/Cloud)
- [ ] Media types are truly different (not same vendor/datacenter)

### One Offsite

- [ ] Offsite location is geographically separate
- [ ] Network connectivity to offsite confirmed
- [ ] Offsite access credentials secured
- [ ] Disaster scenario tested (primary site unavailable)

## Enhanced Strategy Checklist (3-2-1-1-0)

### Immutable/Air-Gapped Copy

- [ ] Immutable storage configured (S3 Object Lock, WORM)
- [ ] OR air-gapped copy procedure documented
- [ ] Immutability period matches retention requirements
- [ ] Immutable copy cannot be deleted by admins

### Zero Errors Verification

- [ ] Automated backup verification enabled
- [ ] Integrity checks configured (checksums)
- [ ] Restore test automation in place
- [ ] Alert on verification failures

## Retention Policy Checklist

- [ ] Retention periods defined per data type
- [ ] Compliance retention requirements documented
- [ ] Automatic deletion configured for expired backups
- [ ] Legal hold capability available
- [ ] Retention costs calculated and budgeted

## Backup Testing Checklist

### Monthly Tests

- [ ] Automated restore test for critical databases
- [ ] Verify backup integrity (checksums)
- [ ] Confirm backup job completion logs
- [ ] Review backup size trends

### Quarterly Tests

- [ ] Full restore test to alternate environment
- [ ] Measure actual RTO vs target
- [ ] Test application functionality post-restore
- [ ] Document any gaps or issues

### Annual Tests

- [ ] Full DR test (simulate site failure)
- [ ] Test restore with different personnel
- [ ] Review and update runbooks
- [ ] Verify compliance attestation

## Operational Checklist

### Daily Monitoring

- [ ] Check backup job status (success/failure)
- [ ] Review backup duration trends
- [ ] Monitor storage utilization
- [ ] Address any alerts/warnings

### Weekly Review

- [ ] Verify backup schedules are current
- [ ] Check for new systems needing backup
- [ ] Review failed backup root causes
- [ ] Update backup inventory if needed

### Monthly Maintenance

- [ ] Test restore of random backup
- [ ] Review and rotate backup credentials
- [ ] Audit backup access logs
- [ ] Update backup documentation

## Security Checklist

- [ ] Backups encrypted at rest (AES-256)
- [ ] Backups encrypted in transit (TLS 1.3)
- [ ] Backup credentials stored securely (vault)
- [ ] Separate credentials for backup system
- [ ] MFA enabled for backup admin access
- [ ] Backup network isolated/segmented
- [ ] Immutable storage enabled for ransomware protection
- [ ] Backup deletion requires approval workflow

## Documentation Checklist

- [ ] Backup policy document approved
- [ ] Backup schedule documented
- [ ] Restore procedures documented (runbooks)
- [ ] Contact list for backup emergencies
- [ ] Escalation procedures defined
- [ ] Compliance evidence collected

---

*Backup Basics Checklists | faion-cicd-engineer*
