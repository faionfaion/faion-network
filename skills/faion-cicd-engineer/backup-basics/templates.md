# Backup Basics Templates

## Template 1: Backup Policy Document

```markdown
# Backup Policy

**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Owner:** DevOps Team
**Approver:** CTO/IT Director

## 1. Purpose

This policy establishes requirements for backing up critical data and systems
to ensure business continuity and disaster recovery capabilities.

## 2. Scope

This policy applies to:
- All production databases and systems
- All customer and business-critical data
- Configuration files and infrastructure as code
- SaaS application data

## 3. Backup Strategy

### 3.1 Strategy Model

We follow the **3-2-1-1-0** backup strategy:
- 3 copies of data
- 2 different media types
- 1 offsite copy
- 1 immutable copy
- 0 errors after verification

### 3.2 Backup Schedule

| System Category | Backup Type | Frequency | Retention |
|-----------------|-------------|-----------|-----------|
| Tier 1: Critical | Full + WAL | Daily + Continuous | 90 days |
| Tier 2: Important | Full + Incremental | Weekly + Daily | 30 days |
| Tier 3: Standard | Full | Weekly | 14 days |

## 4. Recovery Objectives

| System Category | RTO | RPO |
|-----------------|-----|-----|
| Tier 1: Critical | 2 hours | 1 hour |
| Tier 2: Important | 4 hours | 24 hours |
| Tier 3: Standard | 24 hours | 7 days |

## 5. Storage Locations

- **Primary Backup:** [Location, e.g., AWS S3 us-east-1]
- **Secondary Backup:** [Location, e.g., AWS S3 eu-west-1]
- **Immutable Backup:** [Location with Object Lock enabled]

## 6. Security Requirements

- All backups must be encrypted at rest (AES-256)
- All backup transfers must use TLS 1.3
- Backup credentials stored in secrets manager
- Separate backup service accounts with minimal permissions
- MFA required for backup administrative access

## 7. Testing Schedule

| Test Type | Frequency | Responsible |
|-----------|-----------|-------------|
| Automated restore verification | Daily | Automated |
| Manual restore test | Monthly | DevOps Team |
| Full DR test | Quarterly | DevOps + Engineering |
| Policy review | Annually | IT Security |

## 8. Monitoring and Alerting

- Backup job failures: Alert within 15 minutes
- Missed backup window: Alert within 1 hour
- Storage capacity > 80%: Warning alert
- Restore test failure: Immediate critical alert

## 9. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| DevOps Team | Backup configuration, monitoring, testing |
| Security Team | Encryption key management, access control |
| Development Team | Define backup requirements for new systems |
| Management | Policy approval, budget allocation |

## 10. Compliance

This policy supports compliance with:
- [ ] GDPR (data protection, right to erasure)
- [ ] HIPAA (PHI protection)
- [ ] SOC2 (availability, confidentiality)
- [ ] PCI-DSS (cardholder data protection)

## 11. Exceptions

All exceptions to this policy require written approval from [Approver].

## 12. Review

This policy will be reviewed and updated annually or after significant incidents.

---

**Approval:**
- Approved by: _______________
- Date: _______________
```

## Template 2: Backup Schedule Configuration

```yaml
# backup-schedule.yaml
# Copy and customize for your environment

backup_configuration:
  version: "1.0"
  environment: production

  global_settings:
    encryption:
      algorithm: AES-256-GCM
      key_management: aws_kms
      key_rotation: 90_days
    retention:
      default_hot: 7d
      default_warm: 30d
      default_cold: 365d
    verification:
      integrity_check: enabled
      restore_test: weekly

  storage_locations:
    primary:
      provider: aws_s3
      bucket: "${COMPANY}-backups-primary"
      region: us-east-1
      storage_class: STANDARD

    secondary:
      provider: aws_s3
      bucket: "${COMPANY}-backups-secondary"
      region: eu-west-1
      storage_class: STANDARD_IA
      replication_from: primary

    immutable:
      provider: aws_s3
      bucket: "${COMPANY}-backups-immutable"
      region: us-east-1
      object_lock:
        mode: COMPLIANCE
        retention_days: 90

  backup_targets:
    postgresql_production:
      type: database
      method: pg_dump_wal
      connection:
        host: "${DB_HOST}"
        port: 5432
        database: production
        credentials_secret: backup/postgresql
      schedule:
        full: "0 2 * * *"  # Daily 02:00
        wal_archiving: continuous
      retention:
        hot: 7d
        warm: 30d
        cold: 365d
      storage:
        - primary
        - secondary
        - immutable
      recovery_objectives:
        rto: 2h
        rpo: 1h

    application_files:
      type: filesystem
      method: restic
      paths:
        - /var/www/app
        - /etc/nginx
        - /etc/ssl
      exclude:
        - "*.log"
        - "*.tmp"
        - "__pycache__"
        - "node_modules"
      schedule:
        full: "0 3 * * 0"  # Weekly Sunday 03:00
        incremental: "0 3 * * 1-6"  # Daily except Sunday
      retention:
        hot: 14d
        warm: 90d
      storage:
        - primary
        - secondary

    kubernetes_cluster:
      type: kubernetes
      method: velero
      namespaces:
        - production
        - staging
      exclude_resources:
        - events
        - pods
      schedule:
        full: "0 4 * * *"  # Daily 04:00
      retention:
        hot: 30d
      storage:
        - primary

  monitoring:
    metrics_endpoint: prometheus
    alert_channels:
      critical:
        - pagerduty
      warning:
        - slack_ops
      info:
        - email_devops
```

