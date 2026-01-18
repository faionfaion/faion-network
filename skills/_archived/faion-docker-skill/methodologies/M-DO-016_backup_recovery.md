# M-DO-016: Backup and Recovery

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #backup, #recovery, #disaster-recovery, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Data loss destroys businesses. Without tested backups, recovery is impossible. Ransomware, human error, and hardware failure threaten every system.

## Promise

After this methodology, you will implement comprehensive backup strategies. Your data will be recoverable with tested restoration procedures.

## Overview

Backup strategy follows the 3-2-1 rule: 3 copies, 2 different media, 1 offsite. This methodology covers database, file, and infrastructure backups.

---

## Framework

### Step 1: 3-2-1 Backup Rule

```
3-2-1 Rule:
├── 3 copies of data
│   ├── Original
│   ├── Local backup
│   └── Offsite backup
├── 2 different media types
│   ├── SSD/HDD
│   └── Cloud storage
└── 1 offsite location
    └── Different region/provider
```

### Step 2: PostgreSQL Backup

```bash
# pg_dump (logical backup)
pg_dump -h localhost -U user -d mydb -F c -f backup.dump

# With compression
pg_dump -h localhost -U user -d mydb | gzip > backup.sql.gz

# All databases
pg_dumpall -h localhost -U postgres | gzip > all_databases.sql.gz

# Restore
pg_restore -h localhost -U user -d mydb -c backup.dump

# Automated backup script
#!/bin/bash
set -e

BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# Create backup
pg_dump -h localhost -U $PGUSER -d $PGDATABASE -F c -f "$BACKUP_DIR/backup_$DATE.dump"

# Compress
gzip "$BACKUP_DIR/backup_$DATE.dump"

# Upload to S3
aws s3 cp "$BACKUP_DIR/backup_$DATE.dump.gz" "s3://my-backups/postgres/"

# Clean old backups
find $BACKUP_DIR -name "backup_*.dump.gz" -mtime +$RETENTION_DAYS -delete
aws s3 rm s3://my-backups/postgres/ --recursive --exclude "*" --include "backup_*.dump.gz" \
  $(date -d "$RETENTION_DAYS days ago" +%Y%m%d)
```

```yaml
# Kubernetes CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: backup
              image: postgres:16-alpine
              command:
                - /bin/sh
                - -c
                - |
                  pg_dump -h $PGHOST -U $PGUSER -d $PGDATABASE -F c | \
                  gzip | \
                  aws s3 cp - s3://my-backups/postgres/backup_$(date +%Y%m%d).dump.gz
              env:
                - name: PGPASSWORD
                  valueFrom:
                    secretKeyRef:
                      name: postgres-secret
                      key: password
          restartPolicy: OnFailure
```

### Step 3: MySQL Backup

```bash
# mysqldump
mysqldump -h localhost -u user -p mydb > backup.sql
mysqldump -h localhost -u user -p --all-databases > all_databases.sql

# With options for consistency
mysqldump -h localhost -u user -p \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  mydb > backup.sql

# Restore
mysql -h localhost -u user -p mydb < backup.sql

# Point-in-time recovery with binlog
mysqlbinlog binlog.000001 | mysql -h localhost -u user -p
```

### Step 4: MongoDB Backup

```bash
# mongodump
mongodump --uri="mongodb://user:pass@localhost:27017/mydb" --out=/backups

# Restore
mongorestore --uri="mongodb://user:pass@localhost:27017/mydb" /backups/mydb

# With compression
mongodump --uri="..." --archive=backup.archive --gzip

# Continuous backup with oplog
mongodump --uri="..." --oplog --out=/backups/full
mongodump --uri="..." --oplog --query='{"ts":{"$gt":Timestamp(...)}}' --out=/backups/incremental
```

### Step 5: File Backup with Restic

```bash
# Install restic
apt install restic

# Initialize repository
restic init --repo s3:s3.amazonaws.com/my-backups

# Create backup
restic -r s3:s3.amazonaws.com/my-backups backup /var/www

# List snapshots
restic -r s3:s3.amazonaws.com/my-backups snapshots

# Restore
restic -r s3:s3.amazonaws.com/my-backups restore latest --target /restore

# Prune old backups
restic -r s3:s3.amazonaws.com/my-backups forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune
```

```bash
# Automated restic backup script
#!/bin/bash
set -e

export RESTIC_REPOSITORY="s3:s3.amazonaws.com/my-backups"
export RESTIC_PASSWORD_FILE="/etc/restic-password"
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."

# Backup
restic backup /var/www /var/lib/app

# Prune
restic forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --prune

# Verify
restic check
```

### Step 6: AWS Backup