## Template 3: Restore Runbook

```markdown
# Restore Runbook: [System Name]

**System:** [e.g., PostgreSQL Production Database]
**Last Updated:** YYYY-MM-DD
**Owner:** DevOps Team

## Quick Reference

| Parameter | Value |
|-----------|-------|
| RTO | [X hours] |
| RPO | [X hours] |
| Backup Location | [S3 bucket/path] |
| Backup Tool | [pg_restore/restic/velero] |

## Prerequisites

- [ ] Access to backup storage (credentials in [vault path])
- [ ] Access to target restore environment
- [ ] Network connectivity between backup and target
- [ ] Sufficient disk space on target ([X GB minimum])
- [ ] Required tools installed: [list tools]

## Restore Procedures

### Scenario 1: Point-in-Time Recovery (Database Corruption)

**When to use:** Data corruption, accidental deletion, need specific point in time

1. **Stop application writes**
   ```bash
   kubectl scale deployment app --replicas=0 -n production
   ```

2. **Identify target recovery point**
   ```bash
   # List available recovery points
   aws s3 ls s3://backups/postgresql/wal/ --recursive | tail -20

   # Identify timestamp before corruption
   # Format: YYYY-MM-DD HH:MM:SS UTC
   TARGET_TIME="2024-01-15 14:30:00"
   ```

3. **Restore base backup**
   ```bash
   # Download latest full backup before target time
   aws s3 cp s3://backups/postgresql/full/YYYYMMDD.tar.gz ./

   # Extract to data directory
   tar -xzf YYYYMMDD.tar.gz -C /var/lib/postgresql/data/
   ```

4. **Configure recovery**
   ```bash
   # Create recovery.signal file
   touch /var/lib/postgresql/data/recovery.signal

   # Configure postgresql.conf
   cat >> /var/lib/postgresql/data/postgresql.conf << EOF
   restore_command = 'aws s3 cp s3://backups/postgresql/wal/%f %p'
   recovery_target_time = '${TARGET_TIME}'
   recovery_target_action = 'promote'
   EOF
   ```

5. **Start database and verify**
   ```bash
   systemctl start postgresql

   # Verify recovery completed
   psql -c "SELECT pg_is_in_recovery();"  # Should return 'f'

   # Verify data integrity
   psql -c "SELECT COUNT(*) FROM critical_table;"
   ```

6. **Resume operations**
   ```bash
   kubectl scale deployment app --replicas=3 -n production
   ```

### Scenario 2: Full System Restore (Disaster Recovery)

**When to use:** Complete system failure, regional outage, ransomware

1. **Activate DR environment**
   ```bash
   # Switch DNS to DR region
   aws route53 change-resource-record-sets \
     --hosted-zone-id ZXXXXX \
     --change-batch file://dr-dns-change.json
   ```

2. **Restore from immutable backup**
   ```bash
   # Use immutable backup to ensure clean restore
   restic restore latest \
     --repo s3:s3.amazonaws.com/backups-immutable \
     --target /restore \
     --verify
   ```

3. **Deploy application stack**
   ```bash
   kubectl apply -f /restore/kubernetes/
   ```

4. **Verify and validate**
   ```bash
   # Run health checks
   ./scripts/health-check.sh

   # Run data integrity checks
   ./scripts/data-validation.sh
   ```

## Verification Checklist

- [ ] Application responds to health checks
- [ ] Database connections successful
- [ ] Critical data present and accurate
- [ ] Recent transactions visible
- [ ] External integrations functional
- [ ] Monitoring and alerting operational

## Escalation

| Severity | Contact | Method |
|----------|---------|--------|
| P1 (Critical) | On-call engineer | PagerDuty |
| P2 (High) | DevOps lead | Slack #ops-critical |
| P3 (Medium) | DevOps team | Slack #ops |

## Post-Restore Actions

- [ ] Document incident timeline
- [ ] Update backup verification
- [ ] Review and improve runbook
- [ ] Conduct post-mortem if needed
```

## Template 4: Backup Verification Report

```markdown
# Backup Verification Report

**Report Date:** YYYY-MM-DD
**Period:** [Start Date] to [End Date]
**Prepared By:** [Name]

## Executive Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Backup Success Rate | 99.9% | XX.X% | [PASS/FAIL] |
| Restore Test Success | 100% | XX% | [PASS/FAIL] |
| RTO Compliance | [Target] | [Actual] | [PASS/FAIL] |
| RPO Compliance | [Target] | [Actual] | [PASS/FAIL] |

## Backup Job Summary

| System | Total Jobs | Successful | Failed | Success Rate |
|--------|------------|------------|--------|--------------|
| PostgreSQL | XX | XX | X | XX.X% |
| MongoDB | XX | XX | X | XX.X% |
| Application Files | XX | XX | X | XX.X% |
| Kubernetes | XX | XX | X | XX.X% |

## Failed Backups

| Date | System | Error | Resolution |
|------|--------|-------|------------|
| YYYY-MM-DD | [System] | [Error message] | [How resolved] |

## Restore Tests Performed

| Date | System | Type | Duration | Result |
|------|--------|------|----------|--------|
| YYYY-MM-DD | PostgreSQL | Point-in-time | XX min | [PASS/FAIL] |
| YYYY-MM-DD | Full Stack | DR test | XX min | [PASS/FAIL] |

## Storage Utilization

| Location | Capacity | Used | Available | Trend |
|----------|----------|------|-----------|-------|
| Primary (S3 us-east-1) | [X TB] | [X TB] | [X TB] | [+X%/month] |
| Secondary (S3 eu-west-1) | [X TB] | [X TB] | [X TB] | [+X%/month] |
| Immutable | [X TB] | [X TB] | [X TB] | [+X%/month] |

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Next Period Actions

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

---

**Approved By:** _______________
**Date:** _______________
```

## Template 5: GitHub Actions Backup Workflow

```yaml
# .github/workflows/backup.yml
name: Scheduled Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 02:00 UTC
  workflow_dispatch:
    inputs:
      backup_type:
        description: 'Backup type'
        required: true
        default: 'incremental'
        type: choice
        options:
          - full
          - incremental

env:
  BACKUP_BUCKET: ${{ secrets.BACKUP_BUCKET }}
  AWS_REGION: us-east-1

jobs:
  database-backup:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_BACKUP_ACCESS_KEY }}
          aws-secret-access-key: ${{ secrets.AWS_BACKUP_SECRET_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Install backup tools
        run: |
          sudo apt-get update
          sudo apt-get install -y postgresql-client restic

      - name: Initialize Restic repository
        run: |
          restic init --repo s3:s3.amazonaws.com/${{ env.BACKUP_BUCKET }}/database || true
        env:
          RESTIC_PASSWORD: ${{ secrets.RESTIC_PASSWORD }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_BACKUP_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_BACKUP_SECRET_KEY }}

      - name: Backup PostgreSQL
        run: |
          PGPASSWORD=${{ secrets.DB_PASSWORD }} pg_dump \
            -h ${{ secrets.DB_HOST }} \
            -U ${{ secrets.DB_USER }} \
            -d ${{ secrets.DB_NAME }} \
            --format=custom \
            --file=/tmp/database.dump

          restic backup /tmp/database.dump \
            --repo s3:s3.amazonaws.com/${{ env.BACKUP_BUCKET }}/database \
            --tag postgresql \
            --tag ${{ github.event.inputs.backup_type || 'incremental' }}
        env:
          RESTIC_PASSWORD: ${{ secrets.RESTIC_PASSWORD }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_BACKUP_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_BACKUP_SECRET_KEY }}

      - name: Apply retention policy
        run: |
          restic forget \
            --repo s3:s3.amazonaws.com/${{ env.BACKUP_BUCKET }}/database \
            --keep-daily 7 \
            --keep-weekly 4 \
            --keep-monthly 12 \
            --prune
        env:
          RESTIC_PASSWORD: ${{ secrets.RESTIC_PASSWORD }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_BACKUP_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_BACKUP_SECRET_KEY }}

      - name: Verify backup integrity
        run: |
          restic check \
            --repo s3:s3.amazonaws.com/${{ env.BACKUP_BUCKET }}/database
        env:
          RESTIC_PASSWORD: ${{ secrets.RESTIC_PASSWORD }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_BACKUP_ACCESS_KEY }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_BACKUP_SECRET_KEY }}

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Backup Failed",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Backup Failed* :x:\nWorkflow: ${{ github.workflow }}\nRun: ${{ github.run_id }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

*Backup Basics Templates | faion-cicd-engineer*