```hcl
# Terraform AWS Backup
resource "aws_backup_vault" "main" {
  name = "main-backup-vault"
}

resource "aws_backup_plan" "daily" {
  name = "daily-backup"

  rule {
    rule_name         = "daily"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 5 * * ? *)"

    lifecycle {
      delete_after = 30
    }

    copy_action {
      destination_vault_arn = aws_backup_vault.dr.arn
      lifecycle {
        delete_after = 90
      }
    }
  }
}

resource "aws_backup_selection" "databases" {
  name         = "databases"
  plan_id      = aws_backup_plan.daily.id
  iam_role_arn = aws_iam_role.backup.arn

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}
```

---

## Templates

### Disaster Recovery Plan

```markdown
# Disaster Recovery Plan

## Recovery Time Objective (RTO): 4 hours
## Recovery Point Objective (RPO): 1 hour

### Tier 1: Critical Services
- Database: RDS Multi-AZ with automated failover
- Application: Multi-region deployment
- Recovery: Automatic

### Tier 2: Important Services
- Backups: Hourly to S3, replicated to DR region
- Recovery: 1 hour

### Tier 3: Non-Critical Services
- Backups: Daily
- Recovery: 4 hours

## Recovery Procedures

### Database Recovery
1. Identify failure point
2. Check latest backup in S3
3. Launch new RDS from snapshot
4. Update DNS/connection strings
5. Verify data integrity

### Full Region Failover
1. Activate DR region route53 failover
2. Scale up DR infrastructure
3. Verify all services operational
4. Notify stakeholders
```

### Backup Verification Script

```bash
#!/bin/bash
# verify-backups.sh

set -e

BACKUP_BUCKET="s3://my-backups"
TEMP_DIR="/tmp/backup-verify"
SLACK_WEBHOOK="https://hooks.slack.com/..."

notify() {
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"$1\"}" \
    $SLACK_WEBHOOK
}

# Check backup exists
LATEST=$(aws s3 ls $BACKUP_BUCKET/postgres/ | tail -1 | awk '{print $4}')
if [ -z "$LATEST" ]; then
  notify ":x: No backup found!"
  exit 1
fi

# Check backup age
BACKUP_DATE=$(echo $LATEST | grep -oP '\d{8}')
TODAY=$(date +%Y%m%d)
AGE_DAYS=$(( ($(date -d $TODAY +%s) - $(date -d $BACKUP_DATE +%s)) / 86400 ))

if [ $AGE_DAYS -gt 1 ]; then
  notify ":warning: Backup is $AGE_DAYS days old!"
fi

# Test restore
mkdir -p $TEMP_DIR
aws s3 cp "$BACKUP_BUCKET/postgres/$LATEST" "$TEMP_DIR/"
gunzip "$TEMP_DIR/$LATEST"

docker run --rm -v $TEMP_DIR:/backups postgres:16 \
  pg_restore --list /backups/${LATEST%.gz} > /dev/null

notify ":white_check_mark: Backup verification passed: $LATEST"

rm -rf $TEMP_DIR
```

---

## Examples

### Volume Snapshots

```bash
# AWS EBS Snapshot
aws ec2 create-snapshot \
  --volume-id vol-xxx \
  --description "Daily backup"

# GCP Disk Snapshot
gcloud compute disks snapshot disk-name \
  --zone=us-central1-a \
  --snapshot-names=daily-backup

# Azure Disk Snapshot
az snapshot create \
  --resource-group mygroup \
  --name daily-backup \
  --source /subscriptions/.../disks/mydisk
```

### Database Replication

```hcl
# RDS Read Replica for DR
resource "aws_db_instance" "replica" {
  identifier             = "mydb-replica"
  replicate_source_db    = aws_db_instance.primary.identifier

  # DR region
  provider               = aws.dr_region

  instance_class         = "db.t3.medium"
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.db.id]
}
```

---

## Common Mistakes

1. **No backup testing** - Untested backups are not backups
2. **Same location storage** - Backups in same failure domain
3. **No encryption** - Backup data exposed
4. **Missing retention policy** - Storage costs grow forever
5. **No documentation** - Recovery procedures unknown

---

## Checklist

- [ ] 3-2-1 rule implemented
- [ ] Automated backup schedule
- [ ] Offsite replication
- [ ] Encryption at rest
- [ ] Regular restore testing
- [ ] Retention policy defined
- [ ] Monitoring and alerting
- [ ] DR plan documented

---

## Next Steps

- M-DO-010: Infrastructure Patterns
- M-DO-014: Secrets Management
- M-DO-009: Terraform Basics

---

*Methodology M-DO-016 v1.0*
